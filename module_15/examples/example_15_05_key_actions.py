import pygame as pg


# Map key codes to action names without opening a window.
key_actions = {
    pg.K_LEFT: "move_left",
    pg.K_SPACE: "shoot",
}
actions = {"move_left": False, "shoot": False}
key = pg.K_LEFT

print("Known key:", key in key_actions)
if key in key_actions:
    action = key_actions[key]
    actions[action] = True
    print("Action:", action)

print("Move left selected:", actions["move_left"])
print("Action name is a key:", "move_left" in key_actions)
