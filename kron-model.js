(function(root,factory){const model=factory();if(typeof module==='object'&&module.exports)module.exports=model;else root.KronMatrix=model;})(typeof globalThis!=='undefined'?globalThis:this,function(){
  'use strict';
  const DUCK=[[0,0,1,1,0],[0,0,1,1,1],[1,0,1,1,0],[1,1,1,1,0],[0,1,1,0,0]];
  const copy=a=>a.map(row=>row.slice());
  function validate(a){if(!Array.isArray(a)||!a.length||!Array.isArray(a[0])||!a[0].length||a.some(row=>!Array.isArray(row)||row.length!==a[0].length))throw new Error('A nonempty rectangular matrix is required.');}
  function ones(k){if(!Number.isInteger(k)||k<1)throw new Error('A positive integer factor is required.');return Array.from({length:k},()=>Array(k).fill(1));}
  function kron(a,b){validate(a);validate(b);return Array.from({length:a.length*b.length},(_,r)=>Array.from({length:a[0].length*b[0].length},(_,c)=>a[Math.floor(r/b.length)][Math.floor(c/b[0].length)]*b[r%b.length][c%b[0].length]));}
  const enlarge=(a,k)=>kron(a,ones(k));
  function repeatAxis(a,k,axis){ones(k);if(![0,1].includes(axis))throw new Error('Axis 0 or 1 required.');return axis===0?a.flatMap(row=>Array.from({length:k},()=>row.slice())):a.map(row=>row.flatMap(v=>Array(k).fill(v)));}
  const repeated=(a,k)=>repeatAxis(repeatAxis(a,k,0),k,1);
  const roll=(a,dr,dc)=>a.map((row,r)=>row.map((_,c)=>a[((r-dr)%a.length+a.length)%a.length][((c-dc)%row.length+row.length)%row.length]));
  const rotate=a=>Array.from({length:a[0].length},(_,r)=>Array.from({length:a.length},(_,c)=>a[a.length-1-c][r]));
  const owner=(r,c,k)=>[Math.floor(r/k),Math.floor(c/k)];
  const block=(r,c,k)=>({row:r*k,column:c*k,height:k,width:k});
  const scaleBlock=(value,b)=>b.map(row=>row.map(v=>value*v));
  return{DUCK,copy,ones,kron,enlarge,repeatAxis,repeated,roll,rotate,owner,block,scaleBlock};
});
