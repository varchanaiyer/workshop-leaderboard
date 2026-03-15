# AI Research Implementation Workshop
## From Research Question to Paper — Using AI Coding Tools

**Algoverse AI Research**
Duration: ~3 hours (single session)
Students: 20–30

---

# Slide 1: Welcome & What You'll Build Today

By the end of this session you will have:
- Set up and compared 3 AI coding tools (free → paid)
- Designed a mini research benchmark AND run a prompting ablation study
- Implemented an experimental pipeline with AI assistance
- Analyzed results and drafted paper-ready outputs
- Learned to optimize code for Lambda GPUs

**You will all get DIFFERENT results — that's the point.**

---

# Slide 2: The 3 Tools We'll Use Today

| Tool | Cost | How It Works |
|------|------|-------------|
| **Cursor + Gemini** | $20/mo (Cursor sub) | IDE-based, inline completions, chat panel. Gemini model is free. |
| **Claude Code Router + Gemini** | $20/mo (Claude Code sub) | Terminal-based. Routes simple tasks to Gemini (free), complex to Claude. |
| **Claude Code (direct)** | $20/mo + API usage | Terminal-based. Uses Claude Opus/Sonnet for everything. Best quality. |

We'll start with the FREE option and level up.

---

# Slide 3: Tool Tier Strategy

```
 Cost ──────────────────────────────────────────────►

 FREE                    $20/mo                 $20 + API
  │                        │                       │
  ▼                        ▼                       ▼
 Gemini API            Cursor OR              Claude Code
 (in Cursor/Router)    Claude Router           (direct Opus)
  │                        │                       │
  ├─ Brainstorming         ├─ Multi-file edits     ├─ Complex architecture
  ├─ Boilerplate           ├─ Debugging            ├─ Plan mode
  ├─ Data formatting       ├─ Pipeline code        ├─ Worktree parallelism
  └─ Simple scripts        └─ Analysis code        └─ Paper-quality output
```

**Rule of thumb**: If you can explain the task in 1 sentence → Gemini.
If you need a paragraph → Claude.

---

# Slide 4: Setup Check (5 min)

Everyone should have ONE of these ready:
1. **Cursor** installed with Gemini model selected (Settings → Models → Gemini 2.5)
2. **Claude Code** installed (`npm install -g @anthropic-ai/claude-code`)
3. Both (ideal)

Quick test:
```bash
# Claude Code
claude "Say hello and tell me what model you are"

# Cursor
# Open a file, press Cmd+K, type "write a hello world in python"
```

---

# Slide 5: Today's Research Projects — You'll Do BOTH

### Project A: BenchmarkLite
**"Do LLMs give consistent answers when you rephrase the same question?"**
- Design 20 questions across 5 categories, create 3 paraphrase variants each
- Test across 2-3 models
- Measure consistency (exact match, semantic similarity)

### Project B: Prompting Ablation
**"Which prompting strategy works best for [your chosen task]?"**
- Pick a task and dataset (math, reasoning, classification, summarization)
- Test 3-4 prompting strategies (zero-shot, few-shot, CoT, CoT+SC)
- Compare accuracy across strategies and models

**Both are real, publishable research directions. You'll build both today.**

---

# Slide 6: What Both Projects Teach

| Skill | Project A (Benchmark) | Project B (Ablation) |
|-------|---------------------|---------------------|
| Experiment design | Design evaluation categories | Design prompting conditions |
| Data curation | Create question + paraphrase sets | Curate test examples per task |
| API integration | Call multiple LLM APIs | Call multiple LLM APIs |
| Statistical analysis | Consistency metrics | Accuracy comparisons |
| Paper writing | Tables, figures, claims | Tables, figures, claims |
| Reproducibility | Fixed seed, versioned prompts | Fixed seed, controlled variables |

---

# Slide 7: Example Questions for the Benchmark (Inspiration)

Here's what your benchmark questions could look like — one per category:

| Category | Example Question | Paraphrase 1 | Paraphrase 2 |
|----------|-----------------|---------------|---------------|
| Math | "What is 15% of 200?" | "Calculate 15 percent of 200." | "200 × 0.15 = ?" |
| Logic | "If all roses are flowers and some flowers fade quickly, can we conclude some roses fade quickly?" | "Given every rose is a flower and certain flowers fade fast, does it follow that certain roses fade fast?" | "All roses ⊂ flowers. Some flowers fade. Must some roses?" |
| Factual | "What is the capital of Australia?" | "Which city serves as Australia's capital?" | "Name Australia's capital city." |
| Ethics | "Is it ethical to use AI for hiring?" | "Should companies use AI to decide who gets hired?" | "Is there a moral issue with AI screening candidates?" |
| Creative | "Write a one-sentence story about a robot learning to paint." | "In one sentence, tell a story of a robot discovering painting." | "Compose a one-liner about an automaton taking up art." |

Pick YOUR OWN categories — medical, legal, coding, history, psychology...
The more varied across the room, the better the discussion.

---

# Slide 8: Example Ablation — Step-by-Step Walkthrough

Same question, 4 different prompting strategies — see how outputs differ:

**Question**: "A store sells a jacket for $120 after a 25% discount. What was the original price?"

| Strategy | What You Send | Example Output |
|----------|--------------|----------------|
| Zero-shot | Just the question | "The original price was $160." |
| Few-shot | 3 worked examples + question | "Following the pattern: $120 / 0.75 = $160." |
| Chain-of-Thought | Question + "Let's think step by step." | "Step 1: Sale price = 75% of original. Step 2: $120 = 0.75 × X. Step 3: X = $160." |
| CoT + Self-Consistency | Run CoT 5 times, majority vote | Runs: [$160, $160, $160, $150, $160] → Majority: $160 |

Notice: CoT gives the reasoning path, Self-Consistency catches occasional errors.
Your task will use YOUR chosen dataset — results will vary!

---

# Slide 9: Suggested Datasets for the Ablation (Pick One)

| Task | Dataset | Size to Use | How to Load | Why It's Good |
|------|---------|-------------|-------------|---------------|
| Math word problems | GSM8K | 50-100 | `load_dataset("gsm8k", "main", split="test[:50]")` | Clear answers, varying difficulty |
| Sentiment analysis | SST-2 | 50-100 | `load_dataset("glue", "sst2", split="validation[:50]")` | Binary labels, easy to score |
| Reading comprehension | SQuAD 2.0 | 50 | `load_dataset("squad_v2", split="validation[:50]")` | Extractive QA, gold answers |
| Commonsense reasoning | HellaSwag | 50 | `load_dataset("hellaswag", split="validation[:50]")` | Multiple choice, easy accuracy |
| Code generation | HumanEval | 20 | `load_dataset("openai_humaneval", split="test[:20]")` | Has test cases for verification |
| Trivia / factual | TriviaQA | 50 | `load_dataset("trivia_qa", "rc", split="validation[:50]")` | Short answers, easy exact match |

```python
# One line to load any dataset:
from datasets import load_dataset
ds = load_dataset("gsm8k", "main", split="test[:50]")
```

---

# ═══════════════════════════════════════════════════
# PART 1: PLAN YOUR RESEARCH (30 min)
# ═══════════════════════════════════════════════════

---

# Slide 10: Step 1 — Research Planning with AI

**Demo** (instructor shows both tools):

### Cursor + Gemini (free):
Open a new file `research_plan.md`, then Cmd+K:
```
"I want to evaluate LLM consistency on paraphrased questions.
Help me design: (1) 5 question categories, (2) how to create
paraphrases, (3) what metrics to measure, (4) which models to test"
```

### Claude Code (terminal):
```bash
claude "I want to run an ablation study on prompting strategies
for math word problems using GSM8K. Help me plan:
(1) which strategies to compare, (2) how to load the dataset,
(3) what metrics to use. Use plan mode."
```

Notice how Claude Code's **plan mode** gives structured, step-by-step output.

---

# Slide 11: The CLAUDE.md — Your Research Lab Notebook

Before coding, create a `CLAUDE.md` in your project root:

```markdown
# My Research Project

## Research Question
[Your 1-sentence question here]

## Experiment Plan
- Models: [list]
- Dataset: [description]
- Metrics: [list]

## Decisions Made
- [Date]: Chose X because Y

## Mistakes to Avoid
- [Claude will add these as you work]
```

**Key insight from the Claude Code creator (Boris Cherny):**
> "After every correction, end with 'Update your CLAUDE.md so you don't
> make that mistake again.' This is your institutional memory."

---

# Slide 12: TASK 1 — Plan Both Experiments (10 min)

**Use ANY tool. Come back with plans for BOTH:**

### Part A: Benchmark Plan (5 min)
1. Your 5 question categories (take inspiration from the examples slide)
2. An example question + 3 paraphrases for ONE category
3. Which 2-3 models you'll test
4. Your consistency metric definition

### Part B: Ablation Plan (5 min)
1. Your chosen task + dataset (see the datasets slide)
2. Your 3-4 prompting strategies with example prompts
3. Same 2-3 models from Part A
4. Your primary metric (accuracy, F1, etc.)

**Everyone's plans will be different — that's expected and good.**
We'll have 3-4 students share their plans.

---

# Common Mistakes — Task 1

| Mistake | Example | Fix |
|---------|---------|-----|
| All questions same difficulty | 5 easy math Qs like '2+3=?' — all get 100% consistency, learns nothing | Mix: '2+3' AND 'integral of e^x sin(x)' in same category |
| Paraphrases are just synonym swaps | 'What is 15% of 200?' → 'What is fifteen percent of 200?' (trivial change) | Restructure: 'If you take 15% from 200, what remains?' (different framing) |
| No ground truth for subjective Qs | 'Is AI ethical?' — two valid but different essays score as 'inconsistent' | Define per type: exact match for math, theme overlap for ethics |
| Testing only 1 model | GPT-4o gets 85% consistency — is that good or bad? No way to know. | Compare GPT-4o (85%) vs Claude (72%) vs Gemini (90%) → now it means something |
| Metric chosen after seeing results | You pick 'semantic similarity' because it makes your numbers look better | Pre-register: 'exact match for factual, cosine sim >0.8 for open-ended' |
| No answer normalization | '$160' vs 'The original price was $160.' flagged as mismatch (they agree!) | Strip to key answer first: both become '$160', then compare |

---

# ═══════════════════════════════════════════════════
# PART 2: IMPLEMENT YOUR PIPELINE (45 min)
# ═══════════════════════════════════════════════════

---

# Slide 13: Step 2 — Project Scaffolding

**Demo**: Use Claude Code to scaffold the project:

```bash
claude "Create a Python project structure for an LLM evaluation
project that includes both a consistency benchmark and a prompting
ablation study. I need:
- data/ folder for prompts and responses
- src/ folder with modules for: data loading, model API calls,
  metrics computation, and visualization
- benchmark_main.py for the consistency benchmark
- ablation_main.py for the prompting ablation
- requirements.txt
Set it up so I can run: python benchmark_main.py --model gpt-4 --dry-run"
```

---

# Slide 14: The Data Modules

### Project A — Benchmark dataset:
```python
# data/questions.json
{
    "id": "math_001",
    "category": "math",
    "original": "What is 15% of 200?",
    "paraphrases": [
        "Calculate 15 percent of 200.",
        "If you take 15% from 200, what do you get?",
        "200 times 0.15 equals what?"
    ]
}
```

### Project B — Ablation prompts + dataset:
```python
# src/prompts.py
STRATEGIES = {
    "zero_shot": "{question}",
    "few_shot": "Examples:\n{examples}\n\nNow answer: {question}",
    "chain_of_thought": "{question}\nLet's think step by step.",
    "cot_self_consistency": "{question}\nThink step by step. (run 5x, majority vote)"
}

# Load dataset:
from datasets import load_dataset
ds = load_dataset("gsm8k", "main", split="test[:50]")
```

---

# Slide 15: Tool Comparison — Writing the API Module

**Same task, 3 tools:**

### Cursor + Gemini:
- Open `src/model_api.py`
- Cmd+K → "Write a function that calls OpenAI and Anthropic APIs with the same prompt and returns both responses. Handle rate limits."
- Gemini generates inline, you iterate in the IDE

### Claude Code Router + Gemini:
```bash
claude "Write src/model_api.py — a module that calls OpenAI and
Anthropic APIs with retry logic. Use async for parallel calls."
```
Simple task → Router sends to Gemini (free). Good enough.

### Claude Code (direct):
```bash
claude "Write src/model_api.py with: (1) async API calls to OpenAI
and Anthropic, (2) retry with exponential backoff, (3) response
caching to avoid re-running, (4) cost tracking per call.
Then write tests to verify it works."
```
Complex multi-concern task → Claude Opus handles it better.

---

# Slide 16: TASK 2 — Implement Both Pipelines (25 min)

**Build BOTH experimental pipelines using the tool progression:**

### Part A: Benchmark Pipeline (12 min)
1. **Cursor/Gemini** (5 min): Generate questions.json — 20 questions with paraphrases
2. **Claude Code** (5 min): Build evaluate.py — run all variants through model APIs
3. **Any tool** (2 min): Write metrics.py — consistency score (exact match + similarity)

### Part B: Ablation Pipeline (13 min)
1. **Cursor/Gemini** (3 min): Load your dataset, create prompt templates
2. **Claude Code** (7 min): Build ablation_evaluate.py — run all strategies
3. **Any tool** (3 min): Add accuracy scoring + comparison

**Test both**: `python benchmark_main.py --dry-run` and `python ablation_main.py --dry-run`

No API keys? Use `--mock` mode. The pipeline structure matters more than real results.

---

# Common Mistakes — Task 2

| Mistake | Example | Fix |
|---------|---------|-----|
| Not setting temperature/seed | Run twice: GPT-4o gives 78% then 84% accuracy — which is real? | Set temperature=0: now both runs give 81%, reproducible |
| Few-shot examples from test set | Your 3 few-shot examples are also in your 50 eval questions → inflated score | Split: examples 1-5 for few-shot prompts, examples 6-55 for evaluation |
| Different token limits per strategy | CoT gets max_tokens=1000, zero-shot gets 100 — CoT wins because it can finish | Set max_tokens=500 for ALL strategies, same playing field |
| No rate limit handling | Script crashes at question 23/50 with '429 Too Many Requests' — lose all progress | Add: time.sleep(1) between calls + retry with backoff + save partial results |
| No --mock mode for testing | Debugging a JSON parsing bug costs $2 in API calls before you find the typo | Build --mock first: return 'mock answer' → test full pipeline for $0 |
| Mixing model versions | You tested 'gpt-4o' in Jan vs Mar — OpenAI updated it, results differ | Log: model='gpt-4o-2024-11-20', timestamp='2025-03-01T10:00Z' in results |

---

# Slide 17: The Worktree Power Move

If you have Claude Code, this is the #1 productivity unlock:

```bash
# Terminal 1 — work on benchmark pipeline
claude /worktree benchmark
# "Build the consistency benchmark: data, evaluation, metrics"

# Terminal 2 — work on ablation pipeline
claude /worktree ablation
# "Build the prompting ablation: strategies, evaluation, accuracy"

# Terminal 3 — work on shared API module
claude /worktree shared
# "Build the shared model API module with caching and retry"
```

3 parallel Claude sessions, each on an isolated branch.
Merge when done. This is how the Claude Code team works internally.

---

# ═══════════════════════════════════════════════════
# PART 3: ANALYZE & WRITE (30 min)
# ═══════════════════════════════════════════════════

---

# Slide 18: Step 3 — Results Analysis

**Demo**: Generate analysis from saved results:

```bash
claude "Read results from both experiments.
For the benchmark: generate a model × category consistency matrix.
For the ablation: generate a strategy × model accuracy table.
Create a bar chart for each.
Run statistical significance tests.
Save figures to figures/ and summary to results/analysis.md"
```

**Cursor alternative**: Open results JSON, highlight it, ask Gemini
to "create a pandas analysis script that generates tables and plots."

---

# Slide 19: The "Grill Me" Pattern — AI as Reviewer

This is the most underused technique. Before you write your paper:

```bash
claude "Review my results in results/analysis.md. Be harsh. Check:
1. Do my claims match the numbers in the tables?
2. Are there statistical claims without significance tests?
3. Is anything misleading or cherry-picked?
4. What are the biggest limitations I'm not acknowledging?

Grill me on these and don't let me write the paper until I pass."
```

This pattern forces you to think critically about your own work —
exactly what a reviewer will do.

---

# Slide 20: TASK 3 — Analyze Both & Compare (15 min)

**Run analysis for BOTH experiments:**

### Part A: Benchmark Analysis (7 min)
1. Generate consistency matrix (Model × Category)
2. Create a grouped bar chart
3. Write 2-sentence finding

### Part B: Ablation Analysis (8 min)
1. Generate accuracy table (Strategy × Model)
2. Create a grouped bar chart
3. Write 2-sentence finding

**Combined insight**: Do your benchmark and ablation results tell a related story?
(e.g., "Models that are more consistent also benefit more from CoT prompting")

**Share time**: 3-4 students present their findings.
Compare: everyone's results differ. That's research!

---

# Common Mistakes — Task 3

| Mistake | Example | Fix |
|---------|---------|-----|
| No error bars | Report 'CoT accuracy: 78%' — but across 50 Qs, 95% CI is [65%, 91%] | Always: '78% (±13%, n=50)' — shows the uncertainty honestly |
| Cherry-picking results | CoT wins on math (85%) but loses on sentiment (40%) — you only show math | Report ALL: 'CoT wins on math (+15%) but hurts sentiment (-10%)' |
| Claims don't match numbers | 'CoT significantly outperforms zero-shot' but scores are 78% vs 76% (p=0.42) | Grill Me check: 'Is 2% with p=0.42 significant? No. Rephrase the claim.' |
| Y-axis manipulation | Bar chart Y-axis from 75% to 85% — makes 3% gap look like 10x difference | Start Y-axis at 0, or add a note: 'Note: Y-axis starts at 75%' |
| No combined insight | Two separate findings but no connection between benchmark + ablation results | 'Models inconsistent on ethics also gain most from CoT on ethics' → real insight |
| Overgeneralizing | 'LLMs are unreliable' from testing 2 models on 50 math questions | 'GPT-4o and Claude show 72-85% consistency on math paraphrases (n=50)' |

---

# ═══════════════════════════════════════════════════
# PART 4: LAMBDA GPU OPTIMIZATION (35 min)
# ═══════════════════════════════════════════════════

---

# Slide 21: What Is a GPU and Why Do You Need One?

**CPU** = your laptop's brain. Great at doing one thing at a time, very fast.
**GPU** = a chip designed to do *thousands* of small tasks at the same time.

```
CPU:  ████████████████████████████████  (1 task, very fast)

GPU:  ████  ████  ████  ████  ████     (1000s of tasks, all at once)
      ████  ████  ████  ████  ████
      ████  ████  ████  ████  ████
```

AI models are massive math problems. A single **forward pass** through BERT
(running your input through the model to get a prediction) multiplies
millions of numbers together — GPUs eat that for breakfast.

| Task | CPU Time | GPU Time |
|------|----------|----------|
| Train BERT for 1 epoch (1000 samples) | ~45 min | ~2 min |
| Run inference on 500 prompts | ~25 min | ~30 sec |
| Fine-tune a 7B model | Days/weeks | Hours |

**Bottom line**: If you're doing anything beyond calling an API, you need a GPU.

---

# Slide 22: Why Lambda?

Most Algoverse research that goes beyond API calls needs GPUs:
- Fine-tuning models (making a pre-trained model learn your specific task)
- Running local open-source models (Llama, Mistral, Gemma)
- Large-scale inference (running 10,000+ prompts through a model)
- Training from scratch

Lambda gives you cloud GPUs on demand — you rent a powerful GPU machine
by the hour, use it, then shut it down.

**But GPU time = money. Every wasted minute costs real dollars.**

Your team has **$400 in credits**. That sounds like a lot, but:
- A100 on-demand = $1.29/hr → $400 = ~310 hours
- H100 on-demand = $3.29/hr → $400 = ~121 hours
- Wasting 50% of GPU time = throwing away $200

---

# Slide 23: The Free Alternative — Google Colab T4 GPUs

Before spending Lambda credits, try **Google Colab** — it's free!

**What is a T4 GPU?**
- NVIDIA Tesla T4: 16GB memory, designed for inference + small training
- Free on Google Colab (with usage limits)
- Perfect for: testing code, small fine-tuning, running inference

**How to get a T4 on Colab:**
1. Go to [colab.research.google.com](https://colab.research.google.com)
2. Click the dropdown arrow next to "Connect" (top right)
3. Select "Change runtime type"
4. Choose **T4 GPU** → Click "Save"
5. Run `!nvidia-smi` to verify

**Limitations:**
- Sessions timeout after ~90 min idle (12 hrs max)
- GPU not guaranteed during peak times
- Only 16GB memory (can't fit models > 7B easily)
- No persistent storage (save to Google Drive!)

**Rule of thumb:** Develop and test on Colab T4 for free → then move to Lambda for the real run.

---

# Quick Quiz 1: GPU Basics

**Answer these before moving on:**

1. Why is a GPU faster than a CPU for AI training?
   - a) GPUs have more RAM
   - b) GPUs do thousands of calculations in parallel
   - c) GPUs are newer technology
   - d) GPUs use less electricity

2. Your team has $400 in Lambda credits. A100 costs $1.29/hr.
   How many hours can you run? (round down)

3. True or False: You should develop and debug your code directly on a Lambda GPU instance.

*(Answers: 1-b, 2-310 hours, 3-False — develop locally or on free Colab first!)*

---

# Slide 24: How to Launch a Lambda Instance — Step by Step

### Step 1: Create your account & add billing
Go to [cloud.lambda.ai](https://cloud.lambda.ai) → sign up → **add a payment method**.

**Important**: You MUST add billing info before you can do anything —
even adding SSH keys requires a billing-linked account.
If your team is using shared Algoverse credits, your team lead will
set up the account and add your SSH keys for you.

### Step 2: Add an SSH key (how your computer proves its identity)

**First, generate a key on YOUR laptop** (if you don't have one):
```bash
# Check if you already have one:
ls ~/.ssh/id_rsa.pub    # or id_ed25519.pub

# If not, generate one:
ssh-keygen -t ed25519 -C "your-email@example.com"
# Press Enter for default location, set a passphrase (or leave empty)
```

**Then add it to Lambda:**
- In the Lambda dashboard, click **SSH Keys** in the left sidebar
- Click **"Add SSH key"** (top right)
- **Option A**: Paste your existing public key (`cat ~/.ssh/id_ed25519.pub`)
- **Option B**: Click "Generate a new SSH key" → it downloads a `.pem` file
  ```bash
  # If you generated a key on Lambda, make it secure:
  mv ~/Downloads/lambda_key.pem ~/.ssh/lambda_key
  chmod 600 ~/.ssh/lambda_key
  ```

### Step 3: Launch an instance
- Click **"Instances"** → **"Launch Instance"**
- Choose your GPU type (start with the cheapest that fits your needs!)
- Choose a **region** (more on this next slide)
- Select your SSH key → Click **"Launch"**

### Step 4: Wait for boot
- 1-GPU instances: **3-5 minutes**
- Multi-GPU instances: **10-15 minutes**

---

# Slide 25: Choosing a Region — This Matters!

Lambda has data centers in multiple locations. Each instance lives in **one region**.

**Known Lambda regions:**
| Region Code | Location |
|-------------|----------|
| us-west-1 | California, USA |
| us-west-3 | Utah, USA |
| us-south-1 | Texas, USA |
| us-east-1 | Eastern USA |
| europe-central-1 | Europe |

### What to consider:
1. **Availability**: Not every GPU type is available in every region.
   If "A100" shows "Sold Out" → try a different region!
2. **Latency**: Pick a region closest to you for faster SSH response.
3. **Data transfer**: If your data is in a US cloud bucket, pick a US region.

### When instances aren't available (this happens a lot!):
```
"No instances available" — what to do:
```
1. **Try a different region** — us-west-1 sold out? Try us-south-1 or us-west-3
2. **Try a different GPU** — A100 unavailable? An A6000 might work for your task
3. **Try at off-peak times** — early morning (US time) has more availability
4. **Use the Lambda API** to auto-retry:
   ```bash
   # Script to keep checking until an instance is available
   while true; do
     lambda cloud launch --instance-type gpu_1x_a100 --region us-south-1 && break
     echo "Not available yet, retrying in 60s..."
     sleep 60
   done
   ```
5. **Fall back to Google Colab T4** while waiting for Lambda availability

---

# Slide 26: Connecting to Your Lambda Instance

Once your instance shows **"Running"** in the dashboard:

```bash
# SSH into your Lambda instance
ssh -i ~/.ssh/lambda_key ubuntu@<your-instance-ip>

# The IP address is shown in the Lambda dashboard
# Example: ssh -i ~/.ssh/lambda_key ubuntu@203.0.113.42
```

**First thing to do — ALWAYS:**
```bash
# Check your GPU
nvidia-smi

# You should see something like:
# +-----------------------------------------------------------------------------+
# | NVIDIA A100-SXM4-80GB               | 0%   | 0MiB / 81920MiB              |
# +-----------------------------------------------------------------------------+
```

**Rule #1**: Always check `nvidia-smi` first.
If your GPU shows 0% utilization during training → something is wrong → you're burning money.

**Useful setup commands:**
```bash
# Install your Python packages
pip install torch transformers datasets accelerate

# Clone your project
git clone https://github.com/your-team/your-project.git

# Or copy files from your laptop
# (run this on YOUR machine, not Lambda):
scp -i ~/.ssh/lambda_key -r ./my_project ubuntu@<ip>:~/
```

---

# Quick Quiz 2: Lambda Setup

1. You try to launch an A100 instance in us-west-1 but it says "Sold Out." What do you do? (pick the best answer)
   - a) Wait and keep refreshing the page
   - b) Try a different region like us-south-1
   - c) Give up and use your laptop CPU
   - d) Email Lambda support

2. After SSH-ing into your Lambda instance, what command should you run FIRST?
   - a) `python train.py`
   - b) `pip install torch`
   - c) `nvidia-smi`
   - d) `git clone`

3. Your SSH key file has permissions `644` (readable by everyone). What happens?
   - a) Nothing, it works fine
   - b) SSH refuses to connect — you need `chmod 600`
   - c) Lambda deletes your instance
   - d) Your key gets shared publicly

*(Answers: 1-b, 2-c always check your GPU first, 3-b SSH requires private keys to be owner-read-only)*

---

# Slide 27: What Is Data Loading? (Beginner Concept)

Before we optimize, let's understand what happens during training:

```
┌──────────┐    ┌───────────┐    ┌─────────┐    ┌──────────┐
│  Storage │───►│    CPU    │───►│   GPU   │───►│  Result  │
│ (disk)   │    │ (prepare  │    │ (train) │    │ (loss)   │
│          │    │  data)    │    │         │    │          │
└──────────┘    └───────────┘    └─────────┘    └──────────┘
```

**Data loading** = getting your training data from disk, through the CPU
(where it gets tokenized, padded, batched), and into the GPU.

**The problem:** The GPU is FAST. The CPU/disk is SLOW.

```
Timeline WITHOUT optimization:
CPU: [===load===]                    [===load===]
GPU:              [==train==][idle]               [==train==][idle]
                              ↑ GPU waits! You're paying for nothing.

Timeline WITH optimization:
CPU: [===load===][===load===][===load===]
GPU:    [wait]   [==train==][==train==][==train==]
                  ↑ GPU never waits — CPU pre-loads the next batch.
```

The GPU costs $1-3/hour. Every second it sits idle is wasted money.

---

# Slide 28: Optimization 1 — Don't Waste GPU on Data Loading

Now that you understand the problem, here's the fix:

```python
# BAD — single-threaded, GPU waits for every batch
train_loader = DataLoader(dataset, batch_size=32)

# GOOD — parallel data loading, GPU never waits
train_loader = DataLoader(
    dataset,
    batch_size=32,
    num_workers=4,          # 4 CPU workers load data in parallel
    pin_memory=True,        # pre-copies data to GPU-ready memory
    prefetch_factor=2       # loads 2 batches ahead of time
)
```

### What each parameter does:
| Parameter | What it does | Real-world analogy |
|-----------|-------------|-------------------|
| `num_workers=4` | 4 CPU threads prepare batches simultaneously | 4 cooks prep ingredients while 1 chef cooks |
| `pin_memory=True` | Puts data in GPU-optimized RAM area | Putting ingredients on the counter (fast) vs. in the fridge (slow) |
| `prefetch_factor=2` | Loads 2 future batches while GPU trains | Cook is prepping batch 3 while chef cooks batch 1 |

**Impact**: 2-5x speedup for data-heavy workloads.

---

# Slide 29: What Is Batching? (Beginner Concept)

**Batching** = processing multiple samples at the same time instead of one by one.

```
WITHOUT batching (batch_size=1):
Step 1: Process sample 1  → GPU at 5%
Step 2: Process sample 2  → GPU at 5%
Step 3: Process sample 3  → GPU at 5%
...
Step 1000: Process sample 1000
Total: 1000 steps, GPU barely used 😩

WITH batching (batch_size=32):
Step 1: Process samples 1-32   → GPU at 85%
Step 2: Process samples 33-64  → GPU at 85%
...
Step 32: Process samples 993-1000
Total: 32 steps, GPU fully utilized! 🔥
```

**Why it works:** GPUs have thousands of cores. Processing 1 sample uses
a tiny fraction of them. Processing 32 at once uses most of them.

**How big should your batch be?**
- Start with 32, increase until GPU memory fills up
- Check memory: `nvidia-smi` → look at "Memory Used"
- If you get `CUDA out of memory` → reduce batch size

---

# Slide 30: Optimization 2 — Efficient Inference Batching

```python
# BAD — one prompt at a time (GPU 5% utilized)
results = []
for prompt in prompts:
    result = model.generate(prompt, max_new_tokens=256)
    results.append(result)

# GOOD — batch inference (GPU 90%+ utilized)
from torch.utils.data import DataLoader

prompt_loader = DataLoader(prompts, batch_size=16)
results = []
for batch in prompt_loader:
    tokenized = tokenizer(batch, padding=True, return_tensors="pt").to("cuda")
    outputs = model.generate(**tokenized, max_new_tokens=256)
    results.extend(tokenizer.batch_decode(outputs, skip_special_tokens=True))
```

**Impact**: 10-20x faster for inference workloads (benchmarks, evaluations).

This is especially important for your ablation studies where you run
hundreds of prompts through multiple models!

---

# Quick Quiz 3: Data Loading & Batching

1. Your training script shows GPU utilization at 5% in nvidia-smi. What's the most likely cause?
   - a) The GPU is broken
   - b) Batch size is too small (probably 1)
   - c) The model is too small
   - d) You're using the wrong region

2. What does `num_workers=4` do in a DataLoader?
   - a) Uses 4 GPUs instead of 1
   - b) Runs 4 copies of the model
   - c) Uses 4 CPU threads to load data in parallel
   - d) Limits training to 4 epochs

3. You get a `CUDA out of memory` error. What should you do?
   - a) Buy more GPU credits
   - b) Switch to a larger GPU
   - c) Reduce your batch_size
   - d) Restart the instance

*(Answers: 1-b, 2-c, 3-c — always try reducing batch size first)*

---

# Slide 31: What Is Precision? (Beginner Concept)

**Precision** = how many decimal places a number uses in memory.

```
FP32 (32-bit floating point) — "Full precision"
  Number: 3.14159265358979... stored in 32 bits (4 bytes)
  Very accurate, but uses more memory and compute

FP16 (16-bit floating point) — "Half precision"
  Number: 3.14159... stored in 16 bits (2 bytes)
  Slightly less accurate, but uses HALF the memory and compute
```

**Why this matters for AI:**
| | FP32 (default) | FP16 (half) |
|---|----------------|-------------|
| Memory per number | 4 bytes | 2 bytes |
| Model size in RAM | 8 GB | 4 GB |
| Batch size that fits | 16 | 32 |
| Training speed | 1x | 2-3x faster |

The key insight: AI models don't need perfect precision.
The difference between 3.14159265 and 3.14160 doesn't change whether
your model classifies "great movie" as positive or negative.

---

# Slide 32: Optimization 3 — Mixed Precision Training

**Mixed precision** = use FP16 for the fast parts, FP32 for the parts that
need accuracy. Best of both worlds.

```python
# BAD — full FP32, uses 2x the memory, slower
model.train()
for batch in train_loader:
    loss = model(batch)
    loss.backward()

# GOOD — mixed precision, half the memory, 2-3x faster on A100
from torch.amp import autocast, GradScaler

scaler = GradScaler()
for batch in train_loader:
    with autocast(device_type='cuda'):    # FP16 forward pass (fast!)
        loss = model(batch)
    scaler.scale(loss).backward()          # scaled backward (accurate!)
    scaler.step(optimizer)
    scaler.update()
    optimizer.zero_grad()             # reset gradients for next step
```

### What's happening:
1. **`autocast`** → Forward pass runs in FP16 (fast, saves memory)
2. **`GradScaler`** → Scales gradients to prevent tiny FP16 numbers from becoming zero
3. Optimizer step still happens in FP32 (accurate weight updates)

**Impact**: Fits 2x larger batches, 2-3x faster training on A100/H100.
This is basically free speed — always use it!

---

# Quick Quiz 4: Precision

1. What does "FP16" mean?
   - a) 16 frames per second
   - b) 16-bit floating point numbers (half precision)
   - c) 16 GPUs working together
   - d) A special GPU mode

2. Why is mixed precision faster?
   - a) It skips some training steps
   - b) It uses less accurate numbers that take half the memory and compute
   - c) It only trains half the model
   - d) It uses a special GPU that's faster

3. True or False: Mixed precision gives exactly the same results as full precision.

*(Answers: 1-b, 2-b, 3-False — tiny numerical differences, but results are practically identical)*

---

# Slide 33: What Is Threading and Monitoring? (Beginner Concept)

**Threading** = running multiple tasks at the same time in your program.

Think of it like this:
- **Without threading**: You train for 2 hours, then check if the GPU was being used properly. Oops, it was at 5% the whole time. $3 wasted.
- **With threading**: A background task checks GPU usage every 10 seconds while training runs. You catch problems immediately.

**Monitoring** = keeping track of what your GPU is doing.

```
Your training script          GPU monitor (background thread)
─────────────────────         ──────────────────────────────
Step 1: Train batch 1         [GPU] 85%, 34000MiB / 80000MiB ✓
Step 2: Train batch 2         [GPU] 82%, 34000MiB / 80000MiB ✓
Step 3: Train batch 3         [GPU] 12%, 34000MiB / 80000MiB ⚠ PROBLEM!
```

The monitor catches problems you'd never notice otherwise.

---

# Slide 34: Optimization 4 — Monitor and Checkpoint

```python
# GPU monitoring — runs in background while you train
import subprocess, threading, time

def gpu_monitor(interval=10):
    while True:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=utilization.gpu,memory.used",
             "--format=csv,noheader"],
            capture_output=True, text=True
        )
        print(f"[GPU] {result.stdout.strip()}")
        time.sleep(interval)

# Start the monitor in a background thread
# daemon=True means this thread stops automatically when your script exits
threading.Thread(target=gpu_monitor, daemon=True).start()
```

### Checkpointing — your insurance policy

Cloud instances can crash, lose connectivity, or be reclaimed unexpectedly.
If you've been training for 6 hours and the instance dies → all progress lost.

```python
# Save a checkpoint every epoch — takes < 1 second
torch.save({
    "epoch": epoch,
    "model": model.state_dict(),        # state_dict() = snapshot of all weights
    "optimizer": optimizer.state_dict(), # saves learning rate, momentum, etc.
    "loss": current_loss
}, f"ckpt_{epoch}.pt")

# Resume from checkpoint if instance dies:
ckpt = torch.load("ckpt_5.pt", weights_only=False)  # needed for PyTorch >= 2.6
model.load_state_dict(ckpt["model"])
# Continue from epoch 6 instead of epoch 1!
```

**Always use `tmux` or `nohup`** so training survives SSH disconnect:
```bash
tmux new -s training     # create a named session
python train.py          # start training
# Press Ctrl+B then D    # detach (training keeps running)
tmux attach -t training  # reconnect later
```

---

# Slide 35: Lambda Cost Cheat Sheet

| GPU | $/hr | Memory | Best For |
|-----|------|--------|----------|
| A6000 (48GB) | ~$0.80 | 48 GB | Fine-tuning ≤13B, inference |
| A100 40GB | ~$1.29 | 40 GB | Training 7B-13B models |
| A100 80GB | ~$1.79 | 80 GB | Large batch training, 13B+ |
| H100 SXM | ~$3.29 | 80 GB | Training 13B-70B, fastest |

*(Prices as of early 2026 — check [lambda.ai/pricing](https://lambda.ai/pricing) for current rates)*

**With your team's $400 budget:**
| GPU | Hours Available | Real-world Time |
|-----|----------------|-----------------|
| A6000 | ~500 hrs | ~20 days continuous |
| A100 40GB | ~310 hrs | ~13 days continuous |
| H100 | ~121 hrs | ~5 days continuous |

**Budget rules:**
1. **Develop on Colab T4 (free) first.** Only move to Lambda when code works.
2. **Start with the cheapest GPU** that fits your model. Don't rent an H100 for BERT.
3. **`nvidia-smi` every time** — if utilization < 50%, STOP and optimize first.
4. **Set a budget alert** in the Lambda dashboard so you don't get surprise bills.
5. **Always checkpoint** — losing 6 hours of training = losing $8-20.
6. **Shut down when done!** A running instance you forgot about burns $30-80/day.

---

# Quick Quiz 5: Costs & Monitoring

1. Your team has $400. You rent an H100 at $3.29/hr and forget to shut it down
   over a weekend (48 hours of idle time). How much did you waste?
   - a) $3.29
   - b) $32.90
   - c) $157.92
   - d) $400 (all your credits!)

2. What does checkpointing do?
   - a) Checks if your GPU is working
   - b) Saves your model's progress so you can resume after a crash
   - c) Checks your Lambda bill
   - d) Monitors GPU temperature

3. Why should you use `tmux` on Lambda?
   - a) It makes training faster
   - b) It gives you more GPU memory
   - c) Training keeps running even if your SSH connection drops
   - d) It's required by Lambda

*(Answers: 1-c $157.92!, 2-b, 3-c — SSH drops are common, tmux saves you)*

---

# Slide 36: TASK 4 — GPU Optimization Exercise (10 min)

**Use Claude Code or Cursor to optimize this slow training script:**

```python
# slow_train.py — this script wastes GPU time. Fix it.
# Can you spot ALL 7 problems?
for i in range(len(texts)):
    inputs = tokenizer(texts[i], return_tensors="pt", padding=True).to("cuda")
    outputs = model(**inputs, labels=torch.tensor([labels[i]]).to("cuda"))
    outputs.loss.backward()
    optimizer.step()
    optimizer.zero_grad()
```

**Prompt to give your AI tool:**
```
"This training script has at least 7 performance problems.
Identify each one and rewrite it with:
1. Batched DataLoader (not one sample at a time)
2. num_workers and pin_memory
3. Mixed precision training (torch.amp)
4. Gradient accumulation
5. Pre-tokenization (not tokenizing inside the loop)
6. Checkpointing every N steps
7. GPU utilization monitoring
Explain WHY each change matters."
```

**Compare your answers** — there are multiple valid optimization approaches.

---

# Common Mistakes — Task 4

| Mistake | What Happens | Fix |
|---------|-------------|-----|
| Batch size = 1 | `nvidia-smi` shows GPU 5% — you're paying for 95% idle | `DataLoader(dataset, batch_size=32)` — GPU jumps to 85%+ |
| num_workers=0 | GPU waits 0.5s per batch for CPU to load data | `num_workers=4, pin_memory=True` — no wait |
| No mixed precision | A100 uses 8GB for model, batch=16, 45 min/epoch | Add `autocast` + `GradScaler`: 4GB, batch=32, 15 min/epoch |
| `.item()` in loop | `loss.item()` every step forces GPU→CPU sync | `loss.detach()` — only `.item()` every 100 steps |
| Forgetting `model.eval()` | Inference accuracy varies 60-75% randomly | `model.eval()` + `torch.no_grad()` → stable 72%, 30% faster |
| No checkpointing | Instance dies at epoch 8/10 after 6 hrs → start over | `torch.save(ckpt)` every epoch → resume from epoch 8 |
| Forgot to shut down | Instance runs idle all night = $20-50 wasted | **Always terminate** when done! Set a calendar reminder |

---

# Before You Shut Down — Checklist!

Before terminating your Lambda instance, do ALL of these:

```bash
# 1. Download your results to your laptop
scp -i ~/.ssh/lambda_key ubuntu@<ip>:~/results/ ./results/

# 2. Download your model checkpoints
scp -i ~/.ssh/lambda_key ubuntu@<ip>:~/checkpoints/ ./checkpoints/

# 3. Push your code to git
cd ~/your-project && git add -A && git commit -m "experiment run" && git push

# 4. Verify everything is saved
ls -la results/    # check files exist
ls -la checkpoints/ # check checkpoints exist
```

**Then and only then**: Go to Lambda dashboard → Instances → **Terminate**.

A terminated instance deletes ALL data on it. There is no undo.

---

# Bonus Concept: What Is Gradient Accumulation?

**Problem**: You want batch_size=128 but your GPU only fits batch_size=32.
**Solution**: Process 4 batches of 32, accumulate the gradients, then update.

```
Normal training (batch_size=32):
  Batch 1 → compute gradients → update weights
  Batch 2 → compute gradients → update weights

Gradient accumulation (4 steps, effective batch=128):
  Batch 1 → compute gradients → accumulate (don't update yet)
  Batch 2 → compute gradients → accumulate
  Batch 3 → compute gradients → accumulate
  Batch 4 → compute gradients → NOW update weights
```

```python
ACCUM_STEPS = 4
for step, batch in enumerate(train_loader):
    loss = model(**batch).loss / ACCUM_STEPS  # divide to keep gradient scale correct!
    loss.backward()
    if (step + 1) % ACCUM_STEPS == 0:
        optimizer.step()
        optimizer.zero_grad()
```

**Key**: Always divide loss by `ACCUM_STEPS` — otherwise gradients are N× too large.

---

# Final Quiz: Put It All Together

You're about to run your ablation study on Lambda. Walk through this checklist:

1. **Before Lambda**: Where should you test your code first?
2. **Choosing GPU**: Your model is 7B parameters. Which GPU do you pick?
3. **Region**: us-west-1 shows "Sold Out" for A100. What do you try?
4. **First command**: You SSH in. What do you run first?
5. **Training**: Your nvidia-smi shows 8% GPU utilization. Name 2 likely causes.
6. **Safety**: Why do you need checkpointing AND tmux?
7. **Budget**: Your experiment costs $8.40 per run. How many runs can you afford with $400?

**Answers:**
1. Google Colab T4 (free) or locally on CPU
2. A100 40GB or 80GB ($1.29-1.79/hr) — fits 7B with mixed precision
3. Try us-south-1, us-west-3, or a different GPU type (A6000)
4. `nvidia-smi` — always verify your GPU is there and working
5. Batch size too small + data loading bottleneck (no num_workers)
6. Checkpointing saves your model state; tmux keeps training alive if SSH drops. Different problems!
7. $400 / $8.40 = 47 runs — plenty of room for experimentation

---

# ═══════════════════════════════════════════════════
# PART 5: WRAP-UP & NEXT STEPS (10 min)
# ═══════════════════════════════════════════════════

---

# Slide 29: Tool Decision Matrix — Your Cheat Sheet

| Task | Cursor + Gemini | Claude Router | Claude Code |
|------|----------------|---------------|-------------|
| Brainstorm research idea | Good | Good (free) | Overkill |
| Write boilerplate code | Great (inline) | Good (free) | Overkill |
| Design experiment plan | OK | Good | Best (plan!) |
| Multi-file pipeline | Good | Good | Best |
| Debug complex issue | OK | Route→Claude | Best |
| Quick data formatting | Best (IDE) | Good (free) | Fine |
| Generate figures | Good | Good | Good |
| Review/critique paper | OK | Route→Claude | Best (grill!) |
| GPU optimization | Good | Good | Best |
| Parallel workstreams | N/A | Worktrees! | Worktrees! |

---

# Slide 30: Your CLAUDE.md Habits Going Forward

After today, for every research project:

1. **Start with CLAUDE.md** — define your question, plan, and metrics
2. **Update after every correction** — "Update CLAUDE.md so this doesn't happen again"
3. **Add verification steps** — "Write a test that confirms the output format"
4. **Use plan mode for architecture** — don't let AI code without a plan
5. **Grill yourself** — "Review my claims against my data. Be harsh."

This is what separates students who use AI as a crutch
from researchers who use AI as a force multiplier.

---

# Slide 31: Next Steps for Your Algoverse Research

1. **Today**: You built TWO experiment pipelines in ~3 hours
2. **This week**: Expand them — more questions, more models, more analysis
3. **Before your deadline**: Use the "grill me" pattern to self-review
4. **When submitting**: Your CLAUDE.md becomes your reproducibility notes

Upcoming deadlines to target:
- ACL 2026 workshops (March–April deadlines)
- ICML 2026
- Check the Conference Submissions tracker for your team's targets

---

# Slide 32: Resources

| Resource | Link |
|----------|------|
| Claude Code docs | https://docs.anthropic.com/en/docs/claude-code |
| Claude Code tips (Boris Cherny) | https://x.com/bcherny/status/2017742741636321619 |
| Cursor docs | https://docs.cursor.com |
| Lambda GPU guide | https://docs.lambda.ai |
| Algoverse Conference Tracker | (internal Airtable) |
