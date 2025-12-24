import os
import dspy
import json
from dotenv import load_dotenv

# Configure DSPy with your LM
llm = dspy.LM(model="openai/local-model",
              api_base="http://localhost:8080/v1",
              api_key="local",
              temperature=0.0,
              max_tokens=76000,
              chat=True)

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
gemini = dspy.LM("gemini/gemini-2.5-flash", api_key = GEMINI_API_KEY)

# dspy.configure(lm = llm, adapter=dspy.ChatAdapter())
dspy.configure(lm = gemini, adapter=dspy.ChatAdapter())
dspy.settings.configure(cache=False)


class SEDSolverSignature(dspy.Signature):
    """
    Find the transitions that must be applied to go from the initial string to a null string. 
    When a transition is applied, it must follow these logic constraints:
        - You may choose any transition whose src appears in the string.
        - At an instance, the transition is applied only to the first (leftmost) occurrence of src in the current string.
        - Transitions may be applied in any order and any number of times.

    Input: problem description with initial string and transitions.
    Output: list of transitions applied.
    """
    problem = dspy.InputField(
        desc="A JSON string containing problem_id, initial_string, and transitions list"
    )
    solution = dspy.OutputField(
        desc="A JSON string with problem_id and solution (list of indices in the order). Indices should be zero-indexed"
    )


# Create predictor
predictor = dspy.Predict(SEDSolverSignature)


# Load actual problem from data
with open('./data/problems/NFA_000.json', 'r') as f:
    sample_problem = json.load(f)
with open('./data/solutions/NFA_000.json', 'r') as f:
    sample_solution = json.load(f)

problem_json = json.dumps(sample_problem)

# Run predictor
result = predictor(problem=problem_json)

print("Input problem:")
print(json.dumps(sample_problem, indent=2))
print("\nModel output:")
print(result.solution)
print("\nBaseline Solution:")
print(json.dumps(sample_solution, indent=2))
print("\n--------------------------------------- History Inspect ---------------------------------")
dspy.inspect_history()