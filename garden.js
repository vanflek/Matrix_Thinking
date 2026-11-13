(function(){
'use strict';
const M=window.GardenWorld,$=id=>document.getElementById(id),NS='http://www.w3.org/2000/svg';
const state={fence:24,minimum:30,width:4,length:8,stage:0,lessonStep:0};
let world=M.buildWorld(),glyphs=[],drawnN=0,lastWidth=0,dragging=false;
const svg=$('g-world'),plan=$('g-plan'),wrap=$('g-map-wrap');
const make=(tag,attrs,parent,text)=>{const e=document.createElementNS(NS,tag);Object.entries(attrs||{}).forEach(([k,v])=>e.setAttribute(k,v));if(text!==undefined)e.textContent=text;if(parent)parent.appendChild(e);return e;};
const rules=[
'perimeter = 2 * (width + length)',
'fence_ok = perimeter <= fence',
'area_ok = area >= minimum',
'mask = fence_ok & area_ok',
'solutions = np.column_stack((\n    width[mask], length[mask],\n    perimeter[mask], area[mask],\n))'
];
const notes=[
'The whole candidate world is still here, including gardens that will fail. Each cell shows its perimeter; no mask has selected solutions yet. Select any cell to inspect it.',
'True means the four sides can be fenced within the budget. Unused fence is allowed. The whole triangle of choices is checked at once.',
'True means the area meets the minimum. This mask alone does not check whether enough fence is available.',
'Blue cells pass both tests. Yellow passes only the fence rule; violet passes only the area rule. The intersection is the solution set.',
'Every blue cell becomes one row: width, length, fence needed, area. Scroll within the diagram when there are many solutions.'
];
function selected(){return M.cellAt(world,state.width,state.length);}
function choose(width,length,focus=false){
 state.width=Math.max(1,Math.min(world.n,width));state.length=Math.max(1,Math.min(world.n,length));
 render();
 if(focus){const g=glyphs[(state.width-1)*world.n+state.length-1];if(g)g.rect.focus();}
}
function rebuild(){
 if(drawnN===world.n)return;drawnN=world.n;
 $('g-marks').replaceChildren();$('g-values').replaceChildren();
 glyphs=world.cells.map(c=>{
  const rect=make('rect',{class:'g-mark',rx:2,role:'gridcell',tabindex:-1},$('g-marks'));
  make('title',{},rect,`${c.width} by ${c.length} m; fence ${c.perimeter} m; area ${c.area} square metres`);
  const label=make('text',{'text-anchor':'middle',class:'g-map-value','aria-hidden':'true'},$('g-values'));
  const rowValues=c.valid?[c.width,c.length,c.perimeter,c.area].map(v=>make('text',{'text-anchor':'middle',class:'g-map-value','aria-hidden':'true'},$('g-values'),String(v))):[];
  rect.addEventListener('click',()=>choose(c.width,c.length));
  rect.addEventListener('keydown',e=>{
   if(state.stage===4){
    if(!c.valid)return;
    let i=c.solutionIndex;
    if(['ArrowLeft','ArrowUp'].includes(e.key))i--;
    else if(['ArrowRight','ArrowDown'].includes(e.key))i++;
    else if(e.key==='Home')i=0;
    else if(e.key==='End')i=world.solutions.length-1;
    else if(e.key==='Enter'||e.key===' '){e.preventDefault();choose(c.width,c.length);return;}
    else return;
    e.preventDefault();const n=world.solutions[Math.max(0,Math.min(world.solutions.length-1,i))];choose(n.width,n.length,true);return;
   }
   let w=c.width,l=c.length;
   if(e.key==='ArrowUp')w--;else if(e.key==='ArrowDown')w++;else if(e.key==='ArrowLeft')l--;else if(e.key==='ArrowRight')l++;
   else if(e.key==='Home')l=1;else if(e.key==='End')l=world.n;
   else if(e.key==='Enter'||e.key===' '){e.preventDefault();choose(w,l);return;}else return;
   e.preventDefault();choose(w,l,true);
  });
  return {c,rect,label,rowValues};
 });
}
function refreshWorld(){
 world=M.buildWorld(state.fence,state.minimum);
 state.width=Math.min(state.width,world.n);state.length=Math.min(state.length,world.n);
 // Cell validity can change even when the grid dimensions stay the same.
 drawnN=0;rebuild();render();
}
function drawPlan(){
 const c=selected(),land=$('g-land'),measures=$('g-measures');land.replaceChildren();measures.replaceChildren();
 const unit=260/world.n,ox=88,oy=35,N=world.n,px=c.length*unit,py=c.width*unit;
 make('rect',{x:ox,y:oy,width:260,height:260,fill:'#f4f8f2',stroke:'#dde6da'},land);
 for(let i=0;i<=N;i++){
  make('path',{d:`M${ox+i*unit} ${oy}v260 M${ox} ${oy+i*unit}h260`,stroke:'#e0e8dd','stroke-width':.7,fill:'none'},land);
 }
 for(let r=0;r<c.width;r++)for(let col=0;col<c.length;col++){
  const x=ox+col*unit,y=oy+r*unit;
  make('rect',{x:x+.6,y:y+.6,width:unit-1.2,height:unit-1.2,fill:(r+col)%2?'#d3e8d6':'#e0efde'},land);
  const mx=x+unit*.5,my=y+unit*.55,u=unit*.22;
  make('path',{d:`M${mx} ${my+u*.7}v${-u*1.5} M${mx} ${my}q${-u} ${-u} ${-u} 0q${u*.3} ${u*.7} ${u} 0 M${mx} ${my-u*.2}q${u} ${-u} ${u} 0q${-u*.3} ${u*.7} ${-u} 0`,stroke:'#589368','stroke-width':Math.max(.6,unit*.045),fill:'#8cbd89','stroke-linecap':'round'},land);
 }
 make('rect',{x:ox,y:oy,width:px,height:py,fill:'none',stroke:c.fenceOk?'#bd8f20':'#b55847','stroke-width':4,rx:1},land);
 const post=(x,y)=>make('rect',{x:x-2.5,y:y-2.5,width:5,height:5,rx:.5,fill:c.fenceOk?'#ffd343':'#e7a48f',stroke:c.fenceOk?'#91702a':'#9e493b','stroke-width':.7},land);
 for(let i=0;i<=c.length;i++){post(ox+i*unit,oy);post(ox+i*unit,oy+py);}
 for(let i=1;i<c.width;i++){post(ox,oy+i*unit);post(ox+px,oy+i*unit);}
 make('text',{x:ox+px/2,y:oy+py+24,'text-anchor':'middle',fill:'#132d45','font-family':'Consolas,monospace','font-size':13,stroke:'#f8fbf8','stroke-width':4,'paint-order':'stroke'},measures,`length ${c.length} m`);
 make('text',{x:ox-13,y:oy+py/2,'text-anchor':'end',fill:'#132d45','font-family':'Consolas,monospace','font-size':13,stroke:'#f8fbf8','stroke-width':4,'paint-order':'stroke'},measures,`${c.width} m`);
 make('text',{x:218,y:330,'text-anchor':'middle',fill:'#596c7b','font-family':'Consolas,monospace','font-size':11},measures,'each square = 1 m²');
 $('g-handle').setAttribute('transform',`translate(${ox+px} ${oy+py})`);
 $('g-handle-icon').setAttribute('d','M-4 3L3-4 M0 5L5 0');
 $('g-handle').setAttribute('aria-label',`Resize ${c.width} by ${c.length} metre garden. Arrow keys: left/right change length, up/down change width.`);
 $('g-perimeter').textContent=`2 × (${c.width} + ${c.length}) = ${c.perimeter} m`;
 $('g-area').textContent=`${c.width} × ${c.length} = ${c.area} m²`;
 $('g-dimensions').textContent=`${c.width} × ${c.length} m`;
 $('g-fence-strip').innerHTML=Array.from({length:state.fence},(_,i)=>`<i class="${i<c.perimeter?'used':''}"></i>`).join('');
 $('g-fence-strip').dataset.over=String(!c.fenceOk);
 $('g-fence-left').textContent=c.fenceOk?`${state.fence} m available · ${state.fence-c.perimeter} m left over`:`${state.fence} m available · ${c.perimeter-state.fence} m short`;
 $('g-fence-condition').textContent=c.fenceOk?'✓ Fence fits':'✕ Fence too short';
 $('g-area-condition').textContent=c.areaOk?'✓ Area is enough':'✕ Area too small';
 $('g-fence-check').textContent=`${c.perimeter} <= ${state.fence} → ${c.fenceOk?'True':'False'}`;
 $('g-area-check').textContent=`${c.area} >= ${state.minimum} → ${c.areaOk?'True':'False'}`;
 $('g-fence-check').dataset.pass=String(c.fenceOk);$('g-area-check').dataset.pass=String(c.areaOk);
 const problems=[];if(!c.fenceOk)problems.push(`needs ${c.perimeter-state.fence} m more fence`);if(!c.areaOk)problems.push(`needs ${state.minimum-c.area} m² more area`);
 $('g-status').textContent=c.valid?`Suitable: ${c.width} × ${c.length} gives ${c.area} m² and uses ${c.perimeter} of ${state.fence} metres of fence.`:`Not suitable: ${problems.join(' and ')}.`;
 $('g-status').dataset.valid=String(c.valid);
}
function drawMatrix(){
 const W=Math.max(180,svg.getBoundingClientRect().width||650),left=40,top=48,right=10,mode=state.stage;
 let H;
 const axes=$('g-axes');axes.replaceChildren();
 if(mode===4){
  H=Math.max(118,64+world.solutions.length*24);
  ['Width','Length','Fence','Area'].forEach((v,i)=>make('text',{x:14+(W-28)*(i+.5)/4,y:27,'text-anchor':'middle','font-weight':'bold'},axes,v));
  if(!world.solutions.length)make('text',{x:W/2,y:77,'text-anchor':'middle'},axes,'No suitable gardens.');
 }else{
  const side=W-left-right,gridH=Math.min(side,340,world.n*28);
  H=top+gridH+32;
  make('text',{x:left+side/2,y:15,'text-anchor':'middle'},axes,'length →');
  make('text',{x:10,y:top+gridH/2,transform:`rotate(-90 10 ${top+gridH/2})`,'text-anchor':'middle'},axes,'width →');
  for(let i=0;i<world.n;i++){
   if(world.n<=14||i===0||i===world.n-1||(i+1)%2===0){
    make('text',{x:left+(i+.5)*side/world.n,y:top-10,'text-anchor':'middle'},axes,String(i+1));
    make('text',{x:left-10,y:top+(i+.5)*gridH/world.n+4,'text-anchor':'end'},axes,String(i+1));
   }
  }
 }
 svg.setAttribute('viewBox',`0 0 ${W} ${H}`);
 svg.setAttribute('aria-rowcount',mode===4?world.solutions.length:world.n);
 svg.setAttribute('aria-colcount',mode===4?4:world.n);
 svg.setAttribute('aria-label',mode===4?'All suitable gardens: width, length, fence needed, area.':'Candidate gardens: width in rows, length in columns. Arrow keys select a cell.');
 const c0=selected();
 for(const g of glyphs){
  const c=g.c,visible=mode!==4||c.valid,s=mode===4?0:(W-left-right)/world.n,sy=Math.min(s,28,340/world.n);
  const x=mode===4?14:left+(c.length-1)*s+1.1,y=mode===4?42+c.solutionIndex*24:top+(c.width-1)*sy+1.1;
  const w=mode===4?W-28:Math.max(1,s-2.2),h=mode===4?21:Math.max(1,sy-2.2);
  const isSelected=c.width===c0.width&&c.length===c0.length;
  let fill='#edf2f7',text='',white=false;
  if(mode===0){const t=c.perimeter/(4*world.n);fill=`rgb(${Math.round(238-220*t)},${Math.round(245-145*t)},${Math.round(251-35*t)})`;text=String(c.perimeter);white=t>.56;}
  if(mode===1){fill=c.fenceOk?'#1165db':'#edf2f7';text=c.fenceOk?'1':'0';white=c.fenceOk;}
  if(mode===2){fill=c.areaOk?'#2f8768':'#edf2f7';text=c.areaOk?'1':'0';white=c.areaOk;}
  if(mode===3){fill=c.valid?'#1165db':c.fenceOk?'#ffe59a':c.areaOk?'#e6ddf7':'#edf2f7';text=c.valid?'1':'0';white=c.valid;}
  if(mode===4)fill=isSelected?'#dceaff':'#edf4fc';
  Object.entries({x,y,width:w,height:h,fill,opacity:visible?1:0,visibility:visible?'visible':'hidden','aria-hidden':String(!visible),'aria-selected':String(isSelected),'aria-rowindex':mode===4?c.solutionIndex+1:c.width,'aria-colindex':mode===4?1:c.length,'aria-colspan':mode===4?4:1,tabindex:visible&&isSelected?0:-1,'aria-label':`${c.width} by ${c.length} m; fence ${c.perimeter}; area ${c.area}; fence ${c.fenceOk?'fits':'fails'}, area ${c.areaOk?'fits':'fails'}; ${c.valid?'suitable':'not suitable'}`}).forEach(([k,v])=>g.rect.setAttribute(k,v));
  g.label.setAttribute('x',x+w/2);g.label.setAttribute('y',y+h/2+3.7);g.label.style.fill=white?'white':'#526b81';g.label.textContent=text;g.label.style.display=mode!==4&&s>=17?'':'none';g.label.style.fontSize=Math.min(12,s*.42,sy*.6)+'px';
  g.rowValues.forEach((t,i)=>{t.setAttribute('x',14+(W-28)*(i+.5)/4);t.setAttribute('y',y+14);t.style.display=mode===4?'':'none';t.style.fill='#132d45';t.style.fontSize='12px';});
 }
 // Retain a keyboard entry point when the selected garden is filtered out.
 if(mode===4&&!c0.valid&&world.solutions.length)glyphs[world.solutions[0].index].rect.setAttribute('tabindex','0');
}
function drawTable(){
 if(!$('g-table-details').open)return;
 const mode=state.stage,table=$('g-table');table.replaceChildren();
 const head=document.createElement('thead'),hr=document.createElement('tr');
 const labels=mode===4?['Width (m)','Length (m)','Fence (m)','Area (m²)']:['W / L',...Array.from({length:world.n},(_,i)=>i+1)];
 labels.forEach(v=>{const th=document.createElement('th');th.textContent=v;th.scope='col';hr.appendChild(th);});head.appendChild(hr);table.appendChild(head);
 const body=document.createElement('tbody');
 if(mode===4){
  world.solutions.forEach(c=>{
   const tr=document.createElement('tr');
   [c.width,c.length,c.perimeter,c.area].forEach((v,i)=>{
    const td=document.createElement('td');td.dataset.valid='true';td.dataset.selected=String(c.width===state.width&&c.length===state.length);
    if(i===0){const b=document.createElement('button');b.type='button';b.textContent=v;b.setAttribute('aria-label',`Select ${c.width} by ${c.length} garden`);b.addEventListener('click',()=>choose(c.width,c.length));td.appendChild(b);}else td.textContent=v;
    tr.appendChild(td);
   });body.appendChild(tr);
  });
 }else{
  const values=M.matrix(world,mode);
  values.forEach((row,i)=>{
   const tr=document.createElement('tr'),th=document.createElement('th');th.textContent=i+1;th.scope='row';tr.appendChild(th);
   row.forEach((v,j)=>{
    const c=M.cellAt(world,i+1,j+1),td=document.createElement('td'),b=document.createElement('button');
    td.dataset.valid=String(c.valid);td.dataset.selected=String(c.width===state.width&&c.length===state.length);
    b.type='button';b.textContent=v;b.setAttribute('aria-label',`Select ${c.width} by ${c.length}; value ${v}; ${c.valid?'suitable':'not suitable'}`);b.addEventListener('click',()=>choose(c.width,c.length));td.appendChild(b);tr.appendChild(td);
   });body.appendChild(tr);
  });
 }
 table.appendChild(body);
 $('g-table-description').textContent=mode===4?`${world.solutions.length} rows. Select a width value to inspect that solution. Rotated sizes are listed separately.`:mode===0?'Each cell is the fence needed, in metres.':'1 means True and 0 means False for the selected mask. Select a value to inspect its garden.';
}
function render(){
 rebuild();
 $('g-width').max=world.n;$('g-length').max=world.n;
 for(const [key,id]of [['fence','g-fence'],['minimum','g-minimum'],['width','g-width'],['length','g-length']])$(id).value=state[key];
 $('g-width').max=world.n;$('g-length').max=world.n;
 $('g-fence-value').textContent=state.fence+' m';$('g-minimum-value').textContent=state.minimum+' m²';
 $('g-width-value').textContent=state.width+' m';$('g-length-value').textContent=state.length+' m';
 $('g-shape').textContent=state.stage===4?`${world.solutions.length} × 4`:`${world.n} × ${world.n}`;
 $('g-rule').textContent=rules[state.stage];$('g-stage-note').textContent=notes[state.stage];
 document.querySelectorAll('[data-stage]').forEach(b=>b.setAttribute('aria-pressed',String(Number(b.dataset.stage)===state.stage)));
 const legend=state.stage===0?[['#b6d0ee','Less fence'],['#1165db','More fence']]:state.stage===1?[['#1165db','Fence fits · True'],['#edf2f7','Too much fence · False']]:state.stage===2?[['#2f8768','Area fits · True'],['#edf2f7','Too small · False']]:state.stage===3?[['#1165db','Both fit'],['#ffe59a','Only fence fits'],['#e6ddf7','Only area fits'],['#edf2f7','Neither fits']]:[['#b58100','Yellow outline: selected solution']];
 $('g-legend').innerHTML=legend.map(([color,label])=>`<span><i style="background:${color}"></i>${label}</span>`).join('');
 $('g-total').textContent=world.cells.length;$('g-fence-count').textContent=world.fenceCount;$('g-area-count').textContent=world.areaCount;$('g-valid-count').textContent=world.solutions.length;
 $('g-result-title').textContent=`${world.solutions.length} suitable garden${world.solutions.length===1?'':'s'}.`;
 $('g-orientation').textContent=`${world.solutions.length} oriented pair${world.solutions.length===1?'':'s'} represent ${world.distinct} distinct shape${world.distinct===1?'':'s'}. Turning a rectangle swaps its row and column.`;
 $('g-best').disabled=!world.best.length;
 if(world.best.length){
  $('g-best-summary').textContent=world.best.map(c=>`${c.width} × ${c.length}`).join(' or ')+' m · '+world.best[0].area+' m²';
  $('g-best-reason').textContent=`The largest area among all suitable gardens. ${world.best[0].perimeter} m of fence needed; ${state.fence-world.best[0].perimeter} m left over.`;
 }else{
  $('g-best-summary').textContent='No suitable garden';
  $('g-best-reason').textContent=`The largest area within ${state.fence} m of fence is ${world.largestWithinFence} m², below the ${state.minimum} m² minimum. Increase the fence budget or lower the minimum.`;
 }
 $('g-command').textContent=`python garden-numpy.py --fence ${state.fence} --minimum ${state.minimum}`;
 drawPlan();drawMatrix();drawTable();renderLesson();
}
function renderLesson(){
 $('g-principle-world').textContent=`${world.cells.length} candidates`;
 $('g-principle-range').textContent=`All pairs of whole-number side lengths from 1 to ${world.n} m. No condition has filtered them yet.`;
 $('g-principle-masks').textContent=`${world.fenceCount} fit the fence. ${world.areaCount} have enough area. Each mask checks a different property of the same ${world.cells.length} candidates.`;
 $('g-principle-solutions').textContent=`${world.solutions.length} solution${world.solutions.length===1?'':'s'}`;
 const lesson=window.GardenLesson.steps(world)[state.lessonStep];
 $('g-lesson-heading').textContent=lesson.title;
 $('g-lesson-progress').textContent=`Step ${state.lessonStep+1} of 6`;
 $('g-lesson-explanation').textContent=lesson.explanation;
 $('g-lesson-code').textContent=lesson.code;
 $('g-lesson-output').textContent=lesson.output;
 document.querySelectorAll('[data-lesson]').forEach(b=>b.setAttribute('aria-pressed',String(Number(b.dataset.lesson)===state.lessonStep)));
 $('g-lesson-back').disabled=state.lessonStep===0;
 $('g-lesson-next').disabled=state.lessonStep===5;
}
function chooseLesson(step){state.lessonStep=step;state.stage=window.GardenLesson.steps(world)[step].stage;wrap.scrollTop=0;render();}
function preset(w,l){Object.assign(state,{fence:24,minimum:30,width:w,length:l,stage:0,lessonStep:0});wrap.scrollTop=0;refreshWorld();}
$('g-fence').addEventListener('input',e=>{state.fence=Number(e.target.value);wrap.scrollTop=0;refreshWorld();});
$('g-minimum').addEventListener('input',e=>{state.minimum=Number(e.target.value);wrap.scrollTop=0;refreshWorld();});
$('g-width').addEventListener('input',e=>choose(Number(e.target.value),state.length));
$('g-length').addEventListener('input',e=>choose(state.width,Number(e.target.value)));
$('g-reset').addEventListener('click',()=>preset(4,8));
const presets={fits:[4,8],spare:[5,6],fence:[7,7],area:[3,9]};
document.querySelectorAll('[data-example]').forEach(b=>b.addEventListener('click',()=>preset(...presets[b.dataset.example])));
document.querySelectorAll('[data-stage]').forEach(b=>b.addEventListener('click',()=>{state.stage=Number(b.dataset.stage);state.lessonStep=[1,2,3,4,5][state.stage];wrap.scrollTop=0;render();}));
document.querySelectorAll('[data-lesson]').forEach(b=>b.addEventListener('click',()=>chooseLesson(Number(b.dataset.lesson))));
$('g-lesson-back').addEventListener('click',()=>chooseLesson(Math.max(0,state.lessonStep-1)));
$('g-lesson-next').addEventListener('click',()=>chooseLesson(Math.min(5,state.lessonStep+1)));
$('g-best').addEventListener('click',()=>{if(world.best.length){state.stage=4;state.lessonStep=5;wrap.scrollTop=0;choose(world.best[0].width,world.best[0].length);}});
$('g-table-details').addEventListener('toggle',drawTable);
$('g-copy').addEventListener('click',async()=>{try{await navigator.clipboard.writeText($('g-python').textContent);$('g-copy-status').textContent='Complete Python code copied.';}catch(_){$('g-copy-status').textContent='Copy unavailable here; download the Python file instead.';}});
$('g-csv').addEventListener('click',()=>{const csv='width_m,length_m,fence_m,area_m2\n'+M.rows(world).map(r=>r.join(',')).join('\n')+'\n';const a=document.createElement('a'),url=URL.createObjectURL(new Blob([csv],{type:'text/csv;charset=utf-8'}));a.href=url;a.download=`gardens-fence-${state.fence}-area-${state.minimum}.csv`;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);});
function point(event){
 const p=plan.createSVGPoint();p.x=event.clientX;p.y=event.clientY;
 const q=p.matrixTransform(plan.getScreenCTM().inverse());
 const dims=M.fromPoint(world,q.x,q.y,88,35,260/world.n);choose(dims.width,dims.length);
}
plan.addEventListener('pointerdown',e=>{if(e.button!==0)return;dragging=true;plan.setPointerCapture(e.pointerId);point(e);});
plan.addEventListener('pointermove',e=>{if(dragging)point(e);});
plan.addEventListener('pointerup',()=>{dragging=false;});
plan.addEventListener('pointercancel',()=>{dragging=false;});
$('g-handle').addEventListener('keydown',e=>{let w=state.width,l=state.length;if(e.key==='ArrowLeft')l--;else if(e.key==='ArrowRight')l++;else if(e.key==='ArrowUp')w--;else if(e.key==='ArrowDown')w++;else return;e.preventDefault();choose(w,l);});
if(typeof ResizeObserver!=='undefined')new ResizeObserver(()=>{const w=Math.round(svg.getBoundingClientRect().width);if(w!==lastWidth){lastWidth=w;drawMatrix();}}).observe(wrap);
render();
})();

