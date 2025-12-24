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

## Input Format

```json
{
  "problem_id": "<string>",
  "initial_string": "<string>",
  "transitions": [
    { "src": "<pattern>", "tgt": "<replacement>" },
    ...
  ]
}
```

---

## Task

Solve the problem below by finding **one valid sequence** of transition indices that reduces the initial string to `""`.

**Input:**
{{PROBLEM_JSON}}

---

## Output Format

Return **only** valid JSON matching this exact structure:

```json
{
  "problem_id": "<same_as_input>",
  "solution": [<index_0>, <index_1>, ..., <index_n>]
}
```

**Important:**
- No explanations, comments, or extra text
- Solution must be a valid sequence that produces the empty string
- All indices must be valid (0 ≤ index < number of transitions)
