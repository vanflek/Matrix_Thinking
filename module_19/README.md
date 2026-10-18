# Module 19 - Trigonometry: One Point, Different Representations

Describe the same point with Cartesian coordinates or distance and direction.
Explore array-based trigonometry, coordinate conversion, properties, dependency
tracking and reusable graph images in a small interactive laboratory.

## Requirements and launch

Checked with Python 3.13.7, NumPy 2.5.3 and Pygame 2.6.1.
From this folder:

```console
python -m pip install -r requirements.txt
python final/trigonometry_lab.py
```

Only NumPy and Pygame are runtime dependencies. Every Python file is standalone.
There are no runtime images or external data files. The illustrations are reading
materials; they are not loaded by the programs. Pygame selects the Arial system
font when available and otherwise uses its font fallback.

## Controls

- Left / Right: increase / decrease the angle by one degree per key-down event.
- Up / Down: increase / decrease the radius by five units per key-down event.
- Escape or window close: exit.
- No held-key movement is enabled. Pending increments are summed for a frame.
- The angle is normalized on assignment to [0, 360); the radius is clamped at zero.
- A mathematical unit equals a pixel in the main scene. CELL_SIZE only controls
  grid spacing. The scene is 640 pixels wide inside a 900 x 480 window.

## Folders and identifiers

- `steps/`: complete runnable iterations, in reading order.
- `examples/`: independent introductory experiments; 01-06 print results,
  and 07 opens a Pygame window.
- `solutions/`: five independent exercise solutions. Do not apply them in order;
  each starts from the final lab, except 29, which starts from example 07.
- `final/`: the complete lab, identical to iteration 10.
- `patches/`: transitions between adjacent iterations for a working `main.py`.
- `assets/illustrations/`: English-labeled diagrams and actual program captures.

The number 19 is the module. The final number is an example or iteration number,
not a page number. Examples and iterations have separate sequences.

## Runnable iterations

| File | Result |
|---|---|
| `steps/iteration_19_01_skeleton.py` | Five classes, a circle and a fixed vector |
| `steps/iteration_19_02_keyboard.py` | Angle and radius changes from key events |
| `steps/iteration_19_03_projections.py` | Signed vector components on the axes |
| `steps/iteration_19_04_values.py` | Separate scene area and numerical panel |
| `steps/iteration_19_05_graphs.py` | Full curves and current angle markers |
| `steps/iteration_19_06_properties.py` | Controlled angle and radius properties |
| `steps/iteration_19_07_needs_update.py` | Skip unchanged mathematical state |
| `steps/iteration_19_08_dependencies.py` | Cache results according to dependencies |
| `steps/iteration_19_09_cached_images.py` | Reusable background and graph surfaces |
| `steps/iteration_19_10_final.py` | Labeled graph axes and documented final code |

## Independent examples

| File | Experiment |
|---|---|
| `examples/example_19_01_vector_length.py` | Vector length with np.sqrt |
| `examples/example_19_02_single_angle.py` | Degrees, radians and one endpoint |
| `examples/example_19_03_angles_loop.py` | Calculate endpoints with a Python loop |
| `examples/example_19_04_angles_numpy.py` | Calculate endpoints with NumPy arrays |
| `examples/example_19_05_columns_loop.py` | Pair coordinate components in a loop |
| `examples/example_19_06_column_stack.py` | Pair coordinates with np.column_stack |
| `examples/example_19_07_circle.py` | Draw a circle from sampled points |

## Exercise solutions

| File | Change |
|---|---|
| `solutions/solution_19_26_angle_step.py` | Choose a 1-degree or 10-degree turn step |
| `solutions/solution_19_27_reset.py` | Reset source parameters through model properties |
| `solutions/solution_19_28_toggle_projections.py` | Change visibility without invalidating geometry |
| `solutions/solution_19_29_ellipse.py` | Use independent X and Y scales in the circle example |
| `solutions/solution_19_30_opposite_point.py` | Compute a diametrically opposite endpoint |

Solution 26 adds keys 1 and 2; the selected step appears in the window title.
Solution 27 adds R; reset is processed before pending arrow increments.
Solution 28 adds P; two toggle events in one input batch cancel each other.
Solution 29 produces an ellipse in its own window. Solution 30 draws the opposite
point and a diameter without adding extra trigonometric calculations.

## Sequential patches

Copy `steps/iteration_19_01_skeleton.py` to `main.py` in this folder. With Git
available, apply patches one at a time:

```console
git -c core.autocrlf=false apply --check patches/patch_19_01_to_02.patch
git -c core.autocrlf=false apply patches/patch_19_01_to_02.patch
python main.py
```

Continue with 02_to_03 through 09_to_10. Run each result before continuing.
The command-level setting preserves the LF line endings used in these files;
it does not change your Git configuration. If your editor changes line endings,
restore LF before applying a patch. Manual edits must match the source iteration.
You can always run the full file in `steps/` instead of applying patches.

## How the state stays consistent

The model owns radius and angle properties. Setters enforce constraints and mark
derived data stale only when a normalized/clamped parameter actually changes.
GameLogic applies input before checking needs_update. The first calculation is
mandatory. Until update runs, changing a source property can leave derived data
temporarily stale; GameApp always updates before drawing.

Fixed circle samples and full graph curves are prepared once. Current sin/cos
depend on angle; the scaled circle depends on radius; the endpoint depends on both.
The view stores a grid image and clean graph bases, copies each graph base before
adding its current marker, and draws an opaque information panel after the scene.
The circle's screen conversion and dynamic drawing still occur each frame.

Angles are degrees in model state and radians at NumPy trigonometric calls.
Circle samples exclude 360 degrees, while graph samples include both endpoints.
Floating-point residuals near zero are expected; formatted output is not the
underlying stored value. Graph axes show degrees and values from -1 to 1.

## Validation

All 23 programs were executed: six console examples and 17 windowed programs.
Windowed programs rendered a frame, processed exit and cleaned up Pygame.
All nine patches were applied in sequence and compared byte-for-byte to their
target iterations and final program. Additional checks cover cardinal directions,
angle wrapping, radius constraints, property assignments, unchanged-array reuse,
clean graph bases, input changes and all five exercise variants.
The chapter's complete final listing was compared structurally with the file.
