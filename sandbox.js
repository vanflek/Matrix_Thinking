(function () {
  'use strict';
  const M = MatrixSandbox, rows = 24, cols = 36, cell = 20;
  const $ = id => document.getElementById('sand-' + id);
  const names = ['empty', 'sand', 'water', 'wall'];
  const palette = ['#f0f5fa', '#ffd343', '#1165db', '#132d45'];
  const moveNames = ['stay', 'fall with gravity', 'fall diagonally', 'spread sideways', 'swap sand and water'];
  let W = M.preset(), tick = 0, brush = 1, radius = 1;
  let selected = 8 * cols + 18, running = false, timer = null, analysis;
  let painting = false, lastPoint = null, inspected = false;

  function options() {
    return {tick, gravity: $('gravity').value, diagonals: $('diagonals').checked, spread: $('spread').checked};
  }
  function announce(message) { $('status').textContent = message; }
  function pause(message) {
    running = false;
    clearTimeout(timer); timer = null;
    $('play').textContent = 'Play'; $('play').setAttribute('aria-pressed', 'false');
    if (message) announce(message);
  }
  function schedule() {
    if (!running) return;
    timer = setTimeout(() => { commit(false); schedule(); }, Number($('speed').value));
  }
  function toggle() {
    if (running) { pause('Paused. Inspect a cell or paint a new rule environment.'); return; }
    running = true; $('play').textContent = 'Pause'; $('play').setAttribute('aria-pressed', 'true');
    announce('Running. The two upper views show the same current matrix; the lower views preview the next step.');
    schedule();
  }
  function rebuild() { analysis = M.analyze(W, rows, cols, options()); render(); }
  function commit(manual = true) {
    const moves = analysis.accepted.length;
    W = analysis.next; tick++; inspected = false; rebuild();
    if (manual) announce(`Applied step ${tick}: ${moves} accepted moves. The preview now shows step ${tick + 1}.`);
    if (!moves && running) pause(`No moves remain at step ${tick}. Change the world or its rules to continue.`);
  }
  function inspect() {
    pause(); inspected = true; rebuild();
    announce(`Step ${tick + 1} is a preview: ${analysis.accepted.length} accepted moves, ${analysis.rejected.length} competing proposals wait. Apply next world to commit.`);
  }
  function outline(ctx, index, color = '#bf8100', width = 2) {
    ctx.strokeStyle = color; ctx.lineWidth = width;
    ctx.strokeRect((index % cols) * cell + 1, Math.floor(index / cols) * cell + 1, cell - 2, cell - 2);
  }
  function drawWorld(canvas, world, numbers, changes) {
    const ctx = canvas.getContext('2d'); ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.font = '14px Consolas, monospace';
    for (let i = 0; i < world.length; i++) {
      const v = world[i], x = (i % cols) * cell, y = Math.floor(i / cols) * cell;
      ctx.fillStyle = palette[v]; ctx.fillRect(x, y, cell, cell);
      ctx.strokeStyle = v === 3 ? '#31506b' : '#d5e2ee'; ctx.lineWidth = .6;
      ctx.strokeRect(x + .5, y + .5, cell - 1, cell - 1);
      if (numbers) {
        ctx.fillStyle = v >= 2 ? '#fff' : (v === 0 ? '#526b80' : '#132d45');
        ctx.fillText(v, x + cell / 2, y + cell / 2 + .5);
      } else if (v === 1) {
        ctx.fillStyle = '#fff1a2'; ctx.fillRect(x + 3, y + 3, 8, 3);
        ctx.fillStyle = '#c68b16'; ctx.fillRect(x + 15, y + 13, 3, 4);
      } else if (v === 2) {
        ctx.fillStyle = '#66b4ff'; ctx.fillRect(x + 2, y + 3, 14, 2);
      } else if (v === 3) {
        ctx.fillStyle = '#294b68'; ctx.fillRect(x + 2, y + 2, 16, 2);
      }
      if (changes && world[i] !== W[i]) outline(ctx, i, '#569b9c', 1.5);
    }
    outline(ctx, selected);
  }
  function drawMask() {
    const canvas = $('mask'), ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    const colors = ['#f0f5fa', '#1165db', '#387aaa', '#18887f', '#ffd343'];
    const boolean = $('boolean').checked;
    ctx.font = '14px Consolas, monospace'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    for (let i = 0; i < W.length; i++) {
      const kind = boolean ? +(analysis.moves[i] > 0) : analysis.moves[i], x = i % cols * cell, y = Math.floor(i / cols) * cell;
      ctx.fillStyle = colors[kind]; ctx.fillRect(x + 1, y + 1, cell - 2, cell - 2);
      ctx.fillStyle = kind === 0 ? '#526b80' : kind === 4 ? '#132d45' : '#fff';
      ctx.fillText(kind, x + 10, y + 10);
    }
    for (const move of analysis.rejected) outline(ctx, move.source, '#b56118', 1.7);
    if ($('arrows').checked) for (const move of analysis.accepted) {
      const x = move.source % cols * cell + 10, y = Math.floor(move.source / cols) * cell + 10;
      const dx = (move.target % cols - move.source % cols) * 9;
      const dy = (Math.floor(move.target / cols) - Math.floor(move.source / cols)) * 9;
      const angle = Math.atan2(dy, dx);
      ctx.strokeStyle = move.kind === 4 ? '#132d45' : '#163957'; ctx.lineWidth = 1.5;
      // Offset to the cell edge so the numeric mask remains legible.
      const ax = x + 5, ay = y + 5, ex = ax + dx, ey = ay + dy;
      ctx.beginPath(); ctx.moveTo(ax, ay); ctx.lineTo(ex, ey);
      ctx.lineTo(ex - 4 * Math.cos(angle - .6), ey - 4 * Math.sin(angle - .6));
      ctx.moveTo(ex, ey); ctx.lineTo(ex - 4 * Math.cos(angle + .6), ey - 4 * Math.sin(angle + .6)); ctx.stroke();
    }
    outline(ctx, selected);
    $('mask-legend').textContent = boolean ? 'M = (move_code > 0) · 0 No accepted source · 1 Accepted source' : '0 No own move · 1 Fall · 2 Diagonal · 3 Spread · 4 Sand-water swap';
    canvas.setAttribute('aria-label', boolean ? 'Boolean mask of accepted source proposals: 1 accepted, 0 no accepted source. Orange outlines mark rejected proposals.' : 'Accepted source move codes: 0 no own move, 1 gravity, 2 diagonal, 3 spreading, 4 sand-water swap. Orange outlines mark rejected proposals.');
  }
  function cellInfo() {
    const r = Math.floor(selected / cols), c = selected % cols, kind = analysis.moves[selected];
    const accepted = analysis.accepted.find(m => m.source === selected);
    const displaced = analysis.accepted.find(m => m.target === selected && m.kind === 4);
    const rejected = analysis.rejected.some(m => m.source === selected);
    let explanation = W[selected] === 0 ? 'Empty cells can receive a particle.' :
      W[selected] === 3 ? 'Walls never move.' : 'No permitted destination is available in this snapshot.';
    if (accepted) explanation = `Accepted: ${moveNames[kind]} → [${Math.floor(accepted.target / cols)}, ${accepted.target % cols}].`;
    else if (displaced) explanation = `Water is displaced by sinking sand → [${Math.floor(displaced.source / cols)}, ${displaced.source % cols}].`;
    else if (rejected) explanation = 'A move was proposed, but another accepted move claimed a cell first.';
    $('cell').textContent = `W[${r}, ${c}] = ${W[selected]} (${names[W[selected]]}). ${explanation} Next value: ${analysis.next[selected]}.`;
  }
  function render() {
    drawWorld($('world'), W, false, false); drawWorld($('data'), W, true, false);
    drawMask(); drawWorld($('next'), analysis.next, true, true);
    cellInfo();
    $('tick').textContent = `STEP ${tick}`;
    $('next-label').textContent = `STEP ${tick + 1} · PREVIEW`;
    $('counts').textContent = `Sand: ${analysis.counts[1]}  ·  Water: ${analysis.counts[2]}  ·  Walls: ${analysis.counts[3]}. Counts are conserved during simulation.`;
    $('mask-caption').textContent = `${analysis.requested.reduce((a, b) => a + b, 0)} source proposals → ${analysis.accepted.length} accepted moves. ${analysis.rejected.length} orange-outlined sources wait. Uncheck Boolean to see each move type. Swapped water is carried back to the sand's source; it has no separate accepted source proposal.`;
    for (let i = 0; i < 3; i++) $('stage' + i).classList.toggle('active', i === 0 || inspected);
  }
  function point(event, canvas) {
    const rect = canvas.getBoundingClientRect();
    return {r: Math.max(0, Math.min(rows - 1, Math.floor((event.clientY - rect.top) / rect.height * rows))),
      c: Math.max(0, Math.min(cols - 1, Math.floor((event.clientX - rect.left) / rect.width * cols)))};
  }
  function paintAt(r, c) {
    selected = r * cols + c;
    for (let dr = -radius; dr <= radius; dr++) for (let dc = -radius; dc <= radius; dc++) {
      const nr = r + dr, nc = c + dc;
      if (nr <= 0 || nc <= 0 || nr >= rows - 1 || nc >= cols - 1) continue;
      W[nr * cols + nc] = brush;
    }
    inspected = false;
  }
  $('world').addEventListener('pointerdown', e => {
    if (e.button !== 0) return;
    e.preventDefault(); pause(); $('world').focus({preventScroll: true});
    painting = true; lastPoint = point(e, $('world')); $('world').setPointerCapture(e.pointerId);
    paintAt(lastPoint.r, lastPoint.c); rebuild();
  });
  $('world').addEventListener('pointermove', e => {
    if (!painting) return;
    const p = point(e, $('world')), n = Math.max(Math.abs(p.r - lastPoint.r), Math.abs(p.c - lastPoint.c));
    for (let k = 1; k <= n; k++) paintAt(Math.round(lastPoint.r + (p.r - lastPoint.r) * k / n), Math.round(lastPoint.c + (p.c - lastPoint.c) * k / n));
    lastPoint = p; rebuild();
  });
  const endPaint = () => {
    if (!painting) return;
    painting = false; lastPoint = null;
    announce(`World edited with ${names[brush]}. Paused; inspect rules or press Play.`);
  };
  $('world').addEventListener('pointerup', endPaint);
  $('world').addEventListener('pointercancel', endPaint);
  $('world').addEventListener('lostpointercapture', endPaint);
  $('data').addEventListener('pointerdown', e => { const p = point(e, $('data')); selected = p.r * cols + p.c; render(); });
  for (const canvas of [$('world'), $('data')]) canvas.addEventListener('keydown', e => {
    const keys = {ArrowLeft: [0, -1], ArrowRight: [0, 1], ArrowUp: [-1, 0], ArrowDown: [1, 0]};
    if (keys[e.key]) {
      e.preventDefault(); pause();
      const [dr, dc] = keys[e.key], r = Math.floor(selected / cols), c = selected % cols;
      selected = Math.max(0, Math.min(rows - 1, r + dr)) * cols + Math.max(0, Math.min(cols - 1, c + dc)); render();
    } else if (e.key === ' ') {
      e.preventDefault(); pause();
      if (canvas === $('world')) { paintAt(Math.floor(selected / cols), selected % cols); rebuild(); announce('Cell painted.'); }
      else { inspect(); }
    } else if (e.key.toLowerCase() === 'i') { e.preventDefault(); inspect(); }
  });
  $('brushes').addEventListener('click', e => {
    const button = e.target.closest('button[data-brush]'); if (!button) return;
    brush = Number(button.dataset.brush);
    for (const b of $('brushes').querySelectorAll('button')) b.setAttribute('aria-pressed', String(b === button));
  });
  $('size').addEventListener('change', () => { radius = Number($('size').value); });
  $('play').addEventListener('click', toggle); $('step').addEventListener('click', () => { pause(); commit(); });
  $('inspect').addEventListener('click', inspect);
  function reset() {
    pause(); W = M.preset($('preset').value); tick = 0; inspected = false;
    $('gate').disabled = $('preset').value !== 'reservoirs'; rebuild();
    announce('Scene reset. Predict what will move, then inspect the rules.');
  }
  $('preset').addEventListener('change', reset); $('reset').addEventListener('click', reset);
  $('clear').addEventListener('click', () => {
    pause(); W = W.map(v => v === 3 ? 3 : 0); inspected = false; rebuild();
    announce('Particles cleared. Walls remain; paint new sand or water.');
  });
  $('gate').addEventListener('click', () => {
    pause(); for (let r = 8; r <= 9; r++) W[r * cols + 18] = 0;
    $('gate').disabled = true; inspected = false; rebuild();
    announce('Upper gate opened. Water has a route down. Press Play or apply one step.');
  });
  for (const id of ['gravity', 'diagonals', 'spread']) $(id).addEventListener('change', () => {
    pause(); inspected = false; rebuild(); announce('Rule changed. The preview uses the new rule for the whole field.');
  });
  $('arrows').addEventListener('change', drawMask);
  $('boolean').addEventListener('change', drawMask);
  $('speed').addEventListener('change', () => { if (running) { clearTimeout(timer); schedule(); } });
  document.addEventListener('visibilitychange', () => { if (document.hidden && running) pause('Paused while the page is hidden.'); });
  window.addEventListener('blur', () => { if (running) pause('Paused when focus left the page.'); });
  window.addEventListener('keydown', e => { if (e.key === 'Escape' && running) pause('Paused.'); });
  rebuild(); announce('Paused. Two pools, two heights. Open the upper gate or paint your own world.');
})();
