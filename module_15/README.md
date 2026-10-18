# Module 15 - Classes: Bringing Data and Actions Together

Build Line Breaker with five cooperating classes: GameModel, InputController,
GameLogic, GameView and GameApp. The world is stored in three binary layers;
methods apply movement, bullet placement, falling blocks and row clearing.

## Requirements and launch

Use Python 3.13 with NumPy and Pygame. From this folder, install dependencies:

```console
python -m pip install -r requirements.txt
```

Start with `steps/iteration_15_01_skeleton.py`, or run the complete game:

```console
python final/line_breaker.py
```

Each Python file is self-contained. No image or data files are needed at runtime.
The examples print results in the console; game versions open a Pygame window.

## Controls and rules

- Arrow key presses move the player one cell. Movement wraps at all four edges.
  Holding a key does not continuously move the player; key repeat is not enabled.
- Space fires one upward-moving bullet. Only one bullet can be active.
- A hit adds a block immediately below the obstacle and clears the bullet.
- A bullet reaching the top becomes a block in the top row.
- Blocks descend periodically; a random binary row appears at the top.
- Complete rows disappear together. Rows above fall; empty rows appear at the top.
- Any player/block overlap ends the game and closes the window.
- Escape or the window close button quits.

The controller chooses the first supported gameplay keypress in a frame, while
still processing every close request. Bullets move each game step. Block timing
is measured in steps, so changing FPS changes elapsed-time movement speed.

## Folders and numbering

- `examples/`: seven independent console experiments.
- `steps/`: seven complete, consecutive game iterations.
- `final/`: the complete game; its logic matches Iteration 15.07.
- `solutions/`: five independent solutions to Exercises 26-30.
- `patches/`: six unified diffs between adjacent iterations. These are editing
  guides, not Python programs; use the complete target files in `steps/` to run.
- `assets/illustrations/`: chapter diagrams in PNG and editable SVG, with English
  labels. They explain the chapter and are not required by the programs.

`example_15_03` means Example 3 in Module 15; `iteration_15_06` means the sixth
complete game iteration in Module 15. The two sequences are independent and
are not page numbers. Every practice solution starts from the original final
game; do not combine changes from different exercises unless you intend to.

## Examples

- `examples/example_15_01_class_instances.py`
- `examples/example_15_02_self_and_init.py`
- `examples/example_15_03_default_arguments.py`
- `examples/example_15_04_elementwise_maximum.py`
- `examples/example_15_05_key_actions.py`
- `examples/example_15_06_layer_views.py`
- `examples/example_15_07_full_rows.py`

## Game iterations

- `steps/iteration_15_01_skeleton.py`
- `steps/iteration_15_02_player_movement.py`
- `steps/iteration_15_03_bullet_movement.py`
- `steps/iteration_15_04_falling_blocks.py`
- `steps/iteration_15_05_bullet_collision.py`
- `steps/iteration_15_06_full_rows.py`
- `steps/iteration_15_07_game_over.py`

## Practice solutions

- `solutions/solution_15_26_palette.py`
- `solutions/solution_15_27_horizontal.py`
- `solutions/solution_15_28_boundaries.py`
- `solutions/solution_15_29_score.py`
- `solutions/solution_15_30_field_size.py`
