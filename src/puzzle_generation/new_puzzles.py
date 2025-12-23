import os
import json
import random
import itertools

class SedPuzzleGenerator:
    def get_vocab(self, level):
        if level <= 1: return list("AB")
        if level == 2: return list("ABCDE")
        if level == 3: return list("(){}<>?!#.<>$&*[]")
        return list("abcdeABCDE01234{}!#[]?")

    def generate_rule_set(self, vocab, entropy):
        rules = [{"src": "".join(random.choices(vocab, k=random.randint(2,3))), "tgt": ""}]
        for _ in range(random.randint(3,5)):
            src_len = random.randint(1,4)
            tgt_len = random.randint(0, src_len + (entropy>3)*3 + (entropy>1))
            src = "".join(random.choices(vocab, k=src_len))
            tgt = "".join(random.choices(vocab, k=tgt_len))
            if src != tgt and {"src": src, "tgt": tgt} not in rules:
                rules.append({"src": src, "tgt": tgt})
        return rules

    def add_bogus_rules(self, vocab, valid_rules, string, branching):
        if branching < 2 or len(string) < 2: return valid_rules
        start = random.randint(0, len(string)-2)
        bait = string[start:start+2]
        trap = bait[::-1]
        return valid_rules + [{"src": bait, "tgt": trap}]

    def generate_puzzle(self, id, profile):
        entropy, branching, sym = profile
        vocab = self.get_vocab(sym)
        rules = self.generate_rule_set(vocab, entropy)
        void_rules = [r for r in rules if r['tgt']==""] 
        if not void_rules: return None
        current = random.choice(void_rules)['src']

        for _ in range(10 + 3*entropy):
            rule = random.choice(rules)
            if rule['tgt']=="":
                pos = random.randint(0,len(current))
                current = current[:pos] + rule['src'] + current[pos:]
            elif rule['tgt'] in current:
                current = current.replace(rule['tgt'], rule['src'], 1)

        final_rules = self.add_bogus_rules(vocab, rules, current, branching)
        random.shuffle(final_rules)
        return {
            "problem_id": f"{id:03d}",
            "initial_string": current,
            "transitions": final_rules
        }, {"difficulty_profile": {"entropy": entropy, "branching": branching, "symbols": sym}}


generator = SedPuzzleGenerator()
problems_dir = "./data/problems"
metadata_dir = "./data/metadata"
os.makedirs(problems_dir, exist_ok=True)
os.makedirs(metadata_dir, exist_ok=True)

def sample_profiles(range_min, range_max, num_samples):
    axes = [list(range(range_min[i], range_max[i]+1)) for i in range(3)]
    combos = list(itertools.product(*axes))
    # Sample with replacement to ensure num_samples
    return [random.choice(combos) for _ in range(num_samples)]

all_ranges = [
    ((1,1,1),(2,2,2),20),
    ((2,2,2),(3,3,3),20),
    ((2,2,2),(3,3,3),20),
    ((3,3,3),(4,4,4),20)
]

puzzle_counter = 0
for rmin, rmax, num in all_ranges:
    profiles = sample_profiles(rmin, rmax, num)
    for profile in profiles:
        puzzle, meta = generator.generate_puzzle(puzzle_counter, profile)
        pid = puzzle["problem_id"]
        json.dump(puzzle, open(f"{problems_dir}/{pid}.json","w"), indent=2)
        json.dump(meta, open(f"{metadata_dir}/{pid}.json","w"), indent=2)
        print(f"Generated puzzle {pid}")
        puzzle_counter += 1

print(f"\nGenerated {puzzle_counter} puzzles in {problems_dir}/ and metadata in {metadata_dir}/")
