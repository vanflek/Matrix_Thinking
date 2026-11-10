const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..'),data=JSON.parse(fs.readFileSync(path.join(__dirname,'mirror_cases.json'),'utf8'));
const sourceFile=fs.existsSync(path.join(root,'03_mirror_world_makecode.ts'))?path.join(root,'03_mirror_world_makecode.ts'):path.join(root,'makecode/03_mirror_world_makecode.ts');
const source=fs.readFileSync(sourceFile,'utf8').replace(/: number\[\]/g,'').replace(/: number/g,'').replace(/: boolean/g,'');
const buttons={},gestures={},pixels=Array(25).fill(0);
const context=vm.createContext({Button:{A:'A',B:'B'},Gesture:{Shake:'shake'},Math,input:{onButtonPressed:(b,f)=>buttons[b]=f,onGesture:(g,f)=>gestures[g]=f},led:{plotBrightness:(x,y,v)=>pixels[y*5+x]=v}});
vm.runInContext(source,context);
function check(expected){assert.deepEqual(Array.from(vm.runInContext('world',context)),expected.flat());assert.deepEqual(pixels,expected.flat().map(v=>Math.round(v*255/9)));}
check(data.initial);
for(const item of data.cases){
  vm.runInContext('world = '+JSON.stringify(item.before.flat()),context);buttons.A();check(item.horizontal);buttons.A();check(item.before);
  buttons.B();check(item.vertical);buttons.B();check(item.before);
  buttons.A();buttons.B();const ab=Array.from(vm.runInContext('world',context));
  vm.runInContext('world = '+JSON.stringify(item.before.flat()),context);buttons.B();buttons.A();assert.deepEqual(Array.from(vm.runInContext('world',context)),ab);
  gestures.shake();check(data.initial);
}
console.log('PASS: MakeCode A, B, shake and LED brightness mapping agree with MicroPython on 101 matrices. Desktop adapter only.');
