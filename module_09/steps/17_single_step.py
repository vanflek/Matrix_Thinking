# Combine movement, growth and collision
import numpy as np

def hits_body(new_head, snake, eating):
    if eating:
        body = snake
    else:
        body = snake[1:]

    matches = body == new_head
    same_cell = matches.all(axis=1)

    return same_cell.any()

def do_snake_step(state):
    snake = state["snake"]

    new_head = snake[-1] + state["vel"]
    eating = np.array_equal(new_head, state["apple"])

    if hits_body(new_head, snake, eating):
        state["alive"] = False
        return

    snake = np.vstack((snake, new_head))

    if not eating:
        snake = snake[1:]

    state["snake"] = snake

    if eating:
        state["apple"] = None

state = {
    "snake": np.array([
        [5, 2],
        [5, 3],
        [4, 3],
        [3, 3],
        [3, 4],
    ], dtype=np.int16),
    "vel": np.array([0, 1], dtype=np.int16),
    "apple": np.array([3, 5], dtype=np.int16),
    "alive": True,
}

do_snake_step(state)

print("Alive:", state["alive"])
print("Apple:", state["apple"])
print(state["snake"])
