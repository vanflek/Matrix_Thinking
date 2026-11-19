# Repeat the matrix with NumPy

Interactive laboratory: https://matrixthinking.org/scale.html

Run with Python 3.13 in a virtual environment:

```text
python -m pip install -r requirements.txt
python scale_numpy.py
```

The source is a 5x5 brightness matrix. The enlargement is exactly:

```python
rows_repeated = world.repeat(factor, axis=0)
zoomed = rows_repeated.repeat(factor, axis=1)
```

Buttons and keys 1/2/3 choose the factor. Draw in the source picture;
left button paints, right button erases. Numeric matrices and the result
picture inspect the corresponding source cell and full repeated block.
Arrows use np.roll; R uses np.rot90; C uses np.zeros_like; Space restores
the duck. Escape closes the window. No classes or external images.

The only loops over individual cells render the already-computed arrays;
the transformations, colour lookup and selection mask use NumPy arrays.
The website uses a JavaScript teaching model; this file runs real NumPy.
