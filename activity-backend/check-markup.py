from html.parser import HTMLParser
from pathlib import Path
import os
class P(HTMLParser):
    def __init__(self): super().__init__(); self.stack=[]; self.parents={}; self.attributes={}
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if 'id' in attrs:
            self.parents[attrs['id']]=[a[1] for a in self.stack]
            self.attributes[attrs['id']]=attrs
        if tag not in ('meta','link','input','br','img','hr','source','wbr','area','base','embed','param','track'): self.stack.append((tag,attrs.get('id')))
    def handle_endtag(self,tag):
        for i in range(len(self.stack)-1,-1,-1):
            if self.stack[i][0]==tag: self.stack=self.stack[:i]; break
base=Path(os.environ['ACTIVITY_RELEASE']) if 'ACTIVITY_RELEASE' in os.environ else Path(__file__).resolve().parents[1]/'dist'
cases={'microbit':('main','mb-a'),'life':('main','life-play'),'sandbox':('main','sand-play'),'snake':('snake-lab','snake-play'),'tetris':('tetris-lab','tetris-play'),'flight':('arena','arena-play'),'raycast':('ray-lab','ray-play'),'xonix':('xon-lab','xon-play'),'faces':('main','new-round'),'index':('main','apply')}
cases.update({'edges':('main','edge-input'),'fruit':('main','fruit-count'),'garden':('main','g-fence'),'motion':('main','mo-play'),'roll':('main','ro-world'),'microbit-pycharm':('main','numpy')})
cases['scale']=('main','zs-source-canvas')
cases['kron']=('main','zs-source-canvas')
for name,(root,control) in cases.items():
    text=(base/(name+'.html')).read_text(encoding='utf-8'); p=P();p.feed(text)
    assert root in p.parents and root in p.parents[control], (name,root,control,p.parents.get(control))
    assert text.count('src="game-activity.js?')==1 and 'href="privacy.html"' in text
for name, controls in {'fruit':['fruit-download-csv','fruit-copy-code'],'garden':['g-csv','g-copy']}.items():
    text=(base/(name+'.html')).read_text(encoding='utf-8')
    p=P(); p.feed(text)
    for control in controls:
        assert p.attributes[control].get('data-activity-event') in ('download_data','copy_code'), (name,control)
print('PASS: all 18 pages have a single collector and privacy link; controls are inside tracking roots; resource buttons are annotated.')
