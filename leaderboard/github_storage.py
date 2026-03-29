"""
GitHub-backed storage for workshop submissions.
Stores submissions as JSON files in a GitHub repo via the GitHub API.
Images are stored as separate files to keep JSON small and fast.
"""

from __future__ import annotations

import json
import base64
import hashlib
from datetime import datetime, timezone
from typing import Optional

import streamlit as st
from github import Github, GithubException


def secrets_configured() -> bool:
    """Check if GitHub secrets are set up."""
    return "GITHUB_TOKEN" in st.secrets and "GITHUB_REPO" in st.secrets


@st.cache_resource(ttl=300)
def _get_repo():
    """Get the GitHub repo object from secrets. Cached for 5 minutes."""
    if not secrets_configured():
        raise RuntimeError("GitHub secrets not configured")
    g = Github(st.secrets["GITHUB_TOKEN"])
    return g.get_repo(st.secrets["GITHUB_REPO"])


def _file_path(task_num: int) -> str:
    return f"submissions/task_{task_num}.json"


def _image_path(task_num: int, image_hash: str) -> str:
    return f"submissions/images/task_{task_num}_{image_hash}.png"


@st.cache_data(ttl=30)
def get_submissions(task_num: int) -> list[dict]:
    """Fetch submissions for a task from GitHub. Cached for 30 seconds."""
    try:
        repo = _get_repo()
        contents = repo.get_contents(_file_path(task_num))
        decoded = base64.b64decode(contents.content).decode().strip()
        if not decoded:
            return []
        data = json.loads(decoded)
        if not isinstance(data, list):
            return []
        return sorted(data, key=lambda x: x.get("timestamp", ""))
    except GithubException as e:
        if e.status == 404:
            return []
        raise
    except (json.JSONDecodeError, ValueError):
        return []


def _upload_image(repo, task_num: int, image_bytes: bytes) -> str:
    """Upload image as a separate file. Returns the raw GitHub URL."""
    image_hash = hashlib.md5(image_bytes).hexdigest()[:12]
    path = _image_path(task_num, image_hash)

    try:
        existing = repo.get_contents(path)
        # Image already exists, return URL
        return existing.download_url
    except GithubException as e:
        if e.status == 404:
            result = repo.create_file(
                path,
                f"Upload image for task {task_num}",
                image_bytes,
            )
            return result["content"].download_url
        raise


def add_submission(task_num: int, name: str, text: str = "",
                   image_bytes: Optional[bytes] = None) -> int:
    """Add a submission. Returns the rank (1-indexed)."""
    repo = _get_repo()
    path = _file_path(task_num)

    submission = {
        "name": name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "task": task_num,
        "text": text,
    }

    if image_bytes:
        image_url = _upload_image(repo, task_num, image_bytes)
        submission["image"] = image_url

    # Read existing or start fresh
    try:
        contents = repo.get_contents(path)
        decoded = base64.b64decode(contents.content).decode().strip()
        existing = json.loads(decoded) if decoded else []
        if not isinstance(existing, list):
            existing = []
        existing.append(submission)
        repo.update_file(
            path,
            f"Add submission from {name} for task {task_num}",
            json.dumps(existing, indent=2),
            contents.sha,
        )
    except GithubException as e:
        if e.status == 404:
            existing = [submission]
            repo.create_file(
                path,
                f"Add submission from {name} for task {task_num}",
                json.dumps(existing, indent=2),
            )
        else:
            raise

    # Clear cache so new submission shows up
    get_submissions.clear()

    sorted_subs = sorted(existing, key=lambda x: x["timestamp"])
    rank = next(i + 1 for i, s in enumerate(sorted_subs) if s["name"] == name)
    return rank


def clear_task(task_num: int) -> bool:
    """Clear all submissions for a task. Returns True if cleared."""
    try:
        repo = _get_repo()
        contents = repo.get_contents(_file_path(task_num))
        repo.update_file(
            _file_path(task_num),
            f"Clear submissions for task {task_num}",
            json.dumps([], indent=2),
            contents.sha,
        )
        get_submissions.clear()
        return True
    except GithubException as e:
        if e.status == 404:
            return True
        raise


def get_all_submissions() -> dict[int, list[dict]]:
    """Fetch submissions for all tasks."""
    result = {}
    for task_num in range(3):
        result[task_num] = get_submissions(task_num)
    return result


def name_already_submitted(task_num: int, name: str) -> bool:
    """Check if a name has already submitted for a task (uses cached data)."""
    subs = get_submissions(task_num)
    return any(s["name"].strip().lower() == name.strip().lower() for s in subs)
