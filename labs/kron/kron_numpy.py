"""Matrix Thinking: draw a 5x5 world and enlarge it with the NumPy Kronecker product.

Install: python -m pip install numpy pygame
Run:     python kron_numpy.py
No classes, image files or micro:bit are required.
"""
import numpy as np
import pygame

DUCK = np.array([
    [0, 0, 1, 1, 0],
    [0, 0, 1, 1, 1],
    [1, 0, 1, 1, 0],
    [1, 1, 1, 1, 0],
    [0, 1, 1, 0, 0],
], dtype=np.uint8)


def enlarge(world, factor):
    """Each source value scales an entire block of ones."""
    if not isinstance(factor, (int, np.integer)) or factor < 1:
        raise ValueError("factor must be a positive integer")
    block = np.ones((factor, factor), dtype=world.dtype)
    return np.kron(world, block)


def main():
    pygame.init()
    screen = pygame.display.set_mode((1190, 930))
    pygame.display.set_caption("Matrix Thinking — a matrix of blocks")
    font = pygame.font.SysFont("consolas", 18)
    small = pygame.font.SysFont("consolas", 15)
    title = pygame.font.SysFont("arial", 27, bold=True)
    clock = pygame.time.Clock()
    world = DUCK.copy()
    factor = 2
    selected = np.array([0, 2])
    brush = 1  # 1 paint; 0 erase; None inspect
    running = True
    painting = False
    undo_operation = "world = DUCK.copy()"
    ink, paper, blue, yellow = (19, 45, 69), (247, 250, 253), (17, 101, 219), (255, 211, 67)
    palette = np.array([ink, yellow], dtype=np.uint8)
    cell = 24
    views = [((22, 320), False, False), ((172, 320), False, True),
             ((370, 320), True, False), ((760, 320), True, True)]
    buttons = []
    controls = [("x1", "1"), ("x2", "2"), ("x3", "3"), ("Duck", "duck"),
                ("Clear", "clear"), ("Paint", "paint"), ("Erase", "erase"), ("Inspect", "inspect"),
                ("Left", "left"), ("Right", "right"), ("Up", "up"), ("Down", "down"), ("Rotate", "rotate")]
    for i, (label, action) in enumerate(controls):
        row, col = divmod(i, 8)
        buttons.append((pygame.Rect(22 + col * 143, 65 + row * 46, 134, 38), label, action))

    def transform(action):
        nonlocal world, factor, brush, selected, undo_operation, painting
        painting = False
        if action in ("1", "2", "3"):
            factor = int(action)
        elif action == "duck":
            world = DUCK.copy()
            selected = np.array([0, 2])
            undo_operation = "world = DUCK.copy()"
        elif action == "clear":
            world = np.zeros_like(world)
            undo_operation = "world = np.zeros_like(world)"
        elif action in ("paint", "erase", "inspect"):
            brush = {"paint": 1, "erase": 0, "inspect": None}[action]
        elif action == "rotate":
            world = np.rot90(world, k=-1)
            selected = np.array([selected[1], world.shape[1] - 1 - selected[0]])
            undo_operation = "world = np.rot90(world, k=-1)"
        else:
            shift, axis = {"left": (-1, 1), "right": (1, 1), "up": (-1, 0), "down": (1, 0)}[action]
            world = np.roll(world, shift, axis=axis)
            selected[axis] = (selected[axis] + shift) % world.shape[axis]
            undo_operation = f"world = np.roll(world, {shift}, axis={axis})"

    def locate(position):
        for origin, is_output, numbers in views:
            shape = np.array(world.shape) * (factor if is_output else 1)
            c = (position[0] - origin[0]) // cell
            r = (position[1] - origin[1]) // cell
            if 0 <= r < shape[0] and 0 <= c < shape[1]:
                return np.array([r, c]) // (factor if is_output else 1), not is_output and not numbers
        return None, False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                else:
                    keys = {pygame.K_1: "1", pygame.K_2: "2", pygame.K_3: "3", pygame.K_SPACE: "duck",
                            pygame.K_c: "clear", pygame.K_r: "rotate", pygame.K_LEFT: "left", pygame.K_RIGHT: "right",
                            pygame.K_UP: "up", pygame.K_DOWN: "down"}
                    if event.key in keys:
                        transform(keys[event.key])
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button in (1, 3):
                if event.button == 1:
                    clicked = next((action for rect, _, action in buttons if rect.collidepoint(event.pos)), None)
                    if clicked:
                        transform(clicked)
                        continue
                selected_cell, editable = locate(event.pos)
                if selected_cell is not None:
                    selected = selected_cell
                    painting = editable and (brush is not None or event.button == 3)
                    if painting:
                        value = 0 if event.button == 3 else brush
                        world[tuple(selected)] = value  # Matrix indexing changes the drawing.
                        undo_operation = f"world[{selected[0]}, {selected[1]}] = {value}"
            elif event.type == pygame.MOUSEMOTION and painting and (event.buttons[0] or event.buttons[2]):
                selected_cell, editable = locate(event.pos)
                if editable and (event.buttons[2] or brush is not None):
                    selected = selected_cell
                    world[tuple(selected)] = 0 if event.buttons[2] else brush
            elif event.type == pygame.MOUSEBUTTONUP:
                painting = False

        # All changes to the image above are whole-array operations or indexing.
        # One Kronecker product enlarges the entire state, including zeros.
        enlarged = enlarge(world, factor)
        source_rows, source_cols = np.indices(world.shape)
        source_mask = (source_rows == selected[0]) & (source_cols == selected[1])
        block_mask = enlarge(source_mask, factor)
        screen.fill(paper)
        screen.blit(title.render("A small matrix. A bigger world.", True, ink), (22, 20))
        for rect, label, action in buttons:
            active = action == str(factor) or action == {1: "paint", 0: "erase", None: "inspect"}[brush]
            pygame.draw.rect(screen, ink if active else (229, 239, 250), rect, border_radius=5)
            text = small.render(label, True, paper if active else ink)
            screen.blit(text, text.get_rect(center=rect.center))
        screen.blit(font.render("enlarged = np.kron(world, block)", True, blue), (22, 175))
        screen.blit(small.render(f"Shapes: world {world.shape}, block {(factor, factor)}, result {enlarged.shape}", True, ink), (22, 203))
        value = world[tuple(selected)]
        block = np.ones((factor, factor), dtype=world.dtype)
        product = value * block
        repeated = world.repeat(factor, axis=0).repeat(factor, axis=1)
        screen.blit(small.render(f"Selected value: {value}. Each value scales a whole block.", True, ink), (22, 240))
        screen.blit(small.render(f"Same as repeat: {np.array_equal(enlarged, repeated)}", True, blue), (22, 268))
        for array, origin, label in [(block, (610, 230), "block of ones"), (product, (820, 230), f"{value} * block")]:
            screen.blit(small.render(label, True, ink), (origin[0], 208))
            for r, c in np.ndindex(array.shape):
                rect = pygame.Rect(origin[0]+c*20, origin[1]+r*20, 20, 20)
                pygame.draw.rect(screen, yellow if array[r,c] else ink, rect)
                pygame.draw.rect(screen, blue, rect, 1)
                text = small.render(str(array[r,c]), True, ink if array[r,c] else paper)
                screen.blit(text, text.get_rect(center=rect.center))
        labels = ["SOURCE PIXELS", "SOURCE MATRIX", "KRONECKER PIXELS", "KRONECKER MATRIX"]
        for (origin, is_output, numbers), label in zip(views, labels):
            array = enlarged if is_output else world
            mask = block_mask if is_output else source_mask
            colors = palette[array]
            screen.blit(small.render(label, True, ink), (origin[0], 298))
            # Loops only draw the already computed matrices; they do not enlarge them.
            for r, c in np.ndindex(array.shape):
                rect = pygame.Rect(origin[0] + c * cell, origin[1] + r * cell, cell, cell)
                color = tuple(int(v) for v in colors[r, c])
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, (120, 145, 169), rect, 1)
                if mask[r, c]:
                    pygame.draw.rect(screen, (255, 130, 25), rect.inflate(-2, -2), 2)
                if numbers:
                    text = font.render(str(array[r, c]), True, ink if array[r, c] else paper)
                    screen.blit(text, text.get_rect(center=rect.center))
        r, c = selected
        for i, text in enumerate([
            f"world[{r}, {c}] = {world[r,c]} becomes enlarged[{r*factor}:{(r+1)*factor}, {c*factor}:{(c+1)*factor}]",
            f"One cell becomes {factor} x {factor} = {factor*factor} cells. Lit: {np.count_nonzero(world)} -> {np.count_nonzero(enlarged)}",
            "Last source operation: " + undo_operation,
            "Draw in SOURCE PIXELS. Click either matrix or the result to trace the corresponding block.",
            "Arrows: roll | R: rotate | C: clear | Space: duck | 1/2/3: block factor | Escape: close",
        ]):
            screen.blit(small.render(text, True, ink), (22, 715 + i * 28))
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()


if __name__ == "__main__":
    main()
