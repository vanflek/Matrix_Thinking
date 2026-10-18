import numpy as np


PLAYER_LAYER = 0
BULLET_LAYER = 1
layers = np.zeros((2, 2, 3), dtype=np.uint8)
layers[PLAYER_LAYER, 1, 1] = 1

player = layers[PLAYER_LAYER]
# Write values into a separate region of the same array.
layers[BULLET_LAYER] = player
bullet = layers[BULLET_LAYER]

player.fill(0)
print("Player after clearing:")
print(layers[PLAYER_LAYER])
print("Bullet after clearing the player:")
print(layers[BULLET_LAYER])

# The view still refers to the bullet layer in the original array.
bullet.fill(0)
print("Bullet after clearing through the view:")
print(layers[BULLET_LAYER])
