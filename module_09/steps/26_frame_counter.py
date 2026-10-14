# Move every six frames
STEP_FRAMES = 6
step_counter = 0

for frame in range(1, 19):
    step_counter += 1

    if step_counter >= STEP_FRAMES:
        step_counter = 0
        print("Step at frame:", frame)
