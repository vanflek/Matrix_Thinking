import ast
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / '03_mirror_world.py'
if not SOURCE.exists():
    SOURCE = ROOT / 'micropython/03_mirror_world.py'

class Image:
    def __init__(self, width=5, height=5):
        if isinstance(width, str):
            self.data = [[int(v) for v in row] for row in width.split(':')]
        else:
            self.data = [[0] * width for _ in range(height)]
    def get_pixel(self, col, row):
        return self.data[row][col]
    def set_pixel(self, col, row, value):
        assert 0 <= value <= 9
        self.data[row][col] = value

tree = ast.parse(SOURCE.read_text(encoding='utf-8'))
functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
namespace = {'Image': Image}
exec(compile(ast.Module(body=functions, type_ignores=[]), str(SOURCE), 'exec'), namespace)
mirror = namespace['mirror_world']
initial_node = next(n for n in tree.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'initial' for t in n.targets))
initial = Image(ast.literal_eval(initial_node.value.args[0])).data
rng = random.Random(20261109)
cases = []
for matrix in [initial] + [[[rng.randrange(10) for _ in range(5)] for _ in range(5)] for _ in range(100)]:
    source = Image()
    source.data = [row[:] for row in matrix]
    horizontal = mirror(source, True)
    vertical = mirror(source, False)
    assert horizontal.data == [row[::-1] for row in matrix]
    assert vertical.data == matrix[::-1]
    assert source.data == matrix, 'source image must remain unchanged'
    assert mirror(horizontal, True).data == matrix
    assert mirror(vertical, False).data == matrix
    assert mirror(horizontal, False).data == mirror(vertical, True).data
    assert sorted(sum(horizontal.data, [])) == sorted(sum(matrix, []))
    assert sorted(sum(vertical.data, [])) == sorted(sum(matrix, []))
    cases.append({'before': matrix, 'horizontal': horizontal.data, 'vertical': vertical.data})
record = {'initial': initial, 'cases': cases}
(Path(__file__).parent / 'mirror_cases.json').write_text(json.dumps(record), encoding='utf-8')
print('PASS: MicroPython reflections on 101 matrices: source unchanged, brightness preserved, double reflections restore, both axes commute. Desktop Image adapter only.')
