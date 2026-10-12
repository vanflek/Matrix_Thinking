# Module 5 - Scalars, Vectors, and Matrices in NumPy and on Screen

The same data can appear as numbers in a NumPy array, text in the console, or colored cells in a Pygame window. This module connects those views.

## Run the examples

The files were checked with Python 3.13.7, NumPy 2.5.3, and Pygame 2.6.1. Use the Python interpreter selected for your project.

From this folder, install the dependencies:

```bash
python -m pip install -r requirements.txt
```

Start with the console example, then run the complete display program:

```bash
python first_matrix.py
python matrix_visualization.py
```

You can also open a file in PyCharm and run it. Each Python file is standalone. Close a Pygame window with its close button or press **Esc**. Console-only examples finish after printing their results.

## Main examples

| File | What to investigate |
| --- | --- |
| [first_matrix.py](first_matrix.py) | An 8 x 8 array of zeros and its console representation. |
| [matrix_visualization.py](matrix_visualization.py) | The complete chapter listing: an 8 x 8 matrix with four dark corners. |
| [array_shapes.py](array_shapes.py) | Why `(3,)` and `(1, 3)` describe different structures despite equal values. |
| [array_constructors.py](array_constructors.py) | Creation, template-based arrays, identity and diagonal matrices, and triangular regions. |

In `array_constructors.py`, every element created with `empty_like` is explicitly initialized before reading. Uninitialized memory is neither a blank field nor a random-number generator.

## Practice solutions

Try the exercises yourself before opening these files. Each solution prints its matrix and then displays it using the same drawing loop as the main program.

| Exercise | File | Pattern |
| --- | --- | --- |
| 21 | [Four corners](solutions/exercise_21_corners.py) | Four ones, selected with `0` and `-1`. |
| 22 | [Top row](solutions/exercise_22_top_row.py) | A constant row index and changing column index. |
| 23 | [Left column](solutions/exercise_23_left_column.py) | A changing row index and constant column index. |
| 24 | [Frame](solutions/exercise_24_frame.py) | Two rows and two columns. |
| 25 | [Main diagonal: loop](solutions/exercise_25_main_diagonal.py) | Equal row and column indices. |
| 25 | [Main diagonal: NumPy](solutions/exercise_25_main_diagonal_eye.py) | The same result from `np.eye`. |
| 26 | [Secondary diagonal](solutions/exercise_26_secondary_diagonal.py) | `col = COLS - 1 - row`. |
| 27 | [Letter L](solutions/exercise_27_letter_l.py) | The left column and bottom row. |
| 28 | [Letter T](solutions/exercise_28_letter_t.py) | The top row and column 3. |
| 29 | [Smiley](solutions/exercise_29_smiley.py) | A complete matrix created with `np.array`. |
| 30 | [Among Us character](solutions/exercise_30_among_us.py) | Another image described entirely by its values. |

For example:

```bash
python solutions/exercise_24_frame.py
```

Exercises 21-24 also work with a `(3, 5)` matrix: change only the shape in the creation line. Exercises 25-28 use the specified 8 x 8 field. For T, the middle lies between columns 3 and 4; the task deliberately chooses column 3.

## Further experiments from the chapter

- [Rectangular frame](experiments/rectangular_frame.py): the same frame algorithm on a 3 x 5 matrix.
- [Neutral face](experiments/neutral_face.py): four assignments change the smiley's mouth.
- [Wider visor](experiments/wider_visor.py): one assignment changes the character's visor.

The chapter also contains 20 conceptual self-check questions and their answers.

## Trace the data

- A cell value is a scalar. A row can be viewed as a vector. The complete table is a matrix.
- `matrix[row, col]` selects data; `x = col * CELL_SIZE` and `y = row * CELL_SIZE` locate its drawing.
- In this binary model, **0 is light and 1 is dark**. `uint8` itself can store integers from 0 to 255.
- `ROWS, COLS = matrix.shape` keeps window dimensions tied to the data.
- Changing `CELL_SIZE` or display colors changes the presentation without changing the matrix.
- Equality or comparison of indices describes diagonal and triangular patterns.
- The explicit drawing loops make the data-to-screen mapping visible. More efficient display methods come later.

## References

- [Previous module](../module_04/)
- [NumPy array creation routines](https://numpy.org/doc/stable/reference/routines.array-creation.html)
- [Pygame drawing](https://www.pygame.org/docs/ref/draw.html)
