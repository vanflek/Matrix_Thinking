# Module 18 - Xonix: Connected Regions and Groups of Objects

Use Boolean layers to describe territory, a trail, the player and individual
enemies. Find connected regions by expanding a mask; select a region subject to
constraints; preserve object identity with a shared index across arrays.

## Requirements and launch

Checked with Python 3.13.7, NumPy 2.5.3 and Pygame 2.6.1.
From this folder:

```console
python -m pip install -r requirements.txt
python final/xonix.py
```

Every Python file is self-contained. The game needs no external artwork or data.
The illustrations are reading materials, not runtime assets.

## Controls and rules

- Hold exactly one arrow key to move the player. No arrows or multiple arrows
  stop the player. Enemies keep moving. Escape or window close exits.
- The field has 32 rows and 48 columns; the initial territory is its outer frame.
  The player starts at the middle of the top side.
- Outside territory, every player cell becomes part of the unfinished trail.
  Entering the old trail or an enemy meeting any trail cell restarts the level.
- Returning to territory commits the trail. If multiple free regions remain,
  capture one smallest region containing no enemies. Equal areas select the last
  candidate in row-major region discovery order. With no eligible region, or only
  one free region, only the completed line is committed.
- Regions use four-side connectivity. Enemies move diagonally, reflect at
  territory and cannot cross a corner with both side cells blocked. A reflected
  candidate is checked again; if still invalid, position is preserved.
- Enemies do not collide with each other. Separate layers retain their identity
  if their positions overlap.
- Capture at least 75% of the inner field, excluding the frame, to advance.
  Completed inner lines count; unfinished trail cells do not. A defeat preserves
  the level number; successful completion increments it before resetting.
- Enemy count follows the level, capped at the number of distinct inner cells.
  Starting positions are shuffled without replacement. Initial directions are
  (1, 1) in the base game; solution 27 varies them.
- Timing uses seconds: player interval 0.02, enemy-group interval 0.10. Separate
  accumulators are processed in groups: all due enemy steps, then all due player
  steps. This is not a chronological merge of the two schedules. Collision checks
  occur after each group step and each player step; restart exits the update and
  clears both accumulators.

## Data and responsibilities

The field shape is `(3 + enemy_count, rows, cols)`, with Boolean dtype:

| Layer | Meaning |
| --- | --- |
| 0 | Territory |
| 1 | Unfinished trail |
| 2 | Player |
| 3 + i | Enemy i |

`enemy_direction` has shape `(enemy_count, 2)`. Row i stores `(dy, dx)` for enemy i.
Coordinates are always `(row, column)` in matrix operations.

- `GameModel`: state and initial/reset positions.
- `InputController`: events and held arrow keys.
- `GameLogic`: movement, collisions, regions, capture and level rules.
- `GameView`: palette lookup, enlargement and a cached grid; does not mutate state.
- `GameApp`: frame timing, orchestration, display and shutdown.

## Folders and listing labels

- `steps/`: 13 consecutive complete iterations.
- `examples/`: two independent console experiments.
- `final/`: complete game, identical to Iteration 18.13.
- `solutions/`: five independent solutions to Exercises 26-30.
- `patches/`: 12 unified diffs between neighboring iterations.
- `assets/illustrations/`: 20 chapter figures with English artwork labels.

`iteration_18_04` means Iteration 4 in Module 18. `example_18_01` uses a separate
sequence. `solution_18_26` refers to Exercise 26. These are not page numbers.
The chapter may show an iteration as several changes inside specified classes;
its full runnable file is provided for comparison.

## Iterations

| File | Working behavior |
| --- | --- |
| `steps/iteration_18_01_skeleton.py` | Initial frame, player, grid and exit |
| `steps/iteration_18_02_movement_and_trail.py` | Arrow movement, unfinished trail and self-collision |
| `steps/iteration_18_03_region_search.py` | One region found by mask expansion; console check |
| `steps/iteration_18_04_area_capture.py` | All regions enumerated; smallest captured |
| `steps/iteration_18_05_one_enemy.py` | One enemy with its own update interval |
| `steps/iteration_18_06_enemy_reflection.py` | Reflection and blocked-corner checks |
| `steps/iteration_18_07_trail_collision.py` | Trail collisions from either moving side; common restart |
| `steps/iteration_18_08_safe_capture.py` | Capture excludes the region containing the enemy |
| `steps/iteration_18_09_levels.py` | 75% inner-area threshold and level progression |
| `steps/iteration_18_10_enemy_layers.py` | Separate enemy layers, distinct shuffled starts; only first enemy logic |
| `steps/iteration_18_11_independent_enemies.py` | Individual directions and movement; common checks still first-enemy only |
| `steps/iteration_18_12_group_checks.py` | All-enemy collision and eligible-region checks |
| `steps/iteration_18_13_complete_game.py` | Normal first-level startup; no prepared test scenes |

Early iterations intentionally implement only the features introduced so far.
Stages 3-4 and 6-12 include console checks before the playable window. Several
later checks start the window on level 3 so the enemy group is immediately visible.
The final file restores normal level-1 startup.

## Independent examples

- `examples/example_18_01_shuffle.py`: coordinate pairs, in-place row shuffle,
  and the returned None value.
- `examples/example_18_02_group_masks.py`: broadcasting, one overall result,
  one result per enemy, and a shared occupancy mask.

## Practice solutions

Each solution starts from a separate copy of the final game. They are not
cumulative stages. Solutions 26, 28 and 29 print prepared checks before opening
the base game. Solution 27 opens level 6; solution 30 shows the captured percentage.

- `solution_18_26_region_from_start.py`: choose the region seed explicitly.
- `solution_18_27_initial_directions.py`: cycle through four initial directions.
- `solution_18_28_count_collisions.py`: count colliding enemies, not occupied cells.
- `solution_18_29_capture_all_regions.py`: capture all eligible regions.
- `solution_18_30_captured_percent.py`: calculate inner-area percentage in logic,
  display its integer part in the window title; base level comparison unchanged.

All five files are in `solutions/`.

## Applying optional patches

Patches are text descriptions of changes, not Python scripts. Copy
`steps/iteration_18_01_skeleton.py` into a separate working folder as `xonix.py`.
From that folder apply the patches in order:

```console
git apply --check /absolute/path/to/module_18/patches/18_01_to_18_02.patch
git apply /absolute/path/to/module_18/patches/18_01_to_18_02.patch
```

Replace the example path with your actual location; quote paths containing spaces.
Continue through `18_12_to_18_13.patch`. No Git repository initialization is needed.
Git is needed only for these optional patches; complete iterations run without it.
Each applied result is checked byte-for-byte against the next iteration.
