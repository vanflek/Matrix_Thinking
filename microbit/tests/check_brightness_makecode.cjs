const fs=require('fs'),vm=require('vm'),assert=require('assert/strict');
const data=JSON.parse(fs.readFileSync(__dirname+'/brightness_cases.json','utf8'));
const buttons={},gestures={},pixels=Array(25).fill(0);
const context=vm.createContext({Button:{A:'A',B:'B'},Gesture:{Shake:'shake'},
  input:{onButtonPressed:(b,f)=>buttons[b]=f,onGesture:(g,f)=>gestures[g]=f},
  led:{plotBrightness:(x,y,v)=>{assert(v>=0&&v<=255);pixels[y*5+x]=v;}},Math});
// This project uses no TS features other than numeric type annotations.
const source=fs.readFileSync(__dirname+'/../makecode/02_brightness_world_makecode.ts','utf8').replace(/: number\[\]/g,'').replace(/: number/g,'');
vm.runInContext(source,context);
function check(i){const world=Array.from(vm.runInContext('world',context));assert.deepEqual(world,data.states[i]);assert.deepEqual(pixels,world.map(v=>Math.round(v*255/9)));}
check(0);
data.actions.forEach((action,i)=>{if(action==='SHAKE')gestures.shake();else buttons[action]();check(i+1);});
console.log('PASS: MakeCode buttons/gesture, all',data.actions.length,'states and 0..255 rendering agree with the MicroPython lesson. Desktop adapter only.');
