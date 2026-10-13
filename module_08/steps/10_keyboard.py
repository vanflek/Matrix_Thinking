# Keyboard events change the direction stored in state.
import numpy as np
import pygame as pg

def handle_input(events, state):
    movement = state["vel"]

    for event in events:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                movement[:] = (-1, 0)
            elif event.key == pg.K_DOWN:
                movement[:] = (1, 0)
            elif event.key == pg.K_LEFT:
                movement[:] = (0, -1)
            elif event.key == pg.K_RIGHT:
                movement[:] = (0, 1)

state = {
    "pos": np.array([8, 8], dtype=np.int16),
    "vel": np.array([0, 1], dtype=np.int16),
    "targets": np.array([[2, 3], [5, 10], [12, 6]], dtype=np.int16),
}

pg.init()
screen = pg.display.set_mode((320, 160))
pg.display.set_caption("Press arrows - check the console")
screen.fill((245, 245, 245))
pg.display.flip()
clock = pg.time.Clock()
running = True

# The window receives real keyboard events. No player is drawn yet.
while running:
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False

    if running:
        handle_input(events, state)
        for event in events:
            if event.type == pg.KEYDOWN:
                print(state["vel"])
    clock.tick(60)

pg.quit()
