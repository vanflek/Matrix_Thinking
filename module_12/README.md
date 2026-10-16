# Module 12 — ASCII art from pixels to characters

Requirements: Python 3.13, NumPy, Pygame, and the Consolas monospace font.
Install the packages with `python -m pip install -r requirements.txt`.

Run each script with its containing folder as the working directory. In PyCharm,
set **Working directory** to the folder containing the selected script.
`cat.png` and the prepared `symbol_palette.npz` are included with each relevant folder.
The font itself is not redistributed.

## Final programs

Run `final/analyze_symbols.py` to regenerate the measured palette.
Then run `final/image_to_ascii.py` from the same folder.
Up increases character size, Down decreases it, C toggles color, and Esc exits.
Every new image is computed from the original photograph. Large characters remove detail.

## Learning steps

Each script is complete and runs independently. Console steps show numerical results;
image steps show the current visual result. Iteration 12.20 still shows the mosaic while adding a
scalar selection function. Iteration 12.21 also prints the symbol matrix shape; Iteration 12.22 renders it.

- `steps/iteration_12_01_chr_ord.py` — Character codes and string conversion.
- `steps/iteration_12_02_ascii_codes.py` — Collect all 95 printable ASCII symbols.
- `steps/iteration_12_03_render_symbol.py` — Render a symbol offscreen and inspect pixels.
- `steps/iteration_12_04_brightness_loops.py` — Mean brightness using two loops.
- `steps/iteration_12_05_brightness_numpy.py` — Mean brightness using NumPy.
- `steps/iteration_12_06_all_symbols_list.py` — Measure all symbols.
- `steps/iteration_12_07_paired_arrays.py` — Store symbols and brightness in arrays.
- `steps/iteration_12_08_normalize_loops.py` — Normalize using loops.
- `steps/iteration_12_09_normalize_numpy.py` — Normalize using NumPy.
- `steps/iteration_12_10_sort_loops.py` — Move paired data with a loop.
- `steps/iteration_12_11_sort_numpy.py` — Apply the index permutation directly.
- `steps/iteration_12_12_save_palette.py` — Save named arrays to NPZ.
- `steps/iteration_12_13_load_image.py` — Load image.
- `steps/iteration_12_14_gray_loops.py` — Gray loops.
- `steps/iteration_12_15_gray_numpy.py` — Gray numpy.
- `steps/iteration_12_16_blocks_four_loops.py` — Blocks four loops.
- `steps/iteration_12_17_blocks_mean.py` — Blocks mean.
- `steps/iteration_12_18_blocks_reshape.py` — Blocks reshape.
- `steps/iteration_12_19_mosaic_repeat.py` — Mosaic repeat.
- `steps/iteration_12_20_single_block_function.py` — Single block function.
- `steps/iteration_12_21_select_symbols.py` — Select symbols.
- `steps/iteration_12_22_draw_ascii.py` — Draw ascii.
- `steps/iteration_12_23_searchsorted.py` — Searchsorted.
- `steps/iteration_12_24_select_numpy.py` — Select numpy.
- `steps/iteration_12_25_color_means.py` — Color means.
- `steps/iteration_12_26_draw_color.py` — Draw color.
- `steps/iteration_12_27_color_numpy.py` — Color numpy.
- `steps/iteration_12_28_resize.py` — Resize.
- `steps/iteration_12_29_color_toggle.py` — Color toggle.

## Patches and practice

Patches describe adjacent snapshots within either program sequence. They are optional if you use
the complete scripts. Iterations 12.1–12.12 build the analyzer; 12.13–12.29 build the viewer. There is no patch between the two programs.
`examples/` contains small console experiments. `solutions/` contains tasks 26–30.
For task 26, copy the generated `palette_four.npz` to the renderer working folder and
change its `PALETTE_FILE` setting. Task 29 adds S to save the current result.
Task 30 prints measurements; observations about recognizability are the reader's own.

## Numbering

`steps/iteration_12_13_load_image.py` is Iteration 12.13 in the book. `examples/example_12_05_argsort.py` is Example 12.5. Iterations and examples have separate consecutive numbers within each module. The numbers do not refer to pages. A short code fragment belongs to its surrounding iteration unless it is explicitly labeled as a standalone example.

## Standalone examples

- `examples/example_12_01_channel_mean.py` — Example 12.1.
- `examples/example_12_02_paired_arrays.py` — Example 12.2.
- `examples/example_12_03_normalize_loops.py` — Example 12.3.
- `examples/example_12_04_normalize_numpy.py` — Example 12.4.
- `examples/example_12_05_argsort.py` — Example 12.5.
- `examples/example_12_06_reorder_loops.py` — Example 12.6.
- `examples/example_12_07_reorder_numpy.py` — Example 12.7.
- `examples/example_12_08_savez_load.py` — Example 12.8.
- `examples/example_12_09_reshape_matrix.py` — Example 12.9.
- `examples/example_12_10_image_coordinates.py` — Example 12.10.
- `examples/example_12_11_block_address.py` — Example 12.11.
- `examples/example_12_12_select_block.py` — Example 12.12.
- `examples/example_12_13_mean_axes.py` — Example 12.13.
- `examples/example_12_14_block_averages.py` — Example 12.14.
- `examples/example_12_15_nearest_symbol.py` — Example 12.15.
- `examples/example_12_16_symbol_matrix.py` — Example 12.16.
- `examples/example_12_17_searchsorted_scalar.py` — Example 12.17.
- `examples/example_12_18_nearest_sorted.py` — Example 12.18.
- `examples/example_12_19_searchsorted_matrix.py` — Example 12.19.
- `examples/example_12_20_rgb_means.py` — Example 12.20.
- `examples/example_12_21_exercise_paired_arrays.py` — Example 12.21.
- `examples/example_12_22_exercise_argsort.py` — Example 12.22.
- `examples/example_12_23_exercise_broken_pairs.py` — Example 12.23.
- `examples/example_12_24_exercise_block_address.py` — Example 12.24.
- `examples/example_12_25_exercise_mean_axes.py` — Example 12.25.
- `examples/example_12_26_exercise_searchsorted.py` — Example 12.26.
- `examples/example_12_27_exercise_where.py` — Example 12.27.
- `examples/example_12_28_compare_averages.py` — Example 12.28.
- `examples/example_12_29_keep_rgb_axis.py` — Example 12.29.

## Illustrations

The 19 diagrams and example images in `assets/illustrations/` accompany the chapter. Labels are in English. The source photograph `cat.png` was generated for this book.

## Solution files

- `solutions/exercise_26.py` — Exercise 26.
- `solutions/exercise_27.py` — Exercise 27.
- `solutions/exercise_28.py` — Exercise 28.
- `solutions/exercise_29.py` — Exercise 29.
- `solutions/exercise_30.py` — Exercise 30.
