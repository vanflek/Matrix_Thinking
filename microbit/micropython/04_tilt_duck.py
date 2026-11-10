from microbit import Image, display, accelerometer, sleep

# The same 5 x 5 duck, always kept unchanged.
initial = Image("00090:00999:99990:09990:00900")


def axis_state(reading, previous):
    # A wide neutral band keeps a held tilt from repeatedly toggling the image.
    if reading < -300:
        return True
    if reading > 300:
        return False
    return previous


def reflect_world(source, left_right, top_bottom):
    result = Image(5, 5)
    for row in range(5):
        for col in range(5):
            source_row = 4 - row if top_bottom else row
            source_col = 4 - col if left_right else col
            result.set_pixel(col, row, source.get_pixel(source_col, source_row))
    return result


left_right = False
top_bottom = False
world = initial.copy()
display.show(world)

while True:
    if accelerometer.was_gesture("shake"):
        left_right = False
        top_bottom = False
        world = initial.copy()
        display.show(world)
        sleep(300)
    else:
        next_left_right = axis_state(accelerometer.get_x(), left_right)
        next_top_bottom = axis_state(accelerometer.get_y(), top_bottom)
        if next_left_right != left_right or next_top_bottom != top_bottom:
            left_right = next_left_right
            top_bottom = next_top_bottom
            world = reflect_world(initial, left_right, top_bottom)
            display.show(world)
    sleep(40)
