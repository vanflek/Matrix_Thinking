# Module 6 - Slices and Masks: Patterns in the Language of Matrices

Choose whole groups of cells, describe patterns through indices and conditions,
and compare different ways of producing the same matrix.

## Run an example

These files were checked with Python 3.13.7, NumPy 2.5.3, and Pygame 2.6.1.
Use the same interpreter for installation and execution:

```bash
python -m pip install -r requirements.txt
python matrix_visualization.py
```

You can also open any Python file in PyCharm and run it directly. Every file is
standalone. Close a graphical example with the window close button or **Esc**.
Console examples finish after printing their results. All files work independently
of the current working directory.

The complete display program is identical to the chapter listing. Replace only
the block between `PATTERN START` and `PATTERN END` when following the lesson.
Keep `matrix`, `ROWS`, `COLS`, and `CELL_SIZE` consistent with the book.

## Console experiments

| File | Topic |
| --- | --- |
| [slices_1d.py](slices_1d.py) | Start, exclusive stop, step, omitted bounds, and negative indices. |
| [slices_2d.py](slices_2d.py) | Rows, columns, rectangles, and assigning to a selection. |
| [paired_indices_vs_slices.py](paired_indices_vs_slices.py) | Three index pairs versus nine intersections. |
| [scalar_logic.py](scalar_logic.py) | `and`, `or`, and `not`, including the game-door example. |
| [mask_values.py](mask_values.py) | Build a mask, read selected values, write through it, and recompute it. |
| [index_matrices.py](index_matrices.py) | Store row and column indices as data. |
| [mask_operations.py](mask_operations.py) | Union, intersection, and complement of Boolean masks. |

## Patterns in a Pygame window

Each file prints its matrix and displays it. **0 is light; 1 is dark.**
The pattern is built once before the display loop. A smaller piece of NumPy code
does not remove the loops that draw the individual cells.

| File | Pattern |
| --- | --- |
| [vertical_stripes.py](patterns/vertical_stripes.py) | Vertical stripes. |
| [shifted_vertical_stripes.py](patterns/shifted_vertical_stripes.py) | Shifted vertical stripes. |
| [horizontal_stripes.py](patterns/horizontal_stripes.py) | Horizontal stripes. |
| [four_corners.py](patterns/four_corners.py) | Four corners. |
| [frame_slices.py](patterns/frame_slices.py) | Frame slices. |
| [thick_frame.py](patterns/thick_frame.py) | Thick frame. |
| [left_half.py](patterns/left_half.py) | Left half. |
| [right_half.py](patterns/right_half.py) | Right half. |
| [top_half.py](patterns/top_half.py) | Top half. |
| [bottom_half.py](patterns/bottom_half.py) | Bottom half. |
| [centered_square.py](patterns/centered_square.py) | Centered square. |
| [checkerboard_loops.py](patterns/checkerboard_loops.py) | Checkerboard loops. |
| [checkerboard_slices.py](patterns/checkerboard_slices.py) | Checkerboard slices. |
| [cross_slices.py](patterns/cross_slices.py) | Cross slices. |
| [opposite_quarters.py](patterns/opposite_quarters.py) | Opposite quarters. |
| [other_quarters.py](patterns/other_quarters.py) | Other quarters. |
| [letter_h.py](patterns/letter_h.py) | Letter h. |
| [letter_o.py](patterns/letter_o.py) | Letter o. |
| [main_diagonal_loop.py](patterns/main_diagonal_loop.py) | Main diagonal loop. |
| [main_diagonal_indices.py](patterns/main_diagonal_indices.py) | Main diagonal indices. |
| [secondary_diagonal.py](patterns/secondary_diagonal.py) | Secondary diagonal. |
| [letter_x.py](patterns/letter_x.py) | Letter x. |
| [frame_mask.py](patterns/frame_mask.py) | Frame mask. |
| [corners_mask.py](patterns/corners_mask.py) | Corners mask. |
| [cross_mask.py](patterns/cross_mask.py) | Cross mask. |
| [block_and_frame.py](patterns/block_and_frame.py) | Block and frame. |

Change one parameter, predict the result, then run the program. Diagonal examples
assume a square field. Shape-independent frame examples can also use rectangles.

## Practice solutions

Try the exercises in the chapter before opening the solutions. Each solution uses
the same display code and the exact approved pattern-building snippet.

| Exercise | File |
| --- | --- |
| 21 | [two walls](solutions/exercise_21_two_walls.py) |
| 22 | [two shelves](solutions/exercise_22_two_shelves.py) |
| 23 | [frame opening](solutions/exercise_23_frame_opening.py) |
| 24 | [inner frame](solutions/exercise_24_inner_frame.py) |
| 25 | [double frame](solutions/exercise_25_double_frame.py) |
| 26 | [window sill](solutions/exercise_26_window_sill.py) |
| 27 | [dotted line](solutions/exercise_27_dotted_line.py) |
| 28 | [opposite quarters](solutions/exercise_28_opposite_quarters.py) |
| 29 | [thick cross](solutions/exercise_29_thick_cross.py) |
| 30 | [staircase](solutions/exercise_30_staircase.py) |

Exercise 29 also has a [mask-based solution](solutions/exercise_29_thick_cross_mask.py).
Both versions produce the same three-cell-wide cross.

## Repeat the timing experiment

```bash
python benchmark_checkerboard.py
```

The benchmark uses NumPy and Python's standard library. It checks that both
algorithms agree, then reports the median milliseconds per pattern build from
five timed series. It measures clearing and filling preallocated arrays, excluding
allocation, correctness checks, console output, and drawing. Calibration chooses
enough repetitions for each algorithm. Allow a few seconds for it to finish.

The speed ratio depends on this task, the array size, and your computer.
It is not a general NumPy speedup and does not measure rendering speed or FPS.

## Previous module

[Module 5 - Scalars, vectors, and matrices](../module_05/)
