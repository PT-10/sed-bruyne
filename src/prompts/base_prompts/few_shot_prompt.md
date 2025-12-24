# String Rewriting Problem Solver

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

## Examples

### Example 1

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

**Output:**
```json
{
  "problem_id": "EX_001",
  "solution": [0, 0, 1, 1]
}
```

---

### Example 2

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

**Output:**
```json
{
  "problem_id": "EX_002",
  "solution": [0, 1, 2]
}
```

---

### Example 3

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

**Output:**
```json
{
  "problem_id": "EX_003",
  "solution": [0, 1]
}
```

---

## Task

Now solve the following problem and return **only** the JSON output in the specified format.

**Input:**
{{PROBLEM_JSON}}

**Output:**
