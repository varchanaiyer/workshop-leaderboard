# TASK 1: Plan Both Experiments (10 min)

You'll plan **BOTH** projects below. Use any AI tool to help you.

---

## Part A: BenchmarkLite — LLM Consistency (5 min)

**Research question**: Do LLMs give the same answer when you rephrase the same question?

### Example questions for inspiration:

| Category | Example | Paraphrases |
|----------|---------|-------------|
| Math | "What is 15% of 200?" | "Calculate 15 percent of 200." / "200 × 0.15 = ?" |
| Logic | "If all roses are flowers and some flowers fade quickly, must some roses fade quickly?" | "Every rose is a flower. Some flowers fade. Does it follow for roses?" |
| Factual | "What is the capital of Australia?" | "Which city serves as Australia's capital?" |
| Ethics | "Is it ethical to use AI for hiring?" | "Should companies use AI to decide who gets hired?" |
| Creative | "Write a one-sentence story about a robot learning to paint." | "In one sentence, tell a story of a robot discovering painting." |

### Your deliverables:
1. **Choose 5 question categories** — pick YOUR OWN (medical, legal, coding, history, psychology...)
2. **Write 1 example question + 3 paraphrases** for one category
3. **Pick 2-3 models** to test (e.g., GPT-4o, Claude Sonnet, Gemini, Llama 3)
4. **Define your consistency metric** — how will you measure if two answers "match"?

### Suggested prompt:
```
claude "I'm designing a benchmark to test LLM consistency on
paraphrased questions. Use plan mode. Help me:
1. Choose 5 question categories that will show interesting variation
2. Define what 'consistency' means for each category
3. Suggest a scoring rubric (exact match vs semantic similarity)
4. Identify potential confounds I should control for"
```

---

## Part B: Prompting Ablation Study (5 min)

**Research question**: Which prompting strategy works best for [your task]?

### Example walkthrough (math task):

```
Question: "A store sells a jacket for $120 after a 25% discount. Original price?"

Zero-shot → "The original price was $160."
Few-shot  → "Following the pattern: $120 / 0.75 = $160."
CoT       → "Step 1: Sale = 75% of original. Step 2: $120 = 0.75×X. Step 3: X = $160."
CoT+SC    → Run 5×: [$160, $160, $160, $150, $160] → majority vote: $160
```

### Suggested datasets (pick one):

| Task | Dataset | How to Load |
|------|---------|-------------|
| Math word problems | GSM8K | `load_dataset("gsm8k", "main", split="test[:50]")` |
| Sentiment analysis | SST-2 | `load_dataset("glue", "sst2", split="validation[:50]")` |
| Reading comprehension | SQuAD 2.0 | `load_dataset("squad_v2", split="validation[:50]")` |
| Commonsense reasoning | HellaSwag | `load_dataset("hellaswag", split="validation[:50]")` |
| Code generation | HumanEval | `load_dataset("openai_humaneval", split="test[:20]")` |
| Trivia / factual | TriviaQA | `load_dataset("trivia_qa", "rc", split="validation[:50]")` |

### Your deliverables:
1. **Choose your task + dataset** from the table above (or your own)
2. **Design 3-4 prompting strategies** with example prompts
3. **Use same 2-3 models** from Part A
4. **Define your primary metric** (accuracy, F1, exact match, etc.)

### Suggested prompt:
```
claude "I want to compare prompting strategies for [YOUR TASK]
using [YOUR DATASET]. Use plan mode. Help me:
1. Define 4 strategies (zero-shot, few-shot, CoT, CoT+SC)
2. Write template prompts for each
3. How to load and format the dataset
4. What metric captures performance best"
```

---

## What makes answers VARIED across students:
- Different category choices for the benchmark
- Different task/dataset choices for the ablation
- Different paraphrase strategies and metric definitions
- Different prompting template designs

## Sharing (3 min)
Be ready to share:
- Your benchmark categories + one example paraphrase set
- Your ablation task/dataset choice
- One thing the AI suggested that you hadn't thought of
