# AI Research Implementation Workshop — Single Session Agenda

**Duration**: ~3 hours
**Students**: 20–30
**Format**: Instructor demo → student hands-on → share back
**Key change**: Students do BOTH projects (benchmark + ablation), not pick one.

---

## Pre-Workshop Setup (send 1 day before)
- Students install Cursor and/or Claude Code
- See: `handouts/tool_setup_guide.md`

---

## Agenda

| Time | Part | What Happens | Files |
|------|------|-------------|-------|
| 0:00 | **Intro** (15 min) | Slides 1-7: Tools overview, both projects, skills matrix | `slides/00_slide_deck.md` |
| 0:15 | **Examples & Datasets** (10 min) | Slides 8-10: Example questions, ablation walkthrough, dataset options | New slides |
| 0:25 | **Tool Walkthrough** (10 min) | Slides 11-12: Live demo in Cursor+Gemini → Claude Code, CLAUDE.md | — |
| 0:35 | **TASK 1** (10 min) | Students plan BOTH experiments | `exercises/task1_research_plan.md` |
| 0:45 | **Share** (5 min) | 3-4 students share plans | — |
| 0:50 | **Implementation Demo** (15 min) | Slides 14-16: Scaffolding, data modules, tool comparison, worktrees | — |
| 1:05 | **TASK 2** (25 min) | Students build BOTH pipelines | `exercises/task2_implement_pipeline.md` |
| 1:30 | **Break** (5 min) | — | — |
| 1:35 | **Analysis Demo** (10 min) | Slides 19-20: Results analysis, "Grill Me" pattern | — |
| 1:45 | **TASK 3** (15 min) | Students analyze BOTH + combined insight | `exercises/task3_analyze_and_draft.md` |
| 2:00 | **Share** (10 min) | Students present findings, compare varied results | — |
| 2:10 | **Lambda GPU** (15 min) | Slides 22-27: Optimization techniques, cost tips | — |
| 2:25 | **TASK 4** (10 min) | Fix the slow training script | `exercises/task4_gpu_optimization.md` |
| 2:35 | **Share + Compare** (5 min) | Compare optimization approaches | — |
| 2:40 | **Wrap-up** (10 min) | Slides 29-33: Tool cheat sheet, next steps, resources | — |

**Total: ~2 hours 50 min** (with buffer for questions)

---

## Folder Structure

```
ai-research-workshop/
├── WORKSHOP_AGENDA.md              ← This file
├── slides/
│   ├── 00_slide_deck.md            ← Full slide deck (33 slides)
│   ├── build_pptx.py               ← PPTX generator script
│   └── AI_Research_Workshop.pptx   ← Generated presentation
├── exercises/
│   ├── task1_research_plan.md       ← Plan BOTH experiments
│   ├── task2_implement_pipeline.md  ← Build BOTH pipelines
│   ├── task3_analyze_and_draft.md   ← Analyze BOTH + combined insight
│   └── task4_gpu_optimization.md    ← Fix slow_train.py
├── starter-code/
│   ├── option_a_benchmark/          ← Consistency benchmark starter
│   │   ├── CLAUDE.md, main.py, data/questions_sample.json, requirements.txt
│   ├── option_b_ablation/           ← Prompting ablation starter
│   │   ├── CLAUDE.md, main.py, src/prompts.py, data/test_examples_sample.json
│   └── slow_train.py               ← Intentionally broken GPU script
└── handouts/
    └── tool_setup_guide.md          ← Setup for Cursor, Claude Code, Router
```

---

## Key Design Principles

1. **Both projects, not pick one**: Every student builds a benchmark AND an ablation study
2. **Examples and datasets provided**: Concrete inspiration so students know what "good" looks like
3. **Tool progression**: Free (Gemini) → Mid (Router) → Premium (Claude Code direct)
4. **Varied answers by design**: Every task produces different results across students
5. **Share rounds after each task**: 3-4 students, highlights differences
6. **Real research skills**: Plan → Implement → Analyze → Write → Review

---

## Instructor Notes

- **For Task 1**: Show the example questions slide and datasets slide before students start. Encourage creative categories — the more varied, the better.
- **For Task 2**: Students without API keys should use `--mock` mode. Pipeline structure matters more than real results.
- **For Task 3**: If students have mock data, that's fine — focus on analysis CODE and figure generation, not actual numbers.
- **For Task 4**: Most "right answer" task, but still multiple valid optimization combos.
- **For sharing**: Ask "what did your AI tool suggest that surprised you?" — generates great discussion.
- **Combined insight**: Encourage students to connect their benchmark and ablation results — this is a higher-order research skill.
