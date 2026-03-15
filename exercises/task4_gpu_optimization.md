# TASK 4: GPU Optimization Exercise (10 min)

## Before You Start — Preflight Checklist

Before touching Lambda, make sure you can answer YES to all of these:

- [ ] My training code runs without errors on CPU or Colab T4
- [ ] I have a `--dry-run` or `--mock` mode that tests the full pipeline without real API/GPU calls
- [ ] I know which GPU I need (A6000? A100? H100?)
- [ ] I know roughly how long my job will take

**If any answer is NO → fix that first. Don't burn GPU credits debugging.**

---

## How to Launch a Lambda Instance

### Step 1: SSH Key Setup (one-time)

**Note**: You need a billing-linked Lambda account before you can add SSH keys.
If your team uses shared Algoverse credits, your team lead sets up the account
and adds your SSH key for you.

```bash
# First, make sure you have an SSH key on your laptop:
ls ~/.ssh/id_ed25519.pub   # or id_rsa.pub
# If not, generate one:
ssh-keygen -t ed25519 -C "your-email@example.com"

# Option A: Use your existing key
cat ~/.ssh/id_ed25519.pub
# Copy this output → paste in Lambda dashboard → SSH Keys → Add SSH Key

# Option B: Generate a new key on Lambda's dashboard
# Click "Generate a new SSH key" → downloads a .pem file
mv ~/Downloads/lambda_key.pem ~/.ssh/lambda_key
chmod 600 ~/.ssh/lambda_key  # REQUIRED — SSH won't connect without this
```

### Step 2: Launch Instance

1. Go to [cloud.lambda.ai](https://cloud.lambda.ai) → **Instances** → **Launch Instance**
2. Choose GPU type:
   | If your task is... | Choose | $/hr |
   |---------------------|--------|------|
   | Inference / small fine-tune (≤7B) | A6000 (48GB) | ~$0.80 |
   | Training 7B-13B models | A100 40GB | ~$1.29 |
   | Large training / 13B+ | A100 80GB | ~$1.79 |
   | Fastest possible / 70B+ | H100 SXM | ~$3.29 |

3. Choose a **region** (see troubleshooting below)
4. Select your SSH key → Click **Launch**
5. Wait 3-5 minutes for boot

### Step 3: Connect

```bash
# The IP address appears in the Lambda dashboard once instance is running
ssh -i ~/.ssh/lambda_key ubuntu@<your-instance-ip>

# FIRST THING — always verify your GPU:
nvidia-smi
```

### Troubleshooting: "Instance Not Available"

This happens frequently. Lambda GPUs sell out, especially A100s.

| What to try | How |
|-------------|-----|
| Different region | us-west-1 sold out? → try us-south-1 (Texas) or us-west-3 (Utah) |
| Different GPU | A100 unavailable? → A6000 might work for your task |
| Off-peak times | Try early morning US time (lower demand) |
| Auto-retry script | See below |
| Fall back to Colab T4 | Free, always available, good for testing |

```bash
# Auto-retry script (run on your laptop):
while true; do
  echo "Trying to launch A100 in us-south-1..."
  lambda cloud launch --instance-type gpu_1x_a100 --region us-south-1 && break
  echo "Not available. Retrying in 60 seconds..."
  sleep 60
done
```

---

## The Slow Script

This script is intentionally slow. It has **at least 7 performance problems.**

```python
# slow_train.py — this wastes GPU time. Fix it.
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

model = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased")
model = model.to("cuda")
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

texts = ["This movie is great"] * 500 + ["This movie is terrible"] * 500
labels = [1] * 500 + [0] * 500
optimizer = torch.optim.Adam(model.parameters(), lr=2e-5)

for i in range(len(texts)):
    inputs = tokenizer(texts[i], return_tensors="pt", padding=True).to("cuda")
    outputs = model(**inputs, labels=torch.tensor([labels[i]]).to("cuda"))
    outputs.loss.backward()
    optimizer.step()
    optimizer.zero_grad()

print("Training done!")
```

---

## Your Task

**Prompt to give your AI tool:**
```
This training script has at least 7 performance problems.
Identify each one and rewrite the script with:
1. Proper DataLoader with batching (not one sample at a time!)
2. num_workers and pin_memory for parallel data loading
3. Mixed precision training (torch.amp — autocast + GradScaler)
4. Pre-tokenization (don't tokenize inside the loop)
5. Gradient accumulation for larger effective batch sizes
6. Checkpointing every N steps to resume after crashes
7. GPU utilization monitoring in a background thread

Explain WHY each change matters and estimate the speedup.
```

---

## Issues to Find (check your AI's answer against this)

| # | Problem | Why It's Bad | Fix | Speedup |
|---|---------|-------------|-----|---------|
| 1 | Batch size = 1 | GPU at 5% utilization, 95% idle | `DataLoader(dataset, batch_size=32)` | 10-30x |
| 2 | No parallel data loading | GPU waits for CPU every batch | `num_workers=4, pin_memory=True` | 2-5x |
| 3 | FP32 everywhere | 2x memory used, slower math | `autocast` + `GradScaler` (mixed precision) | 2-3x |
| 4 | Tokenizing inside loop | CPU re-tokenizes every step | Pre-tokenize into a `Dataset` class | 2x |
| 5 | No gradient accumulation | Can't simulate larger batches | `loss /= accum_steps`, step every N | memory savings |
| 6 | No checkpointing | Crash = start over from scratch | `torch.save(ckpt)` every epoch | safety |
| 7 | No monitoring | Can't tell if GPU is being used | Background thread with `nvidia-smi` | debugging |

---

## Quick Self-Check Quiz

Before you move on, answer these:

1. **Why does batch_size=1 waste GPU time?**
   GPUs have thousands of cores. Processing 1 sample uses a tiny fraction.
   Processing 32 at once uses most of them.

2. **What does `pin_memory=True` do?**
   Puts data in a special CPU memory area that transfers to GPU faster.
   Like putting ingredients on the counter vs. leaving them in the fridge.

3. **Why do we divide loss by accumulation steps?**
   Without dividing, accumulated gradients are N× too large — like
   having an N× higher learning rate, causing unstable training.

4. **Your nvidia-smi shows 10% utilization and 4GB/80GB memory used.
   Name 2 things to fix.**
   → Increase batch size (use that empty 76GB!) and add `num_workers`

5. **How much does it cost to forget to shut down an A100 instance
   for 24 hours?**
   → 24 × $1.29 = $30.96 — almost 8% of your $400 budget, for nothing!

---

## Bonus Challenge

If you finish early, ask your AI tool:
```
"Now add DistributedDataParallel (DDP) support so this can
run across multiple GPUs. Show the launch command for 4 GPUs."
```

---

## Compare Answers

Everyone will get slightly different optimized code.
Discussion: which optimizations had the biggest impact? Which ones
did your AI tool miss?

**Ranking (most → least impactful):**
1. Batching (1→32): 10-30x
2. Mixed precision: 2-3x
3. num_workers: 2-5x
4. Pre-tokenization: 2x
5. Gradient accumulation: memory savings (not speed)
6. pin_memory: 10-20% transfer speedup
