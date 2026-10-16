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
image steps show the current visual result. B07 still shows the mosaic while adding a
scalar selection function. B08 also prints the symbol matrix shape; B09 renders it.

- `iterations/a00_chr_ord.py` — Character codes and string conversion.
- `iterations/a01_ascii_codes.py` — Collect all 95 printable ASCII symbols.
- `iterations/a02_render_symbol.py` — Render a symbol offscreen and inspect pixels.
- `iterations/a03_brightness_loops.py` — Mean brightness using two loops.
- `iterations/a04_brightness_numpy.py` — Mean brightness using NumPy.
- `iterations/a05_all_symbols_list.py` — Measure all symbols.
- `iterations/a06_paired_arrays.py` — Store symbols and brightness in arrays.
- `iterations/a07_normalize_loops.py` — Normalize using loops.
- `iterations/a08_normalize_numpy.py` — Normalize using NumPy.
- `iterations/a09_sort_loops.py` — Move paired data with a loop.
- `iterations/a10_sort_numpy.py` — Apply the index permutation directly.
- `iterations/a11_save_palette.py` — Save named arrays to NPZ.
- `iterations/b00_load_image.py` — Load image.
- `iterations/b01_gray_loops.py` — Gray loops.
- `iterations/b02_gray_numpy.py` — Gray numpy.
- `iterations/b03_blocks_four_loops.py` — Blocks four loops.
- `iterations/b04_blocks_mean.py` — Blocks mean.
- `iterations/b05_blocks_reshape.py` — Blocks reshape.
- `iterations/b06_mosaic_repeat.py` — Mosaic repeat.
- `iterations/b07_single_block_function.py` — Single block function.
- `iterations/b08_select_symbols.py` — Select symbols.
- `iterations/b09_draw_ascii.py` — Draw ascii.
- `iterations/b10_searchsorted.py` — Searchsorted.
- `iterations/b11_select_numpy.py` — Select numpy.
- `iterations/b12_color_means.py` — Color means.
- `iterations/b13_draw_color.py` — Draw color.
- `iterations/b14_color_numpy.py` — Color numpy.
- `iterations/b15_resize.py` — Resize.
- `iterations/b16_color_toggle.py` — Color toggle.

## Patches and practice

Patches describe adjacent snapshots within sequence A or B. They are optional if you use
the complete scripts. A and B are separate programs; there is no patch from A to B.
`examples/` contains small console experiments. `solutions/` contains tasks 26–30.
For task 26, copy the generated `palette_four.npz` to the renderer working folder and
change its `PALETTE_FILE` setting. Task 29 adds S to save the current result.
Task 30 prints measurements; observations about recognizability are the reader's own.

## Illustrations

The 19 diagrams and example images in `illustrations/` accompany the chapter. All labels are in English. The source photograph `cat.png` was generated for this book.
