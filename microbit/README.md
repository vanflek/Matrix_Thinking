# Matrix Thinking for micro:bit

Small experiments in which a matrix describes a whole display and one rule changes every cell. Both tracks use the same initial data, predictions and observable outcomes.

## Start here: brightness of the whole world

The matrix stores 25 brightness values, arranged in five rows:

```text
0 1 2 3 4
1 2 3 4 5
2 3 4 5 6
3 4 5 6 7
4 5 6 7 8
```

- **A:** subtract one from every cell, keeping values at or above zero.
- **B:** add one to every cell, keeping values at or below nine.
- **Shake:** restore the initial matrix, including its different brightness levels.

Predict a cell, then a row, then the whole next matrix before pressing a button. Zero-valued cells also increase. Saturation loses differences: after values reach nine, subtracting again does not necessarily recover their earlier values. Shaking restores the saved starting state.

| Track | Ready-to-open project | Text source |
| --- | --- | --- |
| MicroPython | Open the `.py` file in the [Python Editor](https://python.microbit.org/) | [Brightness](micropython/02_brightness_world.py) |
| MakeCode Blocks | [Download brightness HEX](makecode/02_brightness_world_makecode.hex?raw=1), then **Import → Import File** in [MakeCode](https://makecode.microbit.org/) | [TypeScript source](makecode/02_brightness_world_makecode.ts) |

MicroPython uses an `Image`. MakeCode stores the logical matrix as 25 numbers in row order and maps 0–9 to the LED API's 0–255 range when drawing. Both implementations transparently loop over the stored values; they do not require or claim native NumPy vectorization. Text and data, rather than the display's global brightness setting, define the world's state.

## Next experiment: shift the whole world

**A** shifts the matrix down by one row; **B** restores it. New top-row values are zero and values crossing the bottom edge disappear. The five stored rows represent one world, not five animation frames.

- [MicroPython source](micropython/01_shift_world.py)
- [MakeCode Blocks HEX](makecode/01_shift_world_makecode.hex?raw=1)
- [MakeCode TypeScript source](makecode/01_shift_world_makecode.ts)
- [Russian block-building instructions](teacher-notes/makecode_blocks_ru.txt)

## Third experiment: mirror the whole world

Start with an asymmetric L-shaped matrix. **A** reflects left to right, **B** reflects top to bottom, and **shake** restores the starting picture.

```text
9 0 0 0 0
9 0 0 0 0
9 0 0 0 0
9 9 9 9 0
0 0 0 0 0
```

Predict the destination of one value, then a row, then the whole picture. Press A twice or B twice and explain why the picture returns. Compare A then B with B then A. Reflections preserve every brightness value; unlike clipping or shifting past an edge, they do not lose information. One reflection in each direction produces a 180-degree turn.

- [MicroPython program](micropython/03_mirror_world.py)
- [MakeCode Blocks HEX](makecode/03_mirror_world_makecode.hex?raw=1)
- [MakeCode TypeScript source](makecode/03_mirror_world_makecode.ts)
- [Open in MakeCode](https://makecode.microbit.org/#pub:github:vanflek/matrix-thinking-microbit-mirror)
- [Teacher notes in Russian](teacher-notes/mirror_ru.txt)
- [Validation record](teacher-notes/mirror_verification.json)

The implementations build a new matrix from the old matrix before drawing. MicroPython's image helper and MakeCode's array helper use explicit loops; this is not native NumPy vectorization.

## Teacher notes and validation

- [Brightness activity in Russian](teacher-notes/brightness_ru.txt)
- [Brightness validation record](teacher-notes/brightness_verification.json)
- [Shift validation record](teacher-notes/shift_verification.json)

MakeCode projects were converted to ordinary editable blocks and checked in the official simulator: input buttons, boundaries and reset. MicroPython logic was checked on desktop with an API adapter. Neither track has been tested on a physical board yet. MakeCode Python and MicroPython are different environments; the files are not interchangeable.

From the repository root, run the desktop checks in this order:

```sh
python microbit/tests/check_shift.py
node microbit/tests/check_makecode.cjs
python microbit/tests/check_brightness.py
node microbit/tests/check_brightness_makecode.cjs
python microbit/tests/check_mirror.py
node microbit/tests/check_mirror_makecode.cjs
```

These tests compare behavior and display mapping; they are not firmware tests.

## Saving changes

This directory is the shared source-and-export archive for the two tracks. A downloaded HEX contains a MakeCode project and can be imported into the editor. Saving a project in MakeCode or saving files on a computer does not automatically update this directory: revised sources and exports must be committed to GitHub.

All three MakeCode editor projects are connected to their own GitHub repositories:

- [Brightness matrix](https://github.com/vanflek/matrix-thinking-microbit-brightness)
- [Shift the whole world](https://github.com/vanflek/matrix-thinking-microbit-shift)
- [Mirror the whole world](https://github.com/vanflek/matrix-thinking-microbit-mirror)

In a connected project, click the GitHub button, review the changes, enter a short message, and choose **Commit & push**. Use **Pull changes** to retrieve edits made on GitHub. Ordinary editor or cloud saving is not a GitHub commit.

These repositories contain editable MakeCode blocks and generated TypeScript. This directory remains the shared archive for MakeCode exports, MicroPython sources and teacher notes; it is not automatically updated by commits in the separate MakeCode repositories. Copy revised sources and exports here when updating the shared lesson package. The book repository root and website branch remain independent.
