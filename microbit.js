(() => {
  'use strict';
  const M = window.MicrobitMatrix;
  const $ = id => document.getElementById(id);
  let lesson = 'brightness', world = M.initial(lesson), before = M.copy(world), selected = [2, 2];
  let changed = false, lastAction = null;
  const cells = [], leds = [];
  const words = {
    brightness: {
      title: 'Change the brightness of the whole world.',
      intro: 'A subtracts one from every value. B adds one. Shake restores the original gradient.',
      a: 'A · Darker −1', b: 'B · Brighter +1',
      initial: 'W = initial brightness matrix',
      prompt: 'Predict what B will do to the zero in the top-left corner. Then try it.',
      rule: 'next = clip(W + amount, 0, 9)',
      detail: 'One arithmetic rule applies to all 25 values. clip keeps each result between 0 and 9.'
    },
    mirror: {
      title: 'Mirror the whole world.',
      intro: 'A reflects left to right. B reflects top to bottom. Shake restores the starting pattern.',
      a: 'A · Left ↔ right', b: 'B · Top ↕ bottom',
      initial: 'W = initial asymmetric pattern',
      prompt: 'Predict where the left-hand vertical line will move after A. Then try two presses.',
      rule: 'A: next[r, c] = W[r, 4 − c]\nB: next[r, c] = W[4 − r, c]',
      detail: 'Reorder the values without changing their brightness. Each reflection reads one unchanged source matrix.'
    },
    shift: {
      title: 'Move the world, one row at a time.',
      intro: 'A shifts every row down. A new zero row enters at the top. B restores the starting pattern.',
      a: 'A · Shift down ↓', b: 'B · Reset pattern',
      initial: 'W = initial pattern matrix',
      prompt: 'Predict where the three bright pixels will go after one press of A.',
      rule: 'next = [zero_row, W[0], W[1], W[2], W[3]]',
      detail: 'Read all source rows from the old world, then replace it. The old bottom row is discarded.'
    }
  };
  function inspect() {
    const [row, col] = selected;
    $('mb-coordinate').textContent = `W[${row}, ${col}]: ${before[row][col]} → ${world[row][col]}`;
    if (lesson === 'mirror' && (lastAction === 'left-right' || lastAction === 'top-bottom')) {
      const sourceRow = lastAction === 'top-bottom' ? 4 - row : row;
      const sourceCol = lastAction === 'left-right' ? 4 - col : col;
      $('mb-coordinate').textContent = `next[${row}, ${col}] ← W[${sourceRow}, ${sourceCol}] = ${before[sourceRow][sourceCol]}`;
    }
    $('mb-before-row').textContent = before[row].join('  ');
    $('mb-after-row').textContent = world[row].join('  ');
    $('mb-row-label').textContent = `Trace row ${row} · before → after`;
    cells.forEach((cell, i) => {
      const r = Math.floor(i / 5), c = i % 5, value = world[r][c];
      cell.textContent = value;
      cell.classList.toggle('selected', r === row && c === col);
      cell.classList.toggle('changed', changed && value !== before[r][c]);
      cell.setAttribute('aria-pressed', String(r === row && c === col));
      cell.setAttribute('aria-label', `Row ${r}, column ${c}, brightness ${value}. Inspect this cell.`);
      leds[i].style.setProperty('--glow', value === 0 ? 0 : .16 + value / 9 * .84);
      leds[i].dataset.value = value;
    });
    $('mb-leds').setAttribute('aria-label', 'LED preview, brightness rows: ' + world.map(row => row.join(' ')).join('; '));
    $('mb-rule-note').textContent = words[lesson].detail;
  }
  function choose(nextLesson) {
    lesson = nextLesson;
    world = M.initial(lesson); before = M.copy(world); changed = false; lastAction = null;
    document.querySelectorAll('[data-mb-lesson]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.mbLesson === lesson)));
    const text = words[lesson];
    $('mb-lab-title').textContent = text.title;
    $('mb-lab-intro').textContent = text.intro;
    $('mb-a').textContent = text.a; $('mb-b').textContent = text.b;
    $('mb-b').dataset.mbAction = lesson === 'shift' ? 'reset' : 'step';
    $('mb-shake').hidden = lesson === 'shift';
    $('mb-shake').textContent = lesson === 'mirror' ? 'Shake · Restore pattern' : 'Shake · Restore gradient';
    $('mb-rule').textContent = text.rule;
    $('mb-last-rule').textContent = text.initial;
    $('mb-status').textContent = text.prompt;
    $('mb-brightness-note').hidden = lesson !== 'brightness';
    $('mb-shift-note').hidden = lesson !== 'shift';
    $('mb-mirror-note').hidden = lesson !== 'mirror';
    inspect();
  }
  function apply(action) {
    before = M.copy(world);
    world = M.transform(world, lesson, action); changed = true; lastAction = action;
    const count = world.flat().filter((v, i) => v !== before.flat()[i]).length;
    const label = action === 'increase' ? 'B: next = clip(W + 1, 0, 9)'
      : action === 'decrease' ? 'A: next = clip(W − 1, 0, 9)'
      : action === 'down' ? 'A: next[row] = W[row − 1]; next[0] = 0'
      : action === 'left-right' ? 'A: next[r, c] = W[r, 4 − c]'
      : action === 'top-bottom' ? 'B: next[r, c] = W[4 − r, c]'
      : (lesson === 'shift' ? 'B' : 'Shake') + ': next = initial.copy()';
    $('mb-last-rule').textContent = label;
    $('mb-status').textContent = action === 'reset'
      ? `Starting matrix restored. ${count} of 25 values changed.`
      : `${count} of 25 values changed. The outlined cells show the differences; inspect a number to trace it.`;
    inspect();
  }
  for (let row = 0; row < 5; row++) for (let col = 0; col < 5; col++) {
    const cell = document.createElement('button'); cell.type = 'button';
    cell.addEventListener('click', () => {selected = [row, col]; inspect();});
    $('mb-matrix').append(cell); cells.push(cell);
    const led = document.createElement('span'); led.setAttribute('aria-hidden', 'true');
    $('mb-leds').append(led); leds.push(led);
  }
  document.querySelectorAll('[data-mb-lesson]').forEach(button => button.addEventListener('click', () => choose(button.dataset.mbLesson)));
  $('mb-a').addEventListener('click', () => apply(lesson === 'brightness' ? 'decrease' : lesson === 'mirror' ? 'left-right' : 'down'));
  $('mb-b').addEventListener('click', () => apply(lesson === 'brightness' ? 'increase' : lesson === 'mirror' ? 'top-bottom' : 'reset'));
  $('mb-shake').addEventListener('click', () => apply('reset'));
  const requestedLesson = new URLSearchParams(window.location.search).get('lesson');
  choose(Object.prototype.hasOwnProperty.call(words, requestedLesson) ? requestedLesson : 'brightness');
})();
