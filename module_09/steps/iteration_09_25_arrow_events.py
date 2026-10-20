# Translate two key events into a single permitted turn
import numpy as np

import pygame as pg

def change_direction(state, new_direction):
    if not state["can_turn"]:
        return

    if np.array_equal(new_direction, state["vel"]):
        return

    if np.array_equal(new_direction, -state["vel"]):
        return

    state["vel"] = new_direction
    state["can_turn"] = False

def handle_input(events, state):
    for event in events:
        if event.type == pg.KEYDOWN:
            new_direction = None

            if event.key == pg.K_UP:
                new_direction = np.array([-1, 0], dtype=np.int16)
            elif event.key == pg.K_DOWN:
                new_direction = np.array([1, 0], dtype=np.int16)
            elif event.key == pg.K_LEFT:
                new_direction = np.array([0, -1], dtype=np.int16)
            elif event.key == pg.K_RIGHT:
                new_direction = np.array([0, 1], dtype=np.int16)

            if new_direction is not None:
                change_direction(state, new_direction)


state = {
    "vel": np.array([0, 1], dtype=np.int16),
    "can_turn": True,
}

events = [
    pg.event.Event(pg.KEYDOWN, key=pg.K_UP),
    pg.event.Event(pg.KEYDOWN, key=pg.K_LEFT),
]

handle_input(events, state)

print("Direction:", state["vel"])
print("Can turn:", state["can_turn"])
