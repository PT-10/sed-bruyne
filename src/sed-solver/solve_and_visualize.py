## original code - https://github.com/precog-iiith/sed-solver/blob/main/src/baseline.py

import os
import json
import time
from schema import Solution, Problem
from visualizer import visualize_solution, animate_solution
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(message)s")

def bfs(problem, time_limit=5):
    initial = problem.initial_string
    transitions = problem.transitions

    queue = [(initial, 0)]
    operation = {initial: -1}  # Map current string to the transition index used
    parent = {initial: None}  # Map current string to its parent string
    start_time = time.time()  # Record the start time

    while queue:
        current_string, steps = queue.pop(0)

        if time.time() - start_time > time_limit:
            return None

        # Check if the target string is empty
        if current_string == "":
            solution = []
            while current_string is not None:
                operation_index = operation[current_string]
                if operation_index != -1:
                    solution.append(operation_index)
                current_string = parent[current_string]

            return solution[::-1]  # Reverse to get the correct order

        # Process all transitions
        for i, transition in enumerate(transitions):
            src = transition.src
            tgt = transition.tgt

            pos = current_string.find(src) if src else 0
            if pos != -1:
                new_string = current_string[:pos] + tgt + current_string[pos + len(src):]

                if new_string not in operation:
                    operation[new_string] = i  # Store the transition index
                    parent[new_string] = current_string
                    queue.append((new_string, steps + 1))

    return None  # No solution found


def solve_single_problem(problem_id, time_limit=15, visualize=False, output_dir="./visualizations"):
    problem_path = f"./data/problems/{problem_id}.json"

    if not os.path.isfile(problem_path):
        logging.error(f"Problem {problem_id} not found at {problem_path}")
        return None

    # load single problem JSON
    with open(problem_path, "r") as f:
        problem_data = json.load(f)
        print(problem_data)

    # build Problem object (same schema used by bfs)
    problem = Problem(**problem_data)

    logging.info(f"Solving puzzle {problem_id}...")

    solution = bfs(problem, time_limit=time_limit)

    if solution is None:
        logging.info(f"No solution found for puzzle {problem_id}")
        return None

    sol = Solution(
        problem_id=problem.problem_id,
        solution=solution
    )

    logging.info(f"Solution found for puzzle {problem_id}: {solution}")

    # Generate visualization if requested
    if visualize:
        logging.info(f"Generating visualization for puzzle {problem_id}...")
        try:
            visualize_solution(problem, sol, output_dir=output_dir)
        except Exception as e:
            logging.error(f"Failed to generate visualization: {e}")

    return sol



if __name__ == "__main__":
    problem_id="BIN_000"
    problem_path = f"./data/problems/{problem_id}.json"

    if not os.path.isfile(problem_path):
        logging.error(f"Problem {problem_id} not found at {problem_path}")

    # load single problem JSON
    with open(problem_path, "r") as f:
        problem_data = json.load(f)
        print(problem_data)

    problem = Problem(**problem_data)
    sol = solve_single_problem(problem_id = problem_id, visualize=True)
    print(sol)
    animate_solution(problem, sol, output_dir="./visualizations")