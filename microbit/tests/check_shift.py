"""Desktop control-flow check; does not execute micro:bit firmware."""
from pathlib import Path
import runpy
import sys
import types

class Image:
    def __init__(self, rows):
        self.rows = tuple(tuple(map(int, row)) for row in rows.split(':')) if isinstance(rows, str) else tuple(rows)
    def copy(self):
        return Image(self.rows)
    def shift_down(self, n):
        return Image(((0,)*5,)*n + self.rows[:5-n])

class StopCheck(Exception): pass
sequence = ['', 'A', 'A', 'B', 'A', 'A', 'A', 'A', 'A', 'B']
position = 0
shown = []

def sleep(_):
    global position
    position += 1
    if position == len(sequence): raise StopCheck()

mock = types.ModuleType('microbit')
mock.Image = Image
mock.display = types.SimpleNamespace(show=lambda image: shown.append(image.rows))
mock.button_a = types.SimpleNamespace(was_pressed=lambda: sequence[position] == 'A')
mock.button_b = types.SimpleNamespace(was_pressed=lambda: sequence[position] == 'B')
mock.sleep = sleep
previous = sys.modules.get('microbit')
sys.modules['microbit'] = mock
try:
    try: runpy.run_path(str(Path(__file__).resolve().parents[1]/'micropython/01_shift_world.py'))
    except StopCheck: pass
finally:
    if previous is None: del sys.modules['microbit']
    else: sys.modules['microbit'] = previous

zero = (0,0,0,0,0)
initial = ((0,9,0,0,0),(0,9,9,0,0),zero,zero,zero)
after_one = (zero,(0,9,0,0,0),(0,9,9,0,0),zero,zero)
after_two = (zero,zero,(0,9,0,0,0),(0,9,9,0,0),zero)
assert shown[0] == initial
assert shown[1:4] == [after_one,after_two,initial]
assert shown[8] == (zero,)*5
assert shown[9] == initial
print('PASS: one/two shifts, five-shift clipping, no-action stability, reset and retained original. Desktop mock only; hardware/simulator not tested.')
