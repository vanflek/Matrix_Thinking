(function (root, factory) {
  const model = factory();
  if (typeof module === 'object' && module.exports) module.exports = model;
  else root.ScaleMatrix = model;
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';
  const DUCK = [[0,0,1,1,0],[0,0,1,1,1],[1,0,1,1,0],[1,1,1,1,0],[0,1,1,0,0]];
  const copy = a => a.map(row => row.slice());
  function repeatAxis(a, factor, axis) {
    if (!Number.isInteger(factor) || factor < 1 || ![0,1].includes(axis)) throw new Error('Positive integer factor and axis 0 or 1 required.');
    return axis === 0 ? a.flatMap(row => Array.from({length:factor}, () => row.slice())) : a.map(row => row.flatMap(value => Array(factor).fill(value)));
  }
  const enlarge = (a, factor) => repeatAxis(repeatAxis(a, factor, 0), factor, 1);
  const roll = (a, dr, dc) => a.map((row,r) => row.map((_,c) => a[((r-dr)%a.length+a.length)%a.length][((c-dc)%row.length+row.length)%row.length]));
  const rotate = a => Array.from({length:a[0].length}, (_,r) => Array.from({length:a.length}, (_,c) => a[a.length-1-c][r]));
  const owner = (r,c,factor) => [Math.floor(r/factor),Math.floor(c/factor)];
  const block = (r,c,factor) => ({row:r*factor,column:c*factor,height:factor,width:factor});
  return {DUCK,copy,repeatAxis,enlarge,roll,rotate,owner,block};
});
