# Prompting Ablation Study

## Research Question
Which prompting strategy works best for [YOUR CHOSEN TASK]?

## Project Structure
```
option_b_ablation/
├── CLAUDE.md              ← You are here
├── data/
│   └── test_examples.json ← 15 test examples for your task
├── src/
│   ├── prompts.py         ← Prompting strategy templates
│   ├── evaluate.py        ← Main evaluation runner
│   ├── metrics.py         ← Accuracy + statistical tests
│   └── visualize.py       ← Generate figures
├── results/               ← Raw responses + analysis
├── figures/               ← Publication-ready plots
└── requirements.txt
```

## Experiment Plan
- **Task**: [Fill in — math, sentiment, QA, code, etc.]
- **Models**: [Fill in your chosen models]
- **Strategies**: zero-shot, few-shot, chain-of-thought, CoT + self-consistency
- **N examples**: 15 test examples × 4 strategies × [num_models]
- **Primary metric**: [accuracy / F1 / exact match]

## Decisions Made
- [Add decisions as you make them]

## Mistakes to Avoid
- [Claude will add entries here as you work — keep this updated!]

## Verification Checklist
- [ ] test_examples.json has 15 entries with expected answers
- [ ] prompts.py has 4 strategy templates
- [ ] evaluate.py runs with --dry-run without errors
- [ ] results JSON has (example × strategy × model) structure
- [ ] accuracy values are between 0 and 100
- [ ] figure saves to figures/ directory
