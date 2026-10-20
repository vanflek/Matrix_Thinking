# Module 21 - A Wireframe Game: One Class, Different Objects

Build a small airplane game with local geometry, independent object state,
heading-relative movement, projectiles, two enemy trajectories, approximate
collision regions, scoring, victory, and defeat. Five application classes keep
their established roles; `WireframeObject` is the shared domain object.

## Install and run

Checked with Python 3.13.7, NumPy 2.5.3, and Pygame 2.6.1.
From this folder:

```console
python -m pip install -r requirements.txt
python final/wireframe_game.py
```

NumPy and Pygame are the only runtime dependencies. Every Python file is
standalone. No external image or data file is needed. A system monospace font
is requested through Pygame, which provides a fallback when unavailable.
Figures in `assets/illustrations/` are reading materials, not runtime assets.

## Controls and rules

| Key | Action |
| --- | --- |
| W / S | Forward / backward relative to the airplane heading |
| A / D | Strafe left / right relative to the airplane heading |
| Left / Right arrow | Turn counterclockwise / clockwise |
| Space | Fire once per press |
| Escape or window close | Exit |

Use an English keyboard layout for letter controls. Movement and turning read
held keys; shooting uses KEYDOWN events without enabled key repeat. Several
Space events in the same frame are represented by one fire action.

Two enemies move diagonally and bounce; four move on one circle in opposing
directions. All enemies spin independently. Enemies do not collide with one
another. Each projectile can destroy at most one enemy, awarding 100 points.
Destroy all six for victory and 600 points. Contact with a surviving enemy
causes defeat. The world freezes after either outcome, while the window keeps
processing exit input and displaying the last state. Restart is added only in
exercise solution 29; H diagnostics only in solution 27.

## Data and coordinate conventions

- World X points right, Y up; world zero appears at the center of a 768 x 768
  window. One world unit equals one screen pixel. CELL_SIZE = 32 is grid spacing.
- Vertices are rows `[x, y, 1]`; edges contain pairs of vertex indices.
- `vertices @ (T @ R @ S).T` scales, rotates, then translates original vertices.
  Original local geometry is not overwritten. Vertex 1 is the airplane nose.
- `dx`, `dy` are world coordinates of the object's local origin. `angle` and
  `orbit_angle` are stored in degrees and converted using `np.deg2rad`.
- `angle` / `angular_speed` describe visual spin. `orbit_angle` / `orbit_speed`
  describe position on a trajectory; the two pairs are independent.
- `motion_type` is interpreted by enemy logic. Assigning it to a projectile
  does not route that projectile through the enemy update.
- Input direction is normalized before multiplying by speed and elapsed time.
  Diagonal enemies use velocity components directly; their speed is about 169.7.
- Geometry bounds and collision radii serve different purposes. Field margins
  use maximum scaled vertex distance plus line width. Chosen collision radii
  are player 21, projectile 9, enemy 34; they do not exactly enclose all shapes.
- Collision checks use current center positions. Fast movement can pass through
  a target between checks. Boundary bounces clamp overshoot rather than solving
  continuous time of impact. This is an intentionally simple discrete model.
- Projectile hits are resolved before player collisions. Only surviving enemies
  can cause defeat. A projectile selects the first matching enemy in list order;
  marked enemies cannot score twice during that update.

## Folders and listing identifiers

- `steps/`: complete runnable iterations in reading order.
- `examples/`: four independent console experiments.
- `solutions/`: five separate practical solutions, each starting from the final
  game. Do not apply them cumulatively.
- `final/`: complete game, identical to iteration 11.
- `patches/`: optional changes between steps and from the final game to solutions.
- `assets/illustrations/`: English diagrams and captures referenced in the chapter.

`iteration_21_04` means module 21, iteration 04, not a page number.
`example_21_04` is an independent sequence. `solution_21_26` answers exercise 26.
Partial code blocks in the chapter show edits inside an existing runnable file;
the files here contain the complete program for each finished step.

## Runnable iterations

| File | Visible result |
| --- | --- |
| `steps/iteration_21_01_skeleton.py` | Airplane and grid; five-class skeleton |
| `steps/iteration_21_02_wireframe_object.py` | Same view; geometry encapsulated per object |
| `steps/iteration_21_03_second_object.py` | A separate triangle with its own transform |
| `steps/iteration_21_04_movement.py` | Heading-relative movement and normalized input |
| `steps/iteration_21_05_field_bounds.py` | Entire airplane stays within the field |
| `steps/iteration_21_06_shooting.py` | Independent projectiles; off-field cleanup |
| `steps/iteration_21_07_rotating_enemies.py` | Smaller airplane and six spinning enemies |
| `steps/iteration_21_08_diagonal_motion.py` | Two enemies move and bounce; four spin in place |
| `steps/iteration_21_09_circular_motion.py` | Four enemies move on a shared circle |
| `steps/iteration_21_10_projectile_collisions.py` | Hits remove objects and add score |
| `steps/iteration_21_11_game_end.py` | Defeat, victory, and frozen end states |

## Independent examples

| File | Topic |
| --- | --- |
| `examples/example_21_01_hypot.py` | Vector length and normalization |
| `examples/example_21_02_clip.py` | Restrict a value to an interval |
| `examples/example_21_03_list_unpacking.py` | Unpack two lists into one |
| `examples/example_21_04_list_comprehension.py` | Filter with a loop and a comprehension |

## Practical solutions

| File | Change and expected result |
| --- | --- |
| `solutions/solution_21_26_diamond.py` | Six diamond enemies; unchanged behavior |
| `solutions/solution_21_27_collision_areas.py` | H toggles regions, including after game end |
| `solutions/solution_21_28_rewards.py` | 150 per diagonal enemy, 100 per circular; total 700 |
| `solutions/solution_21_29_restart.py` | R restarts and reconnects logic and view to new model |
| `solutions/solution_21_30_oscillation.py` | One circular enemy oscillates horizontally |

In solution 29, restart suppresses same-frame fire and uses zero elapsed time for
the first update of the new model. Grid, fonts, view, window, and controller are
reused. Solution 30 keeps six enemies and retains the normal 600-point total.

## Creative extension: three waves

`bonus/wireframe_three_levels.py` implements the chapter's additional creative
exercise. Run it after trying your own solution. Waves contain 2, 4, and 6
enemies; the final mixed wave moves 25% faster. Score carries over (1200 total).
Each wave resets the airplane and projectiles and shows a short ready pause.
Full rules and configuration notes are in `bonus/README.md`.

The main final program remains the six-enemy, 600-point version used throughout
the step-by-step chapter. The bonus patch starts independently from that final.

## Optional patches

You can simply run the complete step files. To inspect or apply a patch, work on
a copy named `main.py` in a scratch directory. Each patch uses `a/main.py` and
`b/main.py` headers and applies with `git apply` from that directory.

For example, copy iteration 01 to `main.py`, then apply
`patch_21_01_to_02.patch` to get iteration 02. Continue in numeric order.
`patch_21_final_to_solution_26.patch` starts from the unmodified final game,
as do the other four solution patches. Do not apply them one after another.

```console
git apply --check path/to/patch_21_01_to_02.patch
git apply path/to/patch_21_01_to_02.patch
python main.py
```

## Verification

All complete files were launched with Python 3.13.7 and Pygame's dummy SDL driver.
Additional checks cover geometry, movement, bounds, both trajectories, tangent
contact and near misses, multiple projectiles and enemies, scoring, update order,
frozen outcomes, diagnostics, restart references, and oscillation checkpoints.
These are automated startup, rendering, and behavior checks, not a claim of a
complete manual playthrough. The chapter's final listing matches the final file.


## File and listing names

`steps/iteration_MM_NN_name.py` contains runnable learning steps in chapter order.
`examples/example_MM_NN_name.py` contains independent experiments.
`solutions/solution_MM_TT_name.py` contains exercise solutions (TT is the exercise number).
`final/` contains complete programs, where provided. Listing identifiers match file stems;
these numbers are not PDF page numbers. Run each program separately.

`bonus/` contains the optional three-level extension.
