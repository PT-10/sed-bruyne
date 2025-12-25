import json, re, csv, time, logging
from pathlib import Path
from typing import Dict, List, Optional
from schema import Problem, Solution
from utils import read_problem_folder, read_solution_folder
from solve_and_visualize import bfs

logging.basicConfig(level=logging.INFO, format="%(message)s")


def parse_batch_response_file(path: Path) -> List[Dict]:
    text = path.read_text()
    blocks = re.findall(r"```json\s*(.*?)\s*```", text, re.DOTALL)
    out = []
    for b in blocks:
        try:
            d = json.loads(b)
            if "problem_id" in d and "solution" in d:
                out.append(d)
        except json.JSONDecodeError:
            pass
    return out


def apply_solution(problem: Problem, sol: List[int]) -> str:
    cur = problem.initial_string
    for i in sol:
        if i >= len(problem.transitions):
            break
        t = problem.transitions[i]
        pos = cur.find(t.src) if t.src else 0
        if pos == -1:
            break
        cur = cur[:pos] + t.tgt + cur[pos + len(t.src):]
    return cur

def is_valid(problem: Problem, sol: List[int]) -> bool:
    return apply_solution(problem, sol) == ""



def analyze(resp: Dict, problems, baselines) -> Dict:
    pid = resp["problem_id"]

    try:
        sol = [int(x) for x in resp["solution"]]
    except Exception:
        return {
            "problem_id": pid,
            "is_valid": False,
            "llm_solution_length": 0,
            "baseline_solution_length": None,
            "unsolved_percentage": None,
            "early_stop": None,
            "deadend": None,
            "error": "non-integer solution format",
        }
    r = dict(problem_id=pid, is_valid=False, llm_solution_length=len(sol),
             baseline_solution_length=None, unsolved_percentage=None,
             early_stop=None, deadend=None, error=None)

    if pid not in problems:
        r["error"] = "missing problem"
        return r

    p = problems[pid]
    if pid in baselines:
        r["baseline_solution_length"] = len(baselines[pid].solution)

    if is_valid(p, sol):
        r["is_valid"] = True
        return r

    rem = apply_solution(p, sol)
    r["unsolved_percentage"] = 100 * len(rem) / max(len(p.initial_string), 1)

    if rem == "":
        r["is_valid"] = True
        return r

    # Create a temporary problem with the remaining string to check if solution can continue
    temp_problem = Problem(
        problem_id=p.problem_id,
        initial_string=rem,
        transitions=p.transitions
    )
    cont = bfs(temp_problem, time_limit=5)
    r["early_stop"] = cont is not None
    r["deadend"] = cont is None
    return r


def process_batch(batch: Path, problems, baselines, outdir: Path):
    logging.info(f"\n=== {batch.name} ===")
    rows = [analyze(r, problems, baselines) for r in parse_batch_response_file(batch)]
    out = outdir / f"{batch.stem}_analysis.csv"

    fields = ["problem_id","is_valid","llm_solution_length",
              "baseline_solution_length","unsolved_percentage",
              "early_stop","deadend","error"]

    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    v = sum(r["is_valid"] for r in rows)
    iv = len(rows) - v
    es = sum(r["early_stop"] is True for r in rows)
    de = sum(r["deadend"] is True for r in rows)

    logging.info(f"Valid: {v}/{len(rows)} | Early-stop: {es} | Deadend: {de}")



def main():
    base = Path("./data")
    batches = Path("./data/gemini_batch_responses")
    out = Path("./data/batch_analysis_markov")
    out.mkdir(exist_ok=True)

    problems = read_problem_folder(base / "problems")
    baselines = read_solution_folder(base / "solutions")

    files = sorted(p for d in batches.iterdir() if d.is_dir() for p in d.glob("*.txt"))
    logging.info(f"Processing {len(files)} batch files")

    for f in files:
        process_batch(f, problems, baselines, out)

    logging.info("Done.")

if __name__ == "__main__":
    main()
