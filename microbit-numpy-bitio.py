"""Run on your computer with NumPy, bitio and a USB-connected micro:bit."""
import numpy as np
import microbit


def show_world(world):
    """Convert a 5 x 5 brightness matrix into a micro:bit image."""
    if world.shape != (5, 5):
        raise ValueError("The micro:bit display needs a 5 x 5 matrix.")
    pixels = np.clip(world, 0, 9).astype(int)
    bitmap = ":".join("".join(str(value) for value in row) for row in pixels)
    microbit.display.show(microbit.Image(bitmap))


world = np.eye(5, dtype=int) * 5
print("Original matrix:\n", world)
show_world(world)
microbit.sleep(3000)

world = np.fliplr(world)
print("Reflected matrix:\n", world)
show_world(world)
microbit.sleep(3000)
