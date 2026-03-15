"""
Prompting Ablation Study: Comparing strategies across models and tasks.

Usage:
    python main.py --model gpt-4o-mini --dry-run     # test without API calls
    python main.py --model gpt-4o-mini --mock         # use fake responses
    python main.py --model gpt-4o-mini                # run for real
    python main.py --model gpt-4o-mini --strategy chain_of_thought  # single strategy
"""

import argparse
import json
import os
from src.prompts import STRATEGIES


def load_examples(path="data/test_examples.json"):
    """Load test examples."""
    with open(path) as f:
        return json.load(f)


def run_ablation(examples, model, strategies, dry_run=False, mock=False):
    """
    Run each example through each strategy.

    TODO: Students implement API calling with their AI tool.
    """
    results = []

    for ex in examples:
        for strat_name, strat_info in strategies.items():
            # Build prompt
            if strat_info["needs_examples"]:
                # Use other examples as few-shot demos (leave-one-out)
                demos = [e for e in examples if e["id"] != ex["id"]][:3]
                demo_formatted = [{"input": d["input"], "output": d["expected_answer"]} for d in demos]
                prompt = strat_info["fn"](ex["input"], demo_formatted)
            else:
                prompt = strat_info["fn"](ex["input"])

            if dry_run:
                print(f"[DRY RUN] {ex['id']} × {strat_name}: {prompt[:60]}...")
                continue

            if mock:
                response = f"Mock {strat_name} answer for: {ex['input'][:30]}..."
            else:
                # TODO: Replace with actual API call
                raise NotImplementedError("Implement API calling in src/evaluate.py")

            results.append({
                "example_id": ex["id"],
                "strategy": strat_name,
                "model": model,
                "prompt": prompt,
                "response": response,
                "expected": ex["expected_answer"],
                "difficulty": ex.get("difficulty", "unknown"),
            })

    return results


def main():
    parser = argparse.ArgumentParser(description="Prompting Ablation Study")
    parser.add_argument("--model", default="gpt-4o-mini")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--mock", action="store_true")
    parser.add_argument("--strategy", default=None, help="Run only this strategy")
    parser.add_argument("--data", default="data/test_examples.json")
    args = parser.parse_args()

    examples = load_examples(args.data)
    print(f"Loaded {len(examples)} test examples")

    # Filter strategies if specified
    strategies = STRATEGIES
    if args.strategy:
        strategies = {args.strategy: STRATEGIES[args.strategy]}
    print(f"Running {len(strategies)} strategies: {list(strategies.keys())}")

    # Run
    results = run_ablation(examples, args.model, strategies, args.dry_run, args.mock)

    if args.dry_run:
        total = len(examples) * len(strategies)
        print(f"\n[DRY RUN] Would make {total} API calls to {args.model}")
        return

    # Save
    os.makedirs("results", exist_ok=True)
    output_path = f"results/{args.model}_ablation.json"
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Saved {len(results)} results to {output_path}")


if __name__ == "__main__":
    main()
