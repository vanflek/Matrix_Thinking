# Module 10 — Game of Life

Run each file separately with Python 3.13, NumPy and (for windowed examples) Pygame. No example imports another teaching script.

## Getting started

Install the dependencies with `python -m pip install -r requirements.txt`.
Run `python life_roll.py` for the complete interactive simulation.
`life_loops.py` uses the original loop-based calculation; `life_argwhere_example.py` prints a coordinate-based calculation in the console.
The base simulation keeps the outermost rows and columns permanently dead.

## Learning steps

- `iterations/s00_world.py`: World matrix.
- `iterations/s01_one_neighborhood.py`: Count one neighborhood.
- `iterations/s02_cell_rules.py`: Rules for one cell.
- `iterations/s03_generation_loops.py`: Generation with loops.
- `iterations/s04_generation_function.py`: Generation function.
- `iterations/s05_display_step.py`: Window and Space to step.
- `iterations/s06_mouse_edit.py`: Mouse editing.
- `iterations/s07_run_pause.py`: Run, pause and N to step.
- `iterations/s08_clear.py`: Clear the field.
- `iterations/s09_cursor_overlay.py`: Cursor overlay.
- `iterations/s10_save_load.py`: Save and load.
- `iterations/s11_patterns.py`: Explore patterns.
- `iterations/s12_roll_directions.py`: Cyclic shifts.
- `iterations/s13_elementwise_addition.py`: Elementwise addition.
- `iterations/s14_eight_shift_sum.py`: Sum eight shifts.
- `iterations/s15_survive_born_masks.py`: Survival and birth masks.
- `iterations/s16_compare_loops_roll.py`: Compare loops and rolls.
- `iterations/s17_life_roll.py`: Complete simulation.
- `iterations/s18_argwhere_coordinates.py`: Source and recipient coordinates.
- `iterations/s19_add_at.py`: Repeated-index accumulation.
- `iterations/s20_argwhere_generation.py`: Generation with argwhere.
- `iterations/s21_compare_three_methods.py`: Compare all three methods.

## Controls

- Steps s05–s06: Space advances one generation. Left click edits cells from s06.
- Windowed steps s07–s10 and s17: Space toggles automatic simulation; N steps while paused.
- C clears from s08. The cursor overlay appears from s09.
- S/L saves/loads from s10. Save paths are relative to the current working directory.
- Esc or the close button exits.

## Exercise solutions

Each file in `solutions` is standalone. Task 28 includes the counter from task 27. Task 29 uses connected edges and a separate `life_torus.npy` save file.

## Illustrations

Diagrams in `illustrations` explain synchronous generations, shifts, elementwise addition, masks, broadcasting and repeated-index accumulation. All labels are in English.

The windowed examples display a thin gray grid. The transparent grid surface is built once and drawn over the cells; the cursor frame is drawn last. Grid lines do not change the world matrix.
