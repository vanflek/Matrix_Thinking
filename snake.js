(()=>{
const model=new SnakeModel(),section=document.querySelector('#snake-lab'),numbers=document.querySelector('#snake-matrix'),board=document.querySelector('#snake-board');
const status=document.querySelector('#snake-status'),explain=document.querySelector('#snake-explain'),play=document.querySelector('#snake-play'),step=document.querySelector('#snake-step');
let timer=null,focusCell=null;
document.querySelectorAll('.col-indices, .row-indices').forEach(axis=>{axis.replaceChildren();for(let i=0;i<10;i++){const label=document.createElement('span');label.textContent=i;axis.append(label);}});
const names=['empty','body','apple','head'],cells=[[],[]];
[numbers,board].forEach((grid,side)=>{for(let r=0;r<10;r++)for(let c=0;c<10;c++){const b=document.createElement('button');b.type='button';b.className='snake-cell';b.dataset.row=r;b.dataset.col=c;
b.addEventListener('pointerenter',()=>highlight(r,c));b.addEventListener('pointerleave',()=>highlight(null,null));b.addEventListener('focus',()=>highlight(r,c));b.addEventListener('blur',()=>highlight(null,null));b.addEventListener('click',()=>highlight(r,c));grid.append(b);cells[side].push(b);}});
function highlight(r,c){focusCell=r===null?null:[r,c];for(const side of cells)side.forEach(b=>b.classList.toggle('inspected',Number(b.dataset.row)===r&&Number(b.dataset.col)===c));document.querySelector('#snake-coordinate').textContent=r===null?'Point to a cell in either view to find its partner.':'field['+r+', '+c+'] = '+model.matrix()[r][c]+' · '+names[model.matrix()[r][c]];}
function stop(){if(timer)clearInterval(timer);timer=null;play.textContent='Play →';play.setAttribute('aria-pressed','false');step.disabled=['lost','won'].includes(model.state);}
function render(){const a=model.matrix();const changed=model.last&&!model.last.collision?[model.last.head,model.last.previous,...(!model.last.ate?[model.last.tail]:[])]:[];
cells.forEach((side,i)=>side.forEach((b,index)=>{const r=Math.floor(index/10),c=index%10,v=a[r][c];b.dataset.value=v;b.textContent=i===0?String(v):v===2?'●':v===3?'••':'';
b.setAttribute('aria-label','Row '+r+', column '+c+': '+v+', '+names[v]);b.classList.toggle('changed',changed.some(p=>p[0]===r&&p[1]===c));}));
document.querySelector('#snake-score').textContent='Apples '+model.score+' · Length '+model.body.length+' · Step '+model.steps;
status.textContent=model.state==='lost'?'Game over — the head hit the body. Restart to try again.':model.state==='won'?'You filled the matrix. You win!':timer?'Playing · steer with the arrows below.':'Paused · choose a direction, then take one step.';
play.disabled=['lost','won'].includes(model.state);step.disabled=play.disabled||!!timer;
document.querySelectorAll('[data-turn]').forEach(b=>{b.setAttribute('aria-pressed',String(JSON.stringify(model.queued||model.direction)===JSON.stringify({up:[-1,0],down:[1,0],left:[0,-1],right:[0,1]}[b.dataset.turn])));});
if(focusCell)highlight(...focusCell);
}
function tick(){const e=model.step();if(!e)return;if(e.collision){stop();explain.textContent='The next head would be at ['+e.head.join(', ')+'], which is occupied by the body. The move is rejected.';}
else{explain.textContent='Head: ['+e.previous.join(', ')+'] → ['+e.head.join(', ')+']. '+(e.ate?'Apple eaten: keep the tail, so the snake grows by one. A new apple is placed in an empty cell.': 'The old head becomes body (1); the old tail at ['+e.tail.join(', ')+'] is released unless the new head occupies that cell.')+(e.wrapped?' The head crossed an edge and wrapped to the opposite side.':'');if(model.state==='won')stop();}
render();}
step.addEventListener('click',tick);play.addEventListener('click',()=>{if(timer)stop();else{timer=setInterval(tick,360);play.textContent='Pause Ⅱ';play.setAttribute('aria-pressed','true');}render();});
document.querySelector('#snake-restart').addEventListener('click',()=>{stop();model.reset();explain.textContent='The head is at [5, 4]. Moving right adds [0, 1]. Predict the next head position, then take a step.';render();});
document.querySelectorAll('[data-turn]').forEach(b=>b.addEventListener('click',()=>{model.turn(b.dataset.turn);render();}));
section.addEventListener('keydown',e=>{if(e.target.matches('select,input,textarea'))return;const d={ArrowUp:'up',ArrowDown:'down',ArrowLeft:'left',ArrowRight:'right'}[e.key];if(d){e.preventDefault();model.turn(d);render();}});
document.querySelector('#snake-colors').addEventListener('change',e=>numbers.classList.toggle('with-colors',e.target.checked));
document.addEventListener('visibilitychange',()=>{if(document.hidden){stop();render();}});
window.addEventListener('blur',()=>{stop();render();});
render();
})();

