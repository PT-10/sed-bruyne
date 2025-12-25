# String Reduction

## Goal
Reduce `initial_string` to `""` using the given transitions.

## Rules
- Each transition replaces `src` with `tgt`
- Apply only if `src` exists; replace the **leftmost** match
- Transitions may be reused in any order
- Use **0-based** transition indices
- Any valid solution is acceptable

## Input
```json
{
  "problem_id": "<string>",
  "initial_string": "<string>",
  "transitions": [
    { "src": "<pattern>", "tgt": "<replacement>" }
  ]
}

Task

Provide one sequence of transition indices that reduces the string to "".

Input: {{PROBLEM_JSON}}
Output

{
  "problem_id": "<same_as_input>",
  "solution": [<i0>, <i1>, ..., <in>]
}

Constraints

    Output JSON only

    Valid indices

    Must reach the empty string