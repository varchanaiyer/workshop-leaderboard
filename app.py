"""
AI Research Workshop — Leaderboard & Submission App
Students submit task answers, see who's first, and compete on the leaderboard.
"""

import json
from datetime import datetime

import streamlit as st
from github_storage import (
    get_submissions,
    add_submission,
    clear_task,
    get_all_submissions,
    name_already_submitted,
)

# ─── CONFIG ─────────────────────────────────────────────────────────────

TASKS = {
    0: {
        "name": "Setup: Install Tools",
        "description": "Install Claude Code or Cursor and submit a screenshot showing it's ready.",
        "accepts_image": True,
        "accepts_text": True,
        "text_label": "Which tool did you install? Any notes?",
        "text_placeholder": "e.g., Installed Claude Code via npm, version 1.2.3",
    },
    1: {
        "name": "Research Plan",
        "description": "Submit your benchmark categories and ablation dataset choice.",
        "accepts_image": False,
        "accepts_text": True,
        "text_label": "Your research plan",
        "text_placeholder": (
            "Benchmark categories: medical, legal, coding, history, psychology\n"
            "Ablation: GSM8K math dataset, testing zero-shot / few-shot / CoT / CoT+SC\n"
            "Models: GPT-4o-mini, Claude Sonnet, Gemini Flash\n"
            "Metric: exact match for math, semantic similarity for others"
        ),
    },
    2: {
        "name": "Pipeline Implementation",
        "description": "Submit a screenshot of your --dry-run --mock output from both pipelines.",
        "accepts_image": True,
        "accepts_text": True,
        "text_label": "Any notes about your implementation?",
        "text_placeholder": "e.g., Used async API calls, added retry with backoff...",
    },
    3: {
        "name": "Analysis & Findings",
        "description": "Upload your figures and write your 2-sentence findings + combined insight.",
        "accepts_image": True,
        "accepts_text": True,
        "text_label": "Your findings (2 sentences each + combined insight)",
        "text_placeholder": (
            "Benchmark: We find that LLM consistency varies significantly across categories, "
            "with math at 92% and ethics at 54%.\n\n"
            "Ablation: Chain-of-thought improves accuracy by 15% over zero-shot on GSM8K.\n\n"
            "Combined: Models that are less consistent on paraphrased questions also "
            "benefit most from structured prompting strategies."
        ),
    },
    4: {
        "name": "GPU Optimization",
        "description": "List the performance issues you found in slow_train.py and your fixes.",
        "accepts_image": False,
        "accepts_text": True,
        "text_label": "Issues found and fixes applied",
        "text_placeholder": (
            "1. Batch size = 1 → Added DataLoader with batch_size=32\n"
            "2. No num_workers → Set num_workers=4, pin_memory=True\n"
            "3. No mixed precision → Added autocast + GradScaler\n"
            "4. .item() in loop → Accumulate on GPU, log every 100 steps\n"
            "5. No model.eval() → Added model.eval() + torch.no_grad()\n"
            "6. No checkpointing → Save every epoch\n"
            "7. No gradient accumulation → Added accumulate_steps=4"
        ),
    },
}

MEDAL = {1: "🥇", 2: "🥈", 3: "🥉"}


# ─── PAGE CONFIG ────────────────────────────────────────────────────────

st.set_page_config(
    page_title="AI Research Workshop",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for dark theme accents
st.markdown("""
<style>
    .stApp { }
    div[data-testid="stMetric"] {
        background-color: rgba(108, 99, 255, 0.1);
        border: 1px solid rgba(108, 99, 255, 0.3);
        border-radius: 8px;
        padding: 10px;
    }
    .rank-1 { color: #FFD700; font-weight: bold; }
    .rank-2 { color: #C0C0C0; font-weight: bold; }
    .rank-3 { color: #CD7F32; font-weight: bold; }
</style>
""", unsafe_allow_html=True)


# ─── SIDEBAR ────────────────────────────────────────────────────────────

st.sidebar.title("🧪 Workshop Hub")
page = st.sidebar.radio(
    "Navigate",
    ["📝 Submit", "🏆 Leaderboard", "🔐 Admin"],
    label_visibility="collapsed",
)


# ─── SUBMIT PAGE ────────────────────────────────────────────────────────

if page == "📝 Submit":
    st.title("📝 Submit Your Work")
    st.markdown("Complete each task and submit here. First to submit gets rank #1!")

    st.divider()

    name = st.text_input("Your Name", placeholder="Enter your name")

    task_options = {num: f"Task {num}: {info['name']}" for num, info in TASKS.items()}
    selected_label = st.selectbox("Select Task", list(task_options.values()))
    task_num = next(num for num, label in task_options.items() if label == selected_label)
    task = TASKS[task_num]

    st.info(f"**{task['name']}**: {task['description']}")

    # Check for duplicate
    if name and name_already_submitted(task_num, name):
        st.warning(f"⚠️ '{name}' has already submitted for this task. Submitting again will add a new entry.")

    # Build the form
    uploaded_image = None
    text_content = ""

    if task["accepts_image"]:
        uploaded_image = st.file_uploader(
            "Upload screenshot / figure",
            type=["png", "jpg", "jpeg", "gif"],
            help="Take a screenshot and upload it here",
        )
        if uploaded_image:
            st.image(uploaded_image, caption="Preview", width=400)

    if task["accepts_text"]:
        text_content = st.text_area(
            task["text_label"],
            placeholder=task["text_placeholder"],
            height=200,
        )

    # Submit button
    if st.button("🚀 Submit", type="primary", use_container_width=True):
        if not name.strip():
            st.error("Please enter your name.")
        elif not text_content.strip() and not uploaded_image:
            st.error("Please provide either text or an image.")
        else:
            with st.spinner("Submitting..."):
                image_bytes = uploaded_image.read() if uploaded_image else None
                rank = add_submission(task_num, name.strip(), text_content.strip(), image_bytes)

            medal = MEDAL.get(rank, "")
            st.success(f"Submitted! You are #{rank} {medal} for {task['name']}!")
            st.balloons()


# ─── LEADERBOARD PAGE ──────────────────────────────────────────────────

elif page == "🏆 Leaderboard":
    st.title("🏆 Leaderboard")
    st.markdown("See who submitted first for each task. Top 3 get medals!")

    tabs = st.tabs([f"Task {num}: {info['name']}" for num, info in TASKS.items()])

    for tab, (task_num, task) in zip(tabs, TASKS.items()):
        with tab:
            submissions = get_submissions(task_num)

            if not submissions:
                st.info("No submissions yet. Be the first! 🏃")
                continue

            st.metric("Total Submissions", len(submissions))

            for i, sub in enumerate(submissions):
                rank = i + 1
                medal = MEDAL.get(rank, f"#{rank}")
                ts = datetime.fromisoformat(sub["timestamp"]).strftime("%H:%M:%S")

                with st.expander(f"{medal} **{sub['name']}** — submitted at {ts}", expanded=(rank <= 3)):
                    cols = st.columns([2, 1])

                    with cols[0]:
                        if sub.get("text"):
                            st.markdown(f"**Response:**\n\n{sub['text']}")

                    with cols[1]:
                        if sub.get("image"):
                            st.image(sub["image"], caption=f"{sub['name']}'s submission", width=300)


# ─── ADMIN PAGE ─────────────────────────────────────────────────────────

elif page == "🔐 Admin":
    st.title("🔐 Admin Panel")

    if "admin_authenticated" not in st.session_state:
        st.session_state.admin_authenticated = False

    if not st.session_state.admin_authenticated:
        password = st.text_input("Enter admin password", type="password")
        if st.button("Login"):
            if password == st.secrets.get("ADMIN_PASSWORD", ""):
                st.session_state.admin_authenticated = True
                st.rerun()
            else:
                st.error("Incorrect password.")
    else:
        st.success("Authenticated as admin")

        # Dashboard
        all_subs = get_all_submissions()
        total = sum(len(subs) for subs in all_subs.values())

        cols = st.columns(6)
        cols[0].metric("Total", total)
        for task_num in range(5):
            cols[task_num + 1].metric(f"Task {task_num}", len(all_subs.get(task_num, [])))

        st.divider()

        # Per-task management
        for task_num, task in TASKS.items():
            with st.expander(f"Task {task_num}: {task['name']} ({len(all_subs.get(task_num, []))} submissions)"):
                subs = all_subs.get(task_num, [])

                if subs:
                    for i, sub in enumerate(subs):
                        rank = i + 1
                        medal = MEDAL.get(rank, f"#{rank}")
                        ts = datetime.fromisoformat(sub["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
                        st.markdown(f"**{medal} {sub['name']}** — {ts}")
                        if sub.get("text"):
                            st.code(sub["text"], language=None)
                        if sub.get("image"):
                            st.image(sub["image"], width=200)
                        st.divider()

                    # Clear button with confirmation
                    col1, col2 = st.columns([3, 1])
                    with col2:
                        if st.button(f"🗑️ Clear Task {task_num}", key=f"clear_{task_num}"):
                            st.session_state[f"confirm_clear_{task_num}"] = True

                    if st.session_state.get(f"confirm_clear_{task_num}"):
                        st.warning(f"Are you sure you want to clear all {len(subs)} submissions for Task {task_num}?")
                        c1, c2, c3 = st.columns([1, 1, 4])
                        with c1:
                            if st.button("Yes, clear", key=f"yes_clear_{task_num}"):
                                clear_task(task_num)
                                st.session_state[f"confirm_clear_{task_num}"] = False
                                st.success(f"Task {task_num} cleared.")
                                st.rerun()
                        with c2:
                            if st.button("Cancel", key=f"cancel_clear_{task_num}"):
                                st.session_state[f"confirm_clear_{task_num}"] = False
                                st.rerun()
                else:
                    st.info("No submissions yet.")

        st.divider()

        # Download all
        all_data = json.dumps(all_subs, indent=2, default=str)
        st.download_button(
            "📥 Download All Submissions (JSON)",
            data=all_data,
            file_name="workshop_submissions.json",
            mime="application/json",
        )

        # Logout
        if st.sidebar.button("🔓 Logout"):
            st.session_state.admin_authenticated = False
            st.rerun()
