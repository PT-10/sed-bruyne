import os
import ast
import json
import dspy
import random
from typing import List


class SEDSolverSignature(dspy.Signature):
    """
    Find the transitions that must be applied to go from the initial string to a null string. 
    When a transition is applied, it must follow these logic constraints:
        - You may choose any transition whose src appears in the string.
        - At an instance, the transition is applied only to the first (leftmost) occurrence of src in the current string.
        - Transitions may be applied in any order and any number of times.

    Input: problem description with initial string and transitions.
    Output: list of transitions applied.
    """
    problem = dspy.InputField(
        desc="A JSON string containing problem_id, initial_string, and transitions list"
    )
    solution = dspy.OutputField(
        desc="A JSON string with problem_id and solution (list of indices in the order). Indices should be zero-indexed"
    )


class ZeroShotSEDSolver(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predictor = dspy.Predict(SEDSolverSignature)

    def forward(self, problem: str):
        return self.predictor(problem=problem)


class CoTSEDSolver(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predictor = dspy.ChainOfThought(SEDSolverSignature)

    def forward(self, problem: str):
        return self.predictor(problem=problem)


def load_json(path):
    with open(path) as f:
        return json.load(f)


def save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)


def problem_to_string(problem):
    return json.dumps(problem, indent=2)


def verify_solution(problem, solution_indices):
    current = problem["initial_string"]
    transitions = problem["transitions"]
    for idx in solution_indices:
        idx = int(idx)
        if idx < 0 or idx >= len(transitions):
            return False
        trans = transitions[idx]
        if trans["src"] not in current:
            return False
        i = current.find(trans["src"])
        current = current[:i] + trans["tgt"] + current[i + len(trans["src"]):]
    return current == ""


def validity_metric(example, pred, trace=None):
    try:
        pred_solution_str = pred.solution
        if not pred_solution_str:
            return 0.0

        problem = json.loads(example["problem"])

        try:
            solution_data = json.loads(pred_solution_str)
            solution_indices = solution_data.get("solution", []) if isinstance(solution_data, dict) else solution_data
        except:
            solution_indices = ast.literal_eval(pred_solution_str)

        return float(verify_solution(problem, solution_indices))
    except:
        return 0.0
    

def load_dataset(problem_dir: str, solution_dir: str,
                 problem_ids: List[str] = None,
                 sample_size: int = None,
                 seed: int = 42) -> List[dspy.Example]:
    all_ids = sorted(f.replace(".json", "") for f in os.listdir(problem_dir) if f.endswith(".json"))
    if problem_ids is not None:
        all_ids = [pid for pid in problem_ids if pid in all_ids]
    if sample_size and sample_size < len(all_ids):
        random.seed(seed)
        all_ids = random.sample(all_ids, sample_size)

    examples = []
    for pid in all_ids:
        try:
            problem = load_json(os.path.join(problem_dir, f"{pid}.json"))
            solution = load_json(os.path.join(solution_dir, f"{pid}.json"))
            ex = dspy.Example(
                problem = problem_to_string(problem),
                solution=json.dumps(solution)
            ).with_inputs("problem")
            examples.append(ex)
        except FileNotFoundError:
            continue
    return examples


def split_dataset(examples: List[dspy.Example],
                  train_ratio: float = 0.7,
                  val_ratio: float = 0.15,
                  seed: int = 42):
    random.seed(seed)
    shuffled = random.sample(examples, len(examples))
    n = len(shuffled)
    train_end = int(n * train_ratio)
    val_end = train_end + int(n * val_ratio)
    return shuffled[:train_end], shuffled[train_end:val_end], shuffled[val_end:]


def evaluate_module(module: dspy.Module, examples: list, metric_fn = validity_metric):

    total = len(examples)
    correct = 0
    results = []

    for example in examples:
        try:
            pred = module(problem=example["problem"])
            score = metric_fn(example, pred)
            correct += score

            results.append({
                "problem": example["problem"][:100],
                "prediction": pred.solution[:200],
                "ground_truth": example["solution"][:200],
                "score": score
            })
        except Exception as e:
            print(f"Error evaluating example: {e}")
            results.append({
                "problem": example["problem"][:100],
                "error": str(e),
                "score": 0.0
            })

    accuracy = correct / total if total > 0 else 0.0

    return {
        "accuracy": accuracy,
        "correct": correct,
        "total": total,
        "results": results
    }
