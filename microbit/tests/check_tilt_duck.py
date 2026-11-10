import ast
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = ROOT / '04_tilt_duck.py'
if not source.exists():
    source = ROOT / 'micropython/04_tilt_duck.py'

class Image:
    def __init__(self, width=5, height=5):
        self.data = [[int(v) for v in row] for row in width.split(':')] if isinstance(width, str) else [[0]*width for _ in range(height)]
    def get_pixel(self, col, row):
        return self.data[row][col]
    def set_pixel(self, col, row, value):
        assert 0 <= value <= 9
        self.data[row][col] = value

tree = ast.parse(source.read_text(encoding='utf-8'))
scope = {'Image': Image}
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n, ast.FunctionDef)], type_ignores=[]), str(source), 'exec'), scope)
node = next(n for n in tree.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'initial' for t in n.targets))
initial = Image(ast.literal_eval(node.value.args[0])).data
assert initial == [[int(v) for v in r] for r in ['00090','00999','99990','09990','00900']]
rng = random.Random(20261110)
matrices = [initial] + [[[rng.randrange(10) for _ in range(5)] for _ in range(5)] for _ in range(100)]
cases = []
for matrix in matrices:
    for horizontal in (False, True):
        for vertical in (False, True):
            image = Image()
            image.data = [r[:] for r in matrix]
            expected = [r[::-1] if horizontal else r[:] for r in (matrix[::-1] if vertical else matrix)]
            assert scope['reflect_world'](image, horizontal, vertical).data == expected
            assert image.data == matrix
            cases.append({'source': matrix, 'horizontal': horizontal, 'vertical': vertical, 'expected': expected})
readings = [(0,0),(-600,0)]*2 + [(-600,0)]*100 + [(0,0)]*100 + [(0,-600),(0,0),(600,0),(0,600)]
readings += [(rng.randrange(-1024,1025),rng.randrange(-1024,1025)) for _ in range(1000)]
h = v = False
frames = []
for x,y in readings:
    expected_h = True if x < -300 else False if x > 300 else h
    expected_v = True if y < -300 else False if y > 300 else v
    h = scope['axis_state'](x,h)
    v = scope['axis_state'](y,v)
    assert (h,v) == (expected_h,expected_v)
    frames.append({'x':x,'y':y,'horizontal':h,'vertical':v})
for reading in (-300, 300, 0):
    for previous in (False,True):
        assert scope['axis_state'](reading,previous) == previous
(Path(__file__).parent/'duck_cases.json').write_text(json.dumps({'initial':initial,'cases':cases,'frames':frames}),encoding='utf-8')
print(f'PASS: MicroPython 404 orientations on 101 matrices; {len(frames)} tilt frames, neutral band, held tilt, boundaries and unchanged source. Desktop adapter only.')
