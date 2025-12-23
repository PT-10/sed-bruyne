You are given a single string-rewriting problem.  
Your task is to find **any sequence of transitions** that reduces the initial string to the empty string (`""`).  
You do **not** need to minimize the number of transitions.

---

### Example 1

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

Output:
{
  "problem_id": "EX_001",
  "solution": [0, 0, 1, 1]
}


### Example 2
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

Output:
{
  "problem_id": "EX_002",
  "solution": [0, 1, 2]
}

Now solve the following problem and return the output in the specified format:

Input:
{{PROBLEM_JSON}}

Output:
