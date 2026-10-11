# Module 2 - Building a World in One Frame with for Loops

Companion programs for **Matrix Thinking**. This module moves from repeated drawing commands to patterns described by data: lists of radii, regular sequences, rows and columns, and labels built from cell addresses.

## Start here

| Program | What it shows |
| --- | --- |
| [circles_list.py](circles_list.py) | Five circle outlines drawn by iterating over a list of radii. |
| [circles_range.py](circles_range.py) | The same picture using `range(200, 0, -40)`. |
| [brick_wall.py](brick_wall.py) | Nested loops build 15 rows of 8 bricks, with four-pixel gaps. |
| [brick_wall_labels.py](brick_wall_labels.py) | Cell addresses become strings, text surfaces, and visible labels. |
| [grid_enumerate.py](grid_enumerate.py) | `enumerate` supplies both an index and a coordinate for a 5-by-8 grid. |

The complete listings in the chapter match `circles_list.py`, `brick_wall.py`, and `grid_enumerate.py`. The other two files apply the short changes explained between those listings.

## Run a program

Checked with **Python 3.13.7** and **Pygame 2.6.1** on Windows. NumPy is not needed here.

```shell
python -m pip install -r requirements.txt
python circles_list.py
```

You can also open and run each file in PyCharm. The picture stays visible for about five seconds, then the program closes automatically. These early examples do not yet handle the close button during the pause.

## Try the experiments first

- Predict the result before changing one value.
- Add a radius to the list without changing the loop body.
- Compare the list with a positive or negative step in `range`. The stop boundary is excluded.
- Follow `row`, `col`, `x`, and `y` with `print`.
- Distinguish a cell address from its pixel position.
- Change `CELL` while keeping `ROWS` and `COLS` fixed: the number of cells stays the same.
- Remember that a visible grid does not automatically mean the program stores a two-dimensional container of cells.

## Example solutions

Each file below is a standalone program. Start each exercise from the original chapter program, rather than accumulating changes from earlier exercises.

| Exercise | File |
| --- | --- |
| 1. Radii with `range` | [circles_range.py](circles_range.py) |
| 2. Change one scalar | [Wider outlines](solutions/exercise_02_wider_outlines.py) |
| 3. Graph paper | [Two independent line loops](solutions/exercise_03_graph_paper.py) |
| 4. Resize the grid | [6 rows, 10 columns, 60-pixel cells](solutions/exercise_04_resize_grid.py) |
| 5. Labels outside the grid | [Row and column labels](solutions/exercise_05_edge_labels.py) |
| 6. Center a label | [Center each text surface](solutions/exercise_06_centered_labels.py) |
| 7. One index instead of two | [Linear cell indices](solutions/exercise_07_linear_indices.py) |
| 8. Observe the data | [Trace coordinates in the console](solutions/exercise_08_trace.py) |
| 17. One scalar changes the picture | [Smaller cells with fixed counts](solutions/exercise_17_smaller_cells.py) |
| 18. A collection of position vectors | [Three centers](solutions/exercise_18_centers.py) |
| 25. Shift several objects | [Add the same displacement](solutions/exercise_25_shift_centers.py) |

For example:

```shell
python solutions/exercise_05_edge_labels.py
```

The remaining exercises focus on tracing values and distinguishing meaning from storage: scalars, vectors, tuples, lists, sequences, and cell addresses. Their explanations and answers are in the chapter.

## Continue learning

- [Previous module](../module_01/)
- [Pygame drawing functions](https://www.pygame.org/docs/ref/draw.html)
- [Pygame font rendering](https://www.pygame.org/docs/ref/font.html)
