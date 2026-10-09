# Module 0 · From Data to Pixels

This folder contains companion programs for **Matrix Thinking, Module 0**. Start with a small colored window, change one value at a time, predict the result, and run the program to check your idea.

## Files

| File | Use it for | Expected result |
| --- | --- | --- |
| [living_window.py](living_window.py) | The opening program and exercises 1–9 | An 800 × 600 green window titled `Module 0 - A living window`, shown for about three seconds. |
| [two_frames.py](two_frames.py) | The example solution to exercise 10 | A green frame for one second, followed by a blue frame for two seconds. |
| [blinking.py](blinking.py) | The example solution to exercise 11 | Five green–black pairs, with a 200 ms pause after each frame. |

Exercise 12 asks you to draw a data-flow diagram; it does not need a separate program. Try the exercises yourself before opening their example solutions.

## Requirements

The examples were checked with **Python 3.13.7** and **Pygame 2.6.1** on Windows. NumPy is not used in this module.

In PyCharm, install `pygame` version `2.6.1` in the interpreter selected for your project. You can use **View → Tool Windows → Python Packages**. Alternatively, from a terminal using the same project environment, install the dependency from this folder:

```shell
python -m pip install -r requirements.txt
```

See the [official PyCharm package instructions](https://www.jetbrains.com/help/pycharm/installing-uninstalling-and-upgrading-packages.html) if you need help selecting the project environment.

## Run a program

Open a `.py` file in PyCharm, right-click in the editor, and select **Run** for that file. Or, in a terminal using your project environment, run:

```shell
python living_window.py
```

These introductory programs pause and then close automatically. They do not yet react to the window's close button: event handling will be introduced later in the book. Wait for each short example to finish.

## Explore the data

- Change the window's width or height before the `resolution` tuple is created.
- Change one RGB component before the `background` tuple is created.
- Change the text assigned to `title`.
- Change the pause duration, expressed in milliseconds.

Keep a copy of the original program so you can return to a known starting point between experiments. The examples use explicit repeated commands because loops have not been introduced yet.

## Reference

- [Pygame documentation](https://www.pygame.org/docs/)
- [Python tutorial](https://docs.python.org/3.13/tutorial/)
