import numpy as np

numerator = np.array([6.0, 4.0, 9.0])
denominator = np.array([2.0, 0.0, 3.0])
allowed = denominator != 0
result = np.zeros_like(numerator)
np.divide(numerator, denominator, out=result, where=allowed)

print(allowed)
print(result)
