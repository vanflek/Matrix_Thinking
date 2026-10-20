# Module 17 - Tetris: Shape, Position and Transformations

Represent a figure by its shape matrix, position coordinates and rotation index.
Use the familiar GameModel, InputController, GameLogic, GameView and GameApp
components, plus a Tetromino class for each moving figure. The field array has
axes `(layer, row, column)`, with a fixed layer and an active layer. Values 1-7
are palette indices; 0 denotes an empty cell.

## Requirements and launch

The materials were checked with Python 3.13.7, NumPy 2.5.3 and Pygame 2.6.1.
From this folder, install the runtime dependencies:

```console
python -m pip install -r requirements.txt
python final/tetris.py
```

Every Python file is self-contained. The game needs no external images, fonts
or data files: Pygame selects an available system font. Chapter illustrations
are reading materials and are not loaded by the game.

To start from the skeleton:

```console
python steps/iteration_17_01_skeleton.py
```

## Controls and rules

- Left / Right: one cell per keypress. Up: rotate 90 degrees counterclockwise.
  Key repeat is not enabled. Different action flags in one update are applied
  in the order left, right, rotation; repeated events of one type share one flag.
- Hold Down to use the fast falling interval (0.06 s instead of 0.50 s).
  Timing uses elapsed seconds, not a count of rendered frames. Changing either
  falling mode resets its waiting timer; after locking, a new figure also starts
  with a fresh timer.
- Escape or the window close button exits. The final game has no Space action.
- Pieces contain four occupied cells. Shapes are chosen independently at random;
  the same shape can appear repeatedly.
- Rotation preserves the top-left anchor `(x, y)` of the current matrix bounding
  rectangle. It does not preserve a separate geometric pivot. There are no wall
  kicks. A move or turn outside the field or overlapping fixed cells is rejected.
- A failed timed downward step locks the figure. Only occupied cells are copied
  to the fixed layer. Complete rows are removed together; empty rows appear at
  the top and retained rows preserve their relative order.
- Clearing n rows at once awards `100 * n * n` points.
- A new figure is checked after row removal. If its occupied cells overlap fixed
  blocks, the active layer is cleared and GAME OVER appears. The window stays
  open and still accepts exit commands.

The base game deliberately omits pause, restart and a landing shadow. Independent
practice solutions implement these features below.

## Folders and listing labels

- `steps/`: ten consecutive complete iterations.
- `examples/`: seven independent experiments; some print results only, while
  others also open a prepared game window.
- `final/`: the complete game, identical to Iteration 17.10.
- `solutions/`: five independent solutions to Exercises 26-30.
- `patches/`: nine unified diffs between adjacent iterations.
- `assets/illustrations/`: ten PNG figures and three editable SVG diagrams.
  All labels inside the artwork are in English.

`iteration_17_04` means Iteration 4 in Module 17. `example_17_03` means Example 3
in this module. These sequences are independent and are not page numbers.
`solution_17_28` is the solution to Exercise 28. A listing caption can identify
the iteration being edited while the chapter shows the changes in several
smaller fragments. Those fragments belong inside the stated class or method;
complete runnable files are provided here for comparison.

## Iterations

| File | Working behavior |
| --- | --- |
| `steps/iteration_17_01_skeleton.py` | Empty two-layer field, grid and exit controls |
| `steps/iteration_17_02_tetromino.py` | Shape catalog and Tetromino class; window still empty |
| `steps/iteration_17_03_first_figure.py` | A T-shaped figure appears in the active layer |
| `steps/iteration_17_04_movement.py` | Manual arrows, rotation and all field boundaries |
| `steps/iteration_17_05_locking.py` | Temporary Space command locks a figure and creates the next |
| `steps/iteration_17_06_collisions.py` | Candidate layer, overlap checks and rollback |
| `steps/iteration_17_07_falling.py` | Elapsed-time gravity, held Down acceleration; Space removed |
| `steps/iteration_17_08_clear_rows.py` | Full-row removal and score |
| `steps/iteration_17_09_game_over.py` | Checked spawning, frozen game state and GAME OVER overlay |
| `steps/iteration_17_10_complete.py` | Explicit axis permutation with transpose and English comments |

Earlier iterations intentionally omit later rules. Before 17.06, figures can
cross fixed blocks. Before 17.09, the new figure's starting placement is not
checked for game-over conditions. Use the complete game for normal play.

## Independent examples

| File | Purpose |
| --- | --- |
| `examples/example_17_01_tetromino.py` | Coordinates, rotation index and resulting shape |
| `examples/example_17_02_locking_mask.py` | Whole-rectangle copying versus occupied-cell copying |
| `examples/example_17_03_overlap.py` | Elementwise products and a single overlap decision |
| `examples/example_17_04_elapsed_time.py` | Known time intervals and the observed downward step |
| `examples/example_17_05_clear_rows.py` | Prepared rows, preserved cell position and score |
| `examples/example_17_06_game_over.py` | A blocked spawning region and the final overlay |
| `examples/example_17_07_transpose_axes.py` | RGB array shapes and coordinate correspondence |

## Practice solutions

Each solution starts from a separate copy of the unmodified final game. Run them
independently; they are not consecutive stages or cumulative patches.

- `solutions/solution_17_26_clockwise.py`: clockwise rotation.
- `solutions/solution_17_27_field_stats.py`: count fixed occupied cells in the title.
- `solutions/solution_17_28_pause.py`: P toggles pause; paused time is not added to
  the falling timer, and exit controls remain active.
- `solutions/solution_17_29_restart.py`: R starts a fresh game after GAME OVER,
  resetting both model state and the logic's falling timer.
- `solutions/solution_17_30_shadow.py`: a gray landing shadow computed using an
  independent probe figure; accepted state, score and time remain unchanged.

## Applying patches

Patches show the exact changes between neighboring complete iterations. They
are not Python programs. All nine patches target a working file named `tetris.py`.

Create a separate working folder, copy `steps/iteration_17_01_skeleton.py` into
it, and rename that copy to `tetris.py`. From that folder, apply patches in order:

```console
git apply --check /absolute/path/to/module_17/patches/17_01_to_17_02.patch
git apply /absolute/path/to/module_17/patches/17_01_to_17_02.patch
```

Replace the example path with your actual patch location; quote paths containing
spaces. Continue through `17_09_to_17_10.patch`. Git is only needed to apply these
optional patches; all complete stages can be run directly without it. No Git
repository initialization is required in the working folder. Each applied result
was verified byte-for-byte against its target iteration.


## File and listing names

`steps/iteration_MM_NN_name.py` contains runnable learning steps in chapter order.
`examples/example_MM_NN_name.py` contains independent experiments.
`solutions/solution_MM_TT_name.py` contains exercise solutions (TT is the exercise number).
`final/` contains complete programs, where provided. Listing identifiers match file stems;
these numbers are not PDF page numbers. Run each program separately.
