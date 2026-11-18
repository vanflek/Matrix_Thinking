(() => {
  'use strict';
  const M = window.RollModel, N = M.size;
  const $ = id => document.getElementById(id);
  const root = $('experiment'), canvas = $('ro-world'), ctx = canvas.getContext('2d');
  const directions = {left:[-1,1], right:[1,1], up:[-1,0], down:[1,0]};
  const keys = {ArrowLeft:'left', ArrowRight:'right', ArrowUp:'up', ArrowDown:'down'};
  let preset = 'cell', initial = M.preset(preset), world = initial.slice(), before = world.slice();
  let selected = [4,4], last = null, tool = 'paint', drawing = false, activePointer = null;
  let operation = 'world[4, 4] = 1', note = 'One lit cell, 99 zeros. They are all part of the world.';
  let pointerValue = 1, lastPaint = -1;
  const buttons = [];
  const mod = n => (n % N + N) % N;
  const sum = a => a.reduce((s,v) => s + v,0);
  const grid = $('ro-matrix');
  for (let r=-1;r<N;r++) for (let c=-1;c<N;c++) {
    if (r === -1 || c === -1) {
      const axis = document.createElement('span');
      axis.className = 'ro-axis'; axis.textContent = r === -1 ? (c === -1 ? '' : c) : r;
      axis.setAttribute('aria-hidden','true'); grid.append(axis);
    } else {
      const button = document.createElement('button');
      button.type='button'; button.className='ro-cell';
      button.dataset.row=r; button.dataset.col=c;
      button.addEventListener('click',() => { selected=[r,c]; render(); });
      button.addEventListener('focus',() => { selected=[r,c]; render(); });
      buttons.push(button); grid.append(button);
    }
  }
  function draw() {
    ctx.clearRect(0,0,520,520); ctx.fillStyle='#fff'; ctx.fillRect(0,0,520,520);
    ctx.font='15px Consolas, monospace'; ctx.textAlign='center'; ctx.textBaseline='middle';
    for (let i=0;i<N;i++) {
      ctx.fillStyle='#596c7b'; ctx.fillText(i,62+i*44,20); ctx.fillText(i,20,62+i*44);
    }
    for (let r=0;r<N;r++) for (let c=0;c<N;c++) {
      const v=world[r*N+c], x=40+c*44, y=40+r*44;
      ctx.fillStyle=v?'#ffd343':'#eef3f8'; ctx.fillRect(x+2,y+2,40,40);
      ctx.strokeStyle=v?'#e3b620':'#d1dfeb'; ctx.lineWidth=1; ctx.strokeRect(x+2.5,y+2.5,39,39);
      if (selected[0]===r && selected[1]===c) {
        ctx.strokeStyle='#b77e00'; ctx.lineWidth=3; ctx.strokeRect(x+3.5,y+3.5,37,37);
      }
    }
    if (last) {
      ctx.strokeStyle='#1165db'; ctx.lineWidth=3; ctx.setLineDash([5,5]);
      if(last.axis===1) { ctx.strokeRect(38,40,4,440); ctx.strokeRect(478,40,4,440); }
      else { ctx.strokeRect(40,38,440,4); ctx.strokeRect(40,478,440,4); }
      ctx.setLineDash([]);
    }
  }
  function render() {
    buttons.forEach((b,i) => {
      b.textContent=world[i]; b.dataset.value=world[i];
      const r=Math.floor(i/N),c=i%N;
      b.setAttribute('aria-label',`world[${r}, ${c}] = ${world[i]}`);
      b.setAttribute('aria-pressed',String(selected[0]===r&&selected[1]===c));
    });
    document.querySelectorAll('[data-preset]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.preset===preset)));
    document.querySelectorAll('[data-tool]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.tool===tool)));
    $('ro-operation').textContent=operation; $('ro-operation-note').textContent=note;
    $('ro-count').textContent=sum(world);
    $('ro-conservation').textContent=last?`${sum(before)} before → ${sum(world)} after. Every value is retained.`:'Painting may change the count. Rolling preserves it.';
    const [r,c]=selected;
    if (last) {
      const sr=last.axis===0?mod(r-last.shift):r, sc=last.axis===1?mod(c-last.shift):c;
      const wrapped=last.axis===0?r-last.shift<0||r-last.shift>=N:c-last.shift<0||c-last.shift>=N;
      $('ro-inspect-title').textContent=`Destination [${r}, ${c}] ← source [${sr}, ${sc}]`;
      $('ro-inspect-rule').textContent=`after[${r}, ${c}] = before[${sr}, ${sc}] = ${world[r*N+c]}`;
      $('ro-inspect-note').textContent=wrapped?'This value crossed the boundary and wrapped to the opposite edge.':'This value moved inside the grid. The same mapping also handles values crossing the edge.';
    } else {
      $('ro-inspect-title').textContent=`Inspect world[${r}, ${c}]`;
      $('ro-inspect-rule').textContent=`world[${r}, ${c}] = ${world[r*N+c]}`;
      $('ro-inspect-note').textContent='The gold outline links this coordinate in the picture and numeric matrix. Choose a direction to trace its source.';
    }
    const axis=last?.axis??1, line=axis===1?r:c;
    $('ro-trace-title').textContent=`${axis===1?'Row':'Column'} ${line} · ${axis===1?'axis=1':'axis=0'}`;
    $('ro-before-label').textContent=`Before: ${axis===1?`before[${line}, :]`:`before[:, ${line}]`}`;
    $('ro-after-label').textContent=`After: ${axis===1?`world[${line}, :]`:`world[:, ${line}]`}`;
    for (const [id,data] of [['ro-before',before],['ro-after',world]]) {
      const container=$(id); container.replaceChildren();
      for(let i=0;i<N;i++) {
        const v=data[axis===1?line*N+i:i*N+line], el=document.createElement('i');
        el.textContent=v; el.dataset.value=v;
        if(last&&((id==='ro-before'&&i===(last.shift>0?N-1:0))||(id==='ro-after'&&i===(last.shift>0?0:N-1))))el.className='ro-wrapped';
        container.append(el);
      }
    }
    draw();
  }
  function move(direction) {
    const [shift,axis]=directions[direction];
    before=world.slice(); world=M.roll(world,shift,axis); last={shift,axis};
    selected[axis]=mod(selected[axis]+shift);
    operation=`world = np.roll(world, ${shift}, axis=${axis})`;
    note=`${direction[0].toUpperCase()+direction.slice(1)} by one. All 100 values roll; ${axis===1?'columns':'rows'} wrap through the edges.`;
    render();
  }
  function load(name) {
    preset=name; initial=M.preset(name); world=initial.slice(); before=world.slice(); last=null;
    selected=name==='cell'?[4,4]:[3,4];
    operation=name==='cell'?'world[4, 4] = 1':name==='duck'?'world[2:7, 2:7] = duck':'world = np.zeros((10, 10), dtype=np.uint8)';
    note=name==='duck'?'A duck replaces the single pixel. The np.roll movement code stays exactly the same.':name==='blank'?'Paint your own world on the left. Then roll it as one matrix.':'One lit cell, 99 zeros. They are all part of the world.';
    render();
  }
  document.querySelectorAll('[data-direction]').forEach(b=>b.addEventListener('click',()=>move(b.dataset.direction)));
  document.querySelectorAll('[data-preset]').forEach(b=>b.addEventListener('click',()=>load(b.dataset.preset)));
  document.querySelectorAll('[data-tool]').forEach(b=>b.addEventListener('click',()=>{tool=b.dataset.tool;render();}));
  $('ro-reset').addEventListener('click',()=>load(preset));
  document.addEventListener('keydown',e=>{
    if (!root.contains(document.activeElement)||e.ctrlKey||e.metaKey||e.altKey||e.target.matches('input,textarea,select,[contenteditable]'))return;
    if(keys[e.key]){e.preventDefault();move(keys[e.key]);}
    else if(e.key.toLowerCase()==='c'){e.preventDefault();load('cell');}
    else if(e.key.toLowerCase()==='r'){e.preventDefault();load(preset);}
    else if(e.code==='Space'&&!e.target.closest('button,a')){e.preventDefault();load('duck');}
  });
  function position(e) {
    const b=canvas.getBoundingClientRect();
    const r=Math.floor(((e.clientY-b.top)*520/b.height-40)/44),c=Math.floor(((e.clientX-b.left)*520/b.width-40)/44);
    return r>=0&&r<N&&c>=0&&c<N?[r,c]:null;
  }
  function paint(e) {
    const p=position(e);if(!p)return;
    selected=p;const i=p[0]*N+p[1];
    if(tool!=='inspect'&&i!==lastPaint) {
      before=world.slice();world[i]=pointerValue;last=null;lastPaint=i;
      operation=`world[${p[0]}, ${p[1]}] = ${pointerValue}`;
      note='Drawing edits individual cells. The arrow controls then roll the entire matrix.';
    }
    render();
  }
  canvas.addEventListener('contextmenu',e=>e.preventDefault());
  canvas.addEventListener('pointerdown',e=>{
    if(![0,2].includes(e.button)||!position(e))return;
    e.preventDefault();canvas.focus();drawing=true;activePointer=e.pointerId;lastPaint=-1;
    pointerValue=e.button===2||tool==='erase'?0:1;
    canvas.setPointerCapture(e.pointerId);paint(e);
  });
  canvas.addEventListener('pointermove',e=>{if(drawing&&e.pointerId===activePointer)paint(e);});
  function stop(e){if(e.pointerId===activePointer){drawing=false;activePointer=null;lastPaint=-1;}}
  canvas.addEventListener('pointerup',stop);canvas.addEventListener('pointercancel',stop);canvas.addEventListener('lostpointercapture',stop);
  window.addEventListener('blur',()=>{drawing=false;activePointer=null;lastPaint=-1;});
  render();
})();
