# Module 20 - Affine Transformations: Controlling Shape and Position

Describe a wireframe with vertices and edges, preserve its original geometry,
and transform all vertices using one homogeneous matrix. Explore translation,
scaling, reflection, rotation, composition, and the effect of changing order.

## Requirements and launch

Checked with Python 3.13.7, NumPy 2.5.3, and Pygame 2.6.1.
From this folder:

```console
python -m pip install -r requirements.txt
python final/affine_transformations.py
```

NumPy and Pygame are the only runtime dependencies. Every Python file is
standalone. The programs do not load external images, fonts, or data files.
The figures in `assets/illustrations/` are reading materials, not runtime assets.

## Controls in the final program

| Key | Change per press |
|---|---|
| Left / Right | Decrease / increase world X displacement by 10 |
| Down / Up | Decrease / increase world Y displacement by 10 |
| Q / E | Increase / decrease the angle by 5 degrees |
| A / D | Decrease / increase the local X scale factor by 0.25 |
| S / W | Decrease / increase the local Y scale factor by 0.25 |
| R | Reset displacement to (100, 50), angle to 30 degrees, scales to 1 |
| Escape or window close | Exit |

Use an English keyboard layout for letter controls. Actions use individual
KEYDOWN events; held-key repeat is not enabled. Release and press again for
another step. Pending increments are added together for a frame. Reset takes
priority over parameter changes in the same frame; exit takes priority over both.

Arrows follow fixed world axes, not the airplane's heading. Increasing a negative
scale factor can shrink the shape: its magnitude controls size, its sign controls
reflection. Zero and negative scales are allowed intentionally. The object may
leave the window; press R to return to the initial setup.

## Coordinate and data conventions

- Mathematical X points right and Y points up. World (0, 0) appears at the center
  of the 640 x 480 window. One mathematical unit equals one pixel.
- CELL_SIZE = 40 changes grid spacing, not the scale of the object coordinates.
- Each original vertex is a row. Iterations 03 onward store [x, y, 1]. The last
  component is a homogeneous coordinate, not a third spatial dimension.
- Transformation matrices are written for point-columns, then applied to rows
  using `vertices @ transform_matrix.T`.
- Standard composition is `translation_matrix @ rotation_matrix @ scale_matrix`:
  scale the local shape, rotate it about local zero, then place it in the world.
- `vertices` stays unchanged. `transformed_vertices` is recomputed from it;
  previous results are not used as the source of the next transformation.
- Vertex 19 is the local origin, vertex 1 is the nose. Vertex 0 is not the origin.
- A purple mark identifies vertex 5 to reveal reflections of a symmetric outline.

## Folders and identifiers

- `steps/`: complete runnable iterations in reading order.
- `examples/`: seven independent console experiments.
- `solutions/`: five separate practical exercise solutions, each based on the
  final program. Do not apply these solutions one after another.
- `final/`: complete laboratory, identical to iteration 10.
- `patches/`: optional transitions between adjacent iterations for `main.py`.
- `assets/illustrations/`: diagrams and actual program captures used in the text.

In `iteration_20_08`, 20 is the module and 08 is the iteration, not a page number.
Examples have their own sequence. Solutions use exercise numbers 26 through 30.

## Runnable iterations

| File | Result |
|---|---|
| `steps/iteration_20_01_skeleton.py` | Triangle, grid, five-class structure |
| `steps/iteration_20_02_airplane.py` | Twenty-vertex airplane with 29 edges |
| `steps/iteration_20_03_homogeneous.py` | Add a constant coordinate; unchanged picture |
| `steps/iteration_20_04_apply_matrix.py` | Translate all vertices from their original coordinates |
| `steps/iteration_20_05_scaling.py` | Scale the local shape, then translate |
| `steps/iteration_20_06_reflections.py` | Marker for reflection and zero-scale experiments |
| `steps/iteration_20_07_rotation.py` | Separate scaling, rotation, and translation |
| `steps/iteration_20_08_composition.py` | Combine three matrices before applying them |
| `steps/iteration_20_09_order.py` | Temporary translate-before-rotate experiment at 90 degrees |
| `steps/iteration_20_10_keyboard.py` | Restore TRS and 30 degrees; add keyboard controls |

Iterations 01-09 show fixed parameter experiments and support only exit controls.
Change model parameters in the file and rerun them. Keyboard parameter control
starts in iteration 10. The change from 09 to 10 intentionally restores the
standard composition and the initial parameter set before adding controls.

## Independent examples

| File | Experiment |
|---|---|
| `examples/example_20_01_vertices_edges.py` | Choose line endpoints using edge indices |
| `examples/example_20_02_homogeneous_translation.py` | Translate a point-column |
| `examples/example_20_03_rows_columns.py` | Rows, columns, transpose, and batches of points |
| `examples/example_20_04_scaling.py` | Scale one point along two axes |
| `examples/example_20_05_rotation.py` | Rotate a point by 30 degrees |
| `examples/example_20_06_composition.py` | Compare sequential and combined transformations |
| `examples/example_20_07_order.py` | Compare rotation-translation orders |

## Practical solutions

| File | Result and additional controls |
|---|---|
| `solutions/solution_20_26_house.py` | New wireframe; R restores zero angle and displacement |
| `solutions/solution_20_27_original_and_result.py` | Fixed gray original and blue transformed outline |
| `solutions/solution_20_28_reflection_keys.py` | X negates sx, Y negates sy; initial angle is zero |
| `solutions/solution_20_29_transformation_order.py` | O toggles order; gold ring marks transformed local zero |
| `solutions/solution_20_30_chosen_pivot.py` | Q/E rotate around the nose; R resets angle to zero |

Solution 29 starts at 90 degrees. R restores its first order (TRS) and starting
parameters. Two O events in one frame cancel each other. Gold ring positions at
the starting angle are (100, 50) and (-50, 100) in world coordinates.

Solution 30 disables movement and scaling controls. Its fixed pivot is (105, 0).
The nose remains there at every angle. Original local zero reaches (105, -105)
at 90 degrees. The gold ring marks the fixed pivot. All solutions preserve the
original vertex array.

## Patches

See `patches/README.md`. Copy iteration 01 to `main.py`, then apply the nine
patches in order. All patches were checked and applied sequentially with Git;
every intermediate result matched its complete iteration. The final result
matched `final/affine_transformations.py`.

## Verification

All seven console examples and all 16 window programs were executed. Window
checks used SDL's dummy video driver, rendered frames, and exited through the
actual main loops. Targeted checks covered keyboard actions, reset precedence,
zero and negative scales, composition equivalence, order changes, and fixed-pivot
rotation. This automated verification does not replace trying the controls in a
visible desktop window. No measured performance improvement is claimed.


## File and listing names

`steps/iteration_MM_NN_name.py` contains runnable learning steps in chapter order.
`examples/example_MM_NN_name.py` contains independent experiments.
`solutions/solution_MM_TT_name.py` contains exercise solutions (TT is the exercise number).
`final/` contains complete programs, where provided. Listing identifiers match file stems;
these numbers are not PDF page numbers. Run each program separately.
