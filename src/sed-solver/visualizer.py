import os

import os
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from schema import Problem, Solution
from graphviz import Digraph


def visualize_solution(problem: Problem, solution: Solution, output_dir="./visualizations"):
    os.makedirs(output_dir, exist_ok=True)

    steps = generate_steps(problem, solution)
    save_graph_visualization(problem, solution, steps, output_dir)

    print(f"Visualization saved to {output_dir}/")


def generate_steps(problem: Problem, solution: Solution):
    steps = []
    current = problem.initial_string

    for idx, t_idx in enumerate(solution.solution):
        t = problem.transitions[t_idx]
        src, tgt = t.src, t.tgt
        pos = current.find(src) if src else 0

        if pos == -1:
            raise ValueError(f"Cannot apply {src}->{tgt} on '{current}'")

        nxt = current[:pos] + tgt + current[pos + len(src):]

        steps.append({
            "step": idx,
            "from": current,
            "to": nxt,
            "transition": t_idx,
            "src": src,
            "tgt": tgt,
            "pos": pos
        })

        current = nxt

    if current != "":
        raise ValueError("Solution does not reach null string")

    return steps

def save_graph_visualization(problem, solution, steps, output_dir):
    try:
        dot = Digraph(comment=f"SED Solution {problem.problem_id}")
    except Exception:
        print("Graphviz not available, skipping PNG graph.")
        return

    os.makedirs(output_dir, exist_ok=True)

    # Vertical layout
    dot.attr(rankdir='TB')  # Top-to-bottom
    dot.attr('node', shape='box', style='filled', fontname='Helvetica', fontsize='12')
    dot.attr('edge', fontsize='10')

    # Start node (highlighted)
    start_label = problem.initial_string or "ε"
    dot.node(start_label, label=start_label, fillcolor='gold')

    # Step node colors
    colors = ['lightblue', 'lightgreen']

    # Add nodes and edges
    for idx, s in enumerate(steps):
        from_label = s["from"] or "ε"
        to_label = s["to"] or "ε"

        # Skip creating start node again
        if to_label != start_label:
            fillcolor = colors[idx % len(colors)]
            # Highlight final null string
            if to_label == "":
                fillcolor = "red"
                to_label = "ε"
            dot.node(to_label, label=to_label, fillcolor=fillcolor)

        # Edge label
        src_display = s["src"] if s["src"] else "ε"
        tgt_display = s["tgt"] if s["tgt"] else "ε"
        dot.edge(from_label, to_label, label=f"[{s['transition']}] {src_display}→{tgt_display}")

    # Render PNG
    out_path = os.path.join(output_dir, f"{problem.problem_id}_graph")
    dot.render(out_path, format="png", cleanup=True)
    print(f"Graph saved as {out_path}.png")


def animate_solution(problem: Problem, solution: Solution, output_dir="./visualizations"):
    os.makedirs(output_dir, exist_ok=True)

    # Prepare steps
    steps = []
    current = problem.initial_string
    for idx, t_idx in enumerate(solution.solution):
        t = problem.transitions[t_idx]
        src, tgt = t.src, t.tgt
        pos = current.find(src) if src else 0
        if pos == -1:
            raise ValueError(f"Cannot apply {src}->{tgt} on '{current}'")
        nxt = current[:pos] + tgt + current[pos+len(src):]
        steps.append({
            "from": current,
            "to": nxt,
            "pos": pos,
            "src": src,
            "tgt": tgt
        })
        current = nxt

    # Matplotlib setup
    fig, ax = plt.subplots(figsize=(12, 2))
    ax.axis('off')

    # Blue heading
    step_text = ax.text(0.5, 0.8, "", ha='center', va='center', fontsize=14, color='blue', transform=ax.transAxes)

    # Character-wise text objects
    char_texts = []

    def draw_string(string, highlight_start=None, highlight_len=None, replace_start=None, replace_len=None):
        # Remove old texts
        for t in char_texts:
            t.remove()
        char_texts.clear()

        x_start = 0.5 - 0.03 * len(string) / 2  # rough centering
        y = 0.5
        for i, ch in enumerate(string):
            if highlight_start is not None and highlight_start <= i < highlight_start + highlight_len:
                color = 'red'
            elif replace_start is not None and replace_start <= i < replace_start + replace_len:
                color = 'green'
            else:
                color = 'black'
            txt = ax.text(x_start + 0.06*i, y, ch, fontsize=24, fontfamily='monospace', ha='center', va='center', color=color)
            char_texts.append(txt)

    # Build frames
    frames = []
    for idx, s in enumerate(steps):
        # Red highlight for src, character by character
        for i in range(len(s['src'])+1):
            frames.append(("highlight", idx, s['from'], s['pos'], i, s['src'], s['tgt']))
        # Green replacement for tgt
        frames.append(("replace", idx, s['from'], s['to'], s['pos'], s['src'], s['tgt']))

    def update(frame):
        if frame[0] == "highlight":
            _, step_idx, string, start, length, src, tgt = frame
            draw_string(string, highlight_start=start, highlight_len=length)
            step_text.set_text(f"Step {step_idx}: Highlighting '{src}' → '{tgt}'")
        elif frame[0] == "replace":
            _, step_idx, old, new, pos, src, tgt = frame
            draw_string(new, replace_start=pos, replace_len=len(tgt))
            step_text.set_text(f"Step {step_idx}: Applied transition '{src}' → '{tgt}'")
        return char_texts + [step_text]

    anim = FuncAnimation(fig, update, frames=frames, interval=500, blit=False)
    output_path = os.path.join(output_dir, f"{problem.problem_id}_animation.gif")
    anim.save(output_path, writer='pillow')
    print(f"Animation saved as {output_path}")
