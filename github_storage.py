"""
GitHub-backed storage for workshop submissions.
Stores submissions as JSON files in a GitHub repo via the GitHub API.
"""

import json
import base64
from datetime import datetime, timezone

import streamlit as st
from github import Github, GithubException


def _get_repo():
    """Get the GitHub repo object from secrets."""
    g = Github(st.secrets["GITHUB_TOKEN"])
    return g.get_repo(st.secrets["GITHUB_REPO"])


def _file_path(task_num: int) -> str:
    return f"submissions/task_{task_num}.json"


def get_submissions(task_num: int) -> list[dict]:
    """Fetch submissions for a task from GitHub. Returns sorted by timestamp."""
    try:
        repo = _get_repo()
        contents = repo.get_contents(_file_path(task_num))
        data = json.loads(base64.b64decode(contents.content).decode())
        return sorted(data, key=lambda x: x["timestamp"])
    except GithubException as e:
        if e.status == 404:
            return []
        raise


def add_submission(task_num: int, name: str, text: str = "",
                   image_bytes: bytes | None = None) -> int:
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
        b64 = base64.b64encode(image_bytes).decode()
        submission["image"] = f"data:image/png;base64,{b64}"

    # Read existing or start fresh
    try:
        contents = repo.get_contents(path)
        existing = json.loads(base64.b64decode(contents.content).decode())
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
        return True
    except GithubException as e:
        if e.status == 404:
            return True
        raise


def get_all_submissions() -> dict[int, list[dict]]:
    """Fetch submissions for all tasks."""
    result = {}
    for task_num in range(5):
        result[task_num] = get_submissions(task_num)
    return result


def name_already_submitted(task_num: int, name: str) -> bool:
    """Check if a name has already submitted for a task."""
    subs = get_submissions(task_num)
    return any(s["name"].strip().lower() == name.strip().lower() for s in subs)
