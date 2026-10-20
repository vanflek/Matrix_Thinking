# Module 6 - Slices and Masks: Patterns in the Language of Matrices

Choose whole groups of cells, describe patterns through indices and conditions,
and compare different ways of producing the same matrix.

## Run an example

These files were checked with Python 3.13.7, NumPy 2.5.3, and Pygame 2.6.1.
Use the same interpreter for installation and execution:

```bash
python -m pip install -r requirements.txt
python examples/example_06_01_matrix_visualization.py
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
| [examples/example_06_34_slices_1d.py](examples/example_06_34_slices_1d.py) | Start, exclusive stop, step, omitted bounds, and negative indices. |
| [examples/example_06_35_slices_2d.py](examples/example_06_35_slices_2d.py) | Rows, columns, rectangles, and assigning to a selection. |
| [examples/example_06_06_paired_indices_vs_slices.py](examples/example_06_06_paired_indices_vs_slices.py) | Three index pairs versus nine intersections. |
| [examples/example_06_33_scalar_logic.py](examples/example_06_33_scalar_logic.py) | `and`, `or`, and `not`, including the game-door example. |
| [examples/example_06_05_mask_values.py](examples/example_06_05_mask_values.py) | Build a mask, read selected values, write through it, and recompute it. |
| [examples/example_06_03_index_matrices.py](examples/example_06_03_index_matrices.py) | Store row and column indices as data. |
| [examples/example_06_04_mask_operations.py](examples/example_06_04_mask_operations.py) | Union, intersection, and complement of Boolean masks. |

## Patterns in a Pygame window

Each file prints its matrix and displays it. **0 is light; 1 is dark.**
The pattern is built once before the display loop. A smaller piece of NumPy code
does not remove the loops that draw the individual cells.

| File | Pattern |
| --- | --- |
| [examples/example_06_32_vertical_stripes.py](examples/example_06_32_vertical_stripes.py) | Vertical stripes. |
| [examples/example_06_29_shifted_vertical_stripes.py](examples/example_06_29_shifted_vertical_stripes.py) | Shifted vertical stripes. |
| [examples/example_06_18_horizontal_stripes.py](examples/example_06_18_horizontal_stripes.py) | Horizontal stripes. |
| [examples/example_06_15_four_corners.py](examples/example_06_15_four_corners.py) | Four corners. |
| [examples/example_06_17_frame_slices.py](examples/example_06_17_frame_slices.py) | Frame slices. |
| [examples/example_06_30_thick_frame.py](examples/example_06_30_thick_frame.py) | Thick frame. |
| [examples/example_06_19_left_half.py](examples/example_06_19_left_half.py) | Left half. |
| [examples/example_06_27_right_half.py](examples/example_06_27_right_half.py) | Right half. |
| [examples/example_06_31_top_half.py](examples/example_06_31_top_half.py) | Top half. |
| [examples/example_06_08_bottom_half.py](examples/example_06_08_bottom_half.py) | Bottom half. |
| [examples/example_06_09_centered_square.py](examples/example_06_09_centered_square.py) | Centered square. |
| [examples/example_06_10_checkerboard_loops.py](examples/example_06_10_checkerboard_loops.py) | Checkerboard loops. |
| [examples/example_06_11_checkerboard_slices.py](examples/example_06_11_checkerboard_slices.py) | Checkerboard slices. |
| [examples/example_06_14_cross_slices.py](examples/example_06_14_cross_slices.py) | Cross slices. |
| [examples/example_06_25_opposite_quarters.py](examples/example_06_25_opposite_quarters.py) | Opposite quarters. |
| [examples/example_06_26_other_quarters.py](examples/example_06_26_other_quarters.py) | Other quarters. |
| [examples/example_06_20_letter_h.py](examples/example_06_20_letter_h.py) | Letter h. |
| [examples/example_06_21_letter_o.py](examples/example_06_21_letter_o.py) | Letter o. |
| [examples/example_06_24_main_diagonal_loop.py](examples/example_06_24_main_diagonal_loop.py) | Main diagonal loop. |
| [examples/example_06_23_main_diagonal_indices.py](examples/example_06_23_main_diagonal_indices.py) | Main diagonal indices. |
| [examples/example_06_28_secondary_diagonal.py](examples/example_06_28_secondary_diagonal.py) | Secondary diagonal. |
| [examples/example_06_22_letter_x.py](examples/example_06_22_letter_x.py) | Letter x. |
| [examples/example_06_16_frame_mask.py](examples/example_06_16_frame_mask.py) | Frame mask. |
| [examples/example_06_12_corners_mask.py](examples/example_06_12_corners_mask.py) | Corners mask. |
| [examples/example_06_13_cross_mask.py](examples/example_06_13_cross_mask.py) | Cross mask. |
| [examples/example_06_07_block_and_frame.py](examples/example_06_07_block_and_frame.py) | Block and frame. |

Change one parameter, predict the result, then run the program. Diagonal examples
assume a square field. Shape-independent frame examples can also use rectangles.

## Practice solutions

Try the exercises in the chapter before opening the solutions. Each solution uses
the same display code and the exact approved pattern-building snippet.

| Exercise | File |
| --- | --- |
| 21 | [two walls](solutions/solution_06_21_two_walls.py) |
| 22 | [two shelves](solutions/solution_06_22_two_shelves.py) |
| 23 | [frame opening](solutions/solution_06_23_frame_opening.py) |
| 24 | [inner frame](solutions/solution_06_24_inner_frame.py) |
| 25 | [double frame](solutions/solution_06_25_double_frame.py) |
| 26 | [window sill](solutions/solution_06_26_window_sill.py) |
| 27 | [dotted line](solutions/solution_06_27_dotted_line.py) |
| 28 | [opposite quarters](solutions/solution_06_28_opposite_quarters.py) |
| 29 | [thick cross](solutions/solution_06_29_thick_cross.py) |
| 30 | [staircase](solutions/solution_06_30_staircase.py) |

Exercise 29 also has a [mask-based solution](solutions/solution_06_29_thick_cross_mask.py).
Both versions produce the same three-cell-wide cross.

## Repeat the timing experiment

```bash
python examples/example_06_02_benchmark_checkerboard.py
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


## File and listing names

`steps/iteration_MM_NN_name.py` contains runnable learning steps in chapter order.
`examples/example_MM_NN_name.py` contains independent experiments.
`solutions/solution_MM_TT_name.py` contains exercise solutions (TT is the exercise number).
`final/` contains complete programs, where provided. Listing identifiers match file stems;
these numbers are not PDF page numbers. Run each program separately.
