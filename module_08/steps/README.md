# Module 8 - Runnable steps

Run one file at a time. Each file is self-contained and recreates its input data.
Install the parent folder requirements first. No imports from other step files are needed.
All window examples close with Esc or the window close button. Focus the window before pressing keys.

These are experiments in chapter order, not patches to concatenate into one script.
Steps 30 and 32 are complete games. Steps 01-29 and 31 isolate smaller ideas.

```bash
python steps/01_show_rules.py
```

| Step | File | What to check |
| --- | --- | --- |
| 01 | [01_show_rules.py](01_show_rules.py) | Define a function, then call it. |
| 02 | [02_arguments.py](02_arguments.py) | The same function receives different arguments. |
| 03 | [03_return_value.py](03_return_value.py) | Use a returned value outside the function. |
| 04 | [04_none.py](04_none.py) | An action and a returned value are different things. |
| 05 | [05_local_names.py](05_local_names.py) | A local assignment leaves an outside name unchanged. |
| 06 | [06_array_change.py](06_array_change.py) | The array changes even though the function returns None. |
| 07 | [07_state.py](07_state.py) | Dictionary keys provide access to whole arrays. |
| 08 | [08_dictionary_updates.py](08_dictionary_updates.py) | Changing data and replacing a dictionary entry. |
| 09 | [09_movement.py](09_movement.py) | Check an ordinary step and wrapping on two axes. |
| 10 | [10_keyboard.py](10_keyboard.py) | Keyboard events change the direction stored in state. |
| 11 | [11_axes.py](11_axes.py) | An axis selects the array dimension affected by an operation. |
| 12 | [12_collect_target.py](12_collect_target.py) | Only visiting a target removes its coordinate row. |
| 13 | [13_rebuild_matrix.py](13_rebuild_matrix.py) | Rebuilding clears the previous player position. |
| 14 | [14_palette_indices.py](14_palette_indices.py) | Repeated integer indices select repeated RGB vectors. |
| 15 | [15_rgb_matrix.py](15_rgb_matrix.py) | A matrix of indices becomes an array of RGB vectors. |
| 16 | [16_repeat_values.py](16_repeat_values.py) | Repeat each element rather than the whole sequence. |
| 17 | [17_repeat_rows.py](17_repeat_rows.py) | Repeat complete rows along axis zero. |
| 18 | [18_repeat_columns.py](18_repeat_columns.py) | Repeat columns after repeating rows. |
| 19 | [19_repeat_rgb.py](19_repeat_rgb.py) | Repeat spatial axes while preserving RGB triples. |
| 20 | [20_swap_matrix_axes.py](20_swap_matrix_axes.py) | Swap the two axes of a two-dimensional matrix. |
| 21 | [21_swap_rgb_axes.py](21_swap_rgb_axes.py) | Swap only the two spatial axes of an RGB array. |
| 22 | [22_surface_preview.py](22_surface_preview.py) | Show the array as a visible image and keep the window open. |
| 23 | [23_compare_rgb_methods.py](23_compare_rgb_methods.py) | A loop and integer indexing produce the same color data. |
| 24 | [24_surface_function.py](24_surface_function.py) | Replace the transformation sequence with one function call. |
| 25 | [25_transparent_overlay.py](25_transparent_overlay.py) | A transparent overlay leaves the field visible. |
| 26 | [26_grid_lines.py](26_grid_lines.py) | Add vertical and horizontal cell boundaries. |
| 27 | [27_grid_border.py](27_grid_border.py) | The outside border follows the last visible pixels. |
| 28 | [28_grid_function.py](28_grid_function.py) | Build the same grid through a reusable function. |
| 29 | [29_quit_function.py](29_quit_function.py) | The quit function controls the lifetime of a real window. |
| 30 | [30_collector_every_frame.py](30_collector_every_frame.py) | First complete game: movement happens on every frame. |
| 31 | [31_step_counter.py](31_step_counter.py) | Count frames before allowing the next movement step. |
| 32 | [32_collector_timed.py](32_collector_timed.py) | Final game: keep processing input between movement steps. |
