# ═══════════════════════════════════════════════════
# IMPLEMENTATION LECTURE 2: Research Implementation
# Algoverse AI Research Program — Spring 2026
# ═══════════════════════════════════════════════════

---

# Today's Agenda

| Time | Section | Leaderboard Task |
|------|---------|-----------------|
| 0:00 | Recap: Lambda + What You Already Did | Review Task 0 & 1 submissions |
| 0:10 | Prompting Strategies Deep Dive | -- |
| 0:30 | **LIVE: Test 4 Strategies** | Submit → Task 5: Prompting Strategy Test |
| 0:50 | Answer Normalization | -- |
| 1:05 | **LIVE: Write normalize_answer()** | Submit → Task 6: Answer Normalization |
| 1:20 | Retry Logic & Crash-Proofing | -- |
| 1:30 | **LIVE: Write call_with_retry()** | Submit → Task 7: Retry Logic |
| 1:45 | Project Scaffolding | -- |
| 2:00 | **LIVE: Build Your Scaffold** | Submit → Task 8: Project Scaffold |
| 2:15 | Common Mistakes | -- |
| 2:25 | **LIVE: Spot the Mistakes** | Submit → Task 9: Spot the Mistakes |
| 2:35 | Wrap-Up & Homework | -- |

**5 leaderboard submissions today.** First to submit gets the medal!

---

# ═══════════════════════════════════════════════════
# SECTION 1: RECAP (10 min)
# ═══════════════════════════════════════════════════

---

# What You've Already Done

**Task 0: Setup** — You installed Claude Code or Cursor.
**Task 1: Research Plan** — You designed your benchmark or ablation pipeline.

Let's look at a few Task 1 submissions from the leaderboard...

*(Instructor: pull up the leaderboard and show 2-3 interesting submissions)*

**Quick check** — raise your hand:
- Who chose the **Benchmark** (paraphrase consistency)?
- Who chose the **Ablation** (prompting strategies)?
- Who has already set up their Lambda SSH key?

---

# Where We're Going Today

Last session you designed the PLAN. Today you build the TOOLS.

```
Session 1 (done):  PLAN          Session 2 (today): BUILD
┌─────────────────────┐          ┌─────────────────────┐
│ ✓ Research question  │          │ Prompting strategies │
│ ✓ Question design    │    →     │ Answer normalization │
│ ✓ Model selection    │          │ Retry logic          │
│ ✓ Metric definition  │          │ Project scaffold     │
└─────────────────────┘          └─────────────────────┘
```

By the end of today you'll have working code for every piece of your pipeline.
**No GPU needed today.** Everything runs on your laptop or Colab.

---

# Your $400 Budget Strategy

| Phase | What | Cost | When |
|-------|------|------|------|
| 1. Design & Test | Write code, test with --dry-run | **$0** | Sessions 1-2 (now) |
| 2. Small Run | 50 samples on Lambda A100 | ~$5-10 | Session 3 |
| 3. Full Run | All samples, all models | ~$20-50 | Session 4 |
| 4. Analysis & Paper | Process results, generate figures | **$0** | Session 5 |

**Today = Phase 1. Save your credits.**

---

# ═══════════════════════════════════════════════════
# SECTION 2: PROMPTING STRATEGIES DEEP DIVE (20 min)
# ═══════════════════════════════════════════════════

---

# What Is Prompting? (Beginner Concept)

**Prompting** = the exact text you send to an LLM to get an answer.

The same question with different prompts gives different results:

```
Question: "A store sells a jacket for $120 after a 25% discount.
           What was the original price?"
```

| Strategy | What You Send | What You Get |
|----------|-------------- |-------------|
| **Zero-shot** | Just the question | "The original price was $160." |
| **Few-shot** | 3 worked examples + question | "Following the pattern: $120 / 0.75 = $160." |
| **Chain-of-Thought** | Question + "Let's think step by step." | "Step 1: Sale = 75%. Step 2: $120 = 0.75 x X. Step 3: X = $160." |
| **CoT + Self-Consistency** | Run CoT 5 times, majority vote | Runs: [$160, $160, $160, $150, $160] → Majority: $160 |

---

# Zero-Shot vs. Few-Shot — What's the Difference?

### Zero-Shot: No examples, just ask
```python
prompt = "What is the sentiment of this review: 'The food was amazing'?"
# Model guesses based on its training
```

### Few-Shot: Give examples first, then ask
```python
prompt = """Classify the sentiment:
Review: "I loved this movie!" → Positive
Review: "Terrible experience." → Negative
Review: "It was okay, nothing special." → Neutral

Review: "The food was amazing" → """
# Model follows the pattern you showed
```

**When to use which:**
- **Zero-shot**: Quick tests, when the task is obvious
- **Few-shot**: When the model needs to understand your format or labels
- **Rule of thumb**: Always TRY zero-shot first. If it fails, add examples.

---

# Chain-of-Thought (CoT) — Making the Model Show Its Work

**The trick**: Add "Let's think step by step" to the end of your prompt.

```python
# WITHOUT CoT
prompt = "If a train travels 60 mph for 2.5 hours, how far does it go?"
# Model might answer: "120 miles"  ← WRONG, guessed

# WITH CoT
prompt = """If a train travels 60 mph for 2.5 hours, how far does it go?
Let's think step by step."""
# Model answers:
# "Step 1: Distance = speed × time
#  Step 2: Distance = 60 × 2.5
#  Step 3: Distance = 150 miles"  ← CORRECT
```

**Why it works**: Forcing the model to show reasoning steps reduces errors.
It's like writing out your work on a math exam instead of doing it in your head.

**The cost**: More output tokens = more expensive. CoT outputs are ~3-5x longer.

---

# Self-Consistency — Voting Catches Errors

**Problem**: Even with CoT, models sometimes make mistakes.
**Solution**: Run it 5 times, take the majority answer.

```python
# Run the same CoT prompt 5 times with temperature=0.7
answers = []
for i in range(5):
    response = call_llm(prompt, temperature=0.7)  # slight randomness
    answer = extract_answer(response)
    answers.append(answer)

# answers = ["$160", "$160", "$160", "$150", "$160"]
# Majority vote: "$160" (4 out of 5)
final_answer = most_common(answers)
```

**Why temperature > 0?** At temperature=0, you get the same answer every time.
Self-Consistency needs variation to catch different reasoning paths.

**The tradeoff**: 5x the API calls = 5x the cost. Worth it for hard problems.

---

# Quick Quiz: Prompting Strategies

1. What does "few-shot" mean?
   - a) Using few words in your prompt
   - b) Giving the model a few examples before asking your question
   - c) Running the model a few times
   - d) Using a small model

2. Why does Chain-of-Thought work better for math?
   - a) It uses a different model
   - b) It forces the model to reason step-by-step instead of guessing
   - c) It costs more, so it must be better
   - d) It uses more GPU memory

3. Self-Consistency runs CoT 5 times and takes majority vote. When is this NOT worth it?
   - a) When the problem is hard
   - b) When accuracy matters more than cost
   - c) When the problem is easy and zero-shot already gets it right
   - d) When you have a deadline

*(Answers: 1-b, 2-b, 3-c — don't spend 5x on problems zero-shot handles)*

---

# ═══════════════════════════════════════════════════
# LEADERBOARD TASK 5: Test Prompting Strategies (15 min)
# ═══════════════════════════════════════════════════

---

# LIVE — Task 5: Test 4 Strategies on One Question

**Open ChatGPT, Claude, or any LLM right now.**

### Your question (or pick your own):
```
A store sells a jacket for $120 after a 25% discount.
What was the original price?
```

### Test all 4 strategies:
1. **Zero-shot** — Just paste the question. Copy the answer.
2. **Few-shot** — Add 2-3 worked examples before the question. Copy the answer.
3. **Chain-of-Thought** — Add "Let's think step by step." Copy the answer.
4. **CoT + Self-Consistency** — Run CoT 3 times. Do all 3 agree? Copy all answers.

### Then answer:
- Which strategy worked best?
- Any surprises?

### Submit your results:
**Go to the leaderboard → Task 5: Prompting Strategy Test → Fill in the form**

First to submit gets the gold medal!

---

# After Submitting: Discussion (5 min)

*(Instructor: pull up the leaderboard and compare submissions)*

**Discussion questions:**
- Did everyone get the same answer across strategies?
- Did anyone find a question where CoT HURT the answer?
- How much longer were CoT responses vs zero-shot?
- If CoT costs 3x more tokens, is the accuracy gain worth it?

**Connection to YOUR research:**
- Ablation students: you'll do this at scale (50-100 questions, 3 models)
- Benchmark students: you'll test if the SAME question with different phrasings gives different strategies different trouble

---

# ═══════════════════════════════════════════════════
# SECTION 3: ANSWER NORMALIZATION (15 min)
# ═══════════════════════════════════════════════════

---

# Why "$160" != "The answer is $160"

This is the **#1 beginner trap** in LLM evaluation.

Your model says:
```
"The original price was $160."
```

Your ground truth is:
```
"$160"
```

**Exact match says: WRONG.** But they agree!

This will ruin your accuracy numbers if you don't handle it.

---

# The Solution: Normalize Before Comparing

```python
import re

def normalize_answer(answer: str) -> str:
    """Strip an LLM response down to just the key answer."""
    # Remove common preambles
    answer = re.sub(r'^(the answer is|the result is|therefore|so)\s*',
                    '', answer.lower().strip())
    # Remove trailing punctuation
    answer = answer.strip('.')
    # Remove extra whitespace
    answer = ' '.join(answer.split())
    return answer
```

But this simple version still fails on many cases:
- `"Paris"` vs `"paris"` → needs `.lower()`
- `"3.14159"` vs `"3.14"` → rounding? or different answers?
- `"Abraham Lincoln"` vs `"Lincoln, Abraham"` → name reordering?
- `"Yes, it is ethical."` vs `"Yes"` → how much context to strip?

**There's no perfect normalizer.** You have to make design choices
and document them. That's part of your research contribution.

---

# Real-World Example: The Leaderboard's Approach

The Algoverse leaderboard uses an **LLM to extract answers**:

```python
# Uses GPT-4o-mini with temperature=0 to extract the core answer
messages = [
    {"role": "system",
     "content": "You are a helpful assistant that extracts answers "
                "from context. Provide only the direct answer, "
                "nothing else. Be concise."},
    {"role": "user",
     "content": f"Context: {context}\n\nQuestion: {question}\n\nAnswer:"}
]
```

**Key design choices:**
- `temperature=0` → same input always gives same output (reproducible)
- Uses an LLM to parse LLM output (meta, but effective)
- Cost: ~$0.001 per extraction (cheap with gpt-4o-mini)

**Your research should document**: which normalization approach you chose and why.

---

# ═══════════════════════════════════════════════════
# LEADERBOARD TASK 6: Answer Normalization (15 min)
# ═══════════════════════════════════════════════════

---

# LIVE — Task 6: Write Your normalize_answer() Function

**Write a Python function that normalizes LLM answers for comparison.**

Test it on these 5 pairs — decide for each: MATCH or NO MATCH?

| Pair | Answer A | Answer B | Your call? |
|------|----------|----------|-----------|
| 1 | "The answer is $160." | "$160" | ? |
| 2 | "Paris" | "paris" | ? |
| 3 | "Abraham Lincoln" | "Lincoln, Abraham" | ? |
| 4 | "3.14159" | "3.14" | ? |
| 5 | "Yes, it is ethical." | "Yes" | ? |

### Rules:
- Pairs 1-2 should clearly match after normalization
- Pairs 3-5 are **design choices** — there's no single right answer
- Your function should handle all 5 consistently

### Submit:
**Go to the leaderboard → Task 6: Answer Normalization**
Paste your function code + results for all 5 pairs.

**Bonus**: If your function handles all 5 with reasonable logic, you're ahead of most published papers.

---

# After Submitting: Compare Approaches (5 min)

*(Instructor: show 2-3 submissions side by side)*

**Discussion:**
- Did everyone handle pair 3 ("Abraham Lincoln" vs "Lincoln, Abraham") the same way?
- What about pair 4 (rounding: "3.14159" vs "3.14")?
- What about pair 5 ("Yes, it is ethical" vs "Yes")?

**Key takeaway**: There is no "correct" normalization. But you MUST:
1. **Pick your approach BEFORE seeing results** (not after)
2. **Document your choices** in CLAUDE.md
3. **Apply it consistently** across all models

---

# ═══════════════════════════════════════════════════
# SECTION 4: RETRY LOGIC & CRASH-PROOFING (15 min)
# ═══════════════════════════════════════════════════

---

# Your API WILL Fail — Plan for It

When you run 600 API calls (50 questions × 4 strategies × 3 models),
some WILL fail:
- **429 Rate Limit** — you're calling too fast
- **500 Server Error** — OpenAI/Anthropic is having a bad day
- **Timeout** — network hiccup
- **Connection Error** — WiFi dropped

**Without retry logic**: Script crashes at call #347 → all results lost → $4 wasted.
**With retry logic**: Script retries failed calls → finishes cleanly → no money wasted.

---

# Exponential Backoff — The Right Way to Retry

```python
import time

def call_with_retry(prompt, model="gpt-4o-mini", max_retries=3):
    """Call an LLM API with automatic retry on failures."""
    for attempt in range(max_retries + 1):
        try:
            response = call_llm(prompt, model=model)

            if response.status_code == 200:
                return response  # Success!

            # Rate limited — wait longer, then retry
            if response.status_code == 429:
                wait = 2 ** attempt * 5  # 5s, 10s, 20s
                print(f"Rate limited. Waiting {wait}s...")
                time.sleep(wait)
                continue

            # Server error — retry
            if response.status_code >= 500:
                wait = 2 ** attempt  # 1s, 2s, 4s
                print(f"Server error {response.status_code}. Retry in {wait}s...")
                time.sleep(wait)
                continue

            # Client error (400, 401, 403) — don't retry, it won't help
            print(f"Client error {response.status_code}: {response.text}")
            return None

        except Exception as e:
            wait = 2 ** attempt
            print(f"Connection error: {e}. Retry in {wait}s...")
            time.sleep(wait)

    print(f"Failed after {max_retries} retries")
    return None  # Don't crash — return None, handle it in the caller
```

**Key design choices:**
- **Exponential backoff**: 1s → 2s → 4s (don't hammer the server)
- **Longer wait for rate limits**: 5s → 10s → 20s
- **Return None on failure** (don't crash the whole experiment)
- **Never retry client errors** (400/401/403 — your request is wrong, retrying won't fix it)

---

# Save Results Immediately — Don't Trust Memory

```python
# BAD: All results in memory — crash during plotting = everything lost
all_results = []
for q in questions:
    result = call_api(q)
    all_results.append(result)  # If crash here → lost
# save_to_file(all_results)  # Script crashes before reaching this line

# GOOD: Save after every API call — crash-proof
import json, time

for i, q in enumerate(questions):
    result = call_with_retry(q)

    # Save IMMEDIATELY — even if the next call crashes
    with open(f"data/results/response_{i:04d}.json", "w") as f:
        json.dump({
            "question": q,
            "response": result,
            "timestamp": time.time(),
            "model": "gpt-4o-mini"
        }, f, indent=2)

    print(f"[{i+1}/{len(questions)}] Saved response_{i:04d}.json")
```

**Horror story**: A student ran 200 API calls ($4), saved to a variable.
Script crashed during plotting. All results lost. Had to re-run everything.

---

# ═══════════════════════════════════════════════════
# LEADERBOARD TASK 7: Retry Logic (10 min)
# ═══════════════════════════════════════════════════

---

# LIVE — Task 7: Write Your call_with_retry()

**Write a Python function that calls an API with exponential backoff.**

### Requirements:
1. Retry on 500, 502, 503, 429 (server errors + rate limit)
2. Don't retry on 400, 401, 403 (client errors)
3. Exponential backoff (1s, 2s, 4s minimum)
4. Return `None` on final failure (don't crash!)
5. Print a log message on every retry

### Bonus points for:
- Different wait times for rate limits vs server errors
- Tracking total retry count across all calls
- Adding a `timeout` parameter

### Submit:
**Go to the leaderboard → Task 7: Retry Logic**
Paste your function code + explain your design choices.

**Tip**: Ask Claude Code or Cursor to help you write this!
```
"Write a call_with_retry() function that calls an LLM API with
exponential backoff. Retry on 500/429, don't retry on 400/401.
Return None on failure. Log every attempt."
```

---

# ═══════════════════════════════════════════════════
# SECTION 5: PROJECT SCAFFOLDING (15 min)
# ═══════════════════════════════════════════════════

---

# The Problem: One Giant main.py

You start coding and end up with one giant `main.py` that does everything:
loading data, calling APIs, computing metrics, making plots.

```python
# main.py (500 lines of chaos)
import openai, json, matplotlib.pyplot as plt

questions = [...]  # 50 lines of hardcoded questions
# ... 100 lines of API calling code ...
# ... 80 lines of metric computation ...
# ... 70 lines of plotting ...
# ... Where is the bug?? Line 347? Line 122? WHO KNOWS
```

**What goes wrong:**
- Bug in plotting → search through 500 lines to find it
- Want to change models → rewrite half the file
- Teammate wants to help → can't both edit the same file
- Reviewer asks "what questions did you test?" → dig through Python code

---

# The Fix: Modular Project Structure

```
my-research-project/
├── data/
│   ├── questions.json          ← your test questions (NOT in code)
│   ├── prompts/
│   │   ├── zero_shot.txt
│   │   ├── few_shot.txt
│   │   └── cot.txt
│   └── results/
│       └── raw_responses.json  ← API responses saved immediately
├── src/
│   ├── data_loader.py          ← loads questions from JSON
│   ├── model_api.py            ← calls LLM APIs (with retry!)
│   ├── metrics.py              ← your normalize_answer + accuracy
│   └── visualization.py        ← generates figures for the paper
├── benchmark_main.py           ← runs the consistency benchmark
├── ablation_main.py            ← runs the prompting ablation
├── CLAUDE.md                   ← your research lab notebook
└── requirements.txt
```

**Notice**: The modules you just built (Task 6: normalize_answer, Task 7: retry)
go directly into `src/metrics.py` and `src/model_api.py`.
You're building your project piece by piece.

---

# Why Separate Data from Code?

Your questions and your code are **different concerns**.

| Scenario | Without data modules | With data modules |
|----------|---------------------|------------------|
| Change a question | Edit Python code, hope nothing breaks | Edit `questions.json`, code unchanged |
| "What 50 questions did I test?" | Read through Python code | Open `questions.json` |
| Rerun with different questions | Rewrite the script | Swap the JSON file |
| Reviewer asks "show your data" | Awkward | Hand them the file |

```json
// data/questions.json — clean, readable, separate
{
  "math": [
    {
      "question": "What is 15% of 200?",
      "paraphrases": ["Calculate 15 percent of 200.", "200 × 0.15 = ?"],
      "expected_answer": "30",
      "difficulty": "easy"
    }
  ]
}
```

---

# The CLAUDE.md Research Lab Notebook

Create a `CLAUDE.md` file in your project root:

```markdown
# My Research Project

## Research Question
Do LLMs give consistent answers when the same question is
rephrased? Testing across GPT-4o, Claude 3.5, and Gemini Pro.

## Experiment Plan
- Models: GPT-4o, Claude 3.5 Sonnet, Gemini 1.5 Pro
- Dataset: 20 questions × 3 paraphrases × 5 categories = 300 prompts
- Metrics: exact match for factual/math, cosine sim > 0.8 for open-ended

## Decisions Made
- [2026-03-15]: Using temperature=0 for reproducibility
- [2026-03-15]: normalize_answer strips preambles, lowercases, removes punctuation
- [2026-03-15]: Retry with exponential backoff (1s, 2s, 4s), return None on failure

## Mistakes to Avoid
- Always save raw API responses BEFORE computing metrics
- Normalize answers before comparing ("$160" vs "The answer is $160")
```

Every decision you make today → write it in CLAUDE.md.

---

# ═══════════════════════════════════════════════════
# LEADERBOARD TASK 8: Build Your Scaffold (15 min)
# ═══════════════════════════════════════════════════

---

# LIVE — Task 8: Build Your Project Scaffold

**Give this prompt to Claude Code or Cursor:**

```
"Create a Python project structure for an LLM evaluation project
that includes both a consistency benchmark and a prompting
ablation study. I need:
- data/ folder for prompts and responses
- src/ folder with modules for: data loading, model API calls,
  metrics computation, and visualization
- benchmark_main.py for the consistency benchmark
- ablation_main.py for the prompting ablation
- requirements.txt
Set it up so I can run: python benchmark_main.py --model gpt-4 --dry-run"
```

### Checklist — verify your scaffold has:
- [ ] `data/questions.json` with at least 3 example questions
- [ ] `src/model_api.py` with your `call_with_retry()` from Task 7
- [ ] `src/metrics.py` with your `normalize_answer()` from Task 6
- [ ] `--dry-run` flag that tests the pipeline without real API calls
- [ ] Results saved to `data/results/` as JSON

### Submit:
**Go to the leaderboard → Task 8: Project Scaffold**
Screenshot your folder tree + paste your `--dry-run` output.

---

# After Submitting: Check Each Other's Work (5 min)

**Pair up and review your neighbor's scaffold:**

1. Can they run `python benchmark_main.py --dry-run` without errors?
2. Does it save results to a file (not just print)?
3. Is `normalize_answer()` in `src/metrics.py` (not buried in main.py)?
4. Is `call_with_retry()` in `src/model_api.py`?
5. Do they have a `CLAUDE.md`?

**If you find a problem**, tell them — fixing it now saves debugging later.

---

# ═══════════════════════════════════════════════════
# SECTION 6: COMMON MISTAKES (10 min)
# ═══════════════════════════════════════════════════

---

# Mistakes That Will Sink Your Research

### Benchmark Design Mistakes

| Mistake | Example | Fix |
|---------|---------|-----|
| All questions same difficulty | 5 easy math like "2+3=?" — 100% consistency | Mix easy AND hard in each category |
| Paraphrases are just synonyms | "15% of 200?" → "fifteen percent of 200?" | Restructure: "If you take 15% from 200, what remains?" |
| Testing only 1 model | "GPT-4o gets 85%" — good or bad? | Compare 2-3 models so the number means something |
| Metric chosen after seeing results | Picked semantic similarity because it gave better numbers | Pre-register your metric BEFORE running |
| No answer normalization | "$160" vs "The answer is $160" scored as mismatch | Use your normalize_answer() function |

### Ablation Design Mistakes

| Mistake | Example | Fix |
|---------|---------|-----|
| Different questions per strategy | Easy for CoT, hard for zero-shot | Same questions across ALL strategies |
| No cost tracking | "CoT+SC is best!" (but costs 5x more) | Report accuracy AND cost per strategy |
| Only 2 strategies | Zero-shot vs CoT — what about few-shot? | Test at least 3-4 |
| No random seed | Results change every time | Set temperature=0, log all prompts |

---

# ═══════════════════════════════════════════════════
# LEADERBOARD TASK 9: Spot the Mistakes (10 min)
# ═══════════════════════════════════════════════════

---

# LIVE — Task 9: Spot the Mistakes

**Read this experiment description. Find ALL the methodology mistakes.**
There are at least 5.

> "I tested GPT-4o on 10 math questions using Chain-of-Thought prompting.
> It got 9/10 correct (90% accuracy). I then tried zero-shot on 10
> **different, easier** questions and it got 7/10 (70%). CoT is clearly
> better. I measured accuracy using semantic similarity because exact match
> gave lower numbers. I didn't set a temperature because the default is fine."

### Can you find all 5+ mistakes?

Think about:
- How many models were tested?
- Were the questions controlled?
- When was the metric chosen?
- Is the temperature reproducible?
- Is the sample size sufficient?

### Submit:
**Go to the leaderboard → Task 9: Spot the Mistakes**
List every mistake you found + what the fix should be.

**The person who finds the most valid mistakes wins!**

---

# Task 9 Answers — How Many Did You Get?

| # | Mistake | Why It's Wrong | Fix |
|---|---------|---------------|-----|
| 1 | Only 1 model tested | 90% means nothing without comparison | Test GPT-4o vs Claude vs Gemini |
| 2 | Different questions per strategy | Can't compare — maybe CoT questions were just easier | Same 10 questions for BOTH strategies |
| 3 | Easier questions for zero-shot | Biases the comparison against zero-shot | Same difficulty across all conditions |
| 4 | Metric chosen after seeing results | Picked semantic similarity because it looked better = p-hacking | Pre-register: "exact match for math" before running |
| 5 | No temperature set | Default varies by provider, results not reproducible | Set temperature=0, document it |
| 6 | Only 10 questions | Too small — 1 question flip = 10% accuracy change | Use 50-100 minimum for meaningful stats |
| 7 | "Clearly better" with no significance test | 90% vs 70% on 10 samples could be random chance | Run a statistical test (McNemar's) or use more samples |

**How many did you find?** 5+ = great research instincts!

---

# ═══════════════════════════════════════════════════
# SECTION 7: REPRODUCIBILITY CHECKLIST (5 min)
# ═══════════════════════════════════════════════════

---

# Before You Say "My Experiment Is Done"

Check every box:

- [ ] **Fixed seed**: `temperature=0` or fixed seed for all API calls
- [ ] **Versioned prompts**: All prompts saved in `data/prompts/` (not hardcoded)
- [ ] **Raw results saved**: Every API response in `data/results/`
- [ ] **Metrics pre-registered**: Defined before running (not picked after)
- [ ] **Multiple models**: At least 2-3 models compared
- [ ] **Answer normalization**: Applied consistently (your Task 6 function)
- [ ] **Error handling**: Retry logic for failed API calls (your Task 7 function)
- [ ] **Cost logged**: Total API spend tracked and reported
- [ ] **`--dry-run` works**: Full pipeline runs without real API calls
- [ ] **CLAUDE.md updated**: All decisions and mistakes documented

---

# ═══════════════════════════════════════════════════
# WRAP-UP & HOMEWORK
# ═══════════════════════════════════════════════════

---

# What You Built Today

| Leaderboard Task | What You Built | Where It Goes |
|-----------------|---------------|--------------|
| Task 5: Prompting Strategy Test | Tested 4 strategies, saw the differences | Your experiment intuition |
| Task 6: Answer Normalization | `normalize_answer()` function | → `src/metrics.py` |
| Task 7: Retry Logic | `call_with_retry()` function | → `src/model_api.py` |
| Task 8: Project Scaffold | Full project structure with --dry-run | Your project repo |
| Task 9: Spot the Mistakes | Research methodology instincts | Avoiding errors in your own work |

**Check the leaderboard** — see where you rank on each task!

---

# Homework Before Next Session

### Must-do:
1. **Finish your scaffold** — `--dry-run` mode should work end-to-end
2. **Add your Task 6 + Task 7 code** into `src/metrics.py` and `src/model_api.py`
3. **Populate `data/questions.json`** with your full question set (from Task 1)
4. **Update CLAUDE.md** with today's decisions
5. **Test on Colab T4** — make sure everything runs before Lambda

### Bonus:
- Make `benchmark_main.py` call a real API for 5 questions (small test)
- Add a `--model` flag so you can switch models from the command line
- Start your `visualization.py` with a simple bar chart of results

### Next Session:
We run the actual experiments, compute metrics, and start generating figures.
**Bring your laptop charged + API keys for OpenAI/Claude/Gemini.**

---

# Resources

| Resource | Link |
|----------|------|
| Workshop Leaderboard | *(your instructor will share the URL)* |
| Lambda Cloud | https://cloud.lambda.ai |
| Lambda docs | https://docs.lambda.ai |
| Google Colab | https://colab.research.google.com |
| HuggingFace Datasets | https://huggingface.co/docs/datasets |
| OpenAI API docs | https://platform.openai.com/docs |
| Anthropic API docs | https://docs.anthropic.com |
