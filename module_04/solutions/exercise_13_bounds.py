# Correct both components before drawing the circle.
width = 800
height = 600
radius = 30
x = 790
y = 590

if x - radius < 0:
    x = radius
elif x + radius > width:
    x = width - radius

if y - radius < 0:
    y = radius
elif y + radius > height:
    y = height - radius

print("Corrected center:", (x, y))
