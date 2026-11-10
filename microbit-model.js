(function (root) {
  'use strict';
  const size = 5;
  const initial = lesson => lesson === 'shift'
    ? ['09000', '09900', '00000', '00000', '00000'].map(row => [...row].map(Number))
    : lesson === 'duck'
    ? ['00090', '00999', '99990', '09990', '00900'].map(row => [...row].map(Number))
    : lesson === 'mirror'
    ? ['90000', '90000', '90000', '99990', '00000'].map(row => [...row].map(Number))
    : Array.from({length: size}, (_, row) => Array.from({length: size}, (_, col) => row + col));
  const copy = world => world.map(row => row.slice());
  function transform(world, lesson, action) {
    if (action === 'reset') return initial(lesson);
    if (lesson === 'mirror' && action === 'left-right') return world.map(row => row.slice().reverse());
    if (lesson === 'mirror' && action === 'top-bottom') return copy(world).reverse();
    if (lesson === 'shift' && action === 'down') return [Array(size).fill(0), ...copy(world).slice(0, -1)];
    if (lesson === 'brightness' && (action === 'increase' || action === 'decrease')) {
      const amount = action === 'increase' ? 1 : -1;
      return world.map(row => row.map(value => Math.max(0, Math.min(9, value + amount))));
    }
    throw new Error('Unknown lesson action');
  }
  const axisState = (reading, previous) => reading < -300 ? true : reading > 300 ? false : previous;
  function duckWorld(leftRight, topBottom) {
    let world = initial('duck');
    if (leftRight) world = world.map(row => row.slice().reverse());
    if (topBottom) world.reverse();
    return world;
  }
  const api = {size, initial, copy, transform, axisState, duckWorld};
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.MicrobitMatrix = api;
})(typeof globalThis !== 'undefined' ? globalThis : this);
