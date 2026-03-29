"""
AI Research Workshop — Live Leaderboard
Submit your work, see the rankings, celebrate the wins.
"""

import json
import base64
from datetime import datetime

import streamlit as st
from github_storage import (
    get_submissions,
    add_submission,
    clear_task,
    get_all_submissions,
    name_already_submitted,
    secrets_configured,
)

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="Workshop Leaderboard", page_icon="🏆", layout="wide")

MEDAL = {1: "🥇", 2: "🥈", 3: "🥉"}

# ── Slide examples (to check paraphrases are original) ──────────────────────
SLIDE_EXAMPLES = {
    "math": {
        "question": "What is 15% of 200?",
        "paraphrases": [
            "Calculate 15 percent of 200.",
            "If you take 15% from 200, what do you get?",
            "200 × 0.15 = ?",
        ],
    },
    "geography": {
        "question": "What is the capital of Australia?",
        "paraphrases": [
            "Name the capital city of Australia.",
            "Which city serves as Australia's capital?",
            "Australia's seat of government is located in which city?",
        ],
    },
}

# ── Task definitions ─────────────────────────────────────────────────────────
TASKS = {
    0: {
        "name": "Setup: Install Tools",
        "description": "Install Claude Code or Cursor and submit a screenshot showing it's ready.",
        "accepts_image": True,
        "accepts_text": True,
        "custom_form": False,
        "text_label": "Which tool did you install? Any notes?",
        "text_placeholder": "e.g., Installed Claude Code via npm, version 1.2.3",
    },
    1: {
        "name": "Research Plan",
        "description": "Define your benchmark experiment: categories, sample question, models, and metric.",
        "accepts_image": False,
        "accepts_text": False,
        "custom_form": True,
    },
    2: {
        "name": "Prompting Strategy Test",
        "description": "Test all 4 prompting strategies on one question and submit your results.",
        "accepts_image": False,
        "accepts_text": False,
        "custom_form": True,
    },
}

# ── Secrets check ────────────────────────────────────────────────────────────
if not secrets_configured():
    st.error("GitHub secrets not configured. Add GITHUB_TOKEN, GITHUB_REPO, and ADMIN_PASSWORD to .streamlit/secrets.toml")
    st.code(
        'GITHUB_TOKEN = "ghp_your_token_here"\n'
        'GITHUB_REPO = "your-username/workshop-submissions"\n'
        'ADMIN_PASSWORD = "your_password"',
        language="toml",
    )
    st.stop()

# ── Sidebar navigation ──────────────────────────────────────────────────────
page = st.sidebar.radio("Navigate", ["📤 Submit", "🏆 Leaderboard", "🔧 Admin"])

# ═════════════════════════════════════════════════════════════════════════════
# PAGE: SUBMIT
# ═════════════════════════════════════════════════════════════════════════════
if page == "📤 Submit":
    st.title("📤 Submit Your Work")
    st.markdown("Enter your name, pick a task, and submit your answer.")

    name = st.text_input("Your Name", placeholder="e.g., Alice Chen")

    task_options = {num: f"Task {num}: {info['name']}" for num, info in TASKS.items()}
    selected_label = st.selectbox("Select Task", list(task_options.values()))
    task_num = next(num for num, label in task_options.items() if label == selected_label)
    task = TASKS[task_num]

    st.info(f"**{task['name']}**: {task['description']}")

    # Check for duplicate
    if name and name_already_submitted(task_num, name):
        st.warning(f"'{name}' has already submitted for this task. Submitting again will add a new entry.")

    # ── Task 1: Custom structured form ───────────────────────────────────
    if task_num == 1:
        project_type = st.radio(
            "Which project are you doing?",
            ["Benchmark (Paraphrase Consistency)", "Ablation (Prompting Strategies)"],
            horizontal=True,
        )
        is_benchmark = project_type.startswith("Benchmark")

        if is_benchmark:
            st.markdown("### Your Benchmark Research Plan")
            st.markdown("Fill in all 4 parts below. Be specific!")

            st.markdown("---")

            # 1. Five categories
            st.markdown("**1. Your 5 Question Categories**")
            st.caption("Pick 5 domains you'll test the LLM on. Make them diverse — mix factual and subjective.")
            categories = st.text_area(
                "Categories",
                placeholder=(
                    "e.g.,\n"
                    "1. Medical (dosage calculations, symptom matching)\n"
                    "2. Legal (case law, statutory interpretation)\n"
                    "3. Coding (algorithm output, debugging)\n"
                    "4. Ethics (trolley problems, AI bias scenarios)\n"
                    "5. History (dates, cause-and-effect)"
                ),
                height=140,
                label_visibility="collapsed",
            )

            st.markdown("---")

            # 2. Example question + 3 paraphrases
            st.markdown("**2. Example Question + 3 Paraphrases** (for one of your categories)")
            st.caption(
                "Write ONE question and 3 paraphrases that are structurally different — "
                "not just synonym swaps. Your paraphrases must be **original** (not from the slides)."
            )
            st.markdown(
                "> **Slide examples (don't copy these):**\n"
                "> - *'What is 15% of 200?'* → *'Calculate 15 percent of 200'*, *'200 × 0.15 = ?'*\n"
                "> - *'What is the capital of Australia?'* → *'Name the capital city of Australia'*\n\n"
                "> **Good original example:**\n"
                "> - Question: *'What is the recommended daily dose of ibuprofen for adults?'*\n"
                "> - P1: *'How many milligrams of ibuprofen can an adult safely take per day?'*\n"
                "> - P2: *'For a grown-up, what\\'s the max ibuprofen intake in 24 hours?'*\n"
                "> - P3: *'An adult has a headache — what ibuprofen dosage should they not exceed daily?'*"
            )
            example_question = st.text_input(
                "Original question",
                placeholder="e.g., What is the recommended daily dose of ibuprofen for adults?",
            )
            para_1 = st.text_input(
                "Paraphrase 1",
                placeholder="e.g., How many milligrams of ibuprofen can an adult safely take per day?",
            )
            para_2 = st.text_input(
                "Paraphrase 2",
                placeholder="e.g., For a grown-up, what's the max ibuprofen intake in 24 hours?",
            )
            para_3 = st.text_input(
                "Paraphrase 3",
                placeholder="e.g., An adult has a headache — what ibuprofen dosage should they not exceed daily?",
            )

            st.markdown("---")

            # 3. Models
            st.markdown("**3. Which 2–3 Models Will You Test?**")
            st.caption("Pick models you have API access to. Using different providers makes the comparison richer.")
            bm_models = st.text_input(
                "Models (Benchmark)",
                placeholder="e.g., GPT-4o-mini, Claude Sonnet, Gemini Flash",
                label_visibility="collapsed",
            )

            st.markdown("---")

            # 4. Consistency metric
            st.markdown("**4. Your Consistency Metric Definition**")
            st.caption(
                "How will you measure whether the LLM gives the same answer to paraphrased questions? "
                "Define it precisely."
            )
            metric = st.text_area(
                "Metric definition",
                placeholder=(
                    "e.g., For factual questions: exact match after normalizing (lowercase, strip punctuation, "
                    "extract key answer). 'The answer is $160' matches '$160'.\n"
                    "For open-ended questions: Jaccard similarity on word sets — "
                    "intersection/union of unique words. Score > 0.7 = consistent."
                ),
                height=120,
                label_visibility="collapsed",
            )

            # Validate paraphrases aren't from slides
            def _is_slide_paraphrase(text: str) -> bool:
                if not text:
                    return False
                text_lower = text.strip().lower()
                for cat_data in SLIDE_EXAMPLES.values():
                    if text_lower == cat_data["question"].lower():
                        return True
                    for p in cat_data["paraphrases"]:
                        if text_lower == p.lower():
                            return True
                return False

            slide_warning = False
            for p in [example_question, para_1, para_2, para_3]:
                if _is_slide_paraphrase(p):
                    slide_warning = True

            if slide_warning:
                st.error("One or more of your questions/paraphrases is copied from the slides. Please write original ones!")

            # Submit button
            all_filled = all([
                name,
                categories.strip(),
                example_question.strip(),
                para_1.strip(),
                para_2.strip(),
                para_3.strip(),
                bm_models.strip(),
                metric.strip(),
            ])

            if st.button("🚀 Submit", disabled=not all_filled or slide_warning, use_container_width=True):
                combined_text = (
                    f"**[Benchmark Pipeline]**\n\n"
                    f"**Categories:**\n{categories.strip()}\n\n"
                    f"**Example Question:** {example_question.strip()}\n"
                    f"- Paraphrase 1: {para_1.strip()}\n"
                    f"- Paraphrase 2: {para_2.strip()}\n"
                    f"- Paraphrase 3: {para_3.strip()}\n\n"
                    f"**Models:** {bm_models.strip()}\n\n"
                    f"**Consistency Metric:**\n{metric.strip()}"
                )
                with st.spinner("Submitting..."):
                    rank = add_submission(task_num, name, text=combined_text)
                st.success(f"Submitted! You are #{rank} for this task.")
                st.balloons()

            if not all_filled:
                st.caption("Fill in all 4 sections to enable the Submit button.")

        # ── Ablation form ────────────────────────────────────────────────
        else:
            st.markdown("### Your Ablation Study Plan")
            st.markdown("Fill in all 4 parts below. Be specific!")

            st.markdown("---")

            # 1. Dataset choice
            st.markdown("**1. Your Dataset**")
            st.caption(
                "Which dataset will you evaluate on? Specify the source, split, and how many examples."
            )
            abl_dataset = st.text_area(
                "Dataset",
                placeholder=(
                    "e.g.,\n"
                    "Dataset: GSM8K (grade-school math)\n"
                    "Source: HuggingFace — load_dataset('gsm8k', 'main', split='test[:50]')\n"
                    "50 test examples, 5 held-out for few-shot prompts\n"
                    "Task type: math word problems with numeric answers"
                ),
                height=120,
                label_visibility="collapsed",
            )

            st.markdown("---")

            # 2. Prompting strategies
            st.markdown("**2. Your 4 Prompting Strategies**")
            st.caption(
                "List each strategy and write out the exact prompt template you'll use. "
                "Show how the question gets wrapped."
            )
            st.markdown(
                "> **Example:**\n"
                "> - **Zero-shot:** `{question}` (no extra context)\n"
                "> - **Few-shot:** `Here are some examples:\\n{examples}\\n\\nNow solve: {question}`\n"
                "> - **Chain-of-thought:** `{question}\\n\\nLet's think step by step.`\n"
                "> - **CoT + Self-consistency:** Same as CoT, but run 5 times and take majority vote"
            )
            abl_strategies = st.text_area(
                "Strategies",
                placeholder=(
                    "e.g.,\n"
                    "1. Zero-shot: Just the question, no extra instructions\n"
                    "2. Few-shot (3 examples): 'Here are some solved examples:\\n"
                    "{ex1}\\n{ex2}\\n{ex3}\\n\\nNow solve: {question}'\n"
                    "3. Chain-of-thought: '{question}\\n\\nLet's think step by step.'\n"
                    "4. CoT + Self-consistency: Run CoT 5 times, extract answer from each, majority vote"
                ),
                height=150,
                label_visibility="collapsed",
            )

            st.markdown("---")

            # 3. Models
            st.markdown("**3. Which 2–3 Models Will You Test?**")
            st.caption("Pick models you have API access to. Using different providers makes the comparison richer.")
            abl_models = st.text_input(
                "Models (Ablation)",
                placeholder="e.g., GPT-4o-mini, Claude Sonnet, Gemini Flash",
                label_visibility="collapsed",
            )

            st.markdown("---")

            # 4. Answer extraction + accuracy metric
            st.markdown("**4. How Will You Extract Answers & Measure Accuracy?**")
            st.caption(
                "The model returns a full response (e.g., 'Step 1: ... The answer is 20'). "
                "How will you extract the final answer and compare it to the expected answer?"
            )
            abl_metric = st.text_area(
                "Answer extraction & accuracy",
                placeholder=(
                    "e.g.,\n"
                    "Extraction: Look for 'Answer: X' or 'the answer is X' pattern. "
                    "If not found, take the last number in the response.\n"
                    "Accuracy: exact match after extracting — "
                    "extracted answer == expected answer (both normalized to numbers).\n"
                    "Per-strategy accuracy = correct / total. "
                    "Statistical comparison: McNemar's test, p < 0.05 = significant."
                ),
                height=140,
                label_visibility="collapsed",
            )

            # Submit button
            all_filled = all([
                name,
                abl_dataset.strip(),
                abl_strategies.strip(),
                abl_models.strip(),
                abl_metric.strip(),
            ])

            if st.button("🚀 Submit", disabled=not all_filled, use_container_width=True):
                combined_text = (
                    f"**[Ablation Pipeline]**\n\n"
                    f"**Dataset:**\n{abl_dataset.strip()}\n\n"
                    f"**Prompting Strategies:**\n{abl_strategies.strip()}\n\n"
                    f"**Models:** {abl_models.strip()}\n\n"
                    f"**Answer Extraction & Accuracy:**\n{abl_metric.strip()}"
                )
                with st.spinner("Submitting..."):
                    rank = add_submission(task_num, name, text=combined_text)
                st.success(f"Submitted! You are #{rank} for this task.")
                st.balloons()

            if not all_filled:
                st.caption("Fill in all 4 sections to enable the Submit button.")

    # ── Task 2: Prompting Strategy Test ──────────────────────────────────
    elif task_num == 2:
        QUESTION = "A store sells a jacket for $120 after a 25% discount. What was the original price?"

        st.markdown("### The Question")
        st.info(f"**{QUESTION}**")
        st.caption("You can use your own question — just keep it the same across all 4 strategies.")

        st.markdown("---")
        st.markdown("### Copy each prompt → paste into ChatGPT, Claude, or any LLM → enter the answer below")

        # ── 1. Zero-shot ──────────────────────────────────────────────────
        st.markdown("#### 1. Zero-shot")
        st.caption("Just the question — no hints, no examples.")
        st.code(QUESTION, language=None)
        zs_answer = st.text_input(
            "Model's answer (zero-shot)",
            key="ans_zs",
            placeholder="e.g., $160",
        )

        st.markdown("---")

        # ── 2. Few-shot ───────────────────────────────────────────────────
        st.markdown("#### 2. Few-shot")
        st.caption("3 worked examples before the question — the model follows the pattern.")
        few_shot_prompt = (
            "Here are some examples:\n"
            "\n"
            "Q: A phone costs $80 after a 20% discount. What was the original price?\n"
            "A: The sale price is 80% of the original. Original = $80 / 0.80 = $100.\n"
            "\n"
            "Q: A book costs $12 after a 40% discount. What was the original price?\n"
            "A: The sale price is 60% of the original. Original = $12 / 0.60 = $20.\n"
            "\n"
            "Q: A shirt costs $45 after a 10% discount. What was the original price?\n"
            "A: The sale price is 90% of the original. Original = $45 / 0.90 = $50.\n"
            "\n"
            f"Now solve:\n"
            f"Q: {QUESTION}\n"
            "A:"
        )
        st.code(few_shot_prompt, language=None)
        fs_answer = st.text_input(
            "Model's answer (few-shot)",
            key="ans_fs",
            placeholder="e.g., $160",
        )

        st.markdown("---")

        # ── 3. Chain-of-Thought ───────────────────────────────────────────
        st.markdown("#### 3. Chain-of-Thought (CoT)")
        st.caption('"Let\'s think step by step" forces the model to show its reasoning.')
        cot_prompt = f"{QUESTION}\n\nLet's think step by step."
        st.code(cot_prompt, language=None)
        cot_answer = st.text_input(
            "Model's answer (CoT)",
            key="ans_cot",
            placeholder="e.g., Step 1: ... Step 2: ... The original price was $160.",
        )

        st.markdown("---")

        # ── 4. CoT + Self-Consistency ─────────────────────────────────────
        st.markdown("#### 4. CoT + Self-Consistency")
        st.caption(
            "Same CoT prompt — paste it **3 separate times** (start a new chat each time). "
            "Record all 3 answers and take the majority."
        )
        sc_prompt = f"{QUESTION}\n\nLet's think step by step."
        st.code(sc_prompt, language=None)
        st.info(
            "**How to do self-consistency:**\n"
            "1. Paste the prompt above → note the answer (Run 1)\n"
            "2. Start a **new chat** → paste again → note the answer (Run 2)\n"
            "3. Start a **new chat** → paste again → note the answer (Run 3)\n"
            "4. Take the majority answer (the one that appears most)"
        )
        sc_answer = st.text_input(
            "All 3 answers + majority",
            key="ans_sc",
            placeholder="e.g., Run 1: $160  |  Run 2: $160  |  Run 3: $150  →  Majority: $160",
        )

        st.markdown("---")
        st.markdown("### Reflect")

        best_strategy = st.selectbox(
            "Which strategy gave the best / most complete answer?",
            ["(select one)", "Zero-shot", "Few-shot", "Chain-of-Thought", "CoT + Self-Consistency"],
        )

        surprises = st.text_area(
            "Any surprises or differences between strategies? (optional)",
            placeholder=(
                "e.g., Zero-shot got it right immediately. CoT was much longer but same answer. "
                "All 3 CoT runs agreed on $160."
            ),
            height=90,
        )

        model_used = st.text_input(
            "Which model(s) did you use?",
            placeholder="e.g., ChatGPT-4o, Claude Sonnet, Gemini Flash",
        )

        all_filled = (
            name
            and zs_answer.strip()
            and fs_answer.strip()
            and cot_answer.strip()
            and sc_answer.strip()
            and best_strategy != "(select one)"
            and model_used.strip()
        )

        if st.button("🚀 Submit", disabled=not all_filled, use_container_width=True):
            combined_text = (
                f"**Model(s):** {model_used.strip()}\n\n"
                f"**Zero-shot:** {zs_answer.strip()}\n"
                f"**Few-shot:** {fs_answer.strip()}\n"
                f"**Chain-of-Thought:** {cot_answer.strip()}\n"
                f"**CoT + Self-Consistency:** {sc_answer.strip()}\n\n"
                f"**Best strategy:** {best_strategy}"
                + (f"\n\n**Surprises:** {surprises.strip()}" if surprises.strip() else "")
            )
            with st.spinner("Submitting..."):
                rank = add_submission(task_num, name, text=combined_text)
            st.success(f"Submitted! You are #{rank} for this task.")
            st.balloons()

        if not all_filled:
            st.caption("Fill in all 4 answers, select the best strategy, and enter the model name to enable Submit.")

# ═════════════════════════════════════════════════════════════════════════════
# PAGE: LEADERBOARD
# ═════════════════════════════════════════════════════════════════════════════
elif page == "🏆 Leaderboard":
    st.title("🏆 Leaderboard")

    tabs = st.tabs([f"Task {num}: {info['name']}" for num, info in TASKS.items()])

    for tab, (task_num, task) in zip(tabs, TASKS.items()):
        with tab:
            submissions = get_submissions(task_num)

            if not submissions:
                st.info("No submissions yet. Be the first!")
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
                            st.image(sub["image"], caption=f"{sub['name']}'s submission", use_container_width=True)

# ═════════════════════════════════════════════════════════════════════════════
# PAGE: ADMIN
# ═════════════════════════════════════════════════════════════════════════════
elif page == "🔧 Admin":
    st.title("🔧 Admin Panel")

    if "admin_auth" not in st.session_state:
        st.session_state.admin_auth = False

    if not st.session_state.admin_auth:
        pw = st.text_input("Admin Password", type="password")
        if st.button("Login"):
            if pw == st.secrets.get("ADMIN_PASSWORD", ""):
                st.session_state.admin_auth = True
                st.rerun()
            else:
                st.error("Wrong password.")
        st.stop()

    # Authenticated
    st.success("Authenticated as admin.")

    all_subs = get_all_submissions()
    total = sum(len(subs) for subs in all_subs.values())
    st.metric("Total Submissions (all tasks)", total)

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
                    if st.button(f"Clear Task {task_num}", key=f"clear_{task_num}"):
                        st.session_state[f"confirm_clear_{task_num}"] = True

                if st.session_state.get(f"confirm_clear_{task_num}"):
                    st.warning(f"Are you sure you want to clear all submissions for Task {task_num}?")
                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button("Yes, clear", key=f"yes_clear_{task_num}"):
                            clear_task(task_num)
                            st.session_state[f"confirm_clear_{task_num}"] = False
                            st.rerun()
                    with c2:
                        if st.button("Cancel", key=f"cancel_clear_{task_num}"):
                            st.session_state[f"confirm_clear_{task_num}"] = False
                            st.rerun()
            else:
                st.info("No submissions.")

    # Download all
    st.divider()
    if st.button("Download All Submissions as JSON"):
        st.download_button(
            "Download",
            data=json.dumps(
                {str(k): v for k, v in all_subs.items()},
                indent=2,
                default=str,
            ),
            file_name="all_submissions.json",
            mime="application/json",
        )
