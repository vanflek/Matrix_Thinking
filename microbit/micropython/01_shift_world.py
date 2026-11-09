from microbit import Image, display, button_a, button_b, sleep

# Each row describes five LEDs. Values are brightness, from 0 to 9.
initial = Image(
    "09000:"
    "09900:"
    "00000:"
    "00000:"
    "00000"
)

world = initial.copy()
display.show(world)
print(world)

while True:
    # A: transform the whole world by one row. The new top row is zero.
    if button_a.was_pressed():
        world = world.shift_down(1)
        display.show(world)
        print(world)

    # B: restore the original world and try a different prediction.
    if button_b.was_pressed():
        world = initial.copy()
        display.show(world)
        print(world)

    sleep(20)
