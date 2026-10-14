# Module 9: Snake — Movement as a Matrix Operation

Install NumPy and Pygame, then run `python snake.py`.
Arrow keys steer the snake; Escape closes the window.
The initial three-cell snake is centered automatically. Use ROWS >= 1 and COLS >= 3.

## Learning steps

Every file is independent. Steps 01–26 print results to the console; step 27 opens the game.
Type the examples from the chapter first, predict the output, and use these files as checkpoints.

- [steps/01_coordinates.py](steps/01_coordinates.py) — Coordinate matrix, tail and head
- [steps/02_vstack.py](steps/02_vstack.py) — Join matrices by rows
- [steps/03_hstack.py](steps/03_hstack.py) — Join matrices by columns
- [steps/04_append_row.py](steps/04_append_row.py) — Append a coordinate vector as one row
- [steps/05_move.py](steps/05_move.py) — Add a head and remove the old tail
- [steps/06_growth.py](steps/06_growth.py) — Keep the tail when eating an apple
- [steps/07_no_growth.py](steps/07_no_growth.py) — Preserve length when the apple is elsewhere
- [steps/08_free_mask.py](steps/08_free_mask.py) — Mark free cells with a Boolean mask
- [steps/09_argwhere_where.py](steps/09_argwhere_where.py) — Compare coordinate representations
- [steps/10_random_apple.py](steps/10_random_apple.py) — Choose a free cell after checking the result
- [steps/11_empty_field.py](steps/11_empty_field.py) — Handle a field with no free cells
- [steps/12_spawn_function.py](steps/12_spawn_function.py) — Return coordinates or None
- [steps/13_coordinates_to_field.py](steps/13_coordinates_to_field.py) — Use paired coordinate indices
- [steps/14_field_and_apple.py](steps/14_field_and_apple.py) — Build occupancy before choosing an apple
- [steps/15_collision_arrays.py](steps/15_collision_arrays.py) — Reduce component matches to a collision flag
- [steps/16_collision_function.py](steps/16_collision_function.py) — Check free cells, body and departing tail
- [steps/17_single_step.py](steps/17_single_step.py) — Combine movement, growth and collision
- [steps/18_win.py](steps/18_win.py) — Fill the last free cell
- [steps/19_respawn.py](steps/19_respawn.py) — Grow and place the next apple
- [steps/20_wrap.py](steps/20_wrap.py) — Check all four boundaries on a rectangular field
- [steps/21_wrapped_step.py](steps/21_wrapped_step.py) — Integrate edge wrapping into a movement step
- [steps/22_opposite_direction.py](steps/22_opposite_direction.py) — Reject the opposite direction
- [steps/23_two_turn_problem.py](steps/23_two_turn_problem.py) — Reproduce two turns before a movement step
- [steps/24_turn_permission.py](steps/24_turn_permission.py) — Allow one turn per completed step
- [steps/25_arrow_events.py](steps/25_arrow_events.py) — Translate two key events into a single permitted turn
- [steps/26_frame_counter.py](steps/26_frame_counter.py) — Move every six frames
- [steps/27_snake.py](steps/27_snake.py) — Complete Snake game
- [solutions/26_colored_head.py](solutions/26_colored_head.py) — Colored Head
- [solutions/27_score.py](solutions/27_score.py) — Score
- [solutions/28_speed.py](solutions/28_speed.py) — Speed
- [solutions/29_walls.py](solutions/29_walls.py) — Walls
- [solutions/30_restart.py](solutions/30_restart.py) — Restart

Each solution is a separate complete game based on the final listing. They are not cumulative patches.
