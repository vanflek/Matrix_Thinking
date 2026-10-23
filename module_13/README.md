# Module 13 - Maze as a Matrix

Requirements: Python 3.13, NumPy, and Pygame.
Install dependencies with `python -m pip install -r requirements.txt`.
No external images, fonts, or maze files are needed to start.

## Where to start

Run `steps/iteration_13_01_skeleton.py` for the starting field, or
`final/maze_generator.py` for the complete program. All Python files are standalone.
The final file contains detailed English comments; its behavior matches Iteration 13.11.

The first versions use explicit loops to explain the algorithm. Iterations 13.9-13.11
replace selected computations with NumPy while preserving their meaning.

## Controls

- Left click: open a passage if allowed. Right click: restore a wall.
- C: clear the field and stop automatic growth.
- G: start/pause automatic growth; one growth step is attempted per frame.
- S: save `maze.npy`. L: load and validate it, then pause growth.
- P: pause and check whether the current passage graph is a tree.
- Esc or the window close button: quit.

Controls are introduced gradually; consult the chapter for the current step.
S and L use the current working directory. To exchange a saved maze between scripts,
give them the same working directory or move `maze.npy` to the next script's working directory.
The loader accepts a single uint8 NPY array with the current field shape and only 0/1 values.

## Numbering and folders

- `steps/`: eleven successive complete versions of one window program.
- `examples/`: ten independent console experiments.
- `final/`: the complete commented program.
- `solutions/`: five independent window programs for exercises 26-30.
- `patches/`: ten unified diffs between adjacent step files, plus `manifest.json`.
- `assets/illustrations/`: nine English-labeled chapter figures, not runtime dependencies.

Iteration 13.5 and Example 13.5 have independent numbers. These are not page numbers.
A short chapter fragment belongs to the surrounding iteration unless labeled as an Example.
Patches show the lines changed between the two snapshots named in their headers.
Use their hunks as an editing guide; the full target snapshot is runnable on its own.

## Learning steps

- `steps/iteration_13_01_skeleton.py` - Field, grid, and mouse cursor.
- `steps/iteration_13_02_manual_building.py` - Manual passage and wall commands.
- `steps/iteration_13_03_local_rule.py` - Local opening rule and first-passage exception.
- `steps/iteration_13_04_cursor_feedback.py` - Allowed/blocked cursor feedback.
- `steps/iteration_13_05_frontier_display.py` - Display every currently allowed opening.
- `steps/iteration_13_06_automatic_growth.py` - Automatic growth, pause, and completion.
- `steps/iteration_13_07_save_load.py` - Save/load with array validation.
- `steps/iteration_13_08_check_maze.py` - Connectivity, edge count, and perfect-maze check.
- `steps/iteration_13_09_numpy_coordinates.py` - NumPy coordinate searches.
- `steps/iteration_13_10_numpy_edges.py` - Edge counting using adjacent slices.
- `steps/iteration_13_11_numpy_frontier.py` - Neighbor contributions and NumPy frontier.

## Standalone examples

- `examples/example_13_01_neighbors.py` - Four-neighbor coordinates and passage counts.
- `examples/example_13_02_opening_rule.py` - Opening-rule checks.
- `examples/example_13_03_frontier.py` - Allowed-opening matrix.
- `examples/example_13_04_growth_step.py` - One random growth step.
- `examples/example_13_05_stack_and_set.py` - Stack and set operations.
- `examples/example_13_06_connectivity.py` - Connectivity checks.
- `examples/example_13_07_perfect_maze.py` - Trees, cycles, and disconnected passages.
- `examples/example_13_08_numpy_coordinates.py` - Coordinate arrays and tuple lists.
- `examples/example_13_09_numpy_edges.py` - Vertical and horizontal edge masks.
- `examples/example_13_10_numpy_frontier.py` - Neighbor counts and frontier masks.

## Practice solutions

- `solutions/solution_13_26_exercise.py` - Passage and allowed-opening counts in the title.
- `solutions/solution_13_27_exercise.py` - N requests one manual growth step.
- `solutions/solution_13_28_exercise.py` - Highlight dead ends in amber.
- `solutions/solution_13_29_exercise.py` - H toggles reachable passages in blue.
- `solutions/solution_13_30_exercise.py` - P reports connected-component count.

Each solution starts from the same final program; changes are not cumulative.
For exercise 29, use the two 3x7 initial arrays printed in the chapter in separate runs
with ROWS=3, COLS=7, and CELL_SIZE=80. Select passage (row=1, col=1), then press H.
The separate arrays contain 2 and 5 reachable passages respectively. The local growth
rule deliberately rejects the joining cell because it has two passage neighbors.
Exercise 30 uses these same arrays to check component counts 2 and 1.
Set the initial arrays directly for these tests; generating a connection with mouse clicks
would change the rule being taught.

## Data rules

`maze` stores 0 for a wall and 1 for a passage. `frontier` marks allowed next openings.
Color indices 2 and 3 are display data and never enter `maze`.
Passage coordinates and the stored cursor cell both use (row, col).
Starting with one passage and adding only allowed cells preserves a tree. Erasing passages
or loading arbitrary binary arrays can break that property, so global checks are separate.
An empty field is not a perfect maze in this program; one isolated passage is.


## File and listing names

`steps/iteration_MM_NN_name.py` contains runnable learning steps in chapter order.
`examples/example_MM_NN_name.py` contains independent experiments.
`solutions/solution_MM_TT_name.py` contains exercise solutions (TT is the exercise number).
`final/` contains complete programs, where provided. Listing identifiers match file stems;
these numbers are not PDF page numbers. Run each program separately.

## Coordinate convention

`state["cell"]` and matrix indices both use `(row, col)`, consistently
with the RGB editor. `clamp_cell(row, col, rows, cols)` returns that same order.
Only Pygame positions and drawing coordinates use `(x, y)` or `(col, row)`.
