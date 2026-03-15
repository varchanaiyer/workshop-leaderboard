"""
BenchmarkLite: Evaluating LLM Consistency on Paraphrased Questions

Usage:
    python main.py --model gpt-4o-mini --dry-run     # test without API calls
    python main.py --model gpt-4o-mini --mock         # use fake responses
    python main.py --model gpt-4o-mini                # run for real
"""

import argparse
import json
import os


def load_questions(path="data/questions.json"):
    """Load the question dataset."""
    with open(path) as f:
        return json.load(f)


def run_evaluation(questions, model, dry_run=False, mock=False):
    """
    Run all questions + paraphrases through the model.

    TODO: Students implement this with their AI tool.
    Steps:
    1. For each question, run the original + all paraphrases
    2. Collect responses
    3. Save to results/raw_responses.json
    """
    results = []

    for q in questions:
        variants = [q["original"]] + q["paraphrases"]

        if dry_run:
            print(f"[DRY RUN] {q['id']} ({q['category']}): {len(variants)} variants")
            continue

        responses = []
        for variant in variants:
            if mock:
                # Fake response for testing the pipeline
                response = f"Mock answer to: {variant[:50]}..."
            else:
                # TODO: Replace with actual API call
                # response = call_llm_api(model, variant)
                raise NotImplementedError("Implement API calling in src/evaluate.py")

            responses.append({
                "prompt": variant,
                "response": response,
            })

        results.append({
            "id": q["id"],
            "category": q["category"],
            "original_question": q["original"],
            "expected_answer": q.get("expected_answer", ""),
            "model": model,
            "responses": responses,
        })

    return results


def compute_metrics(results):
    """
    TODO: Students implement consistency metrics.
    Import from src/metrics.py
    """
    print(f"\nResults for {len(results)} questions:")
    print("(Implement metrics in src/metrics.py)")


def main():
    parser = argparse.ArgumentParser(description="BenchmarkLite Evaluation")
    parser.add_argument("--model", default="gpt-4o-mini", help="Model to evaluate")
    parser.add_argument("--dry-run", action="store_true", help="Print prompts only")
    parser.add_argument("--mock", action="store_true", help="Use fake responses")
    parser.add_argument("--data", default="data/questions.json", help="Dataset path")
    args = parser.parse_args()

    # Load data
    questions = load_questions(args.data)
    print(f"Loaded {len(questions)} questions")

    # Run evaluation
    results = run_evaluation(questions, args.model, args.dry_run, args.mock)

    if args.dry_run:
        total = sum(1 + len(q["paraphrases"]) for q in questions)
        print(f"\n[DRY RUN] Would make {total} API calls to {args.model}")
        return

    # Save results
    os.makedirs("results", exist_ok=True)
    output_path = f"results/{args.model}_responses.json"
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Saved results to {output_path}")

    # Compute metrics
    compute_metrics(results)


if __name__ == "__main__":
    main()
