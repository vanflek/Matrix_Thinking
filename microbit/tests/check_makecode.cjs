const fs = require('fs'), vm = require('vm'), assert = require('assert/strict');
const handlers = {}, display = Array.from({length:5},()=>Array(5).fill('0'));
const context = vm.createContext({Button:{A:'A',B:'B'},input:{onButtonPressed:(key,fn)=>handlers[key]=fn},
  led:{plot:(x,y)=>display[y][x]='9',unplot:(x,y)=>display[y][x]='0'}});
vm.runInContext(fs.readFileSync(__dirname+'/../makecode/01_shift_world_makecode.ts','utf8'),context);
const state = ()=>Array.from(vm.runInContext('world',context));
const picture = ()=>display.map(row=>row.join(''));
const initial=['09000','09900','00000','00000','00000'];
assert.deepEqual(state(),initial); assert.deepEqual(picture(),initial);
handlers.A();assert.deepEqual(state(),['00000','09000','09900','00000','00000']);assert.deepEqual(picture(),state());
handlers.A();assert.deepEqual(state(),['00000','00000','09000','09900','00000']);assert.deepEqual(picture(),state());
handlers.B();assert.deepEqual(state(),initial);assert.deepEqual(picture(),initial);
for(let i=0;i<5;i++)handlers.A();assert.deepEqual(state(),Array(5).fill('00000'));assert.deepEqual(picture(),state());
handlers.B();assert.deepEqual(state(),initial);assert.deepEqual(picture(),initial);
console.log('PASS: MakeCode source events, immutable row-source shift, clipping and reset match the MicroPython lesson outcomes. Desktop adapter; not a firmware test.');
