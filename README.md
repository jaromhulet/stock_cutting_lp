# Stock Cutting Problem Solver

A Python-based optimization solution for the classic stock cutting problem using hill climbing and linear programming.

## Problem Description

The stock cutting problem is an optimization challenge where the goal is to minimize the number of stock pieces needed to fulfill a set of cut requirements. Given:

- A stock length (e.g., a piece of material of fixed length)
- A set of required cuts with specific quantities needed
- The objective is to find cutting patterns that minimize waste and total stock pieces purchased

For example, if you need cuts of lengths 4, 5, and 12 units from stock of length 14 units, the algorithm finds the optimal combination of cutting patterns that meets all requirements while using the fewest stock pieces.

## Architecture

### Two-Stage Optimization Approach

1. **Pattern Generation (Hill Climbing)**
   - Uses a hill climbing algorithm to generate feasible cutting patterns
   - Starts with random patterns and iteratively improves them by minimizing waste
   - Generates multiple candidate patterns to serve as options for the LP solver

2. **Pattern Selection (Linear Programming)**
   - Uses PuLP library to solve a linear programming problem
   - Decides how many of each cutting pattern to use
   - Minimizes total number of stock pieces needed

## Project Structure

```
cutting_problem/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── stock_cutting.py                   # Entry point (may be deprecated)
└── stock_cutting_lp/
    ├── hill_climb.py                  # Hill climbing algorithm implementation
    ├── stock_cutting.py               # Main StockCutting class combining both approaches
    ├── simple_example_problem.py      # Simple example using PuLP directly
    └── run_problem.py                 # Example runner script
```

## Key Classes

### `CutsHillClimb` (hill_climb.py)
- `starting_solution()`: Creates a random initial cutting pattern
- `check_pattern()`: Validates if a pattern fits within stock length
- `create_nbr_hood()`: Generates variations of a pattern (neighborhood search)
- `calc_waste()`: Calculates waste for a given pattern
- `hill_climb()`: Runs the hill climbing algorithm to optimize a single pattern

### `StockCutting` (stock_cutting.py)
- Extends `CutsHillClimb`
- `create_list_of_patterns()`: Generates multiple cutting patterns using hill climbing
- `solve_lp_problem()`: Solves the LP problem to find optimal pattern usage

## Installation

1. Create a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Dependencies

- **pandas**: Data manipulation (used for potential data handling)
- **pulp**: Linear programming solver integration

## Usage

### Basic Example

```python
from stock_cutting_lp.stock_cutting import StockCutting

# Define cuts needed: {length: quantity}
cuts_dict = {
    5: 2,    # Need 2 cuts of length 5
    12: 6,   # Need 6 cuts of length 12
    4: 9     # Need 9 cuts of length 4
}

stock_length = 14  # Each stock piece is 14 units long

# Create solver instance
solver = StockCutting(cuts_dict, stock_length, nbr_hood_size=2)

# Solve with 10 candidate patterns
solver.solve_lp_problem(num_patterns=10)
```

### Running the Example

```bash
cd stock_cutting_lp
python run_problem.py
```

## Output

The solver returns:
- Optimal solution status
- Recommended cutting patterns and how many of each to use
- Number of stock pieces to purchase
- How many of each cut is produced by each pattern

Example output:
```
pattern_0 uses = 2.5
pattern_0 cuts = (4, 5)

pattern_1 uses = 3.0
pattern_1 cuts = (12,)

Purchase 6 stock pieces
```

## Algorithm Details

### Hill Climbing Algorithm

1. Generate a random starting solution (valid cutting pattern)
2. Create a neighborhood of patterns by:
   - Swapping one cut for another
   - Randomly adding or removing cuts
3. Evaluate each neighbor (calculate waste)
4. Move to best neighbor if it improves waste
5. Repeat until convergence or max iterations

### Linear Programming Formulation

- **Decision Variables**: Number of each cutting pattern to use
- **Objective**: Minimize total stock pieces used
- **Constraints**: Meet minimum quantity requirements for each cut type

## Parameters

### `StockCutting.__init__`
- `cuts_dict`: Dictionary of {cut_length: quantity_needed}
- `stock_length`: Length of each stock piece
- `nbr_hood_size`: Size of neighborhood to explore in hill climbing

### `solve_lp_problem`
- `num_patterns`: Number of candidate patterns to generate
- `max_iters`: Maximum iterations for hill climbing (default: 150)

## Notes

- The hill climbing approach intentionally seeks local optima, which can generate diverse patterns that improve overall LP solution quality
- The algorithm is heuristic-based; solutions are typically very good but may not be globally optimal
- Increasing `num_patterns` generally improves solution quality but takes longer
- Results may vary between runs due to randomization in pattern generation

## Future Improvements

- Implement additional metaheuristics (simulated annealing, genetic algorithms)
- Add visualization of cutting patterns
- Implement cutting sequence ordering
- Add support for multiple stock types
- Performance optimization for large instances

---


