from microbit import Image, display, button_a, button_b, accelerometer, sleep

# One asymmetric picture. Each number is a pixel's brightness, from 0 to 9.
initial = Image("90000:90000:90000:99990:00000")


def mirror_world(source, left_right):
    # Read from the old image. Build the complete next world before drawing it.
    result = Image(5, 5)
    for row in range(5):
        for col in range(5):
            if left_right:
                value = source.get_pixel(4 - col, row)
            else:
                value = source.get_pixel(col, 4 - row)
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
        world = mirror_world(world, True)
        display.show(world)
        print(world)
    elif b and not a:
        world = mirror_world(world, False)
        display.show(world)
        print(world)
    sleep(20)
