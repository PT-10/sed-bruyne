# sed-bruyne
> Can your LLM assist in solving these sed puzzles?

![Animation](src/visualizations/BIN_000_animation.gif)

```json
{
  "problem_id": "BIN_000",
  "initial_string": "1010000100100",
  "transitions": [
    {
      "src": "100",
      "tgt": ""
    },
    {
      "src": "101",
      "tgt": "11"
    },
    {
      "src": "00",
      "tgt": "0"
    },
    {
      "src": "01",
      "tgt": "11"
    }
  ]
}
```

Ensure you have graphviz installed
```bash
sudo apt update
sudo apt install -y graphviz build-essential cmake git
```

For running a local llm via OpenAI compatible endpoint for DSPy prompt-tuning, we run our llms through llama.cpp, you may use a provider of your choice.
