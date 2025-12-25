import os, json
from pathlib import Path
from typing import Dict, List
from tqdm import tqdm
from openai import OpenAI

BASE_DIR = Path(__file__).parent.parent
PROMPTS_DIR = BASE_DIR / "prompts" / "base_prompts"
PROBLEMS_DIR = BASE_DIR / "data" / "problems"
OUTPUT_DIR = BASE_DIR / "data" / "SmolLM3"

LOCAL_ENDPOINT = "http://localhost:8080/v1"
LOCAL_MODEL = "local-model"

PROMPT_TYPES = {
    "zero_shot": "zero_shot_prompt.md",
    "cot": "CoT_prompt.md",
    "few_shot": "few_shot_prompt.md",
    "few_shot_cot": "Fewshot_CoT.md",
}


def load_prompt(name: str) -> str:
    return (PROMPTS_DIR / name).read_text()


def load_problem(path: Path) -> Dict:
    return json.loads(path.read_text())


def get_problems() -> List[Path]:
    return sorted(PROBLEMS_DIR.glob("*.json"))


def format_prompt(template: str, problem: Dict) -> str:
    return template.replace("{{PROBLEM_JSON}}", json.dumps(problem, indent=2))


def query_llm(client: OpenAI, prompt: str) -> str:
    try:
        res = client.chat.completions.create(
            model=LOCAL_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=2048,
        )
        return res.choices[0].message.content
    except Exception as e:
        return json.dumps({"error": str(e)})


def run():
    client = OpenAI(base_url=LOCAL_ENDPOINT, api_key="not-needed")
    problems = get_problems()
    prompts = {k: load_prompt(v) for k, v in PROMPT_TYPES.items()}

    for ptype, template in prompts.items():
        out_dir = OUTPUT_DIR / ptype
        out_dir.mkdir(parents=True, exist_ok=True)

        for prob_file in tqdm(problems, desc=ptype):
            pid = prob_file.stem
            out_file = out_dir / f"{pid}_response.txt"
            if out_file.exists():
                continue

            problem = load_problem(prob_file)
            prompt = format_prompt(template, problem)
            response = query_llm(client, prompt)
            out_file.write_text(response)


if __name__ == "__main__":
    run()
