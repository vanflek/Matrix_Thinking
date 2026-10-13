# Count frames before allowing the next movement step.
STEP_FRAMES = 6
step_counter = 0
for frame in range(1, 13):
    step_counter += 1
    if step_counter >= STEP_FRAMES:
        step_counter = 0
        print("Move on frame", frame)
