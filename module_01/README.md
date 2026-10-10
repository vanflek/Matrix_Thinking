# Module 1 · From Pixels to Shapes

Companion programs for **Matrix Thinking, Module 1**. Describe positions, colors, and shapes with numbers; predict what will change, then run the program and compare the result with your prediction.

## Main examples

| File | What it shows |
| --- | --- |
| [pixel.py](pixel.py) | One white pixel at `(100, 100)` on a black background. The pixel is deliberately tiny. |
| [circle.py](circle.py) | A filled cyan circle whose center is calculated from the window dimensions. |
| [line.py](line.py) | A yellow segment joining two position vectors. |
| [rectangle.py](rectangle.py) | A green rectangle described by its top-left position, width, and height. |
| [draw_order_rectangle_first.py](draw_order_rectangle_first.py) | A red circle drawn over a green rectangle. |
| [draw_order_circle_first.py](draw_order_circle_first.py) | The same figures and data, with the two drawing commands reversed. |
| [exercise_template.py](exercise_template.py) | A black window with a marked place for your own drawing commands. |

The four single-shape programs and the exercise template match the complete listings in the chapter. The drawing-order examples combine the rectangle program with the chapter's short patches.

## Run the examples

Checked with **Python 3.13.7** and **Pygame 2.6.1** on Windows. NumPy is not needed for this module.

Install the dependency into your project interpreter:

```shell
python -m pip install -r requirements.txt
```

Open a program in PyCharm and run that file, or use a terminal in this folder:

```shell
python circle.py
```

Each program shows its image for about five seconds and then closes automatically. These early examples do not yet handle the window's close button; wait for the short pause to finish. The exercise template shows only a black background until you add drawing commands.

## Experiment before reading the solutions

- Change one value at a time and predict the visible result.
- Change component values before the tuple containing them is created. For example, edit `start_x` before `start_pos = (start_x, start_y)`.
- To move a whole segment, give both endpoints the same displacement.
- To resize a rectangle without moving its top-left corner, change its width or height.
- Change `width` and `height` in the source and run again to check computed center positions.
- Compare the two drawing-order programs: the last color written to an overlapping pixel remains visible.

## Example solutions

Try each exercise yourself first. Every file below is a standalone program: it combines the chapter's exercise template with the corresponding answer. It can be run directly, for example:

```shell
python solutions/exercise_09_house.py
```

| Exercise | Files | What to compare |
| --- | --- | --- |
| 5. Move a pixel | [Center](solutions/exercise_05_center.py), [corner](solutions/exercise_05_corner.py), [one pixel inward](solutions/exercise_05_inward.py) | `(400, 300)`, `(799, 599)`, and `(798, 598)` in an 800 × 600 window. |
| 6. Two-circle target | [Target](solutions/exercise_06_target.py), [reversed order](solutions/exercise_06_reversed_order.py) | Both circles share a center; the larger one hides the smaller one when drawn last. |
| 7. Crosshair | [exercise_07_crosshair.py](solutions/exercise_07_crosshair.py) | Two lines meet at the computed center and reach the window edges. |
| 8. Frame | [exercise_08_frame.py](solutions/exercise_08_frame.py) | A five-pixel green border drawn inside the window bounds. |
| 9. House | [exercise_09_house.py](solutions/exercise_09_house.py) | The walls are drawn before the door and windows. |
| 10. Flag | [exercise_10_flag.py](solutions/exercise_10_flag.py) | A white rectangle provides the middle stripe between red and blue stripes. |
| 11. Sight | [exercise_11_sight.py](solutions/exercise_11_sight.py) | Short crossing lines and three circle outlines share a computed center. |
| Extra: move a whole drawing | [extra_shift_house.py](solutions/extra_shift_house.py) | Every part of the house moves 50 pixels right; the ground stays in place. |

Exercises 1–4 ask you to read numerical descriptions and predict their results. Check those predictions with the main programs and the exercise template; the detailed explanations are in the book.

## Reference

- [Pygame drawing functions](https://www.pygame.org/docs/ref/draw.html)
- [Pygame Surface](https://www.pygame.org/docs/ref/surface.html)
- [Previous module: From Data to Pixels](../module_00/)
