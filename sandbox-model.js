/* Whole-field sandbox: matrix shifts and Boolean masks, packed as BigInt planes.
 * analyzeState is the physics kernel. Its loops visit a fixed list of directions,
 * never cells or particles. fromWorld/toWorld/display are display/edit adapters.
 */
(function (root) {
  'use strict';
  const EMPTY = 0, SAND = 1, WATER = 2, WALL = 3;
  const GRAVITY = {down: [1, 0], left: [0, -1], up: [-1, 0], right: [0, 1]};

  const geometries = new Map();
  function geometry(rows, cols) {
    if (!Number.isInteger(rows) || !Number.isInteger(cols) || rows < 1 || cols < 1) throw new Error('Invalid matrix dimensions.');
    const key = `${rows},${cols}`;
    if (geometries.has(key)) return geometries.get(key);
    const size = rows * cols, full = (1n << BigInt(size)) - 1n;
    const row = (1n << BigInt(cols)) - 1n;
    const left = full / row, right = left << BigInt(cols - 1);
    const evenColumns = (((1n << BigInt(cols + (cols & 1))) - 1n) / 3n) & row;
    const pair = evenColumns | ((row ^ evenColumns) << BigInt(cols));
    const pairWidth = 2 * cols, paddedRows = 2 * Math.ceil(rows / 2);
    const repeat = ((1n << BigInt(paddedRows * cols)) - 1n) / ((1n << BigInt(pairWidth)) - 1n);
    const even = pair * repeat & full;
    // Reduction masks sum all bits with log2(N) whole-field operations.
    const padded = 2 ** Math.ceil(Math.log2(size)), reductions = [];
    for (let width = 1; width < padded; width *= 2) {
      const low = (1n << BigInt(width)) - 1n;
      const copies = ((1n << BigInt(padded)) - 1n) / ((1n << BigInt(2 * width)) - 1n);
      reductions.push({shift: BigInt(width), mask: low * copies});
    }
    const g = {rows, cols, size, full, even, left, right, reductions};
    geometries.set(key, g); return g;
  }
  function shift(bits, dr, dc, g) {
    // Zero exterior; clear edge columns BEFORE shifting to prevent row wrapping.
    if (dc > 0) bits &= g.full ^ g.right;
    if (dc < 0) bits &= g.full ^ g.left;
    const offset = dr * g.cols + dc;
    return (offset >= 0 ? bits << BigInt(offset) : bits >> BigInt(-offset)) & g.full;
  }
  const neighbor = (bits, dr, dc, g) => shift(bits, -dr, -dc, g);
  function population(bits, g) {
    for (const {shift: n, mask} of g.reductions) bits = (bits & mask) + ((bits >> n) & mask);
    return Number(bits);
  }
  function fromWorld(world, rows, cols) {
    const g = geometry(rows, cols);
    if (world.length !== g.size) throw new Error('World dimensions do not match.');
    let sand = 0n, water = 0n, walls = 0n, bit = 1n;
    // Import an edited/display matrix. Not used to advance simulation time.
    for (const value of world) {
      if (value === SAND) sand |= bit;
      else if (value === WATER) water |= bit;
      else if (value === WALL) walls |= bit;
      else if (value !== EMPTY) throw new Error('Unknown material ID.');
      bit <<= 1n;
    }
    return {g, sand, water, walls};
  }
  function analyzeState(state, options = {}) {
    const {g, sand, water, walls} = state, {full} = g;
    const empty = full ^ (sand | water | walls), mobile = sand | water;
    const [dy, dx] = GRAVITY[options.gravity || 'down'] || GRAVITY.down;
    const [py, px] = [-dx, dy], even = g.even;
    const plus = (options.tick & 1) ? full ^ even : even, minus = full ^ plus;
    const phases = [{dr: dy, dc: dx, scope: full, kind: 1}];
    if (options.diagonals !== false) {
      phases.push({dr: dy + py, dc: dx + px, scope: plus, kind: 2},
        {dr: dy - py, dc: dx - px, scope: minus, kind: 2},
        {dr: dy + py, dc: dx + px, scope: minus, kind: 2},
        {dr: dy - py, dc: dx - px, scope: plus, kind: 2});
    }
    if (options.spread !== false) {
      phases.push({dr: py, dc: px, scope: plus & water, kind: 3},
        {dr: -py, dc: -px, scope: minus & water, kind: 3},
        {dr: py, dc: px, scope: minus & water, kind: 3},
        {dr: -py, dc: -px, scope: plus & water, kind: 3});
    }
    let remaining = mobile, claimed = 0n, requested = 0n, targets = 0n;
    let outSand = 0n, inSand = 0n, outWater = 0n, inWater = 0n;
    const kinds = [0n, 0n, 0n, 0n, 0n], groups = [];
    // The only physics loop visits at most NINE directional masks, not cells.
    for (const {dr, dc, scope, kind} of phases) {
      let allowed = full;
      if (kind === 2) allowed ^= neighbor(walls, dy, dx, g) & neighbor(walls, dr - dy, dc - dx, g);
      const emptyAhead = neighbor(empty, dr, dc, g);
      const swapEligible = kind === 3 ? 0n : sand & neighbor(water, dr, dc, g);
      const proposed = remaining & scope & allowed & (emptyAhead | swapEligible);
      remaining &= full ^ proposed; requested |= proposed;
      let free = full ^ claimed;
      // First accept all non-overlapping sand-water swaps for this direction.
      const swaps = proposed & swapEligible & free & neighbor(free, dr, dc, g);
      claimed |= swaps | shift(swaps, dr, dc, g);
      free = full ^ claimed;
      const ordinary = proposed & emptyAhead & free & neighbor(free, dr, dc, g);
      const accepted = swaps | ordinary, destination = shift(accepted, dr, dc, g);
      claimed |= ordinary | shift(ordinary, dr, dc, g); targets |= destination;
      const sandSources = accepted & sand, waterSources = accepted & water;
      outSand |= sandSources; inSand |= shift(sandSources, dr, dc, g);
      outWater |= waterSources | shift(swaps, dr, dc, g);
      inWater |= shift(waterSources, dr, dc, g) | swaps;
      kinds[kind] |= ordinary; kinds[4] |= swaps;
      groups.push({dr, dc, kind, proposed, accepted, swaps, rejected: proposed & (full ^ accepted)});
    }
    const nextState = {g, sand: (sand & (full ^ outSand)) | inSand,
      water: (water & (full ^ outWater)) | inWater, walls};
    const acceptedMask = kinds[1] | kinds[2] | kinds[3] | kinds[4];
    return {nextState, kinds, groups, requested, targets, claimed, acceptedMask,
      counts: [population(empty, g), population(sand, g), population(water, g), population(walls, g)],
      proposedCount: population(requested, g), acceptedCount: population(acceptedMask, g)};
  }

  // Canvas/inspection adapters: expanding bits for pixels and arrows is NOT physics.
  function expand(bits, size) {
    return Uint8Array.from(bits.toString(2).padStart(size, '0').split('').reverse(), Number);
  }
  function toWorld(state) {
    const {g} = state, s = expand(state.sand, g.size), w = expand(state.water, g.size), b = expand(state.walls, g.size);
    return Uint8Array.from(s, (value, i) => value + 2 * w[i] + 3 * b[i]);
  }
  function display(state, result) {
    const {g} = state, world = toWorld(state), moves = new Uint8Array(g.size), accepted = [], rejected = [];
    for (const group of result.groups) {
      const acceptedCells = expand(group.accepted, g.size), rejectedCells = expand(group.rejected, g.size), swaps = expand(group.swaps, g.size);
      for (let source = 0; source < g.size; source++) {
        const kind = swaps[source] ? 4 : group.kind;
        if (acceptedCells[source]) { moves[source] = kind; accepted.push({source, target: source + group.dr * g.cols + group.dc, value: world[source], kind}); }
        if (rejectedCells[source]) rejected.push({source, target: source + group.dr * g.cols + group.dc, value: world[source], kind});
      }
    }
    return {...result, next: toWorld(result.nextState), moves, accepted, rejected,
      requested: expand(result.requested, g.size), targets: expand(result.targets, g.size), rows: g.rows, cols: g.cols};
  }
  function analyze(world, rows, cols, options = {}) {
    const state = fromWorld(world, rows, cols);
    return display(state, analyzeState(state, options));
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
  const api = {EMPTY, SAND, WATER, WALL, GRAVITY, analyze, analyzeState, fromWorld, toWorld, display, geometry, shift, population, preset};
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  root.MatrixSandbox = api;
})(typeof globalThis !== 'undefined' ? globalThis : this);
