# Module 3 - Conditions, Branches, and while Loops

Companion programs for **Matrix Thinking**. A row number selects a displacement, a cell address selects a color, a Boolean flag saves a decision, and a changing counter controls repetition.

## Start here

| Program | What it shows |
| --- | --- |
| [brick_wall.py](brick_wall.py) | Odd-numbered rows start half a cell to the left. |
| [chessboard.py](chessboard.py) | The parity of `row + col` selects a color. |
| [framed_chessboard.py](framed_chessboard.py) | An `if` / `elif` chain detects border cells; a nested branch colors the interior. |
| [framed_chessboard_flag.py](framed_chessboard_flag.py) | `enumerate` provides indices and coordinates; `is_border` stores a Boolean result. |
| [while_counter.py](while_counter.py) | A console-only counter shows how `while` checks its condition before each repetition. |
| [framed_chessboard_while.py](framed_chessboard_while.py) | The final chapter program: draw once, then service the window during a waiting loop. |

The five graphical examples match the complete listings in the chapter. `while_counter.py` matches the short console example after introducing `+=`.

## Run a program

Checked with **Python 3.13.7** and **Pygame 2.6.1** on Windows. NumPy is not needed here.

```shell
python -m pip install -r requirements.txt
python brick_wall.py
```

Run each file on its own, including from PyCharm. The early graphical examples request a 5000 ms pause. The final example requests 300 pauses of 16 ms each, totaling 4800 ms. Actual elapsed time can be longer. Each program closes automatically when its pause or waiting loop ends; these examples do not yet implement a response to the close button. `pg.event.pump()` services internal events but does not implement that response.

## Trace the data

- `%` computes a remainder; `==` compares values and produces a Boolean result.
- `=` assigns a value. A comparison does not change the value being compared.
- An `if` / `elif` / `else` chain selects its first matching branch. Separate `if` statements perform separate checks.
- `(row, col)` is a cell address. `(x, y)` is its pixel position. An RGB tuple is a color vector.
- Reset `is_border` for every new cell, but initialize `steps` only once before its loop.
- A waiting-loop iteration is not an animation frame: drawing and display update happen before the loop.

Predict each result before running a program. Change one rule or parameter at a time, then use `print` to inspect intermediate values.

## Practical solutions

Start each exercise from the original program specified in the chapter. Each solution below is a complete standalone program.

| Exercise | File |
| --- | --- |
| 8. Shift the even rows | [Inverted row selection](solutions/exercise_08_inverted_rows.py) |
| 8. Remove all row shifts | [No shift](solutions/exercise_08_no_shift.py) |
| 9. Use 80-by-30 brick cells | [Smaller bricks](solutions/exercise_09_smaller_bricks.py) |
| 10. Create a 6-by-10 interior with 60-pixel cells | [Rectangular board](solutions/exercise_10_rectangular_board.py) |
| 11. Select three different insets | [Three insets](solutions/exercise_11_three_insets.py) |
| 12. Restore the flag reset for each cell | [Correct flag placement](solutions/exercise_12_flag_reset.py) |
| 13. Move the increment into the loop | [Correct counter indentation](solutions/exercise_13_counter_fixed.py) |
| 14. Request 125 pauses of 16 ms | [16 ms pauses](solutions/exercise_14_wait_16.py) |
| 14. Request 250 pauses of 8 ms | [8 ms pauses](solutions/exercise_14_wait_8.py) |

For example:

```shell
python solutions/exercise_11_three_insets.py
```

Exercise 12 deliberately moves the reset to an incorrect location before restoring it; the linked file contains the corrected version. The faulty infinite loop from exercise 13 is discussed in the chapter without running it; only the corrected version is included here. Questions 1-7 and their explanations are in the chapter.

## Continue learning

- [Previous module](../module_02/)
- [Pygame drawing functions](https://www.pygame.org/docs/ref/draw.html)
- [Pygame time functions](https://www.pygame.org/docs/ref/time.html)
