# Module 11 — Color as a Vector: From a Palette to an RGB Array

The same image can be represented by palette indices or by RGB values stored directly in each cell. This module builds an RGB pixel editor using functions, NumPy arrays and Pygame.

## Getting started

Tested with Python 3.13.7, NumPy 2.5.3 and Pygame 2.6.1.

```sh
python -m pip install -r requirements.txt
python rgb_editor.py
```

Run each teaching file separately. Every file is self-contained and does not import another teaching script. Console examples do not open a window.

## Learning steps

- `iterations/s00_rgb_canvas.py`: Display the RGB canvas and grid.
- `iterations/s01_cursor_frame.py`: Locate a cell and draw its cursor frame.
- `iterations/s02_editor_state.py`: Store tool settings in a dictionary.
- `iterations/s03_channel_controls.py`: Select and adjust a color component.
- `iterations/s04_brush_frame.py`: Show the brush color in the cursor frame.
- `iterations/s05_click_paint.py`: Paint one cell per click.
- `iterations/s06_drag_paint.py`: Paint while holding the mouse button.
- `iterations/s07_erase.py`: Erase with Shift.
- `iterations/s08_pipette.py`: Read a cell color into the brush.
- `iterations/s09_view_and_copy.py`: Compare a view, a copy and a separate brush (console).
- `iterations/s10_clear.py`: Clear the entire canvas.
- `iterations/s11_save_load_npy.py`: Save and validate RGB arrays.
- `iterations/s12_export_png.py`: Export a clean PNG image.

## Small console examples

- `examples/rgb_axes.py`: select a scalar, RGB vector and channel matrix.
- `examples/canvas_fill.py`: create and fill a canvas using broadcasting.
- `examples/rgb_surface.py`: convert an array to a Pygame surface and check its dimensions.

## Editor controls

| Action | Control |
|---|---|
| Select the red, green or blue component | R / G / B |
| Adjust the selected component | Mouse wheel, in steps of 5 |
| Paint | Left click or hold the left mouse button |
| Erase with the background color | Shift + left mouse button |
| Pick a cell color | Right click |
| Clear the canvas | C |
| Save the array | S |
| Load the array | L |
| Export a clean PNG | P |
| Exit | Esc or close the window |

The editor stores cells in an array with shape `(ROWS, COLS, 3)` and dtype `uint8`. Grid lines and the cursor frame are screen overlays; neither is saved with the image. Very fast mouse movement may leave gaps because this version does not interpolate between sampled positions.

Files are saved in the current working directory: `pixel_art_rgb.npy` contains the original cell array; `pixel_art_rgb.png` contains the enlarged image. Loading accepts only an array with the expected shape and dtype. Saving again overwrites the previous file.

## Exercise solutions

Run each solution independently; solutions do not depend on the previous exercise.

- `solutions/exercise_26.py`: four colored quadrants, 8 rows and 12 columns.
- `solutions/exercise_27.py`: a 3 x 3 brush and eraser clipped at the canvas boundaries.
- `solutions/exercise_28.py`: E exports only the red channel to `red_channel.png`; P keeps the normal export.
- `solutions/exercise_29.py`: U restores the canvas from before its last clear, once. A new clear replaces the backup.
- `solutions/exercise_30.py`: O exports one pixel per cell to `pixel_art_cells.png`; P exports the enlarged image.

## Illustrations

The `illustrations` directory contains diagrams of RGB axes, shared and copied data, the frame/export pipeline, and the five practical tasks. All labels are in English.
