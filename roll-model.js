/* A browser equivalent of NumPy roll. Rows first, columns second. */
(() => {
  'use strict';
  const size = 10;
  const duck = [[0,0,1,1,0],[0,0,1,1,1],[1,0,1,1,0],[1,1,1,1,0],[0,1,1,0,0]];
  function preset(name) {
    const world = Array(size * size).fill(0);
    if (name === 'cell') world[4 * size + 4] = 1;
    if (name === 'duck') duck.forEach((row,r) => row.forEach((v,c) => { world[(r+2)*size+c+2] = v; }));
    return world;
  }
  function roll(world, shift, axis, rows = size, cols = size) {
    if (world.length !== rows * cols || ![0,1].includes(axis) || !Number.isInteger(shift)) throw new Error('Invalid roll');
    const wrap = (i,n) => ((i % n) + n) % n;
    return world.map((_,i) => {
      const r = Math.floor(i / cols), c = i % cols;
      return world[(axis === 0 ? wrap(r-shift,rows) : r)*cols + (axis === 1 ? wrap(c-shift,cols) : c)];
    });
  }
  const api = { size, duck, preset, roll };
  if (typeof module !== 'undefined') module.exports = api;
  if (typeof window !== 'undefined') window.RollModel = api;
})();
