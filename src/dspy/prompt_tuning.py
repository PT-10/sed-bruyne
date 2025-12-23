import os
import json
import random
import dspy

llm = dspy.LM(
    model="openai/local-model",
    api_base="http://localhost:8080/v1",
    api_key="local",
    temperature=0.0,
    max_tokens=32512,
    chat=True  # <-- Important: use chat mode for instruction-following
)
dspy.configure(lm=llm)

def load_json(path):
    with open(path) as f:
        return json.load(f)

def load_prompt(path):
    with open(path) as f:
        return f.read()

def embed_problem(prompt: str, problem: dict) -> str:
    return prompt.replace("{{PROBLEM_JSON}}", json.dumps(problem, indent=2))

def parse_model_output(text: str):
    try:
        start = text.index("{")
        end = text.rindex("}") + 1
        return json.loads(text[start:end])
    except Exception:
        return None

def exact_match(pred: dict, gold: dict) -> float:
    if not pred:
        return 0.0
    return float(pred.get("solution") == gold.get("solution"))

def prefix_match(pred: dict, gold: dict) -> float:
    if not pred:
        return 0.0
    p = pred.get("solution", [])
    g = gold.get("solution", [])
    k = min(len(p), len(g))
    return sum(p[i] == g[i] for i in range(k)) / max(len(g), 1)

class PromptSolver(dspy.Signature):
    prompt: str = dspy.InputField()
    output: str = dspy.OutputField()

solver = dspy.Predict(PromptSolver)

def collect_problem_ids(problem_dir):
    return sorted(fname.replace(".json","") for fname in os.listdir(problem_dir) if fname.endswith(".json"))

def run_tuning(base_prompt_path, tuned_prompt_dir, problem_dir, baseline_dir, num_problems):
    base_prompt = load_prompt(base_prompt_path)
    all_problem_ids = collect_problem_ids(problem_dir)
    sampled_ids = random.sample(all_problem_ids, num_problems)

    total_exact = 0.0
    total_prefix = 0.0
    detailed_results = []

    print(f"\nTuning prompt: {os.path.basename(base_prompt_path)}")
    print(f"Evaluating on {num_problems} problems\n")

    for pid in sampled_ids:
        problem_path = os.path.join(problem_dir, f"{pid}.json")
        baseline_path = os.path.join(baseline_dir, f"{pid}.json")

        if not os.path.exists(baseline_path):
            print(f"Missing baseline for {pid}, skipping")
            continue

        problem = load_json(problem_path)
        baseline = load_json(baseline_path)

        full_prompt = embed_problem(base_prompt, problem)

        # Chat-mode: system + user message
        response = solver(prompt=[
            {"role": "system", "content": "You are an expert SED solver. Return only JSON with problem_id and solution."},
            {"role": "user", "content": full_prompt}
        ])

        pred = parse_model_output(response.output)
        em = exact_match(pred, baseline)
        pm = prefix_match(pred, baseline)
        total_exact += em
        total_prefix += pm

        detailed_results.append({
            "problem_id": pid,
            "exact_match": em,
            "prefix_match": pm,
            "prediction": pred,
            "baseline": baseline,
        })

        print(f"{pid:10s} | exact={em} | prefix={pm}")

    avg_exact = total_exact / num_problems
    avg_prefix = total_prefix / num_problems
    print("\nSUMMARY")
    print(f"Exact Match Avg : {avg_exact:.3f}")
    print(f"Prefix Match Avg: {avg_prefix:.3f}")

    tuned_name = os.path.basename(base_prompt_path).replace(".md", "_tuned.md")
    tuned_prompt_path = os.path.join(tuned_prompt_dir, tuned_name)
    with open(tuned_prompt_path, "w") as f:
        f.write(base_prompt)
        f.write("\n\n---\n")
        f.write(f"<!-- Avg Exact Match: {avg_exact:.4f} -->\n")
        f.write(f"<!-- Avg Prefix Match: {avg_prefix:.4f} -->\n")

    results_path = tuned_prompt_path.replace(".md", "_results.json")
    with open(results_path, "w") as f:
        json.dump(detailed_results, f, indent=2)

    print(f"\nTuned prompt saved to: {tuned_prompt_path}")
    print(f"Results saved to: {results_path}")

if __name__ == "__main__":
    BASE_PROMPT_NAME = "zero_shot_prompt.md"
    NUM_PROBLEMS = 20
    SEED = 42

    BASE_PROMPT_DIR = "./prompts/base_prompts"
    TUNED_PROMPT_DIR = "./prompts/tuned_prompts"
    PROBLEM_DIR = "./data/problems"
    BASELINE_DIR = "./data/solutions"

    random.seed(SEED)
    os.makedirs(TUNED_PROMPT_DIR, exist_ok=True)
    BASE_PROMPT_PATH = os.path.join(BASE_PROMPT_DIR, BASE_PROMPT_NAME)

    run_tuning(
        base_prompt_path=BASE_PROMPT_PATH,
        tuned_prompt_dir=TUNED_PROMPT_DIR,
        problem_dir=PROBLEM_DIR,
        baseline_dir=BASELINE_DIR,
        num_problems=NUM_PROBLEMS,
    )
