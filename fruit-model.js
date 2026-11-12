/* Browser counterpart of fruit-market.py. All prices and counts are integers. */
(function (root) {
  'use strict';
  function buildWorld() {
    const cells = [], solutions = [];
    for (let n = 1; n <= 9; n++) for (let p = 1; p <= 63; p++) {
      const bananas = 10 - n, cost = n * p, remaining = 72 - cost;
      const enough = remaining > 0, whole = remaining % bananas === 0;
      const cell = { n, p, bananas, cost, remaining, enough, whole,
        valid: enough && whole, bananaPrice: Math.floor(remaining / bananas),
        index: cells.length, solutionIndex: -1 };
      if (cell.valid) { cell.solutionIndex = solutions.length; solutions.push(cell); }
      cells.push(cell);
    }
    return { cells, solutions, prices: [...new Set(solutions.map(c => c.p))].sort((a, b) => a - b) };
  }
  function cellAt(world, n, p) {
    if (!Number.isInteger(n) || n < 1 || n > 9 || !Number.isInteger(p) || p < 1 || p > 63) throw new RangeError('Outside the 9 x 63 world');
    return world.cells[(n - 1) * 63 + p - 1];
  }
  function solutionRows(world) { return world.solutions.map(c => [c.n, c.bananas, c.p, c.bananaPrice]); }
  function matrix(world, mode) {
    if (mode === 3) return solutionRows(world);
    if (![0, 1, 2].includes(mode)) throw new RangeError('Unknown view');
    return Array.from({ length: 9 }, (_, row) => world.cells.slice(row * 63, (row + 1) * 63).map(c => mode === 0 ? c.cost : mode === 1 ? c.remaining : Number(c.valid)));
  }
  const api = { buildWorld, cellAt, solutionRows, matrix };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.FruitMarket = api;
})(typeof globalThis !== 'undefined' ? globalThis : this);
