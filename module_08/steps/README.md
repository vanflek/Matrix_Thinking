# Module 8 - Runnable steps

Run one file at a time. Each file is self-contained and recreates its input data.
Install the parent folder requirements first. No imports from other step files are needed.
All window examples close with Esc or the window close button. Focus the window before pressing keys.

These are experiments in chapter order, not patches to concatenate into one script.
Steps 30 and 32 are complete games. Steps 01-29 and 31 isolate smaller ideas.

```bash
python steps/iteration_08_01_show_rules.py
```

| Step | File | What to check |
| --- | --- | --- |
| 01 | [steps/iteration_08_01_show_rules.py](iteration_08_01_show_rules.py) | Define a function, then call it. |
| 02 | [steps/iteration_08_02_arguments.py](iteration_08_02_arguments.py) | The same function receives different arguments. |
| 03 | [steps/iteration_08_03_return_value.py](iteration_08_03_return_value.py) | Use a returned value outside the function. |
| 04 | [steps/iteration_08_04_none.py](iteration_08_04_none.py) | An action and a returned value are different things. |
| 05 | [steps/iteration_08_05_local_names.py](iteration_08_05_local_names.py) | A local assignment leaves an outside name unchanged. |
| 06 | [steps/iteration_08_06_array_change.py](iteration_08_06_array_change.py) | The array changes even though the function returns None. |
| 07 | [steps/iteration_08_07_state.py](iteration_08_07_state.py) | Dictionary keys provide access to whole arrays. |
| 08 | [steps/iteration_08_08_dictionary_updates.py](iteration_08_08_dictionary_updates.py) | Changing data and replacing a dictionary entry. |
| 09 | [steps/iteration_08_09_movement.py](iteration_08_09_movement.py) | Check an ordinary step and wrapping on two axes. |
| 10 | [steps/iteration_08_10_keyboard.py](iteration_08_10_keyboard.py) | Keyboard events change the direction stored in state. |
| 11 | [steps/iteration_08_11_axes.py](iteration_08_11_axes.py) | An axis selects the array dimension affected by an operation. |
| 12 | [steps/iteration_08_12_collect_target.py](iteration_08_12_collect_target.py) | Only visiting a target removes its coordinate row. |
| 13 | [steps/iteration_08_13_rebuild_matrix.py](iteration_08_13_rebuild_matrix.py) | Rebuilding clears the previous player position. |
| 14 | [steps/iteration_08_14_palette_indices.py](iteration_08_14_palette_indices.py) | Repeated integer indices select repeated RGB vectors. |
| 15 | [steps/iteration_08_15_rgb_matrix.py](iteration_08_15_rgb_matrix.py) | A matrix of indices becomes an array of RGB vectors. |
| 16 | [steps/iteration_08_16_repeat_values.py](iteration_08_16_repeat_values.py) | Repeat each element rather than the whole sequence. |
| 17 | [steps/iteration_08_17_repeat_rows.py](iteration_08_17_repeat_rows.py) | Repeat complete rows along axis zero. |
| 18 | [steps/iteration_08_18_repeat_columns.py](iteration_08_18_repeat_columns.py) | Repeat columns after repeating rows. |
| 19 | [steps/iteration_08_19_repeat_rgb.py](iteration_08_19_repeat_rgb.py) | Repeat spatial axes while preserving RGB triples. |
| 20 | [steps/iteration_08_20_swap_matrix_axes.py](iteration_08_20_swap_matrix_axes.py) | Swap the two axes of a two-dimensional matrix. |
| 21 | [steps/iteration_08_21_swap_rgb_axes.py](iteration_08_21_swap_rgb_axes.py) | Swap only the two spatial axes of an RGB array. |
| 22 | [steps/iteration_08_22_surface_preview.py](iteration_08_22_surface_preview.py) | Show the array as a visible image and keep the window open. |
| 23 | [steps/iteration_08_23_compare_rgb_methods.py](iteration_08_23_compare_rgb_methods.py) | A loop and integer indexing produce the same color data. |
| 24 | [steps/iteration_08_24_surface_function.py](iteration_08_24_surface_function.py) | Replace the transformation sequence with one function call. |
| 25 | [steps/iteration_08_25_transparent_overlay.py](iteration_08_25_transparent_overlay.py) | A transparent overlay leaves the field visible. |
| 26 | [steps/iteration_08_26_grid_lines.py](iteration_08_26_grid_lines.py) | Add vertical and horizontal cell boundaries. |
| 27 | [steps/iteration_08_27_grid_border.py](iteration_08_27_grid_border.py) | The outside border follows the last visible pixels. |
| 28 | [steps/iteration_08_28_grid_function.py](iteration_08_28_grid_function.py) | Build the same grid through a reusable function. |
| 29 | [steps/iteration_08_29_quit_function.py](iteration_08_29_quit_function.py) | The quit function controls the lifetime of a real window. |
| 30 | [steps/iteration_08_30_collector_every_frame.py](iteration_08_30_collector_every_frame.py) | First complete game: movement happens on every frame. |
| 31 | [steps/iteration_08_31_step_counter.py](iteration_08_31_step_counter.py) | Count frames before allowing the next movement step. |
| 32 | [steps/iteration_08_32_collector_timed.py](iteration_08_32_collector_timed.py) | Final game: keep processing input between movement steps. |
