/* Exact browser model of garden-numpy.py; drawing is handled separately. */
(function(root){
'use strict';
function buildWorld(fence=24,minimum=30){
  if(!Number.isInteger(fence)||fence<4||fence>200||!Number.isInteger(minimum)||minimum<1) throw new RangeError('Use a whole fence budget of 4–200 m and a positive whole minimum area.');
  const n=Math.floor(fence/2),cells=[],solutions=[];
  let largestWithinFence=0,largestValid=null;
  for(let width=1;width<=n;width++)for(let length=1;length<=n;length++){
    const perimeter=2*(width+length),area=width*length;
    const fenceOk=perimeter<=fence,areaOk=area>=minimum;
    const c={width,length,perimeter,area,fenceOk,areaOk,valid:fenceOk&&areaOk,index:cells.length,solutionIndex:-1};
    if(fenceOk)largestWithinFence=Math.max(largestWithinFence,area);
    if(c.valid){c.solutionIndex=solutions.length;solutions.push(c);largestValid=Math.max(largestValid||0,area);}
    cells.push(c);
  }
  const best=solutions.filter(c=>c.area===largestValid);
  const distinct=new Set(solutions.map(c=>[Math.min(c.width,c.length),Math.max(c.width,c.length)].join(','))).size;
  return {fence,minimum,n,cells,solutions,best,distinct,largestWithinFence,
    fenceCount:cells.filter(c=>c.fenceOk).length,areaCount:cells.filter(c=>c.areaOk).length};
}
function cellAt(world,width,length){
  if(!Number.isInteger(width)||!Number.isInteger(length)||width<1||length<1||width>world.n||length>world.n)throw new RangeError('Outside the world');
  return world.cells[(width-1)*world.n+length-1];
}
function rows(world){return world.solutions.map(c=>[c.width,c.length,c.perimeter,c.area]);}
function matrix(world,stage){
  if(stage===4)return rows(world);
  if(![0,1,2,3].includes(stage))throw new RangeError('Unknown stage');
  return Array.from({length:world.n},(_,i)=>world.cells.slice(i*world.n,(i+1)*world.n).map(c=>stage===0?c.perimeter:Number(stage===1?c.fenceOk:stage===2?c.areaOk:c.valid)));
}
function fromPoint(world,x,y,originX,originY,unit){
  return {width:Math.max(1,Math.min(world.n,Math.round((y-originY)/unit))),length:Math.max(1,Math.min(world.n,Math.round((x-originX)/unit)))};
}
const api={buildWorld,cellAt,rows,matrix,fromPoint};
if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.GardenWorld=api;
})(typeof globalThis!=='undefined'?globalThis:this);

