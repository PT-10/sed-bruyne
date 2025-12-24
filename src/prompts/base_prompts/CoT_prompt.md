# String Rewriting Problem Solver (Chain-of-Thought)

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

## Solving Strategy

Follow this step-by-step approach:

1. **Examine** the current string state
2. **Identify** which transition patterns (`src`) appear in the current string
3. **Choose** one applicable transition (consider which helps progress toward empty string)
4. **Apply** the transition to the **leftmost** occurrence of its `src` pattern
5. **Record** the transition index used
6. **Update** the string state
7. **Repeat** steps 1-6 until the string becomes empty

**Helpful Tips:**
- Look for transitions where `tgt` is shorter than `src` (these reduce string length)
- Look for transitions where `tgt` is `""` (void rules - these eliminate characters)
- Track your string state carefully at each step
- If stuck, consider which transitions create patterns that other transitions can match

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

**Input:**
{{PROBLEM_JSON}}

---

## Instructions

**Step 1**: Analyze the transitions and identify useful patterns (void rules, reducing rules)

**Step 2**: Reason through your solution step-by-step:
- Show the current string at each step
- Explain which transition you're applying and why
- Show the resulting string after each application

**Step 3**: Provide the final solution in valid JSON format

---

## Output Format

First, show your reasoning:
```
Step 1: Current string = "<string>"
  → Apply transition [index] ("<src>" → "<tgt>")
  → New string = "<result>"

Step 2: Current string = "<result>"
  → Apply transition [index] ("<src>" → "<tgt>")
  → New string = "<result>"

...

Step N: Current string = "<remaining>"
  → Apply transition [index] ("<src>" → "<tgt>")
  → New string = ""
```

Then, provide the solution:
```json
{
  "problem_id": "<same_as_input>",
  "solution": [<index_0>, <index_1>, ..., <index_n>]
}
```
