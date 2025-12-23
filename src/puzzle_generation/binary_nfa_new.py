import json
import random
import os

class NFAPuzzleGenerator:
    def __init__(self):
        self.alphabet = ["0", "1"]

    def generate_nfa_puzzle(self, puzzle_id, difficulty):
        num_states = 3 + difficulty
        states = [f"Q{i}" for i in range(num_states)]
        start, final = states[0], states[-1]

        # Backbone path for guaranteed solvability
        path_length = 4 + difficulty
        backbone = []
        current = start
        for _ in range(path_length - 1):
            next_s = random.choice(states)
            char = random.choice(self.alphabet)
            backbone.append((current, char, next_s))
            current = next_s
        backbone.append((current, random.choice(self.alphabet), final))

        transitions = [{"src": f"{s}{c}", "tgt": n} for s, c, n in backbone]

        # Add traps and nondeterminism
        for _ in range(difficulty * 2):
            s, c, n = random.choice(states), random.choice(self.alphabet), random.choice(states)
            if s != final and {"src": f"{s}{c}", "tgt": n} not in transitions:
                transitions.append({"src": f"{s}{c}", "tgt": n})

        # Final state reduction
        transitions.append({"src": final, "tgt": ""})

        initial_string = start + "".join([c for _, c, _ in backbone])
        problem_id = f"NFA_{puzzle_id:03d}"

        puzzle_data = {"problem_id": problem_id, "initial_string": initial_string, "transitions": transitions}
        metadata = {"difficulty_profile": {"type": "nfa_simulation", "difficulty": difficulty, "states": num_states, "path_length": len(backbone)}}

        return puzzle_data, metadata


class BinaryPuzzleGenerator:
    def generate_binary_puzzle(self, puzzle_id, difficulty):
        vocab = ["0", "1"]
        rules = []

        # Ensure at least one terminal rule
        term_src = "".join(random.choice(vocab) for _ in range(random.randint(2, 3)))
        rules.append({"src": term_src, "tgt": ""})

        # Generate other rules
        for _ in range(3 + difficulty // 2):
            src = "".join(random.choice(vocab) for _ in range(random.randint(1, 3)))
            tgt = "".join(random.choice(vocab) for _ in range(random.randint(0, (len(src)+2) if difficulty>3 else len(src))))
            if src != tgt and {"src": src, "tgt": tgt} not in rules:
                rules.append({"src": src, "tgt": tgt})

        # Backward expansion to generate initial string
        current_string = random.choice([r['src'] for r in rules if r['tgt'] == ""])
        for _ in range(5 + difficulty * 2):
            rule = random.choice(rules)
            if rule['tgt'] == "":
                idx = random.randint(0, len(current_string))
                current_string = current_string[:idx] + rule['src'] + current_string[idx:]
            elif rule['tgt'] in current_string:
                idx = current_string.find(rule['tgt'])
                current_string = current_string[:idx] + rule['src'] + current_string[idx+len(rule['tgt']):]

        problem_id = f"BIN_{puzzle_id:03d}"
        puzzle_data = {"problem_id": problem_id, "initial_string": current_string, "transitions": rules}
        metadata = {"difficulty_profile": {"type": "binary_only", "difficulty": difficulty}}
        return puzzle_data, metadata


def save_puzzles(generator, count, difficulties, problems_dir, metadata_dir, prefix):
    os.makedirs(problems_dir, exist_ok=True)
    os.makedirs(metadata_dir, exist_ok=True)
    counter = 0
    for difficulty in difficulties:
        for _ in range(count):
            puzzle, metadata = generator(counter, difficulty)
            pid = puzzle["problem_id"]
            with open(os.path.join(problems_dir, f"{pid}.json"), 'w') as f:
                json.dump(puzzle, f, indent=2)
            with open(os.path.join(metadata_dir, f"{pid}.json"), 'w') as f:
                json.dump(metadata, f, indent=2)
            counter += 1
    return counter


nfa_gen = NFAPuzzleGenerator()
bin_gen = BinaryPuzzleGenerator()

nfa_count = save_puzzles(nfa_gen.generate_nfa_puzzle, 10, range(1, 5), "./data/problems", "./data/metadata", "NFA")
bin_count = save_puzzles(bin_gen.generate_binary_puzzle, 10, range(1, 5), "./data/problems", "./data/metadata", "BIN")

print(f"Generated {nfa_count} NFA puzzles and {bin_count} Binary puzzles.")
