import os, json, random
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-2.5-flash-lite"

PROMPTS = "./prompts/base_prompts"
PROBLEMS = "./data/problems"
OUT = "./data/gemini_batch_responses"


PROMPT_METHODS = {
    "cot": os.path.join(PROMPTS, "CoT_prompt.md"),
    "few_shot": os.path.join(PROMPTS, "few_shot_prompt.md"),
    "few_shot_cot": os.path.join(PROMPTS, "Fewshot_CoT.md"),
}

def load_json(p):
    with open(p) as f:
        return json.load(f)

def load_text(p):
    with open(p) as f:
        return f.read()

def sample_problems(n=50):
    files = [os.path.join(PROBLEMS, f) for f in os.listdir(PROBLEMS) if f.endswith(".json")]
    return random.sample(files, min(n, len(files)))

def create_batch_prompt(template, problems):
    base_template = template.split("## Task")[0] + "## Task\n\n"
    base_template += "Solve ALL of the following problems. For each problem, provide the solution in the format specified above.\n\n"
    base_template += "Process these problems one by one:\n\n"

    # Add all problems
    for i, prob in enumerate(problems, 1):
        base_template += f"--- PROBLEM {i}/{len(problems)} ---\n"
        base_template += f"```json\n{json.dumps(prob, indent=2)}\n```\n\n"

    base_template += "Now provide solutions for ALL problems above. Clearly separate each solution."
    return base_template

def prompt_gemini(text):
    try:
        r = client.models.generate_content(
            model=MODEL,
            contents=text,
        )
        return r.text
    except Exception as e:
        return f"ERROR: {e}"

def save_batch(method, text, problem_ids):
    d = os.path.join(OUT, method)
    os.makedirs(d, exist_ok=True)

    # Save full response
    path = os.path.join(d, "batch_response_all_50.txt")
    with open(path, "w") as f:
        f.write(text)
    print(f"  Saved: {path}")

    # Save metadata about which problems were included
    meta_path = os.path.join(d, "batch_metadata.json")
    with open(meta_path, "w") as f:
        json.dump({
            "num_problems": len(problem_ids),
            "problem_ids": problem_ids
        }, f, indent=2)
    print(f"  Saved metadata: {meta_path}")

# --- Main ---
def main():
    # Sample 50 problems
    problem_files = sample_problems(50)
    problems = [load_json(pf) for pf in problem_files]
    problem_ids = [p["problem_id"] for p in problems]

    print(f"Sampled {len(problems)} problems")
    print(f"Problem IDs: {', '.join(problem_ids[:10])}... (showing first 10)")
    print(f"\nSending 3 batch requests (1 per method)\n")

    for method, prompt_file in PROMPT_METHODS.items():
        print(f"\n{'='*80}")
        print(f"METHOD: {method.upper()}")
        print(f"{'='*80}")

        # Load template
        template = load_text(prompt_file)

        # Create batch prompt with all 50 problems
        print(f"Creating batch prompt with {len(problems)} problems...")
        batch_prompt = create_batch_prompt(template, problems)

        print(f"Prompt size: {len(batch_prompt):,} characters")
        print(f"Sending to Gemini ({MODEL})...")

        # Get response for all problems in one request
        response = prompt_gemini(batch_prompt)

        # Save the batch response
        save_batch(method, response, problem_ids)

        print(f"✓ Completed {method}")

    print(f"\n{'='*80}")
    print(f"DONE! All 3 batch requests completed.")
    print(f"Outputs saved to: {OUT}")
    print(f"{'='*80}")

if __name__ == "__main__":
    main()
