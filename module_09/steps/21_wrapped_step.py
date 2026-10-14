# Integrate edge wrapping into a movement step
import numpy as np

def hits_body(new_head, snake, eating):
    if eating:
        body = snake
    else:
        body = snake[1:]

    matches = body == new_head
    same_cell = matches.all(axis=1)

    return same_cell.any()

def do_snake_step(state, field_size):
    snake = state["snake"]

    new_head = (snake[-1] + state["vel"]) % field_size
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
    "snake": np.array([[1, 3], [1, 4], [1, 5]], dtype=np.int16),
    "vel": np.array([0, 1], dtype=np.int16),
    "apple": np.array([0, 0], dtype=np.int16),
    "alive": True,
}
do_snake_step(state, np.array([4, 6]))
print(state["snake"])
