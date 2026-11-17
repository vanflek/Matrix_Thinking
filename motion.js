(function(){
'use strict';
const M=window.MotionWorld,$=id=>document.getElementById(id),R=M.ROWS,C=M.COLS;
let state,previous,current,result,timer=null,direction=1,drag=null;
let probe={row:9,col:11};
const scenes={
 movement:'Move the duck while the previous frame stays fixed. Both its old and new positions can pass the mask.',
 noise:'The duck is still. Small brightness fluctuations change the current frame. Raise the threshold above 8 to suppress this noise.',
 lighting:'The duck is still, but the entire scene gets brighter. A brightness-change mask can respond across the whole world.',
 contrast:'The moving duck is only slightly brighter than its background. Lower the threshold to reveal its changes.'
};
const canvases=['previous','current','difference','mask'].map(k=>({key:k,canvas:$('mo-'+k),ctx:$('mo-'+k).getContext('2d')}));
const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
function stop(){if(timer!==null){clearInterval(timer);timer=null;}$('mo-play').textContent='Start animation';$('mo-play').setAttribute('aria-pressed','false');}
function preset(scene){
 stop();state={row:8,col:12,brightness:210,light:0,noise:0,seed:1,threshold:30,scene};
 if(scene==='noise')Object.assign(state,{col:8,noise:8,threshold:3});
 if(scene==='lighting')Object.assign(state,{col:8,light:55});
 if(scene==='contrast')state.brightness=55;
 previous=M.frame({row:8,col:8,brightness:state.brightness});direction=1;render();
}
function draw(){
 const arrays={previous,current,difference:result.difference,mask:result.mask};
 for(const {key,canvas,ctx} of canvases){
  const values=arrays[key],s=20;
  for(let i=0;i<values.length;i++){
   const v=values[i];
   ctx.fillStyle=key==='mask'?(v?'#ffd343':'#edf2f7'):key==='difference'?`rgb(${Math.round(237-v*.82)},${Math.round(244-v*.56)},${Math.round(252-v*.12)})`:`rgb(${v},${v},${v})`;
   ctx.fillRect((i%C)*s,Math.floor(i/C)*s,s,s);
  }
  ctx.strokeStyle=key==='previous'||key==='current'?'rgba(200,220,230,.15)':'rgba(19,45,69,.10)';ctx.lineWidth=1;
  ctx.beginPath();for(let r=0;r<=R;r++){ctx.moveTo(0,r*s);ctx.lineTo(C*s,r*s);}for(let c=0;c<=C;c++){ctx.moveTo(c*s,0);ctx.lineTo(c*s,R*s);}ctx.stroke();
  ctx.strokeStyle='#e39200';ctx.lineWidth=3;ctx.strokeRect(probe.col*s+1.5,probe.row*s+1.5,s-3,s-3);
 }
}
function inspect(){
 const i=probe.row*C+probe.col,p=previous[i],c=current[i],d=result.difference[i],m=result.mask[i];
 $('mo-pixel-label').textContent=`Inspecting [${probe.row}, ${probe.col}] in all four matrices`;
 $('mo-pixel-values').innerHTML=[['previous',p],['current',c],['difference',d],['mask',m?'True':'False']].map(([k,v])=>`<span>${k}<b>${v}</b></span>`).join('');
 $('mo-pixel-rule').textContent=`current - previous = ${c} - ${p} = ${c-p}\nabs(${c-p}) = ${d}\n${d} > ${state.threshold} → ${m?'True':'False'}`;
 $('mo-probe-row').value=probe.row;$('mo-probe-col').value=probe.col;
}
function table(){
 if(!$('mo-matrix-details').open)return;
 const arrays={previous,current,difference:result.difference,mask:result.mask},a=arrays[$('mo-matrix-choice').value];
 let html='<thead><tr><th scope="col">r / c</th>'+Array.from({length:C},(_,c)=>`<th scope="col">${c}</th>`).join('')+'</tr></thead><tbody>';
 for(let r=0;r<R;r++)html+=`<tr><th scope="row">${r}</th>`+Array.from({length:C},(_,c)=>`<td data-r="${r}" data-c="${c}" aria-selected="${r===probe.row&&c===probe.col}">${a[r*C+c]}</td>`).join('')+'</tr>';
 $('mo-table').innerHTML=html+'</tbody>';
}
function render(){
 current=M.frame(state);result=M.detect(previous,current,state.threshold);
 for(const key of ['threshold','row','col','light','noise','brightness']){$('mo-'+key).value=state[key];$('mo-'+key+'-value').textContent=state[key];}
 $('mo-count').textContent=`${result.count} / ${R*C}`;
 $('mo-fraction').textContent=(result.fraction*100).toFixed(1)+'%';
 $('mo-scenario').textContent=scenes[state.scene]||'Change one camera setting at a time. Compare its effect across all 768 pixels.';
 $('mo-reference').textContent=timer===null?'Reference frozen: current changes, previous stays fixed.':'Animation: each new frame is compared with the immediately preceding frame.';
 document.querySelectorAll('[data-scene]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.scene===state.scene)));
 draw();inspect();table();
}
function move(row,col){stop();state.row=clamp(row,0,16);state.col=clamp(col,0,24);render();}
function setProbe(row,col){probe={row:clamp(row,0,R-1),col:clamp(col,0,C-1)};draw();inspect();table();}
function point(e){const b=e.currentTarget.getBoundingClientRect();return {row:clamp(Math.floor((e.clientY-b.top)/b.height*R),0,R-1),col:clamp(Math.floor((e.clientX-b.left)/b.width*C),0,C-1)};}
document.querySelectorAll('[data-scene]').forEach(b=>b.addEventListener('click',()=>preset(b.dataset.scene)));
for(const key of ['threshold','row','col','light','noise','brightness'])$('mo-'+key).addEventListener('input',e=>{stop();state[key]=Number(e.target.value);if(['light','noise','brightness'].includes(key))state.scene='custom';render();});
$('mo-capture').addEventListener('click',()=>{stop();previous=current.slice();render();});
$('mo-reset').addEventListener('click',()=>preset('movement'));
$('mo-frame').addEventListener('click',()=>{stop();state.seed++;render();});
$('mo-play').addEventListener('click',()=>{
 if(timer!==null){stop();render();return;}
 previous=current.slice();
 timer=setInterval(()=>{previous=current.slice();if(state.col+direction>24||state.col+direction<0)direction=-direction;state.col+=direction;state.seed++;render();},350);
 $('mo-play').textContent='Pause animation';$('mo-play').setAttribute('aria-pressed','true');render();
});
document.addEventListener('visibilitychange',()=>{if(document.hidden){stop();render();}});
for(const {canvas,key} of canvases){
 canvas.addEventListener('pointerdown',e=>{if(e.button!==0)return;const p=point(e);setProbe(p.row,p.col);if(key==='current'&&p.row>=state.row&&p.row<state.row+8&&p.col>=state.col&&p.col<state.col+8){stop();drag={row:p.row-state.row,col:p.col-state.col};canvas.setPointerCapture(e.pointerId);}});
 canvas.addEventListener('pointermove',e=>{const p=point(e);if(drag&&key==='current')move(p.row-drag.row,p.col-drag.col);else if(e.pointerType==='mouse')setProbe(p.row,p.col);});
 canvas.addEventListener('pointerup',()=>{drag=null;});canvas.addEventListener('pointercancel',()=>{drag=null;});
}
$('mo-current').addEventListener('keydown',e=>{let r=state.row,c=state.col;if(e.key==='ArrowLeft')c--;else if(e.key==='ArrowRight')c++;else if(e.key==='ArrowUp')r--;else if(e.key==='ArrowDown')r++;else return;e.preventDefault();move(r,c);});
for(const key of ['row','col'])$('mo-probe-'+key).addEventListener('input',e=>{if(e.target.value==='')return;setProbe(key==='row'?Math.round(Number(e.target.value)):probe.row,key==='col'?Math.round(Number(e.target.value)):probe.col);});
$('mo-matrix-details').addEventListener('toggle',table);$('mo-matrix-choice').addEventListener('change',table);
$('mo-table').addEventListener('click',e=>{const cell=e.target.closest('td[data-r]');if(cell)setProbe(Number(cell.dataset.r),Number(cell.dataset.c));});
preset('movement');
})();
