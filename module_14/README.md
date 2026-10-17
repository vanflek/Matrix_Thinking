# Module 14 - Matrix Multiplication in Action: Bug Buster

Requirements: Python 3.13, NumPy and Pygame.
Install with `python -m pip install -r requirements.txt`.
No external images or data files are required to run any program.

## Start here

Run `steps/iteration_14_01_skeleton.py` for the starting window,
or `final/bug_buster.py` for the complete game.
Arrow key presses move one cell with cyclic wrapping. Space captures a bug
only when it shares the player's cell. Escape or the close button quits.
The final version adds a circular flashlight; the grid remains visible everywhere.
Movement wraps, but the light uses ordinary Euclidean distance and is clipped by the field.

## Numbering and folders

- `examples/`: 17 standalone console experiments. Example 14.13 includes the
  setup from Example 14.12. Example 14.15 includes the corner experiment and
  the comparison with open-grid coordinates.
- `steps/`: four consecutive complete game versions.
- `final/`: the commented complete game, with the same behavior as Iteration 14.4.
- `solutions/`: five independent exercise solutions. Exercises 26 and 27 run
  in the console; 28 also prints the ring checks and opens a game window;
  29 and 30 open game windows.
- `patches/`: three unified diffs between adjacent iterations. They are editing
  guides, not Python programs. The runnable target files are in `steps/`.
- `assets/illustrations/`: English-labeled chapter figures, not runtime dependencies.

Example and Iteration numbers are independent, not page numbers.
Each Python file is self-contained. Practice tasks 28-30 start independently
from the original final game. Do not carry the ring mask into Exercise 29.

## Examples

- `examples/example_14_01_elementwise_product.py`
- `examples/example_14_02_mask_intersection.py`
- `examples/example_14_03_image_mask.py`
- `examples/example_14_04_matrix_product.py`
- `examples/example_14_05_factor_order.py`
- `examples/example_14_06_shape_constraints.py`
- `examples/example_14_07_weighted_scores.py`
- `examples/example_14_08_identity.py`
- `examples/example_14_09_cyclic_permutation.py`
- `examples/example_14_10_two_dimensional_shifts.py`
- `examples/example_14_11_inverse_operators.py`
- `examples/example_14_12_build_operators.py`
- `examples/example_14_13_operator_checks.py`
- `examples/example_14_14_world_layers.py`
- `examples/example_14_15_distance_mask.py`
- `examples/example_14_16_open_grid_broadcasting.py`
- `examples/example_14_17_shift_comparison.py`

## Game iterations

- `steps/iteration_14_01_skeleton.py`
- `steps/iteration_14_02_arrow_controls.py`
- `steps/iteration_14_03_capture.py`
- `steps/iteration_14_04_flashlight.py`

## Practice solutions

- `solutions/solution_14_26_group_shift.py`
- `solutions/solution_14_27_composed_operator.py`
- `solutions/solution_14_28_ring_light.py`
- `solutions/solution_14_29_two_lights.py`
- `solutions/solution_14_30_three_bugs.py`

The intentional invalid multiplication in Example 14.6 is commented out.
Uncomment it only when studying the expected ValueError.
