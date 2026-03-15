"""
Prompting strategy templates for the ablation study.

Each strategy is a function that takes a question (and optional examples)
and returns the full prompt to send to the model.

TODO: Students customize these for their chosen task.
"""


def zero_shot(question):
    """Direct question, no examples, no guidance."""
    return question


def few_shot(question, examples):
    """
    Provide N examples before the question.

    Args:
        question: The test question
        examples: List of {"input": ..., "output": ...} dicts
    """
    prompt = "Here are some examples:\n\n"
    for i, ex in enumerate(examples, 1):
        prompt += f"Example {i}:\nInput: {ex['input']}\nAnswer: {ex['output']}\n\n"
    prompt += f"Now answer this:\nInput: {question}\nAnswer:"
    return prompt


def chain_of_thought(question):
    """Ask the model to think step by step."""
    return f"{question}\n\nLet's think through this step by step."


def cot_self_consistency(question, n_samples=5):
    """
    Chain-of-thought with self-consistency.
    Run N times and take majority vote.

    Returns the prompt (caller handles running N times and voting).
    """
    return f"{question}\n\nThink through this step by step, then give your final answer."


# Registry of all strategies
STRATEGIES = {
    "zero_shot": {
        "fn": zero_shot,
        "needs_examples": False,
        "description": "Direct question, no guidance",
    },
    "few_shot": {
        "fn": few_shot,
        "needs_examples": True,
        "description": "3-5 examples provided before question",
    },
    "chain_of_thought": {
        "fn": chain_of_thought,
        "needs_examples": False,
        "description": "Step-by-step reasoning prompted",
    },
    "cot_self_consistency": {
        "fn": cot_self_consistency,
        "needs_examples": False,
        "description": "CoT run 5x with majority vote",
    },
}
