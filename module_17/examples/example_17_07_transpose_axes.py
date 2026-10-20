import numpy as np


pixels = np.zeros((2, 4, 3), dtype=np.uint8)
pixels[0, 2] = [255, 0, 0]

pixels_for_pygame = np.transpose(pixels, (1, 0, 2))
print(pixels.shape)
print(pixels_for_pygame.shape)
print(pixels_for_pygame[2, 0])
