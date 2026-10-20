# Converting a value does not change the stored coordinate.
y = 300.25
print("Coordinate for drawing:", int(y))
print("Stored coordinate:", y)

# Discarding the fraction on every update prevents accumulation.
y = 300
for step in range(4):
    y = int(y + 0.25)
    print("Truncated update:", y)

# Preserve the fraction and convert only for drawing.
y = 300
for step in range(4):
    y = y + 0.25
    print("Stored:", y, "For drawing:", int(y))
