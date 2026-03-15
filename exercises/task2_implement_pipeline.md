# TASK 2: Implement Both Pipelines (25 min)

Build **BOTH** experimental pipelines using the tool progression below.

---

## Part A: Benchmark Pipeline (12 min)

### Step 1: Data Module (5 min) — Use Cursor + Gemini

Create `data/questions.json` with 20 questions (4 per category), each with 3 paraphrases.

**Prompt:**
```
Create a JSON file with 20 questions across 5 categories:
[YOUR CATEGORIES]. Each question should have:
- id, category, original question, 3 paraphrases, expected_answer

Make the paraphrases genuinely different in structure, not just
synonym swaps. Include questions of varying difficulty.
```

**Expected JSON format:**
```json
[
  {
    "id": "math_001",
    "category": "math",
    "original": "What is 15% of 200?",
    "paraphrases": [
      "Calculate 15 percent of 200.",
      "If you take 15% from 200, what do you get?",
      "200 × 0.15 = ?"
    ],
    "expected_answer": "30"
  }
]
```

### Step 2: Evaluation Runner (5 min) — Use Claude Code

```bash
claude "Build src/evaluate.py that:
1. Loads questions from data/questions.json
2. Runs each original + all 3 paraphrases through an LLM API
3. Saves raw responses to results/raw_responses.json
4. Supports --model, --dry-run, and --mock flags
Make it work with: python benchmark_main.py --model gpt-4o-mini --dry-run"
```

**What `evaluate.py` should contain:**

```python
def evaluate_question(question: dict, model: str, mock: bool = False) -> dict:
    """
    Send original + all paraphrases to the model.

    Input:  {"id": "math_001", "original": "What is 15% of 200?",
             "paraphrases": ["Calculate 15 percent of 200.", ...]}

    Output: {"id": "math_001", "model": "gpt-4o-mini",
             "original_response": "30",
             "paraphrase_responses": ["30", "30", "The answer is 30"],
             "timestamp": "2026-03-01T10:00:00Z"}
    """

def run_all(questions: list, model: str, mock: bool, dry_run: bool) -> list:
    """
    Loop through all questions.
    - If dry_run: just print count ("Would run 80 prompts"), don't call API
    - If mock: return fake responses like "mock_answer_for_{id}"
    - Otherwise: call the real API

    IMPORTANT: Save results to results/raw_responses.json after EACH question
    (so a crash at question 15 doesn't lose questions 1-14).
    """
```

**Key decisions to make:**
- Which API library? (`openai`, `anthropic`, `google-generativeai`)
- Temperature? (use `0` for reproducibility)
- Max tokens? (same for ALL calls — e.g., `max_tokens=500`)
- Rate limits? (add `time.sleep(1)` between calls, retry on 429)

### Step 3: Metrics (2 min) — Any tool

```bash
claude "Write src/metrics.py with these three functions.
Include examples in the docstrings."
```

**What `metrics.py` should contain:**

```python
def exact_match(response_a: str, response_b: str) -> bool:
    """
    Are the two responses the same answer after normalization?

    Normalization: lowercase, strip whitespace, remove punctuation,
    extract the key answer (e.g., "$160" from "The answer is $160.")

    Examples:
      exact_match("The answer is $160.", "$160")  → True
      exact_match("Paris", "paris")               → True
      exact_match("It's ethical", "There are concerns") → False
    """

def semantic_similarity(response_a: str, response_b: str) -> float:
    """
    How similar are the responses in meaning? Returns 0.0 to 1.0.

    Simple approach (no ML needed):
      words_a = set(response_a.lower().split())
      words_b = set(response_b.lower().split())
      return len(words_a & words_b) / len(words_a | words_b)

    Better approach: TF-IDF cosine similarity (use sklearn)

    Examples:
      semantic_similarity("The capital is Canberra", "Canberra is the capital") → ~0.95
      semantic_similarity("Yes, AI hiring is ethical", "No, AI hiring is bad")  → ~0.4
    """

def consistency_score(original_response: str,
                      paraphrase_responses: list[str]) -> dict:
    """
    Compare the original against ALL paraphrase responses.

    Returns: {
      "exact_match_rate": 0.67,      # 2 out of 3 matched exactly
      "avg_similarity": 0.85,        # average semantic similarity
      "all_responses_agree": False,   # True only if ALL match
      "num_paraphrases": 3
    }

    This is THE key metric for the benchmark.
    """
```

### Verify:
```bash
python benchmark_main.py --dry-run --mock
# Should print 20 questions × 4 variants = 80 prompts
```

---

## Part B: Ablation Pipeline (13 min)

### Step 1: Data + Prompts (3 min) — Use Cursor + Gemini

Load your dataset and create prompt templates:

```python
# Load dataset (one line!)
from datasets import load_dataset
ds = load_dataset("gsm8k", "main", split="test[:50]")

# Define strategies — each is a template string
STRATEGIES = {
    "zero_shot": "{question}",
    "few_shot": "Here are some examples:\n{examples}\n\nNow solve: {question}",
    "chain_of_thought": "{question}\n\nLet's think step by step.",
    "cot_self_consistency": "{question}\n\nLet's think step by step."
    # (same prompt as CoT, but run 5 times and take majority vote)
}
```

**Important:** Your few-shot examples must NOT come from your test set.
Use examples 1-5 for few-shot prompts, evaluate on examples 6-55.

### Step 2: Evaluation Runner (7 min) — Use Claude Code

```bash
claude "Build ablation_evaluate.py that:
1. Loads dataset from HuggingFace (or data/test_examples.json)
2. Runs each example through ALL prompting strategies
3. Saves results as (example × strategy × model) to results/ablation.json
4. Supports --model, --strategy, --dry-run, --mock flags
Make it work with: python ablation_main.py --model gpt-4o-mini --dry-run"
```

**What `ablation_evaluate.py` should contain:**

```python
def format_prompt(question: str, strategy: str, examples: list = None) -> str:
    """
    Apply the strategy template to a question.

    Examples:
      format_prompt("What is 25% of 80?", "chain_of_thought")
      → "What is 25% of 80?\n\nLet's think step by step."

      format_prompt("What is 25% of 80?", "few_shot", examples=[...])
      → "Here are some examples:\n...\n\nNow solve: What is 25% of 80?"
    """

def extract_answer(response: str, task_type: str) -> str:
    """
    Parse the final answer from a model's response.

    WITHOUT this, "Step 1: 25% = 0.25. Step 2: 0.25 × 80 = 20. Answer: 20"
    won't match the expected answer "20".

    Strategies:
    - Look for "Answer: X" or "the answer is X" patterns
    - Take the last number in the response (for math tasks)
    - For sentiment: look for "positive" / "negative"

    Examples:
      extract_answer("Step 1: ... Step 2: ... The answer is 20.", "math") → "20"
      extract_answer("The sentiment is positive.", "sentiment")           → "positive"
    """

def run_single(question: str, expected: str, strategy: str,
               model: str, mock: bool) -> dict:
    """
    Run ONE question with ONE strategy on ONE model.

    For cot_self_consistency: run the SAME prompt 5 times,
    extract answer from each, take the majority vote.

    Returns: {
      "question": "What is 25% of 80?",
      "expected": "20",
      "strategy": "chain_of_thought",
      "model": "gpt-4o-mini",
      "response": "Step 1: 25% = 0.25. Step 2: 0.25 × 80 = 20. Answer: 20",
      "extracted_answer": "20",
      "correct": True,
      "timestamp": "2026-03-01T10:00:00Z"
    }
    """

def run_all(dataset: list, strategies: list, model: str,
            mock: bool, dry_run: bool) -> list:
    """
    Nested loop: for each example × each strategy → run_single().

    50 examples × 4 strategies = 200 API calls
    (CoT-SC runs 5x internally, so ~250 extra for that strategy)

    Save incrementally to results/ablation.json after each example.
    """
```

**Key decisions to make:**
- Same temperature for ALL strategies (`temperature=0`)
- Same `max_tokens` for ALL strategies (e.g., 500) — don't give CoT more room
- Separate few-shot examples from test data (data contamination!)
- Log exact model ID and timestamp in every result

### Step 3: Accuracy Scoring (3 min) — Any tool

```bash
claude "Write src/ablation_metrics.py with these functions.
Include examples in the docstrings."
```

**What `ablation_metrics.py` should contain:**

```python
def accuracy(results: list[dict]) -> float:
    """
    What fraction of answers were correct?

    Example: 39 out of 50 correct → 0.78 (78%)
    """

def per_strategy_accuracy(all_results: list[dict]) -> dict:
    """
    Group results by strategy, compute accuracy for each.

    Returns: {
      "zero_shot":             {"accuracy": 0.62, "correct": 31, "total": 50},
      "few_shot":              {"accuracy": 0.72, "correct": 36, "total": 50},
      "chain_of_thought":      {"accuracy": 0.78, "correct": 39, "total": 50},
      "cot_self_consistency":  {"accuracy": 0.82, "correct": 41, "total": 50}
    }

    This is THE key output for the ablation study.
    """

def per_strategy_per_model(all_results: list[dict]) -> dict:
    """
    Group by strategy AND model for the full comparison matrix.

    Returns: {
      "zero_shot":   {"gpt-4o-mini": 0.62, "claude-sonnet": 0.58},
      "few_shot":    {"gpt-4o-mini": 0.72, "claude-sonnet": 0.70},
      ...
    }
    """

def statistical_comparison(scores_a: list[bool],
                           scores_b: list[bool]) -> dict:
    """
    Are two strategies significantly different?

    Use McNemar's test (or paired t-test on per-example 0/1 scores).

    Returns: {
      "strategy_a_accuracy": 0.72,
      "strategy_b_accuracy": 0.78,
      "difference": 0.06,
      "p_value": 0.034,
      "significant": True    # p < 0.05
    }

    If p < 0.05 → "The difference is statistically significant."
    If p >= 0.05 → "We cannot conclude the strategies differ."
    """
```

### Verify:
```bash
python ablation_main.py --dry-run --mock
# Should print 50 examples × 4 strategies = 200 prompts
```

---

## No API keys? That's fine!

Use `--mock` mode to test the full pipeline with fake responses.
The pipeline **structure** matters more than real results during the workshop.

Ask Claude to verify:
```bash
claude "Check my pipeline output in results/. Verify:
1. All questions/examples have responses
2. No empty or malformed entries
3. The JSON structure is consistent"
```

---

## Quick Reference: What Each File Does

| File | Input | Output | Key Function |
|------|-------|--------|-------------|
| `data/questions.json` | — | 20 questions with paraphrases | Your experiment data |
| `src/evaluate.py` | questions.json | results/raw_responses.json | Send questions to LLM APIs |
| `src/metrics.py` | raw_responses.json | consistency scores | Compare original vs paraphrases |
| `src/prompts.py` | — | strategy templates | Define zero-shot, few-shot, CoT, CoT+SC |
| `src/ablation_evaluate.py` | dataset + prompts | results/ablation.json | Run all strategies on all examples |
| `src/ablation_metrics.py` | ablation.json | accuracy per strategy | Score and compare strategies |

---

## What makes answers VARIED:
- Different dataset content (everyone wrote different questions)
- Different API calling patterns (async vs sync)
- Different metric implementations (Jaccard vs TF-IDF vs exact match)
- Different answer extraction logic
- Different error handling approaches
