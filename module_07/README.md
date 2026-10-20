# Module 7 - Palette and Matrix: Building a Pixel Art Editor

One matrix stores color indices, another stores RGB vectors, and a cursor vector
selects where the data changes. The same drawing can be displayed with different
palettes or cell sizes. Cell-by-cell drawing is kept deliberately to make this
conversion visible; faster display techniques come in the next module.

## Run the editor

Checked with Python 3.13.7, NumPy 2.5.3, and Pygame 2.6.1.
Open a terminal in this module's folder, then use the same interpreter for both:

```bash
python -m pip install -r requirements.txt
python steps/iteration_07_07_pixel_art_editor_info.py
```

In PyCharm, open a script and run it directly. Each script is standalone.
Check the run configuration's working directory: saved files are relative to
that directory, which can differ from the script's folder.

## Versions in chapter order

| File | Added behavior |
| --- | --- |
| [steps/iteration_07_01_pixel_art_editor.py](steps/iteration_07_01_pixel_art_editor.py) | Move the cursor, cycle colors, and paint one cell. |
| [steps/iteration_07_02_pixel_art_editor_io.py](steps/iteration_07_02_pixel_art_editor_io.py) | Save and load the canvas matrix; handle a missing file. |
| [steps/iteration_07_03_pixel_art_editor_png.py](steps/iteration_07_03_pixel_art_editor_png.py) | Export the canvas and grid without the cursor. |
| [steps/iteration_07_04_pixel_art_editor_brush_center.py](steps/iteration_07_04_pixel_art_editor_brush_center.py) | Intermediate brush: try it away from edges first. Negative slice bounds deliberately remain unresolved here. |
| [steps/iteration_07_05_pixel_art_editor_brush.py](steps/iteration_07_05_pixel_art_editor_brush.py) | Clip the brush area to the canvas with min/max. |
| [steps/iteration_07_06_pixel_art_editor_shift.py](steps/iteration_07_06_pixel_art_editor_shift.py) | Cycle colors backward with Shift + Space. |
| [steps/iteration_07_07_pixel_art_editor_info.py](steps/iteration_07_07_pixel_art_editor_info.py) | Final chapter version: toggle the data overlay with I. |

## Controls in the final version

| Key | Action |
| --- | --- |
| Arrow keys | Move one cell per key-down event; wrap at the edges. |
| Space | Select the next color, then paint the brush area. |
| Shift + Space | Select the previous color, then paint. |
| S | Save the matrix to art.npy. |
| L | Load art.npy; keep the current drawing if it is missing. |
| P | Save art.png after drawing cells and grid, before cursor and labels. |
| I | Show or hide cursor, cell index, and selected color. |
| Esc / window close | Exit. |

The starting selected color is 1, so the first Space paints with index 2.
Moving the cursor does not paint. The default brush radius is 1: a 3 by 3 square
away from the edges, clipped near a boundary. There is no mouse control or
automatic key repeat in these versions.

S and P overwrite their respective files. NPY stores the array values, shape,
and dtype; it does not store the palette, cursor, or selected color. PNG stores
the rendered image. Use this editor's own NPY files with matching canvas size
and valid palette indices. General file validation is outside this module.

## Practice solutions

Try the chapter exercises first. Each file below is a complete runnable program.
Except for 26-27 and 29-30, these are independent copies of the final editor,
not cumulative steps. Exercises 21 and 25 restore features already present in
that version. Exercise 30 intentionally starts with an empty canvas: there is
no single correct icon.

| Exercise | File | What to try |
| --- | --- | --- |
| 21 | [palette_directions](solutions/solution_07_21_palette_directions.py) | Space and Shift + Space cycle and paint in both directions. |
| 22 | [palette_info](solutions/solution_07_22_palette_info.py) | I also displays the number of palette colors. |
| 23 | [brush_sizes](solutions/solution_07_23_brush_sizes.py) | Keys 1, 2, 3 select brush radii 0, 1, 2. |
| 24 | [rectangular_canvas](solutions/solution_07_24_rectangular_canvas.py) | Check brush clipping on a 6 by 10 canvas. |
| 25 | [clean_png](solutions/solution_07_25_clean_png.py) | I, then P: the PNG contains neither labels nor cursor. |
| 26 | [save_and_reload](solutions/solution_07_26_save_and_reload.py) | S/L use saves/art.npy. Save before loading. |
| 27 | [missing_file](solutions/solution_07_27_missing_file.py) | Missing saves/art.npy prints a message and preserves the canvas. |
| 28 | [two_palettes](solutions/solution_07_28_two_palettes.py) | Draw, then press T to change colors while preserving the matrix. |
| 29 | [separate_color](solutions/solution_07_29_separate_color.py) | Q/E select a color; Space only paints. |
| 30 | [own_icon](solutions/solution_07_30_own_icon.py) | Q/E and a one-cell brush; save, restart, load, and add a detail. |

For exercises 26 and 27, create a folder named `saves` in the working directory
before pressing S. From a terminal opened in this module's folder:

```bash
mkdir saves
python solutions/solution_07_27_missing_file.py
```

Keep the same working directory when restarting. Exercise 26 intentionally
assumes the save exists; exercise 27 adds the missing-file handler. All other
examples use art.npy in the working directory. The rectangular exercise needs
its own 6 by 10 save; do not load a 16 by 16 save into it.

## Previous module

[Module 6 - Slices and masks](../module_06/)


## File and listing names

`steps/iteration_MM_NN_name.py` contains runnable learning steps in chapter order.
`examples/example_MM_NN_name.py` contains independent experiments.
`solutions/solution_MM_TT_name.py` contains exercise solutions (TT is the exercise number).
`final/` contains complete programs, where provided. Listing identifiers match file stems;
these numbers are not PDF page numbers. Run each program separately.
