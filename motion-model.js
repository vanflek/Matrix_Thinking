(function(root){
'use strict';
const ROWS=24,COLS=32,DUCK=['00011100','00010110','00011100','10011000','11111110','01111100','00111000','00000000'];
function frame({row=8,col=8,brightness=210,light=0,noise=0,seed=1}={}){
 if(!Number.isInteger(row)||!Number.isInteger(col)||row<0||row>16||col<0||col>24)throw new RangeError('Duck outside frame');
 return Array.from({length:ROWS*COLS},(_,i)=>{
  const r=Math.floor(i/COLS),c=i%COLS;
  let value=32+((Math.floor(r/4)+Math.floor(c/4))%2)*6;
  if(r>=row&&r<row+8&&c>=col&&c<col+8&&DUCK[r-row][c-col]==='1')value=brightness;
  return Math.max(0,Math.min(255,value+light+Math.floor((((i*37+seed*101)%17)-8)*noise/8)));
 });
}
function detect(previous,current,threshold=30){
 if(previous.length!==ROWS*COLS||current.length!==previous.length||threshold<0||threshold>255)throw new RangeError('Invalid frames or threshold');
 const difference=current.map((v,i)=>Math.abs(v-previous[i]));
 const mask=difference.map(v=>Number(v>threshold));
 const count=mask.reduce((a,b)=>a+b,0);
 return {difference,mask,count,fraction:count/(ROWS*COLS)};
}
const api={ROWS,COLS,DUCK,frame,detect};
if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.MotionWorld=api;
})(typeof globalThis!=='undefined'?globalThis:this);
