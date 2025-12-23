You are given a single string-rewriting problem.  
Your task is to find **any sequence of transitions** that reduces the initial string to the empty string (`""`).  
You do **not** need to minimize the number of transitions.

---

## Input Format

```json
{
  "problem_id": "<id_number>",
  "initial_string": "<string>",
  "transitions": [
    { 
      "src": "<string>",
      "tgt": "<string>" 
    }
  ]
}
```
## Rewrite Rules

When a transition is applied, it must follow these logic constraints:

  - You may choose any transition whose src appears in the string.

   - A transition is applied only to the first (leftmost) occurrence of src in the current string.

  - Transitions may be applied in any order and any number of times.


## Task
Solve the given problem instance below by producing one valid sequence of transition indices that reduces the initial string to "". Do not include explanations, comments, or extra text.

{{PROBLEM_JSON}}

Return one list of transition indices (0-based) that reduces the string to "". The output must exactly match the following format:
```json
{
  "problem_id": <id_number>,
  "solution": <list_of_transition_indices>
  }
```





