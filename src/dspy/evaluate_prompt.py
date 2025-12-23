import os, json, glob, csv
import dspy

llm = dspy.LM(
    model="openai/local-model",
    api_base="http://localhost:8080/v1",
    api_key="local",
    temperature=0.0,
    max_tokens=32152
)
dspy.configure(lm=llm)

class PromptSolver(dspy.Signature):
    prompt: str = dspy.InputField()
    output: str = dspy.OutputField()
solver = dspy.Predict(PromptSolver)

prompt_path = "./prompts/tuned_prompts/zero_shot_prompt_tuned.md"
problems_dir = "./data/problems"
solutions_dir = "./data/solutions"
output_csv = "./evaluation/zero_shot_prompt_eval.csv"

with open(prompt_path) as f:
    prompt_template = f.read()

rows = []
for problem_file in sorted(glob.glob(f"{problems_dir}/*.json")):
    pid = os.path.basename(problem_file).replace(".json","")
    solution_file = os.path.join(solutions_dir, f"{pid}.json")
    if not os.path.exists(solution_file):
        print(f"Skipping {pid} (no baseline)")
        continue

    problem = json.load(open(problem_file))
    baseline = json.load(open(solution_file))
    prompt = prompt_template.replace("{{PROBLEM_JSON}}", json.dumps(problem, indent=2))

    pred_text = solver(prompt=prompt).output
    try:
        pred_json = json.loads(pred_text[pred_text.index("{"):pred_text.rindex("}")+1])
        solved = int(pred_json.get("solution")==baseline.get("solution"))
        pred_solution = pred_json.get("solution")
    except Exception:
        solved = 0
        pred_solution = None

    rows.append({
        "problem_id": pid,
        "solved": solved,
        "predicted_solution": json.dumps(pred_solution),
        "baseline_solution": json.dumps(baseline.get("solution"))
    })
    print(f"{pid:10s} | solved = {solved}")

with open(output_csv,"w",newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["problem_id","solved","predicted_solution","baseline_solution"])
    writer.writeheader()
    writer.writerows(rows)

print(f"Evaluation complete. CSV saved to {output_csv}")
