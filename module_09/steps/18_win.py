# Fill the last free cell
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

def fill_field(matrix, snake):
    matrix[:] = 0
    matrix[snake[:, 0], snake[:, 1]] = 5

def spawn_apple(matrix):
    free_cells = np.argwhere(matrix == 0)

    if len(free_cells) == 0:
        return None

    index = np.random.randint(len(free_cells))
    return free_cells[index]

matrix = np.zeros((1, 3), dtype=np.uint8)

state = {
    "snake": np.array([
        [0, 0],
        [0, 1],
    ], dtype=np.int16),
    "vel": np.array([0, 1], dtype=np.int16),
    "apple": np.array([0, 2], dtype=np.int16),
    "alive": True,
    "won": False,
}

do_snake_step(state)

if state["alive"]:
    fill_field(matrix, state["snake"])

    if state["apple"] is None:
        state["apple"] = spawn_apple(matrix)
        state["won"] = state["apple"] is None

    if state["apple"] is not None:
        row, col = state["apple"]
        matrix[row, col] = 3

print("Alive:", state["alive"])
print("Won:", state["won"])
print("Apple:", state["apple"])
print(matrix)
