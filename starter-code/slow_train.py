"""
INTENTIONALLY SLOW training script for the GPU optimization exercise.
Students must identify all performance issues and fix them using AI tools.

Issues to find:
1. Batch size of 1 (processes one sample at a time)
2. No DataLoader (manual loop)
3. No parallel data loading (num_workers)
4. No mixed precision (FP32 everything)
5. Tokenizing inside the training loop
6. No gradient accumulation
7. No checkpointing
8. No GPU utilization monitoring
9. No learning rate scheduler
10. Creating tensors inside loop (repeated CUDA allocations)
"""

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

# Load model
model = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased")
model = model.to("cuda")
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

# "Dataset" — 1000 examples
texts = ["This movie is great and I loved every minute of it"] * 500 + \
        ["This movie is terrible and I hated every minute of it"] * 500
labels = [1] * 500 + [0] * 500

optimizer = torch.optim.Adam(model.parameters(), lr=2e-5)

# Training loop — EVERYTHING is wrong here
model.train()
for i in range(len(texts)):
    # Problem: tokenizing one at a time inside the loop
    inputs = tokenizer(texts[i], return_tensors="pt", padding=True, truncation=True).to("cuda")

    # Problem: creating label tensor inside the loop
    label_tensor = torch.tensor([labels[i]]).to("cuda")

    # Problem: batch size = 1
    outputs = model(**inputs, labels=label_tensor)

    # Problem: no mixed precision
    outputs.loss.backward()

    # Problem: stepping every single sample
    optimizer.step()
    optimizer.zero_grad()

    if i % 100 == 0:
        print(f"Step {i}/{len(texts)}, Loss: {outputs.loss.item():.4f}")

print("Training done!")
