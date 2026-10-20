# Module 23 - 3D Graphics and Coordinate Systems

Build a wireframe scene from vertices and edges. Move a camera, apply perspective,
clip edges against a near plane, and rotate two Cobra Mk III ships about their
own axes. Geometry is embedded in the scripts; no external model is needed.

## Install and run

Tested with Python 3.13.7, NumPy 2.5.3, and Pygame 2.6.1.
From this module's directory:

```console
python -m pip install -r requirements.txt
python final/wireframe_scene.py
```

The program opens a 1000-by-1000 window. From iteration 05 onward it captures the
mouse and hides the pointer. Escape exits and releases the mouse.

## Controls

| Input | Action |
| --- | --- |
| W / S | Move forward / backward in camera coordinates |
| A / D | Move left / right in camera coordinates |
| Space / left Ctrl | Move along the camera's positive / negative Y axis |
| Mouse | Change yaw and pitch |
| Q / E | Increase / decrease camera roll |
| Escape or window close | Exit |

Early steps introduce these controls progressively. Use an English keyboard
layout. The camera can move through ships; collision detection is not included.

## Folders and listing IDs

- `steps/`: complete runnable states, from iteration 01 through 16.
- `examples/`: independent console experiments with their own input data.
- `final/`: complete scene, identical to iteration 16.
- `solutions/`: runnable answers to exercises 26–30.
- `patches/`: optional changes from one complete step to the next.
- `assets/illustrations/`: chapter reading materials, when present; not runtime assets.

`iteration_23_08` means module 23, iteration 08, not page 08. Examples use an
independent sequence (`example_23_04`). `solution_23_27` answers exercise 27.
Exercise 29 has separate local-axis and world-axis versions. `listings.json`
maps these IDs to files. A runnable iteration may combine several explanations
from the chapter. Type the code, predict the result, and compare it with the
supplied program.

Run the first step with:

```console
python steps/iteration_23_01_skeleton.py
```

Steps 13 and 14 change orientation storage and show local axes. Step 15 adds
animation. Step 16 assembles the final listing with object settings together.

## Run exercise solutions

```console
python solutions/solution_23_26_perspective.py
python solutions/solution_23_27_clipping.py
python solutions/solution_23_28_third_ship.py
python solutions/solution_23_29_local.py
python solutions/solution_23_29_world.py
python solutions/solution_23_30_time.py
```

Solutions 27, 28, and 30 import the supplied `solutions/wireframe_scene.py`, an
identical copy of the final program. Keep it beside those scripts when copying
them elsewhere. Importing it does not open a window. Solutions 26, 27, and 30
are console programs; 28 and both 29 variants open windows. Run the 29 variants
one at a time and keep the camera still while comparing their red X indicators.

## Coordinates and matrix conventions

- Geometry uses point rows `[x, y, z, 1]`; directions use `[dx, dy, dz, 0]`.
- Initially X points right, Y up, and Z forward. Screen Y points down.
- World placement is `vertices @ scale @ orientation @ translation`.
- `get_rotation_matrix()` converts world directions to the rotated frame;
  its transpose converts directions back. Only a pure rotation has this inverse
  obtained simply by transposing.
- Each object's stored orientation maps local directions to world directions.
  Its first three spatial rows are unit local axes expressed in world coordinates.
- Intrinsic updates use `step @ orientation`, in sequential local Z, X, Y order.
  `orientation @ step` updates orientation about a world-axis direction without
  changing the separately stored object position.
- Linear speeds are world units per second, angular speeds radians per second.
  Mouse sensitivity is radians per mouse pixel, so mouse displacement is not
  multiplied by frame duration.
- Edge endpoints have shape `(edge_count, 2, 4)`. Clip to camera `z >= near`
  before projection and division by `w`. Empty results retain `(0, 2, 4)`.
- Screen lines have shape `(visible_edge_count, 2, 2)`. Pygame clips drawing to
  its surface. The code does not explicitly clip to all viewing-frustum planes.
- Both ships share the original mesh and retain independent transform state.
  Local-axis indicators use a display length of 1.6 and do not inherit mesh scale.

This is a transparent wireframe renderer: all surviving edges are drawn,
including edges on the far side. There is no face visibility or depth buffer.
Sequential finite rotations around multiple moving axes approximate continuous
motion; their result can vary slightly with time-step size. Exercise 30 uses
one axis deliberately. Repeated floating-point products can accumulate drift
over very long runs; the chapter does not add a re-orthonormalization algorithm.

## Optional patches

To apply patches, copy iteration 01 to a scratch directory as `main.py`. From
that directory, apply each patch in order with Git:

```console
git apply /path/to/module_23/patches/patch_23_01_to_02.patch
```

Replace the path with your actual patch path; quote it if it contains spaces.
Each patch targets `main.py`. `patches/manifest.json` records its source and
destination stages. All 15 patches were replayed and compared with the complete
step files. Patches are optional; the complete files remain the primary route.

## Geometry source

The Cobra Mk III vertices and edges come from the BBC Micro Elite ship blueprint:
[annotated source](https://elite.bbcelite.com/disc/ship_blueprints_c/variable/ship_cobra_mk_3.html).
The chapter explains which parts of Elite's original rendering are simplified.


## File and listing names

`steps/iteration_MM_NN_name.py` contains runnable learning steps in chapter order.
`examples/example_MM_NN_name.py` contains independent experiments.
`solutions/solution_MM_TT_name.py` contains exercise solutions (TT is the exercise number).
`final/` contains complete programs, where provided. Listing identifiers match file stems;
these numbers are not PDF page numbers. Run each program separately.

`solutions/wireframe_scene.py` is the shared implementation imported by the solution files; keep it beside them.
