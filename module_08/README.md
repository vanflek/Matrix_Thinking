# Module 8 - Functions: Organizing Actions on Data

Build **Collector**, a small game in which a moving cell visits every target.
Vectors describe position and direction, a matrix stores target coordinates,
and a dictionary groups the game state. Functions describe actions on that data.
The display uses palette indexing, repetition along spatial axes, and an axis
swap to convert the matrix into a Pygame surface.

## Run the game

Checked with Python 3.13.7, NumPy 2.5.3, and Pygame 2.6.1.
Open a terminal in this module's folder and use the same interpreter for both:

```bash
python -m pip install -r requirements.txt
python collector.py
```

In PyCharm, select the interpreter with these packages and run the chosen file.
Every script is standalone; no saved images or other data files are required.

## Chapter versions

| File | Purpose |
| --- | --- |
| [collector_every_frame.py](collector_every_frame.py) | First complete program: one movement step per rendered frame. Deliberately fast; run this version before introducing the step counter. |
| [collector.py](collector.py) | Final chapter program: one step every `STEP_FRAMES` frames, with input and rendering handled every frame. |

Both versions use the chapter's functions and calculations. English comments
explain their roles. These are complete files, so you can run either directly.

## Controls and rules

| Control | Action |
| --- | --- |
| Arrow keys | Change direction; the player keeps moving after the key is released. |
| Esc or window close | Exit, including after victory. |

The player starts moving right. Crossing an edge wraps to the opposite edge.
Red cells are targets; the player is blue. A target disappears when the player
visits its cell. After the last target, movement stops and the window title
announces victory. The window stays open until you close it.

At the nominal 60 FPS, `STEP_FRAMES = 6` gives ten steps per second.
This is frame counting, not elapsed-time movement: a lower actual frame rate
also slows the game. `clock.tick(FPS)` sets an upper limit, not a guaranteed rate.

## Small experiments in chapter order

These scripts print results and finish. Predict the output before running them.

| File | Topic |
| --- | --- |
| [functions.py](examples/functions.py) | Parameters, arguments, returned sizes, and local variables. |
| [array_changes.py](examples/array_changes.py) | Changing array elements versus rebinding a name; a function returning `None`. |
| [state_and_targets.py](examples/state_and_targets.py) | A dictionary containing vectors and a coordinate matrix; movement and collection. |
| [axes.py](examples/axes.py) | Index positions, `shape`, deletion, repetition, and swapping axes. |
| [palette_and_image.py](examples/palette_and_image.py) | Repeated color indices, RGB array shapes, and preparation of a Surface without opening a window. |

For example:

```bash
python examples/axes.py
```

## Practice solutions

Try the chapter exercises first. These are **independent complete versions** of
`collector.py`, not cumulative additions. Each can be run directly.

| Exercise | File | Change |
| --- | --- | --- |
| 26 | [eight targets](solutions/exercise_26_eight_targets.py) | Eight target coordinates on the original 16 by 16 field. |
| 27 | [rectangular field](solutions/exercise_27_rectangular_field.py) | Ten rows, eighteen columns, and 30-pixel cells. |
| 28 | [dark palette](solutions/exercise_28_dark_palette.py) | Change appearance while keeping the game state and rules. |
| 29 | [pause](solutions/exercise_29_pause.py) | Space toggles pause. The step counter and position freeze; arrows are ignored while paused. Events retain their order within each frame. |
| 30 | [restart](solutions/exercise_30_restart.py) | After victory, R creates fresh state and resets the counter. R has no effect before victory. This version does not include pause. |

For example:

```bash
python solutions/exercise_29_pause.py
```

## Previous module

[Module 7 - Palette and matrix](../module_07/)
