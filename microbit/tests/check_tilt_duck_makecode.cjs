const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..'),d=JSON.parse(fs.readFileSync(path.join(__dirname,'duck_cases.json'),'utf8'));
const file=fs.existsSync(path.join(root,'04_tilt_duck_makecode.ts'))?path.join(root,'04_tilt_duck_makecode.ts'):path.join(root,'makecode/04_tilt_duck_makecode.ts');
const source=fs.readFileSync(file,'utf8').replace(/: number\[\]/g,'');
let x=0,y=0,draws=0,tick;const pixels=Array(25).fill(0),gestures={};
const c=vm.createContext({Math,Dimension:{X:'x',Y:'y'},Gesture:{Shake:'shake'},input:{acceleration:a=>a==='x'?x:y,onGesture:(g,f)=>gestures[g]=f},basic:{pause:()=>{},forever:f=>tick=f},led:{plotBrightness:(col,row,v)=>{pixels[row*5+col]=v;draws++;}}});
vm.runInContext(source,c);
function compare(expected){assert.deepEqual(Array.from(vm.runInContext('world',c)),expected.flat());assert.deepEqual(pixels,expected.flat().map(v=>Math.round(v*255/9)));}
compare(d.initial);
for(const item of d.cases){vm.runInContext(`initialWorld=${JSON.stringify(item.source.flat())};leftRight=${item.horizontal};topBottom=${item.vertical};reflectWorld()`,c);compare(item.expected);assert.deepEqual(Array.from(vm.runInContext('initialWorld',c)),item.source.flat());}
vm.runInContext(`initialWorld=${JSON.stringify(d.initial.flat())};resetWorld()`,c);
for(const f of d.frames){x=f.x;y=f.y;tick();assert.equal(vm.runInContext('leftRight',c),f.horizontal);assert.equal(vm.runInContext('topBottom',c),f.vertical);const expected=(f.vertical?[...d.initial].reverse():d.initial).map(r=>f.horizontal?[...r].reverse():[...r]);compare(expected);}
x=-600;y=-600;tick();const previousDraws=draws;for(let i=0;i<100;i++)tick();assert.equal(draws,previousDraws,'held tilt should not redraw or toggle');
x=y=0;gestures.shake();compare(d.initial);tick();compare(d.initial);
const modelPath=path.resolve(root,'../matrix_thinking_site/dist/microbit-model.js');
if(fs.existsSync(modelPath)){const M=require(modelPath);let h=false,v=false;for(const f of d.frames){h=M.axisState(f.x,h);v=M.axisState(f.y,v);assert.equal(h,f.horizontal);assert.equal(v,f.vertical);const expected=(v?[...d.initial].reverse():d.initial).map(r=>h?[...r].reverse():[...r]);assert.deepEqual(M.duckWorld(h,v),expected);}}
console.log('PASS: MakeCode and browser model match MicroPython; 404 orientations, tilt sequence, no held-tilt toggling, shake reset and exact LED mapping.');
