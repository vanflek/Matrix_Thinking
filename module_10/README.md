# Module 10 — Game of Life

Run each file separately with Python 3.13, NumPy and (for windowed examples) Pygame. No example imports another teaching script.

## Getting started

Install the dependencies with `python -m pip install -r requirements.txt`.
Run `python final/life_roll.py` for the complete interactive simulation.
`examples/example_10_01_life_loops.py` uses the original loop-based calculation; `examples/example_10_02_life_argwhere.py` prints a coordinate-based calculation in the console.
The base simulation keeps the outermost rows and columns permanently dead.

## Learning steps

- `steps/iteration_10_01_world.py`: World matrix.
- `steps/iteration_10_02_one_neighborhood.py`: Count one neighborhood.
- `steps/iteration_10_03_cell_rules.py`: Rules for one cell.
- `steps/iteration_10_04_generation_loops.py`: Generation with loops.
- `steps/iteration_10_05_generation_function.py`: Generation function.
- `steps/iteration_10_06_display_step.py`: Window and Space to step.
- `steps/iteration_10_07_mouse_edit.py`: Mouse editing.
- `steps/iteration_10_08_run_pause.py`: Run, pause and N to step.
- `steps/iteration_10_09_clear.py`: Clear the field.
- `steps/iteration_10_10_cursor_overlay.py`: Cursor overlay.
- `steps/iteration_10_11_save_load.py`: Save and load.
- `steps/iteration_10_12_patterns.py`: Explore patterns.
- `steps/iteration_10_13_roll_directions.py`: Cyclic shifts.
- `steps/iteration_10_14_elementwise_addition.py`: Elementwise addition.
- `steps/iteration_10_15_eight_shift_sum.py`: Sum eight shifts.
- `steps/iteration_10_16_survive_born_masks.py`: Survival and birth masks.
- `steps/iteration_10_17_compare_loops_roll.py`: Compare loops and rolls.
- `steps/iteration_10_18_life_roll.py`: Complete simulation.
- `steps/iteration_10_19_argwhere_coordinates.py`: Source and recipient coordinates.
- `steps/iteration_10_20_add_at.py`: Repeated-index accumulation.
- `steps/iteration_10_21_argwhere_generation.py`: Generation with argwhere.
- `steps/iteration_10_22_compare_three_methods.py`: Compare all three methods.

## Controls

- Steps iteration_10_06–iteration_10_07: Space advances one generation. Left click edits cells from iteration_10_07.
- Windowed steps iteration_10_08–iteration_10_11 and iteration_10_18: Space toggles automatic simulation; N steps while paused.
- C clears from iteration_10_09. The cursor overlay appears from iteration_10_10.
- S/L saves/loads from iteration_10_11. Save paths are relative to the current working directory.
- Esc or the close button exits.

## Exercise solutions

Each file in `solutions` is standalone. Task 28 includes the counter from task 27. Task 29 uses connected edges and a separate `life_torus.npy` save file.

## Illustrations

Diagrams in `illustrations` explain synchronous generations, shifts, elementwise addition, masks, broadcasting and repeated-index accumulation. All labels are in English.

The windowed examples display a thin gray grid. The transparent grid surface is built once and drawn over the cells; the cursor frame is drawn last. Grid lines do not change the world matrix.


## File and listing names

`steps/iteration_MM_NN_name.py` contains runnable learning steps in chapter order.
`examples/example_MM_NN_name.py` contains independent experiments.
`solutions/solution_MM_TT_name.py` contains exercise solutions (TT is the exercise number).
`final/` contains complete programs, where provided. Listing identifiers match file stems;
these numbers are not PDF page numbers. Run each program separately.
