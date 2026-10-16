import numpy as np

symbols = np.array(["@", ".", " "], dtype="<U1")
brightness = np.array([0.0, 127.5, 255.0])

np.savez(
    "palette_example.npz",
    symbols=symbols,
    brightness=brightness
)

data = np.load("palette_example.npz")
print(data.files)

loaded_symbols = data["symbols"]
loaded_brightness = data["brightness"]
data.close()

print(loaded_symbols)
print(loaded_brightness)
print(loaded_symbols.shape, loaded_brightness.shape)
print(loaded_symbols.dtype, loaded_brightness.dtype)
