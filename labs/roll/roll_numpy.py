import numpy as np
import pygame

pygame.init()
screen = pygame.display.set_mode((1000, 620))
pygame.display.set_caption("Matrix Thinking: move the whole world")
pygame.key.set_repeat(220, 110)

font = pygame.font.SysFont("consolas", 24)
small_font = pygame.font.SysFont("consolas", 18)
clock = pygame.time.Clock()

size = 10
cell_size = 40
field_x, matrix_x, top = 40, 560, 150

initial = np.zeros((size, size), dtype=np.uint8)
initial[4, 4] = 1
world = initial.copy()

duck = np.array([
    [0, 0, 1, 1, 0],
    [0, 0, 1, 1, 1],
    [1, 0, 1, 1, 0],
    [1, 1, 1, 1, 0],
    [0, 1, 1, 0, 0],
], dtype=np.uint8)

moves = {
    pygame.K_LEFT:  (-1, 1),
    pygame.K_RIGHT: (1, 1),
    pygame.K_UP:    (-1, 0),
    pygame.K_DOWN:  (1, 0),
}

operation = "world[4, 4] = 1"
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            elif event.key in moves:
                shift, axis = moves[event.key]
                world = np.roll(world, shift, axis=axis)
                operation = f"world = np.roll(world, {shift}, axis={axis})"

            elif event.key == pygame.K_SPACE:
                initial = np.zeros((size, size), dtype=np.uint8)
                initial[2:7, 2:7] = duck
                world = initial.copy()
                operation = "A duck is now stored in the matrix."

            elif event.key == pygame.K_c:
                initial = np.zeros((size, size), dtype=np.uint8)
                initial[4, 4] = 1
                world = initial.copy()
                operation = "One cell is now stored in the matrix."

            elif event.key == pygame.K_r:
                world = initial.copy()
                operation = "world = initial.copy()"

        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION):
            buttons = pygame.mouse.get_pressed()
            if event.type == pygame.MOUSEBUTTONDOWN:
                paint = event.button == 1
                erase = event.button == 3
            else:
                paint, erase = buttons[0], buttons[2]

            x, y = event.pos
            column = (x - field_x) // cell_size
            row = (y - top) // cell_size
            if (paint or erase) and 0 <= row < size and 0 <= column < size:
                world[row, column] = 1 if paint else 0
                operation = f"world[{row}, {column}] = {world[row, column]}"

    screen.fill("#F8FAF7")
    screen.blit(font.render("THE WORLD", True, "#132D45"), (40, 35))
    screen.blit(font.render("THE SAME WORLD AS NUMBERS", True, "#132D45"), (560, 35))
    screen.blit(small_font.render(operation, True, "#1165DB"), (40, 90))

    for row in range(size):
        for column in range(size):
            value = int(world[row, column])
            colour = "#FFD33D" if value else "#EAF0F6"

            for left in (field_x, matrix_x):
                rectangle = pygame.Rect(
                    left + column * cell_size,
                    top + row * cell_size,
                    cell_size - 3,
                    cell_size - 3,
                )
                pygame.draw.rect(screen, colour, rectangle, border_radius=4)
                if left == matrix_x:
                    number = font.render(str(value), True, "#132D45")
                    screen.blit(number, number.get_rect(center=rectangle.center))

    controls = [
        "Arrows: roll | Space: duck | C: one cell | R: reset | Esc: quit",
        "Draw on the left: left mouse = 1, right mouse = 0.",
    ]
    for line, text in enumerate(controls):
        screen.blit(small_font.render(text, True, "#132D45"), (40, 565 + line * 25))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
