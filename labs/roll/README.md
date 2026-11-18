# Roll the whole world

A complete procedural Python example: one 10 × 10 NumPy array stores the entire
world. Arrow keys apply `np.roll` to the array. Values crossing an edge reappear
on the opposite edge. No classes, extra assets or hardware are required.

[Try the browser laboratory](https://matrixthinking.org/roll.html).

## Run

Download this folder or the [complete ZIP](https://matrixthinking.org/roll-example.zip).
Open it in PyCharm and select the Python interpreter for the project. In its terminal:

```sh
python -m pip install -r requirements.txt
python roll_numpy.py
```

The program opens a Pygame window with a picture and the same matrix as numbers.
Click that window before using the keyboard.

| Control | Action |
| --- | --- |
| Arrow keys | Roll the entire matrix by one cell |
| Space | Load the duck |
| C | Load one cell at row 4, column 4 |
| Left mouse button / drag | Paint 1 on the picture |
| Right mouse button / drag | Paint 0 on the picture |
| R | Restore the last loaded preset |
| Escape or close button | Exit |

Reset restores the one-cell or duck preset, not the last hand-drawn image.

## The transformation

```python
world = np.roll(world,  1, axis=1)  # right
world = np.roll(world, -1, axis=1)  # left
world = np.roll(world,  1, axis=0)  # down
world = np.roll(world, -1, axis=0)  # up
```

Each line is a separate example, not a sequence to run for one move.
Rows increase downward; columns increase to the right. `axis=0` shifts along rows,
`axis=1` along columns. The operation moves every value, including all the zeros.
It preserves the shape and the number of lit cells.

Try moving right ten times, or moving right and then left. Both restore the original
matrix. With a duck or your own drawing, the same line of movement code still works.
An image can split across the display edges: the world wraps, rather than clipping.

The Python movement uses real NumPy. The browser demonstrates the same operation
in JavaScript. Drawing/input adapters visit individual cells; world movement is
expressed as a whole-array operation in the Python program.

Reference: [NumPy roll documentation](https://numpy.org/doc/stable/reference/generated/numpy.roll.html).
Program code is covered by the repository's [MIT license](../../LICENSE).
