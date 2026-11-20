# A matrix of blocks

Interactive page: https://matrixthinking.org/kron.html

One matrix stores a 5×5 drawing. A second matrix contains a square block of ones. The entire enlarged world is calculated with `np.kron(world, block)`. A separate `np.repeat` calculation checks equivalence. NumPy performs the array transformations; Pygame draws the results. No classes or image assets.

## Run

```sh
python -m pip install -r requirements.txt
python kron_numpy.py
```

## Controls

- Click source pixels to paint; right-click to erase. Choose Inspect to trace without drawing.
- Click either numeric matrix or the output picture to select the corresponding source value and product block.
- Buttons and 1/2/3 set the block size; arrow keys move with wrapping; R rotates; C clears; Space restores the duck; Escape closes.

The display includes both pictures and numeric matrices, the block of ones, the selected value times that block, and a live comparison with repeat. `np.kron` builds scaled blocks; it is distinct from the `@` matrix-multiplication operator.
