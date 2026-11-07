/* A closed, synchronous cellular sandbox. No rendering dependencies. */
(function (root) {
  'use strict';
  const EMPTY = 0, SAND = 1, WATER = 2, WALL = 3;
  const GRAVITY = {down: [1, 0], left: [0, -1], up: [-1, 0], right: [0, 1]};

  function analyze(world, rows, cols, options = {}) {
    if (world.length !== rows * cols) throw new Error('World dimensions do not match.');
    const tick = options.tick || 0;
    const [dy, dx] = GRAVITY[options.gravity || 'down'] || GRAVITY.down;
    const perpendicular = [-dx, dy];
    const proposals = [], requested = new Uint8Array(world.length);
    const valid = (r, c) => r >= 0 && c >= 0 && r < rows && c < cols;
    // Each source reads only W, never a partly updated world.
    for (let source = 0; source < world.length; source++) {
      const value = world[source];
      if (value !== SAND && value !== WATER) continue;
      const r = Math.floor(source / cols), c = source % cols;
      const side = ((r + c + tick) & 1) ? -1 : 1;
      const directions = [[dy, dx, 1]]; // 1 = gravity
      if (options.diagonals !== false) {
        for (const sign of [side, -side]) {
          directions.push([dy + sign * perpendicular[0], dx + sign * perpendicular[1], 2]);
        }
      }
      if (value === WATER && options.spread !== false) {
        for (const sign of [side, -side]) directions.push([sign * perpendicular[0], sign * perpendicular[1], 3]);
      }
      for (const [dr, dc, kind] of directions) {
        const nr = r + dr, nc = c + dc;
        if (!valid(nr, nc)) continue;
        const target = nr * cols + nc, targetValue = world[target];
        const swap = value === SAND && targetValue === WATER && kind !== 3;
        if (targetValue !== EMPTY && !swap) continue;
        // A diagonal may go around one corner, but not between two touching walls.
        if (kind === 2 && world[(r + dy) * cols + c + dx] === WALL &&
            world[(r + dr - dy) * cols + c + dc - dx] === WALL) continue;
        proposals.push({source, target, value, kind: swap ? 4 : kind});
        requested[source] = 1;
        break;
      }
    }
    // Alternating order avoids a permanently preferred side. Swaps claim BOTH cells.
    // A water particle displaced by sand cannot also take its own proposed move.
    const ordered = (tick & 1) ? proposals.slice().reverse() : proposals;
    const claimed = new Uint8Array(world.length), accepted = [], rejected = [];
    const moves = new Uint8Array(world.length), targets = new Uint8Array(world.length);
    const next = world.slice();
    for (const move of ordered) {
      const {source, target, kind} = move;
      if (claimed[source] || claimed[target]) { rejected.push(move); continue; }
      claimed[source] = claimed[target] = 1;
      accepted.push(move);
      moves[source] = kind;
      targets[target] = 1;
      next[target] = world[source];
      next[source] = world[target];
    }
    const counts = [0, 0, 0, 0];
    for (const value of world) counts[value]++;
    return {next, moves, targets, requested, accepted, rejected, counts, rows, cols};
  }

  function preset(name = 'reservoirs', rows = 24, cols = 36) {
    const world = new Uint8Array(rows * cols);
    const put = (r, c, v) => { if (r >= 0 && c >= 0 && r < rows && c < cols) world[r * cols + c] = v; };
    for (let r = 0; r < rows; r++) { put(r, 0, WALL); put(r, cols - 1, WALL); }
    for (let c = 0; c < cols; c++) { put(0, c, WALL); put(rows - 1, c, WALL); }
    if (name === 'empty') return world;
    if (name === 'hourglass') {
      for (let r = 2; r < 11; r++) {
        put(r, 5 + r, WALL); put(r, 30 - r, WALL);
        if (r < 9) for (let c = 6 + r; c < 30 - r; c++) put(r, c, SAND);
      }
      for (let r = 16; r < 22; r++) for (let c = 6; c < 30; c++) put(r, c, WATER);
      return world;
    }
    for (let c = 4; c <= 18; c++) put(10, c, WALL);
    for (let r = 5; r <= 10; r++) { put(r, 4, WALL); put(r, 18, WALL); }
    for (let r = 7; r < 10; r++) for (let c = 5; c < 18; c++) put(r, c, WATER);
    for (let c = 17; c <= 33; c++) put(21, c, WALL);
    for (let r = 17; r <= 21; r++) { put(r, 17, WALL); put(r, 33, WALL); }
    for (let c = 18; c < 33; c++) put(20, c, WATER);
    for (let r = 2; r <= 6; r++) for (let c = 25 - (r - 2); c <= 25 + (r - 2); c++) put(r, c, SAND);
    return world;
  }
  const api = {EMPTY, SAND, WATER, WALL, GRAVITY, analyze, preset};
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  root.MatrixSandbox = api;
})(typeof globalThis !== 'undefined' ? globalThis : this);
