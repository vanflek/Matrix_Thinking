(() => {
  'use strict';
  const M = ScaleMatrix, $ = id => document.getElementById(id);
  let world=M.copy(M.DUCK),factor=2,tool='paint',selected=[0,2],probe=null,painting=false,lastPaint='',lastOperation='world = DUCK.copy()';
  const cell=26, base=$('zs-source-canvas'), output=$('zs-output-canvas');
  function matrix(a,id,isOutput){
    const host=$(id), n=a.length,m=a[0].length;host.replaceChildren();host.style.setProperty('--cols',m+1);
    const axis=t=>{const e=document.createElement('span');e.className='zs-axis';e.textContent=t;host.append(e);};
    axis('r/c');for(let c=0;c<m;c++)axis(c);
    for(let r=0;r<n;r++){axis(r);for(let c=0;c<m;c++){
      const b=document.createElement('button');b.type='button';b.className='zs-cell';b.textContent=a[r][c];b.dataset.value=a[r][c];b.dataset.row=r;b.dataset.col=c;
      const own=isOutput?M.owner(r,c,factor):[r,c], linked=own[0]===selected[0]&&own[1]===selected[1];
      if(linked)b.classList.add('linked');if(isOutput&&probe&&probe[0]===r&&probe[1]===c)b.classList.add('focused');
      b.setAttribute('aria-label',`${isOutput?'zoomed':'world'}[${r}, ${c}] = ${a[r][c]}`);b.setAttribute('aria-pressed',String(linked));host.append(b);
    }}
  }
  function draw(canvas,a,isOutput){
    canvas.width=a[0].length*cell;canvas.height=a.length*cell;const ctx=canvas.getContext('2d');
    for(let r=0;r<a.length;r++)for(let c=0;c<a[0].length;c++){
      ctx.fillStyle=a[r][c]?'#ffd343':'#132d45';ctx.fillRect(c*cell,r*cell,cell,cell);ctx.strokeStyle='#54708a';ctx.lineWidth=1;ctx.strokeRect(c*cell+.5,r*cell+.5,cell-1,cell-1);
    }
    const b=isOutput?M.block(...selected,factor):{row:selected[0],column:selected[1],height:1,width:1};
    ctx.strokeStyle='#ff8b23';ctx.lineWidth=4;ctx.strokeRect(b.column*cell+2,b.row*cell+2,b.width*cell-4,b.height*cell-4);
    if(isOutput&&probe){ctx.strokeStyle='#52a7ff';ctx.lineWidth=3;ctx.strokeRect(probe[1]*cell+3,probe[0]*cell+3,cell-6,cell-6);}
  }
  function render(){
    const rows=M.repeatAxis(world,factor,0),zoomed=M.repeatAxis(rows,factor,1),b=M.block(...selected,factor),lit=world.flat().filter(Boolean).length;
    draw(base,world,false);draw(output,zoomed,true);matrix(world,'zs-source-matrix',false);matrix(zoomed,'zs-output-matrix',true);
    $('zs-source-shape').textContent=`world.shape = (${world.length}, ${world[0].length})`;
    $('zs-output-shape').textContent=`zoomed.shape = (${zoomed.length}, ${zoomed[0].length})`;
    $('zs-operation').textContent=`zoomed = world.repeat(${factor}, axis=0).repeat(${factor}, axis=1)`;
    $('zs-pipeline').textContent=`(${world.length}, ${world[0].length}) → (${rows.length}, ${rows[0].length}) → (${zoomed.length}, ${zoomed[0].length})`;
    $('zs-counts').textContent=`${lit} → ${lit*factor*factor} lit cells`;
    $('zs-selected').textContent=`world[${selected[0]}, ${selected[1]}] = ${world[selected[0]][selected[1]]}`;
    $('zs-block').textContent=`zoomed[${b.row}:${b.row+b.height}, ${b.column}:${b.column+b.width}]\n${factor} × ${factor} = ${factor*factor} matching cells`;
    $('zs-explain').textContent=`The orange source cell becomes the entire orange-outlined block. Every cell in it is ${world[selected[0]][selected[1]]}. Select a zero to see that empty space is repeated too.`;
    $('zs-last-operation').textContent=lastOperation;
    $('zs-row-code').textContent=`rows_repeated = world.repeat(${factor}, axis=0)\n# shape: (${rows.length}, ${rows[0].length})\n\n`+rows.map(row=>row.join(' ')).join('\n');
    document.querySelectorAll('[data-zs-factor]').forEach(b=>b.setAttribute('aria-pressed',String(Number(b.dataset.zsFactor)===factor)));
    document.querySelectorAll('[data-zs-tool]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.zsTool===tool)));
  }
  function pick(r,c,isOutput){if(isOutput){selected=M.owner(r,c,factor);probe=[r,c];}else{selected=[r,c];probe=null;}render();}
  function coords(e,canvas){const rect=canvas.getBoundingClientRect();return [Math.min(canvas.height/cell-1,Math.max(0,Math.floor((e.clientY-rect.top)*canvas.height/rect.height/cell))),Math.min(canvas.width/cell-1,Math.max(0,Math.floor((e.clientX-rect.left)*canvas.width/rect.width/cell)))];}
  function paint(e){const [r,c]=coords(e,base),key=`${r},${c}`;if(key===lastPaint)return;lastPaint=key;selected=[r,c];probe=null;if(tool!=='inspect'||e.button===2||e.buttons===2){const value=e.buttons===2||e.button===2||tool==='erase'?0:1;world=M.copy(world);world[r][c]=value;lastOperation=`world[${r}, ${c}] = ${value}`;}render();}
  base.addEventListener('contextmenu',e=>e.preventDefault());
  base.addEventListener('pointerdown',e=>{if(![0,2].includes(e.button))return;painting=true;lastPaint='';base.setPointerCapture(e.pointerId);base.focus();paint(e);});
  base.addEventListener('pointermove',e=>{if(painting)paint(e);});
  base.addEventListener('pointerup',()=>{painting=false;lastPaint='';});base.addEventListener('pointercancel',()=>{painting=false;lastPaint='';});
  output.addEventListener('pointerdown',e=>{if(e.button!==0)return;pick(...coords(e,output),true);});
  for(const [id,isOutput] of [['zs-source-matrix',false],['zs-output-matrix',true]]){
    $(id).addEventListener('click',e=>{const b=e.target.closest('[data-row]');if(!b)return;const r=Number(b.dataset.row),c=Number(b.dataset.col);pick(r,c,isOutput);$(id).querySelector(`[data-row="${r}"][data-col="${c}"]`).focus();});
    $(id).addEventListener('keydown',e=>{const b=e.target.closest('[data-row]');if(!b)return;const d={ArrowUp:[-1,0],ArrowDown:[1,0],ArrowLeft:[0,-1],ArrowRight:[0,1]}[e.key];if(!d)return;e.preventDefault();const n=isOutput?world.length*factor:world.length,m=isOutput?world[0].length*factor:world[0].length,r=Math.min(n-1,Math.max(0,Number(b.dataset.row)+d[0])),c=Math.min(m-1,Math.max(0,Number(b.dataset.col)+d[1]));pick(r,c,isOutput);$(id).querySelector(`[data-row="${r}"][data-col="${c}"]`).focus();});
  }
  document.querySelectorAll('[data-zs-factor]').forEach(b=>b.addEventListener('click',()=>{factor=Number(b.dataset.zsFactor);probe=null;render();$('zs-status').textContent=`Each source cell now has ${factor*factor} copies.`;}));
  document.querySelectorAll('[data-zs-tool]').forEach(b=>b.addEventListener('click',()=>{tool=b.dataset.zsTool;render();}));
  function operation(name){
    if(name==='duck'){world=M.copy(M.DUCK);selected=[0,2];lastOperation='world = DUCK.copy()';}
    else if(name==='clear'){world=world.map(row=>row.map(()=>0));lastOperation='world = np.zeros_like(world)';}
    else if(name==='rotate'){world=M.rotate(world);selected=[selected[1],world[0].length-1-selected[0]];lastOperation='world = np.rot90(world, k=-1)';}
    else{const [dr,dc]={up:[-1,0],down:[1,0],left:[0,-1],right:[0,1]}[name];world=M.roll(world,dr,dc);selected=[(selected[0]+dr+world.length)%world.length,(selected[1]+dc+world[0].length)%world[0].length];lastOperation=`world = np.roll(world, ${dr||dc}, axis=${dr?0:1})`;}
    probe=null;render();$('zs-status').textContent='The whole matrix changed. The enlarged world was calculated again.';
  }
  document.querySelectorAll('[data-zs-op]').forEach(b=>b.addEventListener('click',()=>operation(b.dataset.zsOp)));
  base.addEventListener('keydown',e=>{if(e.ctrlKey||e.altKey||e.metaKey)return;const op={ArrowUp:'up',ArrowDown:'down',ArrowLeft:'left',ArrowRight:'right',Space:'duck',KeyC:'clear',KeyR:'rotate'}[e.code];if(op){e.preventDefault();operation(op);}else if(['Digit1','Digit2','Digit3'].includes(e.code)){e.preventDefault();factor=Number(e.code.at(-1));probe=null;render();}});
  render();
})();
