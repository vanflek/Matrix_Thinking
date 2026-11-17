# Two frames. One matrix rule.

Compare two whole grayscale frames using NumPy. A synthetic camera makes a pixel
duck move across a 24 × 32 world; no webcam or micro:bit is required.

[Try the interactive laboratory](https://matrixthinking.org/motion.html).

## Run in PyCharm or a terminal

Open this folder as a project and select your Python interpreter. In its terminal:

```sh
python -m pip install -r requirements.txt
python motion_numpy.py
```

For a console check without a graphical window (only NumPy is needed):

```sh
python motion_numpy.py --check
```

The default example selects 44 of 768 pixels. A stationary, identical pair selects 0.

## Controls

| Key | Action |
| --- | --- |
| Arrow keys | Move the duck within the current frame |
| Space | Use the current frame as the previous frame |
| Page Up / Page Down | Increase / decrease the threshold by 5 |
| N | Toggle deterministic noise and generate another sample |
| L | Toggle a lighting change |
| C | Toggle duck contrast and reset the previous frame |
| R | Reset the experiment |
| Escape | Close the window |

The reference stays fixed until Space, C or R. Change one setting at a time.
The website additionally offers an animation comparing adjacent frames and a
numeric inspector; the Python example keeps the reference explicit.

## The whole-field calculation

```python
difference = np.abs(current.astype(np.int16) - previous.astype(np.int16))
motion_mask = difference > threshold
changed_pixels = np.count_nonzero(motion_mask)
changed_fraction = np.mean(motion_mask)
```

Convert **before** subtracting: unsigned 8-bit values cannot hold a negative
difference. The calculation applies to all corresponding pixels at once; it has
no Python loop over individual cells. Rendering adapts the resulting arrays to
Pygame surfaces.

The mask measures brightness changes, not object identities. Both the duck's old
and new positions can be selected. Noise or illumination changes can also trigger
it. Try a higher threshold for noise, then lower it to detect a low-contrast duck.

The Python model and browser model use the same background, duck mask and noise
formula, so their frame values and masks agree for the same parameters.

The Python code is covered by the repository's [MIT license](../../LICENSE).
