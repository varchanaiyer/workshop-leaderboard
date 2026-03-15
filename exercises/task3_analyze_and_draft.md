# TASK 3: Analyze Both & Compare (15 min)

Run analysis for **BOTH** experiments and find a combined insight.

---

## Part A: Benchmark Analysis (7 min)

### Step 1: Generate a Results Table (3 min)

```bash
claude "Read results/raw_responses.json. Create a table showing:
- Rows: question categories
- Columns: models tested
- Values: average consistency score (0-1)
Save as results/consistency_table.csv and print it formatted."
```

### Step 2: Create One Figure (2 min)

```
"Using matplotlib, create a grouped bar chart from
results/consistency_table.csv. X-axis: categories,
bars grouped by model, Y-axis: consistency score.
Title: 'LLM Consistency Across Question Categories'.
Save to figures/consistency_barplot.png"
```

### Step 3: Write 2-Sentence Finding (2 min)

Example:
> "We find that LLM consistency varies significantly across question
> categories, with math questions showing 92% consistency while ethical
> reasoning drops to 54%. This suggests paraphrase sensitivity is
> task-dependent rather than a general model property."

---

## Part B: Ablation Analysis (8 min)

### Step 1: Generate a Results Table (3 min)

```bash
claude "Read results/ablation.json. Create a table showing:
- Rows: prompting strategies
- Columns: models tested
- Values: accuracy (%)
Include a row for 'Average across models'.
Save as results/strategy_table.csv and print it formatted."
```

### Step 2: Create One Figure (2 min)

```
"Using matplotlib, create a grouped bar chart from
results/strategy_table.csv. X-axis: prompting strategy,
bars grouped by model, Y-axis: accuracy %.
Title: 'Prompting Strategy Comparison on [YOUR TASK]'.
Save to figures/strategy_comparison.png"
```

### Step 3: Write 2-Sentence Finding (3 min)

Example:
> "Chain-of-thought prompting improves accuracy by 15% over zero-shot
> on GSM8K math problems, with the gap widening for harder questions.
> Self-consistency voting adds another 3% but at 5x the API cost."

---

## Combined Insight

Do your benchmark and ablation results tell a related story?

For example:
- "Models that are more consistent on paraphrased questions also benefit more from CoT prompting"
- "The category where consistency is lowest is also where prompting strategy matters most"

Use the "Grill Me" pattern:
```bash
claude "Based on my results from BOTH experiments, help me write
a combined 3-sentence insight. Then CRITIQUE it:
- Does the claim match the numbers?
- Am I overgeneralizing from a small sample?
- What caveats should I mention?
Be honest and harsh."
```

---

## Sharing Round (5 min)

3-4 students present:
- Their two tables (benchmark + ablation)
- Their two figures
- Their combined insight

**Discussion questions:**
- Did anyone get opposite results on the same project?
- What would you need to do to make this publishable?
- Which AI tool was most helpful for analysis?
