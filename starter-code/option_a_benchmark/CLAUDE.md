# BenchmarkLite — LLM Consistency on Paraphrased Questions

## Research Question
Do LLMs give consistent answers when the same question is rephrased?

## Project Structure
```
option_a_benchmark/
├── CLAUDE.md              ← You are here
├── data/
│   └── questions.json     ← 20 questions × 3 paraphrases
├── src/
│   ├── evaluate.py        ← Main evaluation runner
│   ├── metrics.py         ← Consistency scoring
│   └── visualize.py       ← Generate figures
├── results/               ← Raw responses + analysis
├── figures/               ← Publication-ready plots
└── requirements.txt
```

## Experiment Plan
- **Models**: [Fill in your chosen models]
- **Categories**: [Fill in your 5 categories]
- **Metrics**: exact_match, semantic_similarity, consistency_score
- **N questions**: 20 (4 per category) × 4 variants (1 original + 3 paraphrases)
- **Total API calls**: 20 × 4 × [num_models]

## Decisions Made
- [Add decisions as you make them]

## Mistakes to Avoid
- [Claude will add entries here as you work — keep this updated!]

## Verification Checklist
- [ ] questions.json has 20 entries, each with 3 paraphrases
- [ ] evaluate.py runs with --dry-run without errors
- [ ] results JSON has correct structure
- [ ] metrics produce values between 0 and 1
- [ ] figure saves to figures/ directory
