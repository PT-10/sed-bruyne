"""
Example script demonstrating the visualization feature of the SED solver.
"""

from baseline import solve_single_problem

if __name__ == "__main__":
    # Example 1: Solve with visualization enabled
    print("=" * 80)
    print("Example 1: Solving BIN_000 with visualization")
    print("=" * 80)

    solution = solve_single_problem(
        problem_id="BIN_000",
        visualize=True,
        output_dir="./visualizations"
    )

    if solution:
        print(f"\n✓ Solution found: {solution.solution}")
        print(f"✓ Visualization files created in ./visualizations/")
    else:
        print("\n✗ No solution found")

    print("\n" + "=" * 80)
    print("Visualization files created:")
    print("  - visualizations/BIN_000_visualization.txt  (human-readable)")
    print("  - visualizations/BIN_000_visualization.json (machine-readable)")
    print("=" * 80)

    # Example 2: Solve without visualization (faster)
    print("\n\nExample 2: Solving without visualization (default)")
    print("=" * 80)

    solution = solve_single_problem(
        problem_id="BIN_000",
        visualize=False  # This is the default
    )

    if solution:
        print(f"✓ Solution found: {solution.solution}")
    else:
        print("✗ No solution found")
