import os
import dspy
from dotenv import load_dotenv
from dspy.teleprompt import SIMBA
from base import load_dataset, split_dataset, validity_metric, evaluate_module, SEDSolverSignature

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

examples = load_dataset("./data/problems", "./data/solutions")
train, val, test = split_dataset(examples)
print(f"Loaded {len(examples)} examples: {len(train)} train, {len(val)} val, {len(test)} test")

# ChainOfThought for reasoning + SIMBA's introspective optimization
program = dspy.ChainOfThought(SEDSolverSignature)

# SIMBA with higher max_demos for aggressive hybrid optimization
# This allows SIMBA to freely choose between:
# - Generating self-reflective improvement rules
# - Adding successful execution traces as demonstrations
# - Combining both strategies
teleprompter = SIMBA(
    metric=validity_metric,
    bsize=32,                # Mini-batch size for identifying challenging examples
    num_candidates=6,        # More candidates for exploration
    max_steps=10,            # More iterations for better optimization
    max_demos=8,             # Allow more demonstrations (hybrid CoT + few-shot)
    temperature_for_sampling=0.2,
    temperature_for_candidates=0.2
)

print("Optimizing with SIMBA hybrid approach (CoT + few-shot demonstrations)...")
print("SIMBA will introspectively decide the best combination of rules and demos.")
optimized_program = teleprompter.compile(
    program,
    trainset=train
)

optimized_program.save("optimized_simba_hybrid.json")
print("Saved optimized SIMBA hybrid program to optimized_simba_hybrid.json")

# Evaluate on validation set
print("\nEvaluating on validation set...")
val_results = evaluate_module(optimized_program, val, validity_metric)
print(f"Validation accuracy: {val_results['accuracy']:.2%} ({val_results['correct']}/{val_results['total']})")

# Evaluate on test set
print("\nEvaluating on test set...")
test_results = evaluate_module(optimized_program, test, validity_metric)
print(f"Test accuracy: {test_results['accuracy']:.2%} ({test_results['correct']}/{test_results['total']})")
