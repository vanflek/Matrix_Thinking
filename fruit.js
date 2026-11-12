(function () {
  'use strict';
  const M = window.FruitMarket, world = M.buildWorld();
  const $ = id => document.getElementById(id);
  const state = { n: 8, p: 7, stage: 0 };
  const count = $('fruit-count'), price = $('fruit-price'), svg = $('fruit-world');
  const axes = $('fruit-axes'), marks = $('fruit-marks'), resultValues = $('fruit-result-values');
  const stageButtons = [...document.querySelectorAll('[data-stage]')];
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  const ns = 'http://www.w3.org/2000/svg';
  const rules = [
    'apple_cost = apples * apple_price',
    'remaining = 72 - apple_cost',
    'mask = (remaining > 0) & (remaining % bananas == 0)',
    'solutions = np.column_stack((\n    apples[mask], bananas[mask],\n    apple_price[mask], banana_price[mask],\n))'
  ];
  const notes = [
    'The same multiplication fills every cell. Darker cells mean a higher total apple cost.',
    'Subtract the whole apple-cost matrix from 72. Very pale cells leave no money for bananas.',
    'Keep a cell only if the money left is positive and divides exactly among the bananas.',
    'Each True cell becomes one row. The four columns keep the quantities and their matching prices together.'
  ];
  const make = (tag, attrs, parent, text) => {
    const e = document.createElementNS(ns, tag);
    Object.entries(attrs).forEach(([key, value]) => e.setAttribute(key, value));
    if (text !== undefined) e.textContent = text;
    if (parent) parent.appendChild(e);
    return e;
  };
  const apple = '<svg viewBox="0 0 48 48" aria-hidden="true"><path d="M25 15C14 7 5 18 9 31c3 10 10 14 15 10 6 4 13-1 16-11 4-13-6-23-15-15Z" fill="#1165db"/><path d="M24 16c-1-5 1-10 4-12" fill="none" stroke="#132d45" stroke-width="2.5" stroke-linecap="round"/><path d="M26 10c1-7 10-8 13-4-3 6-9 7-13 4Z" fill="#66aa91"/><path d="M14 23c-1 3-1 6 1 9" fill="none" stroke="#bddcff" stroke-width="2" stroke-linecap="round"/></svg>';
  const banana = '<svg viewBox="0 0 48 48" aria-hidden="true"><path d="M12 9c7 19 17 23 28 18-2 12-15 19-26 11C4 31 4 19 9 10Z" fill="#ffd343" stroke="#ab7a0d" stroke-width="1.2"/><path d="M10 11c-1 16 10 27 24 23" fill="none" stroke="#b88a13" stroke-width="1.3"/><path d="m9 10 2-5 4 2-2 5M39 26l4-1 1 4-5 2" fill="#70551c"/></svg>';
  let drawn = false;
  const glyphs = world.cells.map(c => {
    const group = make('g', {}, marks);
    const rect = make('rect', { class: 'fruit-mark', role: 'gridcell', tabindex: '-1', rx: 1,
      'aria-rowindex': c.n, 'aria-colindex': c.p }, group);
    const title = make('title', {}, rect);
    title.textContent = `${c.n} apples at ${c.p}; apple cost ${c.cost}; money left ${c.remaining}; ${c.valid ? `${c.bananas} bananas at ${c.bananaPrice}, valid` : 'not a valid basket'}`;
    rect.addEventListener('click', () => choose(c.n, c.p));
    rect.addEventListener('keydown', event => {
      if (state.stage === 3 && c.valid) {
        let index = c.solutionIndex;
        if (event.key === 'ArrowUp' || event.key === 'ArrowLeft') index--;
        else if (event.key === 'ArrowDown' || event.key === 'ArrowRight') index++;
        else if (event.key === 'Home') index = 0;
        else if (event.key === 'End') index = world.solutions.length - 1;
        else if (event.key !== 'Enter' && event.key !== ' ') return;
        event.preventDefault();
        const next = world.solutions[Math.max(0, Math.min(world.solutions.length - 1, index))];
        choose(next.n, next.p); glyphs[next.index].rect.focus(); return;
      }
      let n = c.n, p = c.p;
      if (event.key === 'ArrowUp') n--;
      else if (event.key === 'ArrowDown') n++;
      else if (event.key === 'ArrowLeft') p--;
      else if (event.key === 'ArrowRight') p++;
      else if (event.key === 'Home') p = 1;
      else if (event.key === 'End') p = 63;
      else if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); choose(n, p); return; }
      else return;
      event.preventDefault();
      n = Math.min(9, Math.max(1, n)); p = Math.min(63, Math.max(1, p));
      choose(n, p);
      glyphs[(n - 1) * 63 + p - 1].rect.focus();
    });
    const texts = c.valid ? [c.n, c.bananas, c.p, c.bananaPrice].map(v => make('text', {
      class: 'fruit-answer-value', 'text-anchor': 'middle', visibility: 'hidden'
    }, resultValues, String(v))) : [];
    return { c, group, rect, texts };
  });

  function choose(n, p) {
    M.cellAt(world, n, p);
    state.n = n; state.p = p;
    count.value = String(n); price.value = String(p);
    renderInspector(); renderWorld(); renderNumeric();
  }

  function renderInspector() {
    const c = M.cellAt(world, state.n, state.p);
    $('fruit-count-value').textContent = String(c.n);
    $('fruit-price-value').textContent = `${c.p} ${c.p === 1 ? 'coin' : 'coins'}`;
    $('fruit-basket').innerHTML = apple.repeat(c.n) + banana.repeat(c.bananas);
    $('fruit-basket').setAttribute('aria-label', `${c.n} apples and ${c.bananas} bananas`);
    const bananaAnswer = c.valid ? `${c.remaining} ÷ ${c.bananas} = ${c.bananaPrice}` : c.remaining <= 0 ? 'No positive price' : `${c.remaining} / ${c.bananas} · not whole`;
    $('fruit-breakdown').innerHTML = [
      ['Apples cost', `${c.n} × ${c.p} = ${c.cost}`],
      ['Money left', `72 − ${c.cost} = ${c.remaining}`],
      ['Banana price', bananaAnswer]
    ].map(([label, value]) => `<div class="fruit-calculation"><span>${label}</span><strong>${value}</strong></div>`).join('');
    const status = $('fruit-status');
    status.dataset.valid = String(c.valid);
    status.textContent = c.valid ? `Valid: ${c.n} apples at ${c.p} + ${c.bananas} bananas at ${c.bananaPrice}. Exactly 10 fruits and 72 coins.` : c.remaining <= 0 ? 'Rejected: no money remains for a positive banana price.' : `Rejected: ${c.remaining} coins cannot be divided into ${c.bananas} equal whole-coin prices.`;
    $('fruit-selection').textContent = `Selected: apples ${c.n} · price ${c.p}`;
    document.querySelectorAll('[data-apple-price]').forEach(button => button.setAttribute('aria-pressed', String(Number(button.dataset.applePrice) === c.p)));
  }

  function renderWorld(animate = false) {
    const W = Math.max(260, svg.parentElement.clientWidth - 2 * parseFloat(getComputedStyle(svg.parentElement).paddingLeft));
    const final = state.stage === 3, columns = Math.max(1, Math.min(3, Math.floor(W / 190)));
    const gap = 18, block = (W - gap * (columns - 1)) / columns, perBlock = Math.ceil(world.solutions.length / columns);
    const left = 30, cw = (W - left - 10) / 63, top = 30, rh = 25;
    const H = final ? 40 + perBlock * 27 : top + 9 * rh + 30;
    const motion = animate && drawn && !reduced.matches;
    svg.setAttribute('viewBox', `0 0 ${W} ${H}`); svg.setAttribute('height', H);
    svg.setAttribute('aria-rowcount', final ? 46 : 9); svg.setAttribute('aria-colcount', final ? 4 : 63);
    svg.setAttribute('aria-label', final ? 'All 46 solution rows; columns are apples, bananas, apple price and banana price' : 'Candidate purchases; rows are apple counts, columns are apple prices');
    axes.replaceChildren();
    if (!final) {
      for (let n = 1; n <= 9; n++) make('text', { x: 18, y: top + (n - .5) * rh + 4, 'text-anchor': 'end' }, axes, String(n));
      (W < 450 ? [1, 15, 30, 45, 63] : [1, 7, 14, 21, 28, 35, 42, 49, 56, 63]).forEach(p => make('text', { x: left + (p - .5) * cw, y: 17, 'text-anchor': 'middle' }, axes, String(p)));
      make('text', { x: left, y: H - 5 }, axes, 'Apple price →');
      make('text', { x: W - 10, y: H - 5, 'text-anchor': 'end' }, axes, 'Rows: apple count');
    } else {
      for (let col = 0; col < columns; col++) ['Apples', 'Bananas', 'A price', 'B price'].forEach((label, i) => make('text', { x: col * (block + gap) + (i + .5) * block / 4, y: 18, 'text-anchor': 'middle' }, axes, label));
    }
    glyphs.forEach(({ c, group, rect, texts }) => {
      let x = left + (c.p - 1) * cw, y = top + (c.n - 1) * rh, w = Math.max(.5, cw - 1.3), h = rh - 3;
      const selected = c.n === state.n && c.p === state.p;
      let alpha = state.stage === 0 ? .12 + .73 * c.cost / 567 : state.stage === 1 ? c.remaining > 0 ? .16 + .69 * c.remaining / 71 : .04 : c.valid ? .85 : .055;
      if (final) {
        if (c.valid) { const col = Math.floor(c.solutionIndex / perBlock), row = c.solutionIndex % perBlock; x = col * (block + gap); y = 30 + row * 27; w = block; h = 24; alpha = selected ? .22 : .075; }
        else { h = 0; alpha = 0; }
      }
      group.style.transition = motion ? 'transform 650ms ease' : '';
      rect.style.transition = motion ? 'width 650ms ease,height 650ms ease,fill-opacity 300ms ease' : '';
      group.setAttribute('transform', `translate(${x},${y})`);
      rect.setAttribute('width', w); rect.setAttribute('height', h); rect.setAttribute('fill-opacity', alpha);
      rect.setAttribute('aria-selected', String(selected));
      rect.setAttribute('tabindex', selected && (!final || c.valid) ? '0' : '-1');
      rect.setAttribute('aria-hidden', String(final && !c.valid));
      rect.setAttribute('aria-rowindex', final && c.valid ? c.solutionIndex + 1 : c.n);
      rect.setAttribute('aria-colindex', final ? 1 : c.p);
      const shownValue = state.stage === 0 ? c.cost : state.stage === 1 ? c.remaining : Number(c.valid);
      rect.setAttribute('aria-label', final && c.valid ? `${c.n} apples, ${c.bananas} bananas, apple price ${c.p}, banana price ${c.bananaPrice}` : `${c.n} apples, apple price ${c.p}; value ${shownValue}; ${c.valid ? 'valid' : 'invalid'}`);
      texts.forEach((text, i) => {
        text.style.transition = motion ? 'x 650ms ease,y 650ms ease' : '';
        text.setAttribute('x', final ? x + (i + .5) * w / 4 : x + w / 2); text.setAttribute('y', y + 16);
        text.setAttribute('visibility', final ? 'visible' : 'hidden');
      });
    });
    $('fruit-legend').textContent = ['567 candidates · darker = higher apple cost', 'Money left · very pale = zero or negative', '46 True (1) cells · 521 False (0) cells', '46 rows · [apples, bananas, apple price, banana price]'][state.stage];
    drawn = true;
  }

  function renderNumeric() {
    if (!$('fruit-numeric').open) return;
    const table = $('fruit-matrix-table');
    if (state.stage === 3) {
      table.innerHTML = '<thead><tr><th>Apples</th><th>Bananas</th><th>Apple price</th><th>Banana price</th></tr></thead><tbody>' + world.solutions.map(c => `<tr><td class="${c.n === state.n && c.p === state.p ? 'selected' : ''}"><button type="button" data-n="${c.n}" data-p="${c.p}" aria-label="Inspect solution: ${c.n} apples at ${c.p}">${c.n}</button></td><td>${c.bananas}</td><td>${c.p}</td><td>${c.bananaPrice}</td></tr>`).join('') + '</tbody>';
      return;
    }
    const rows = M.matrix(world, state.stage);
    table.innerHTML = '<thead><tr><th scope="col">n ↓ / price →</th>' + Array.from({ length: 63 }, (_, p) => `<th scope="col">${p + 1}</th>`).join('') + '</tr></thead><tbody>' + rows.map((row, y) => `<tr><th scope="row">${y + 1}</th>` + row.map((v, x) => {
      const c = world.cells[y * 63 + x], classes = [state.stage === 2 && c.valid ? 'valid' : '', c.n === state.n && c.p === state.p ? 'selected' : ''].join(' ');
      return `<td class="${classes}"><button type="button" data-n="${c.n}" data-p="${c.p}" aria-label="${c.n} apples at ${c.p}: value ${v}">${v}</button></td>`;
    }).join('') + '</tr>').join('') + '</tbody>';
  }

  function setStage(stage) {
    state.stage = stage;
    stageButtons.forEach(button => button.setAttribute('aria-pressed', String(Number(button.dataset.stage) === stage)));
    $('fruit-rule').textContent = rules[stage]; $('fruit-stage-note').textContent = notes[stage];
    $('fruit-shape').textContent = stage === 3 ? '46 × 4' : '9 × 63';
    renderWorld(true); renderNumeric();
  }

  count.addEventListener('input', () => choose(Number(count.value), state.p));
  price.addEventListener('input', () => choose(state.n, Number(price.value)));
  stageButtons.forEach(button => button.addEventListener('click', () => setStage(Number(button.dataset.stage))));
  document.querySelectorAll('[data-example]').forEach(button => button.addEventListener('click', () => {
    const example = button.dataset.example;
    choose(example === 'valid' ? 8 : example === 'fraction' ? 3 : 9, example === 'valid' ? 7 : example === 'fraction' ? 4 : 9);
  }));
  $('fruit-numeric').addEventListener('toggle', renderNumeric);
  $('fruit-matrix-table').addEventListener('click', event => {
    const button = event.target.closest('button[data-n]');
    if (button) choose(Number(button.dataset.n), Number(button.dataset.p));
  });
  $('fruit-possible-prices').innerHTML = world.prices.map(p => `<button type="button" data-apple-price="${p}" aria-label="Inspect a solution with apple price ${p}" aria-pressed="false">${p}</button>`).join('');
  $('fruit-possible-prices').addEventListener('click', event => {
    const button = event.target.closest('[data-apple-price]');
    if (!button) return;
    const p = Number(button.dataset.applePrice), c = world.solutions.find(c => c.p === p && c.n === state.n) || world.solutions.find(c => c.p === p);
    choose(c.n, c.p);
  });
  $('fruit-copy-code').addEventListener('click', async () => {
    try { await navigator.clipboard.writeText($('fruit-python-code').textContent); $('fruit-copy-status').textContent = 'Complete Python program copied.'; }
    catch (_) { $('fruit-copy-status').textContent = 'Copy is unavailable here. Select the code below or use Download Python code.'; }
  });
  $('fruit-download-csv').addEventListener('click', () => {
    const csv = 'apples,bananas,apple_price,banana_price\n' + M.solutionRows(world).map(row => row.join(',')).join('\n') + '\n';
    const url = URL.createObjectURL(new Blob([csv], { type: 'text/csv;charset=utf-8' }));
    const a = document.createElement('a'); a.href = url; a.download = 'fruit-market-46-solutions.csv'; a.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  });
  new ResizeObserver(() => renderWorld()).observe(svg.parentElement);
  renderInspector(); setStage(0);
})();
