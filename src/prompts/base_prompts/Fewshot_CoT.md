# String Rewriting Problem Solver (Few-Shot with Reasoning)

## Objective
Transform the given `initial_string` into an **empty string** (`""`) by applying a sequence of transitions.

---

## Rules

You are provided with:
- An `initial_string` to transform
- A list of `transitions`, where each transition has:
  - `src`: pattern to find in the string
  - `tgt`: replacement text

**Application Rules:**
1. **Pattern Matching**: You may apply a transition only if its `src` appears in the current string
2. **Leftmost Application**: Always replace the **first (leftmost)** occurrence of `src`
3. **Unlimited Reuse**: Transitions may be applied multiple times and in any order
4. **Zero-Based Indexing**: Track transitions by their 0-based index in the transitions array

**Goal**: Reach the empty string `""` (you do NOT need to find the shortest solution)

---

## Example 1

**Input:**
```json
{
  "problem_id": "EX_001",
  "initial_string": "ABAB",
  "transitions": [
    { "src": "AB", "tgt": "B" },
    { "src": "B", "tgt": "" }
  ]
}
```

**Reasoning:**

Step 1: Current string = "ABAB"
  - Available transitions: [0] "AB"→"B", [1] "B"→""
  - "AB" appears at position 0 (leftmost)
  - Apply transition [0]: "AB" → "B"
  - New string = "BAB"

Step 2: Current string = "BAB"
  - "AB" appears at position 1
  - Apply transition [0]: "AB" → "B"
  - New string = "BB"

Step 3: Current string = "BB"
  - "AB" not found
  - "B" appears at position 0 (leftmost)
  - Apply transition [1]: "B" → ""
  - New string = "B"

Step 4: Current string = "B"
  - Apply transition [1]: "B" → ""
  - New string = ""

**Output:**
```json
{
  "problem_id": "EX_001",
  "solution": [0, 0, 1, 1]
}
```

---

## Example 2

**Input:**
```json
{
  "problem_id": "EX_002",
  "initial_string": "XXY",
  "transitions": [
    { "src": "XX", "tgt": "X" },
    { "src": "X", "tgt": "" },
    { "src": "Y", "tgt": "" }
  ]
}
```

**Reasoning:**

Step 1: Current string = "XXY"
  - Available transitions: [0] "XX"→"X", [1] "X"→"", [2] "Y"→""
  - "XX" appears at position 0
  - Apply transition [0]: "XX" → "X"
  - New string = "XY"

Step 2: Current string = "XY"
  - "XX" not found
  - "X" appears at position 0
  - Apply transition [1]: "X" → ""
  - New string = "Y"

Step 3: Current string = "Y"
  - Apply transition [2]: "Y" → ""
  - New string = ""

**Output:**
```json
{
  "problem_id": "EX_002",
  "solution": [0, 1, 2]
}
```

---

## Example 3

**Input:**
```json
{
  "problem_id": "EX_003",
  "initial_string": "AABB",
  "transitions": [
    { "src": "AA", "tgt": "" },
    { "src": "BB", "tgt": "" }
  ]
}
```

**Reasoning:**

Step 1: Current string = "AABB"
  - Transition [0] "AA"→"" creates a void (eliminates "AA")
  - "AA" appears at position 0
  - Apply transition [0]: "AA" → ""
  - New string = "BB"

Step 2: Current string = "BB"
  - Transition [1] "BB"→"" creates a void (eliminates "BB")
  - Apply transition [1]: "BB" → ""
  - New string = ""

**Output:**
```json
{
  "problem_id": "EX_003",
  "solution": [0, 1]
}
```

---

## Task

Now solve the following problem. Show your step-by-step reasoning first, then provide the solution in JSON format.

**Input:**
{{PROBLEM_JSON}}

**Your Response:**
