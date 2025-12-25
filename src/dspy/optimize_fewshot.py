import os
import dspy
from dotenv import load_dotenv
from dspy.teleprompt import BootstrapFewShotWithRandomSearch
from base import load_dataset, split_dataset, validity_metric, evaluate_module, SEDSolverSignature

llm = dspy.LM(model="openai/local-model",
              api_base="http://localhost:8080/v1",
              api_key="local",
              temperature=0.0,
              max_tokens=16000,
              chat=True)

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
gemini = dspy.LM("gemini/gemini-2.5-flash", api_key = GEMINI_API_KEY)

dspy.configure(lm = llm, adapter=dspy.ChatAdapter())
# dspy.configure(lm = gemini, adapter=dspy.ChatAdapter())
dspy.settings.configure(cache=False)

examples = load_dataset("./data/problems", "./data/solutions")
train, val, test = split_dataset(examples)
print(f"Loaded {len(examples)} examples: {len(train)} train, {len(val)} val, {len(test)} test")

program = dspy.Predict(SEDSolverSignature)

teleprompter = BootstrapFewShotWithRandomSearch(
    metric=validity_metric,
    max_bootstrapped_demos=2,
    max_labeled_demos=2,
    num_candidate_programs=10,
    num_threads=4
)

print("Optimizing few-shot prompt with BootstrapFewShotWithRandomSearch...")
optimized_program = teleprompter.compile(
    program,
    trainset=train,
    valset=val
)

optimized_program.save("optimized_fewshot_cot.json")
print("Saved optimized few-shot CoT program to optimized_fewshot_cot.json")

# Evaluate on test set
print("\nEvaluating on test set...")
from base import evaluate_module
results = evaluate_module(optimized_program, test, validity_metric)
print(f"Test accuracy: {results['accuracy']:.2%} ({results['correct']}/{results['total']})")
