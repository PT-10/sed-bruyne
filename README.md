# sed-bruyne
> Can your LLM assist in solving these sed puzzles?\
 Evaluating LLM reasoning capabilities on string rewriting puzzles (Semi-Thue systems)

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
## Repository Structure

```
root/
├── src/
│   ├── puzzle_generation/
│   │   ├── binary_nfa_new.py      # NFA and Binary puzzle generators
│   │   └── new_puzzles.py         # General Semi-Thue puzzle generator
│   │
│   │
│   ├── sed-solver/
│   │   ├── baseline.py            # BFS baselines
│   │   ├── main.py                # Main solver interface
│   │   ├── utils.py               # Puzzle solving utilities
│   │   ├── visualizer.py          # Solution path visualization
│   │   ├── solve_and_visualize.py # Combined solving and visualization
│   │   ├── gemini_batch_test.py   # Gemini API batch testing
│   │   ├── local_llm_inference.py # Local LLM inference via OpenAI API
│   │   └── batch_response_parser.py # Parse batch API responses
│   │
│   ├── dspy/
│   │   ├── base.py                # DSPy base configuration
│   │   ├── llm_sed_solver.py      # DSPy solver module
│   │   ├── optimize_zero_shot.py  # Zero-shot prompt optimization
│   │   ├── optimize_fewshot.py    # Few-shot prompt optimization
│   │   └── optimize_simba_hybrid.py # SIMBA optimizer experiments
│   │
│   ├── data/
│   │   ├── problems/              # Generated puzzle files (JSON)
│   │   ├── metadata/              # Puzzle difficulty profiles (JSON)
│   │   ├── solutions/             # Reference solutions (JSON)
│   │   └── LLM Responses/         # Collected LLM responses
|   |       ├── gemini-response/           # Gemini API responses for different prompt templates
|   |       |   ├── batch_analysis/        # Consolidated csvs for evaluation of batch responses per prompt
│   │       |   └── prompt-folders         # Individual prompt folders holding the batch responses
│   │       └── SmolLM3/               # Zero-shot prompt responses of local LLM
│   │
│   ├── prompts/
│   │   ├── base_prompts/          # Prompt templates 
|   |   └── smaller_prompts/       # Smaller concise prompts
│   │
│   └── visualizations/            # Generated graphs and animations
│
├── requirements.txt               # Python dependencies
├── .env-example                   # Environment variable template
└── README.md
```

## Setup

### 1. Install Dependencies

Ensure you have graphviz installed
```bash
sudo apt update
sudo apt install -y graphviz build-essential cmake git
```
### 2. Configure API Keys (Optional)

For LLM evaluation with cloud providers:

```bash
cp .env-example .env
# Edit .env and add your API keys:
# GEMINI_API_KEY="your-key"
```
For running a local llm via OpenAI compatible endpoint for DSPy prompt-tuning, we run our llms through llama.cpp, you may use a provider of your choice.

```bash
# Install llama.cpp or your preferred local LLM server
# Configure the endpoint in your DSPy scripts
```

## Usage
```bash
git clone https://github.com/PT-10/sed-bruyne.git
cd src
```

### Generate Puzzles

#### NFA and Binary Puzzles
```bash
python puzzle_generation/binary_nfa_new.py
```
Generates:
- `NFA_XXX.json`: NFA simulation puzzles (40 puzzles)
- `BIN_XXX.json`: Binary Semi-Thue puzzles (40 puzzles)

#### General Semi-Thue Puzzles
```bash
python puzzle_generation/new_puzzles.py
```
Generates:
- `XXX.json`: General puzzles with varied alphabets (80 puzzles)
- Difficulty controlled by 3 axes: **entropy**, **branching**, **symbols**

### Solve Puzzles

#### Run Baselines 
```bash
python sed-solver/baseline.py
```


#### Visualize Solution
```bash
python sed-solver/solve_and_visualize.py --problem_id BIN_000
```

Outputs:
- `{problem_id}_graph.png`: State transition graph
- `{problem_id}_animation.gif`: Animated solution path


### Prompt Optimization

#### Zero-Shot 
```bash
python optimize_zero_shot.py
```

#### Few-Shot with Prompt Optimization (MIPROv2)
```bash
python optimize_fewshot.py
```

#### SIMBA Optimizer
```bash
python optimize_simba_hybrid.py
```

#### Batch Testing with Gemini
```bash
python sed-solver/gemini_batch_test.py
```



## Puzzle Types

| Type | Prefix | Model | Alphabet | Difficulty Control |
|------|--------|-------|----------|-------------------|
| **NFA** | `NFA_XXX` | NFA Simulation | `{0, 1}` + states | State count, path length |
| **Binary** | `BIN_XXX` | Semi-Thue | `{0, 1}` | Difficulty level (1-4) |
| **General** | `XXX` | Semi-Thue | Variable | Entropy, Branching, Symbols |

### Difficulty Axes (General Puzzles)

1. **Entropy** (1-4): Controls rule complexity and initial string length
   - Higher entropy → longer target strings, more iterations

2. **Branching** (1-4): Controls bogus rule addition
   - `branching >= 2` → adds reversal trap rules

3. **Symbols** (1-4): Controls vocabulary size
   - Level 1: `{A, B}`
   - Level 2: `{A, B, C, D, E}`
   - Level 3: Special characters `{(), <>, !, #, ...}`
   - Level 4: Mixed alphanumeric

## Optimizer Choice

**Reference:** https://dspy.ai/learn/optimization/optimizers/

Experiments use:
- **MIPROv2**
- **SIMBA**

## LLMs Tested

- **SmolLM3-128K**
- **Qwen3-VL-256K**
- **Gemini Flash 2.5-lite**
- **GPT5.2**
- **Gemini 3**
