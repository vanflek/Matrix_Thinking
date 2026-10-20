# Module 9: Snake — Movement as a Matrix Operation

Install NumPy and Pygame, then run `python final/snake.py`.
Arrow keys steer the snake; Escape closes the window.
The initial three-cell snake is centered automatically. Use ROWS >= 1 and COLS >= 3.

## Learning steps

Every file is independent. Steps 01–26 print results to the console; step 27 opens the game.
Type the examples from the chapter first, predict the output, and use these files as checkpoints.

- [steps/iteration_09_01_coordinates.py](steps/iteration_09_01_coordinates.py) — Coordinate matrix, tail and head
- [steps/iteration_09_02_vstack.py](steps/iteration_09_02_vstack.py) — Join matrices by rows
- [steps/iteration_09_03_hstack.py](steps/iteration_09_03_hstack.py) — Join matrices by columns
- [steps/iteration_09_04_append_row.py](steps/iteration_09_04_append_row.py) — Append a coordinate vector as one row
- [steps/iteration_09_05_move.py](steps/iteration_09_05_move.py) — Add a head and remove the old tail
- [steps/iteration_09_06_growth.py](steps/iteration_09_06_growth.py) — Keep the tail when eating an apple
- [steps/iteration_09_07_no_growth.py](steps/iteration_09_07_no_growth.py) — Preserve length when the apple is elsewhere
- [steps/iteration_09_08_free_mask.py](steps/iteration_09_08_free_mask.py) — Mark free cells with a Boolean mask
- [steps/iteration_09_09_argwhere_where.py](steps/iteration_09_09_argwhere_where.py) — Compare coordinate representations
- [steps/iteration_09_10_random_apple.py](steps/iteration_09_10_random_apple.py) — Choose a free cell after checking the result
- [steps/iteration_09_11_empty_field.py](steps/iteration_09_11_empty_field.py) — Handle a field with no free cells
- [steps/iteration_09_12_spawn_function.py](steps/iteration_09_12_spawn_function.py) — Return coordinates or None
- [steps/iteration_09_13_coordinates_to_field.py](steps/iteration_09_13_coordinates_to_field.py) — Use paired coordinate indices
- [steps/iteration_09_14_field_and_apple.py](steps/iteration_09_14_field_and_apple.py) — Build occupancy before choosing an apple
- [steps/iteration_09_15_collision_arrays.py](steps/iteration_09_15_collision_arrays.py) — Reduce component matches to a collision flag
- [steps/iteration_09_16_collision_function.py](steps/iteration_09_16_collision_function.py) — Check free cells, body and departing tail
- [steps/iteration_09_17_single_step.py](steps/iteration_09_17_single_step.py) — Combine movement, growth and collision
- [steps/iteration_09_18_win.py](steps/iteration_09_18_win.py) — Fill the last free cell
- [steps/iteration_09_19_respawn.py](steps/iteration_09_19_respawn.py) — Grow and place the next apple
- [steps/iteration_09_20_wrap.py](steps/iteration_09_20_wrap.py) — Check all four boundaries on a rectangular field
- [steps/iteration_09_21_wrapped_step.py](steps/iteration_09_21_wrapped_step.py) — Integrate edge wrapping into a movement step
- [steps/iteration_09_22_opposite_direction.py](steps/iteration_09_22_opposite_direction.py) — Reject the opposite direction
- [steps/iteration_09_23_two_turn_problem.py](steps/iteration_09_23_two_turn_problem.py) — Reproduce two turns before a movement step
- [steps/iteration_09_24_turn_permission.py](steps/iteration_09_24_turn_permission.py) — Allow one turn per completed step
- [steps/iteration_09_25_arrow_events.py](steps/iteration_09_25_arrow_events.py) — Translate two key events into a single permitted turn
- [steps/iteration_09_26_frame_counter.py](steps/iteration_09_26_frame_counter.py) — Move every six frames
- [steps/iteration_09_27_snake.py](steps/iteration_09_27_snake.py) — Complete Snake game
- [solutions/solution_09_26_colored_head.py](solutions/solution_09_26_colored_head.py) — Colored Head
- [solutions/solution_09_27_score.py](solutions/solution_09_27_score.py) — Score
- [solutions/solution_09_28_speed.py](solutions/solution_09_28_speed.py) — Speed
- [solutions/solution_09_29_walls.py](solutions/solution_09_29_walls.py) — Walls
- [solutions/solution_09_30_restart.py](solutions/solution_09_30_restart.py) — Restart

Each solution is a separate complete game based on the final listing. They are not cumulative patches.


## File and listing names

`steps/iteration_MM_NN_name.py` contains runnable learning steps in chapter order.
`examples/example_MM_NN_name.py` contains independent experiments.
`solutions/solution_MM_TT_name.py` contains exercise solutions (TT is the exercise number).
`final/` contains complete programs, where provided. Listing identifiers match file stems;
these numbers are not PDF page numbers. Run each program separately.
