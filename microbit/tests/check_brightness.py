"""Check event logic against an independent brightness model; not firmware."""
from pathlib import Path
import json, random, runpy, sys, types

class Image:
    def __init__(self, value, height=None):
        self.values = [int(c) for c in value if c != ':'] if isinstance(value,str) else [0]*(value*height)
    def copy(self):
        image=Image(5,5); image.values=self.values[:]; return image
    def get_pixel(self,x,y): return self.values[y*5+x]
    def set_pixel(self,x,y,value):
        assert 0 <= value <= 9
        self.values[y*5+x]=value

class Done(Exception): pass
rng=random.Random(8)
actions=['B','A','A','SHAKE']+['A']*12+['SHAKE']+['B']*12+['SHAKE']+[rng.choice(['A','B','SHAKE']) for _ in range(100)]
position=0
actual=[]
def sleep(_):
    global position
    position+=1
    if position==len(actions): raise Done()
fake=types.ModuleType('microbit')
fake.Image=Image
fake.display=types.SimpleNamespace(show=lambda image:actual.append(image.values[:]))
fake.button_a=types.SimpleNamespace(was_pressed=lambda:actions[position]=='A')
fake.button_b=types.SimpleNamespace(was_pressed=lambda:actions[position]=='B')
fake.accelerometer=types.SimpleNamespace(was_gesture=lambda gesture:gesture=='shake' and actions[position]=='SHAKE')
fake.sleep=sleep
prior=sys.modules.get('microbit');sys.modules['microbit']=fake
try:
    try:runpy.run_path(str(Path(__file__).resolve().parents[1]/'micropython/02_brightness_world.py'),init_globals={'print':lambda *args:None})
    except Done:pass
finally:
    if prior is None:del sys.modules['microbit']
    else:sys.modules['microbit']=prior
initial=[row+col for row in range(5) for col in range(5)]
expected=[initial[:]]
for action in actions:
    previous=expected[-1]
    expected.append(initial[:] if action=='SHAKE' else [min(9,max(0,value+(1 if action=='B' else -1))) for value in previous])
assert actual==expected
assert actual[16]==[0]*25
assert actual[29]==[9]*25
Path(__file__).with_name('brightness_cases.json').write_text(json.dumps({'actions':actions,'states':expected}),encoding='utf-8')
print('PASS: MicroPython controller and fresh-image update match',len(actions),'steps, including limits, zero pixels and shake reset. Desktop adapter only.')
