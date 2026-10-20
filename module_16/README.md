# Module 16 - Matrix Invaders: Familiar Structure, New Rules

Build a second game with the five components introduced in Line Breaker:
GameModel, InputController, GameLogic, GameView and GameApp. Four binary layers
describe the player, the player's bullet, the enemy formation and the enemy bullet.
The array axes are `(layer, row, column)`.

## Requirements and launch

Use Python 3.13 with NumPy and Pygame. The programs were checked with Python
3.13.7, NumPy 2.5.3 and Pygame 2.6.1. From this folder, install dependencies:

```console
python -m pip install -r requirements.txt
```

Run the complete game:

```console
python final/matrix_invaders.py
```

Or start with the first complete iteration:

```console
python steps/iteration_16_01_skeleton.py
```

Every Python file is self-contained. No external images or data files are needed
at runtime. The files in `examples/` print results; game versions open a window.
The illustrations are reading materials, not game assets.

## Controls and rules

- Press an arrow key to move the player one cell. Movement wraps at all four edges.
  Holding a key does not continuously move the player; key repeat is not enabled.
- The controller accepts the first supported gameplay keypress in each frame.
  Escape and window close requests are still processed independently.
- Space fires one upward-moving bullet. A hit removes one enemy and the bullet.
  A missed bullet disappears at the top. Only one player bullet can be active.
- The formation moves horizontally, descends at a side boundary, and reverses.
  It never wraps. A descent and a horizontal move are separate formation steps.
- A descent attempts an enemy shot if no enemy bullet is active. The shooter is
  the middle candidate in the lowest occupied row, choosing the right middle
  entry when the candidate count is even. This is not a geometric-center rule.
- The enemy bullet moves downward with its own counter. It disappears at the
  bottom after the player collision check. Opposing bullets do not cancel.
- Player/enemy contact, an enemy bullet hit, or enemies reaching the bottom row
  ends the game and closes the window. Escape or the close button quits.
- Clearing a formation loads the next template, cycling through three patterns.
  Player position stays; bullets, direction and counters reset. A new formation
  overlapping the player ends the game immediately.
- Defeat takes priority over loading another wave. The base game has no final win.

Timing periods count update calls, not elapsed milliseconds. If actual FPS drops,
movement slows. A positive integer period is required; a larger period is slower.
Patterns must be nonempty 2D binary arrays that fit horizontally and end above
the bottom row when placed starting at row 1. Assertions check these contracts.

## Folders and numbering

- `steps/`: six consecutive, complete game iterations.
- `examples/`: two independent console experiments.
- `final/`: the complete game; its logic matches Iteration 16.06.
- `solutions/`: five independent solutions to Exercises 26-30.
- `patches/`: five unified diffs between adjacent iterations; see below.
- `assets/illustrations/`: seven chapter figures in PNG and editable SVG.
  Labels inside the figures are in English.

`example_16_02` means Example 2 in Module 16. `iteration_16_05` means Iteration 5
in Module 16. The sequences are independent; the numbers are not page numbers.
Short fragments printed in the chapter explain individual operations. Use the
complete iteration files to run each stage.

## Game iterations

| File | Working behavior |
| --- | --- |
| `steps/iteration_16_01_skeleton.py` | Player movement, shooting, stationary enemies and grid; no collision rules yet |
| `steps/iteration_16_02_enemy_movement.py` | Formation shifts, edge turns, frame counter and bottom-row defeat |
| `steps/iteration_16_03_bullet_collision.py` | Player bullet hits; collision checks after relevant moves |
| `steps/iteration_16_04_player_collision.py` | Immediate player/enemy contact checks |
| `steps/iteration_16_05_enemy_bullet.py` | Shooter selection, enemy fire and independent bullet timing |
| `steps/iteration_16_06_waves.py` | Three templates, checked placement and wave transitions |

Earlier iterations intentionally omit rules introduced later. In particular,
player/enemy contact starts in 16.04; enemy bullets start in 16.05; new waves
start in 16.06.

## Console examples

- `examples/example_16_01_shift_without_wrap.py`: cyclic and noncyclic shifts.
- `examples/example_16_02_choose_shooter.py`: row reduction, candidate selection
  and the empty-formation case.

## Practice solutions

Every solution starts from the unmodified final game. Run each separately:

- `solutions/solution_16_26_horizontal_player.py`: horizontal-only movement.
- `solutions/solution_16_27_leftmost_shooter.py`: leftmost shooter in the lowest row.
- `solutions/solution_16_28_triangle_pattern.py`: fourth template, a 25-enemy triangle.
- `solutions/solution_16_29_faster_waves.py`: periods 12, 10, 8, 6, 4, 3, 3, ...
- `solutions/solution_16_30_three_waves.py`: victory after three cleared waves;
  defeat has priority, and quitting is not victory.

## Applying the patches

The complete files in `steps/` are the simplest way to run a stage. Patches show
exact changes between neighboring iterations and are not Python programs.

All patches target a working file named `matrix_invaders.py`. To apply them with
Git, create a separate empty working folder, copy
`steps/iteration_16_01_skeleton.py` into it, and rename that copy to
`matrix_invaders.py`. From that folder, apply patches in numeric order:

```console
git apply --check /absolute/path/to/module_16/patches/16_01_to_16_02.patch
git apply /absolute/path/to/module_16/patches/16_01_to_16_02.patch
```

Replace the example absolute path with the actual location of the patch; quote
the path if it contains spaces. Repeat for 16.02 -> 16.03 through 16.05 -> 16.06.
No Git repository initialization is needed for these working-file patches.
Each resulting file was compared byte-for-byte with its target iteration.

The final game differs from Iteration 16.06 only in its window title and explanatory
comments. Its game logic is identical. Dependencies apply equally to all stages.


## File and listing names

`steps/iteration_MM_NN_name.py` contains runnable learning steps in chapter order.
`examples/example_MM_NN_name.py` contains independent experiments.
`solutions/solution_MM_TT_name.py` contains exercise solutions (TT is the exercise number).
`final/` contains complete programs, where provided. Listing identifiers match file stems;
these numbers are not PDF page numbers. Run each program separately.
