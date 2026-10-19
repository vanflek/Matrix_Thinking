# Module 22 - Raycasting and Thinking in Masks

Turn a matrix maze into a first-person view. Build and inspect the data path:
coordinates, valid addresses, wall flags, first-hit indices, depth, screen strips,
and perspective floor segments. Then compare full-array, batched, and active-ray
search while preserving their outputs.

## Install and run

Tested with Python 3.13.7, NumPy 2.5.3, and Pygame 2.6.1.
From this module's folder:

```console
python -m pip install -r requirements.txt
cd final
python maze_raycasting.py
```

To start at the beginning, open a terminal in `steps/` and run:

```console
python iteration_22_01_skeleton.py
```

The programs load `maze.npy` relative to the **current working directory**.
The same supplied map is included in `steps/`, `solutions/`, and `final/`.
Run from the folder containing the selected script and map, or set that folder
as the working directory in your IDE. Copy both files if making a scratch copy.
Console examples in `examples/` define their own input arrays and need no map.
No external image or font file is required at runtime.

## Controls

| Input | Action |
| --- | --- |
| W / S | Forward / backward relative to the view direction |
| A / D | Strafe left / right without turning |
| Horizontal mouse movement | Turn the view |
| Escape or window close | Exit |

Use an English keyboard layout for letter controls. From iteration 02 onward,
the program captures the mouse and hides the system cursor; Escape releases it
and exits. Iteration 01 shows a stationary observer. Later diagnostic iterations
temporarily show the map or camera-coordinate geometry to expose intermediate
results. The final program displays the first-person view.

## Coordinates, map, and assumptions

- `maze[row, column]`: 0 is a wall; 1 is a passage. The supplied uint8 map has
  16 rows and 32 columns. `CELL_SIZE = 30`, giving a 480-by-960-unit world.
- Positions use `[y, x]`, with y downward and x rightward. Angle zero looks
  right; a positive angle turns toward increasing y. Angles are in radians.
- The supplied start cell is `(8, 16)`, at world position `[255, 495]`.
  When using a map from module 13, choose an existing passage in `GameModel`.
  Smaller maps may not contain the supplied start indices. Keep 0/1 meanings.
- `np.repeat` enlarges the colored map image, not the underlying maze matrix.
- World bounds are checked before map indexing. Movement uses short axis-aligned
  substeps to avoid skipping a wall cell. The observer has a point collision
  model, not a circular body with a radius.
- Ray-array axis 0 is distance samples; axis 1 is rays. Finite samples approximate
  a continuous intersection: even a small step may miss a very short corner
  crossing. This chapter does not implement exact grid traversal (DDA).
- A no-hit ray retains its last sampled distance and `has_wall = False`.
  Exiting the map stops its active search but does not create a wall there.
- Wall strips use forward depth, not oblique ray length. In the final program,
  ray angles pass through evenly spaced screen-strip centers.
- Camera segments store `[side, depth]`, not world `[y, x]`. Near clipping uses
  `depth >= 1.0` before perspective division. The camera height is `CELL_SIZE/2`.
- Final drawing order: ceiling and floor, floor grid, walls, display update.
  Wall colors use ray distance for fading; wall heights use forward depth.

## Folders and listing IDs

- `steps/`: complete runnable iterations in reading order.
- `examples/`: independent console experiments.
- `solutions/`: separate solutions to exercises 26–30.
- `final/`: complete program, identical to iteration 23.
- `patches/`: optional changes between steps and branches from the final program.
- `assets/illustrations/`: chapter diagrams and captures, with English internal
  labels; these files are reading materials, not runtime dependencies.

`iteration_22_04` means module 22, iteration 04, not page 04. Examples have their
own sequence: `example_22_04`. `solution_22_26` answers exercise 26. The same IDs
appear in the chapter. A chapter iteration can contain several edit fragments;
its file is the complete runnable state after those edits. Type, predict, and
run your own version, using these files to compare results.

## Runnable iterations

| File | Result / topic |
| --- | --- |
| `steps/iteration_22_01_skeleton.py` | Top-down map, grid, and stationary observer |
| `steps/iteration_22_02_movement.py` | Normalized keyboard movement, mouse look, and wall checks |
| `steps/iteration_22_03_rays.py` | Sample points and rays on the map |
| `steps/iteration_22_04_valid_addresses.py` | Valid map-address mask |
| `steps/iteration_22_05_wall_flags.py` | Read wall flags through the valid-address mask |
| `steps/iteration_22_06_any.py` | Check whether each ray hits a wall with any |
| `steps/iteration_22_07_argmax.py` | Locate first hits with argmax and has_wall |
| `steps/iteration_22_08_endpoints.py` | Select endpoints through paired index arrays |
| `steps/iteration_22_09_first_person.py` | First-person wall strips (perspective still approximate) |
| `steps/iteration_22_10_wall_color.py` | Distance-dependent wall colors |
| `steps/iteration_22_11_forward_depth.py` | Use forward depth for wall heights |
| `steps/iteration_22_12_stripe_centers.py` | Compute ray angles from screen-strip centers |
| `steps/iteration_22_13_floor_ceiling.py` | Ceiling and floor backgrounds |
| `steps/iteration_22_14_dense_samples.py` | Dense sampling and its computational cost |
| `steps/iteration_22_15_broadcasting.py` | Replace repeated coordinate grids with broadcasting |
| `steps/iteration_22_16_batches.py` | Search in batches of 256 samples |
| `steps/iteration_22_17_active_rays.py` | Continue only active rays and retain original IDs |
| `steps/iteration_22_18_floor_segments.py` | World floor segments, shown from above |
| `steps/iteration_22_19_camera_segments.py` | Floor segments in camera coordinates |
| `steps/iteration_22_20_near_clipping.py` | Near clipping with a loop; diagnostic camera view |
| `steps/iteration_22_21_floor_projection.py` | Perspective floor grid behind the walls |
| `steps/iteration_22_22_numpy_clipping.py` | Vectorized near clipping with divide, where, and out |
| `steps/iteration_22_23_complete.py` | Complete first-person program with hit-count caption |

## Independent examples

| File | Result / topic |
| --- | --- |
| `examples/example_22_01_maze_data.py` | Map values and a continuous position |
| `examples/example_22_02_normalization.py` | Vector length and movement normalization |
| `examples/example_22_03_cell_checks.py` | Cell indices, walls, and world bounds |
| `examples/example_22_04_ray_samples.py` | Sample points along one ray |
| `examples/example_22_05_meshgrid.py` | All angle-distance combinations with meshgrid |
| `examples/example_22_06_ray_coordinates.py` | Coordinate matrices for several rays |
| `examples/example_22_07_valid_addresses.py` | Coordinate-to-index conversion and valid addresses |
| `examples/example_22_08_masked_walls.py` | Masked map reading and wall flags |
| `examples/example_22_09_any.py` | One any result per ray |
| `examples/example_22_10_argmax.py` | First maximum and the all-False case |
| `examples/example_22_11_endpoint_indices.py` | Paired indexing for endpoints |
| `examples/example_22_12_perspective.py` | Perspective wall height |
| `examples/example_22_13_wall_colors.py` | Wall brightness and RGB broadcasting |
| `examples/example_22_14_forward_depth.py` | Ray length versus forward depth |
| `examples/example_22_15_stripe_centers.py` | Screen-strip centers and relative angles |
| `examples/example_22_16_sampling_cost.py` | Sample count and array sizes |
| `examples/example_22_17_broadcasting_rays.py` | Coordinate broadcasting without meshgrid |
| `examples/example_22_18_batch_indices.py` | Local and global sample indices in a batch |
| `examples/example_22_19_active_ray_ids.py` | Active-ray columns and original ray IDs |
| `examples/example_22_20_compare_and_time.py` | Shape checks, allclose, and perf_counter |
| `examples/example_22_21_floor_segments.py` | Stack two endpoints into a segment array |
| `examples/example_22_22_camera_coordinates.py` | Coordinates relative to the camera |
| `examples/example_22_23_near_intersection.py` | Intersection with the near boundary |
| `examples/example_22_24_floor_projection.py` | Perspective projection of floor points |
| `examples/example_22_25_masked_divide.py` | Masked division with a prepared output array |

## Practical solutions

| File | Result / topic |
| --- | --- |
| `solutions/solution_22_26_field_of_view.py` | Field of view: change FOV_DEGREES to 40, 60, or 90 |
| `solutions/solution_22_27_distance_bands.py` | Four distance bands for wall colors |
| `solutions/solution_22_28_grid_step.py` | Independent GRID_STEP values: 15, 30, or 60 |
| `solutions/solution_22_29_clipping_lab.py` | Console comparison of loop and NumPy clipping, including empty inputs |
| `solutions/solution_22_30_search_benchmark.py` | Console correctness comparison across 60 scenes, then search-only timing |

Solutions are independent, not cumulative. Solutions 26–28 run a window;
29–30 print console results. Solution 30 needs `maze.npy`; it checks two maps,
five passage-center positions, and six angles. It checks shapes, compares
coordinates and distances with an explicit tolerance, and checks Boolean flags
exactly. It restores the supplied scene before timing each search method.
Timings vary by machine, scene, and workload; rendering is excluded.

## Optional patches

Copy iteration 01 to a scratch folder as `main.py`, along with `maze.npy`.
Each patch uses `a/main.py` and `b/main.py` headers and is applied in that folder:

```console
git apply --check path/to/patch_22_01_to_02.patch
git apply path/to/patch_22_01_to_02.patch
python main.py
```

Apply step patches in numeric order. Each `patch_22_final_to_solution_N.patch`
starts independently from a fresh copy of `final/maze_raycasting.py` as `main.py`.
The patches for solutions 29 and 30 replace the window entry point with console
experiments; 29 also replaces the game classes with standalone clipping functions.
Git and patches are optional: complete programs are supplied for every step.
See `patches/README.md` and `patches/manifest.json` for exact source/target pairs.

## Verification

The working sources have automated startup checks under Pygame's dummy SDL driver
(two frames and a close event), plus console checks. Additional numerical checks
cover agreement between three search methods, camera coordinates, projection,
near clipping, movement, and map bounds. This is not a manual mouse/focus test or
a guarantee for every possible input. The final printed listing matches the
final Python file. Local packaging checks verify all patch targets byte for byte.
