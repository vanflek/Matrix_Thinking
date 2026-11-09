from microbit import Image, display, button_a, button_b, accelerometer, sleep

# The matrix stores brightness. Different cells start with different values.
initial = Image(
    "01234:"
    "12345:"
    "23456:"
    "34567:"
    "45678"
)

def change_brightness(source, amount):
    # Apply the SAME arithmetic rule everywhere; keep values within 0..9.
    result = Image(5, 5)
    for row in range(5):
        for col in range(5):
            value = source.get_pixel(col, row) + amount
            value = max(0, min(9, value))
            result.set_pixel(col, row, value)
    return result

world = initial.copy()
display.show(world)
print(world)

while True:
    a = button_a.was_pressed()
    b = button_b.was_pressed()

    if accelerometer.was_gesture("shake"):
        world = initial.copy()
        display.show(world)
        print(world)
    elif a and not b:
        world = change_brightness(world, -1)
        display.show(world)
        print(world)
    elif b and not a:
        world = change_brightness(world, 1)
        display.show(world)
        print(world)

    sleep(20)
