You are a string-rewriting solver.  
Your task is to reduce the given string to the empty string ("") by applying a sequence of transitions.  
Follow these rules carefully:

1. Each transition has a source string (`src`) and target string (`tgt`).
2. You may apply a transition **only if its `src` appears in the current string**.
3. Always apply the transition to the **first (leftmost) occurrence** of `src`.
4. Transitions can be applied **any number of times** and in any order.
5. Your goal is to reach the empty string "" — you do **not** need to minimize the number of steps.
6. Track the **0-based index** of each transition you apply.

---

### Examples

**Example 1**

Input:
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

Step-by-step reasoning:

- Current string: "ABAB"\
    Apply transition [0] ("AB" → "B") → "BB"

- Current string: "BB"\
    Apply transition [0] ("AB" → "B") → cannot apply, move to next

- Current string: "BB"\
    Apply transition [1] ("B" → "") → "B"

- Current string: "B"\
    Apply transition [1] ("B" → "") → ""

Output:
```json
{
  "problem_id": "EX_001",
  "solution": [0, 1, 1]
}
```

### Example 2
Input:
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

Step-by-step reasoning:

- Current string: "XXY"\
    Apply transition [0] ("XX" → "X") → "XY"

- Current string: "XY"\
    Apply transition [1] ("X" → "") → "Y"

- Current string: "Y"\
    Apply transition [2] ("Y" → "") → ""

Output:
```json
{
  "problem_id": "EX_002",
  "solution": [0, 1, 2]
}
```

Now your task is to solve the problem below

Input:
```json
{
  "problem_id": "<id_number>",
  "initial_string": "<string>",
  "transitions": [
    { "src": "<string>", "tgt": "<string>" }
  ]
}
```

### Note
- Apply the first match only.

- Keep reasoning explicit: show current string → transition applied → new string.

- Transitions can be repeated any number of times.

- Output must be valid JSON with "problem_id" and "solution" keys.
