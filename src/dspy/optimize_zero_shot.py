import os
import dspy
from dotenv import load_dotenv
from dspy.teleprompt import MIPROv2
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

program = dspy.Predict(SEDSolverSignature)

teleprompter = MIPROv2(metric = validity_metric,
                       auto="light",
                       init_temperature=1.0)

print("Optimizing with MIPROv2...")

#remove max_bootstrapped_demos and max_labeled_demos to use same pipeline for few-shot
optimized_program = teleprompter.compile(
                                        program,
                                        trainset=train,
                                        valset=val,
                                        max_bootstrapped_demos=0,
                                        max_labeled_demos=0
                                        )

optimized_program.save("optimized_zero_shot.json")
print("Saved optimized program to optimized_zero_shot.json")

# Evaluate on test set
print("\nEvaluating on test set...")
from base import evaluate_module
results = evaluate_module(optimized_program, test, validity_metric)
print(f"Test accuracy: {results['accuracy']:.2%} ({results['correct']}/{results['total']})")
