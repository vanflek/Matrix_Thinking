# Module 4 - Pygame Skeleton: Loop, Events, and Drawing

Companion programs for **Matrix Thinking**. Coordinates describe a position, elapsed time determines displacement, and input changes the data used to draw each frame.

## Start here

| Program | What it shows |
| --- | --- |
| [steps/iteration_04_01_falling_circle.py](steps/iteration_04_01_falling_circle.py) | Automatic movement using speed and elapsed time. The program closes at the bottom boundary. |
| [steps/iteration_04_02_falling_circle_events.py](steps/iteration_04_02_falling_circle_events.py) | The same movement with close-button and Esc handling. |
| [steps/iteration_04_03_keyboard_circle.py](steps/iteration_04_03_keyboard_circle.py) | One 40-pixel step per arrow-key press, with position limits. |
| [steps/iteration_04_04_mouse_circle.py](steps/iteration_04_04_mouse_circle.py) | Read the mouse position, constrain the circle, and hide the system cursor. |

These four files match the complete listings in the chapter. All examples are independent: run one file at a time.

## Run a program

Checked with **Python 3.13.7** and **Pygame 2.6.1** on Windows. NumPy is not required.

```shell
python -m pip install -r requirements.txt
python steps/iteration_04_01_falling_circle.py
```

You can also open an individual file in PyCharm and run it there.

The first two programs close automatically after about 1.1 seconds. Temporarily change `speed = 240` to `speed = 60` for a longer observation. The first version services the window with `pg.event.pump()` but does not yet handle the close button or Esc. The second version does. The keyboard and mouse versions run until you close the window or press Esc. Make the window active before testing keyboard input.

In the keyboard version, release a key before pressing it again. Key repeat has not been enabled, so holding an arrow does not create continuous movement.

## Experiments

Predict what will change before running each version.

| File | Experiment |
| --- | --- |
| [examples/example_04_03_fps_60.py](examples/example_04_03_fps_60.py) | Speed 60 pixels per second, with a 60 FPS limit. |
| [examples/example_04_02_fps_15.py](examples/example_04_02_fps_15.py) | The same speed and elapsed-time calculation, with a 15 FPS limit. |
| [examples/example_04_04_no_background_clear.py](examples/example_04_04_no_background_clear.py) | Exercise 7: previous drawings remain visible as a trail. |
| [examples/example_04_01_background_after_circle.py](examples/example_04_01_background_after_circle.py) | Exercise 7: filling after drawing erases the circle before the frame is shown. |

The FPS experiments should take about 4.5 seconds each. The frame limit affects smoothness; multiplying speed by measured time preserves the intended movement speed. `Clock.tick()` sets an approximate upper limit, not a guaranteed frame rate. These experiments use the first program and close automatically at the bottom boundary.

For example:

```shell
python examples/example_04_02_fps_15.py
```

## Self-check examples

| Exercise | File | Expected observation |
| --- | --- | --- |
| 5 | [Fractional position](solutions/solution_04_05_fractional_position.py) | Console: repeated truncation stays at 300; preserved fractions reach 301.0. |
| 8 | [Loop flag](solutions/solution_04_08_loop_flag.py) | Console: all three messages appear, including the end of the current iteration. |
| 10 | [Close request](solutions/solution_04_10_close_request.py) | Complete falling-circle program with a QUIT handler; Esc handling is intentionally absent. |
| 13 | [Window bounds](solutions/solution_04_13_bounds.py) | Console: both coordinates are corrected to (770, 570). |
| 15 | [Visible cursor](solutions/solution_04_15_show_cursor.py) | The system cursor and our circle are both visible. |
| 16 | [Keyboard rectangle](solutions/solution_04_16_keyboard_rectangle.py) | Move a 120-by-80 rectangle in 40-pixel steps, keeping all four sides inside the window. |

The chapter contains all 16 questions and their explanations. These files provide standalone versions of the executable examples; use `steps/iteration_04_02_falling_circle_events.py` for the nested Esc check in exercise 11 and `steps/iteration_04_03_keyboard_circle.py` for the movement in exercise 12.

## Trace the data

- The pair `(x, y)` describes position. Its components, radius, speed, and elapsed time are scalars.
- Speed is measured in pixels per second; `dt` is measured in seconds. Their product is displacement in pixels.
- Keep fractional coordinates between updates. `int(y)` in the drawing call does not overwrite `y`.
- `pg.event.get()` retrieves queued messages. Your code decides how to respond.
- `running = False` prevents the next loop iteration; it does not skip the rest of the current one.
- The circle center must stay within `radius` and `width - radius` horizontally, and `radius` and `height - radius` vertically.
- Clamping the circle's coordinates does not move the actual mouse pointer. Hiding the pointer does not stop position queries.
- Draw the background, draw the circle, and then show the prepared frame.

## References

- [Previous module](../module_03/)
- [Pygame events](https://www.pygame.org/docs/ref/event.html)
- [Pygame time](https://www.pygame.org/docs/ref/time.html)
- [Pygame keyboard](https://www.pygame.org/docs/ref/key.html)
- [Pygame mouse](https://www.pygame.org/docs/ref/mouse.html)


## File and listing names

`steps/iteration_MM_NN_name.py` contains runnable learning steps in chapter order.
`examples/example_MM_NN_name.py` contains independent experiments.
`solutions/solution_MM_TT_name.py` contains exercise solutions (TT is the exercise number).
`final/` contains complete programs, where provided. Listing identifiers match file stems;
these numbers are not PDF page numbers. Run each program separately.
