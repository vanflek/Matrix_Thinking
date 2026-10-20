# Bonus game: three waves

Run from the module folder:

```console
python bonus/wireframe_three_levels.py
```

Use the same NumPy/Pygame requirements and controls as the final game.

| Wave | Enemies | Movement speed |
| --- | --- | --- |
| 1 | Two diagonal enemies | Normal |
| 2 | Four circular enemies | Normal |
| 3 | Two diagonal and four circular enemies | 1.25 times normal |

Each enemy awards 100 points. The score carries over, so clearing all three
waves gives 1200 points. Victory appears only after the final wave. Contact
with a surviving enemy ends the entire game, including on earlier waves.

Each wave has a 1.2-second ready pause. The airplane returns to its initial
position and heading, and old projectiles are cleared. During the pause the
world is frozen and fire presses are discarded; Escape/window close still work.
The transition follows the normal collision order: hits, surviving enemies
against the player, then wave completion. There is no restart key in this bonus.

`GameModel.levels` is a list of dictionaries. `level_index` starts at zero;
the HUD adds one for readers. Counts select prefixes of two predefined diagonal
and four circular configurations; supported counts are 0..2 and 0..4, respectively.
Keep at least one enemy per level. `speed_factor` scales travel speed, while
visual spin remains independent. Creating enemies is handled by
`GameLogic.start_level`; rendering and collision algorithms are reused.

Try the creative exercise before comparing this complete implementation.
The optional `patches/patch_21_final_to_three_levels.patch` applies to a copy of
the unmodified final game named `main.py`, not to a practical solution.
