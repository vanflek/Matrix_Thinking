/* Aggregate lab engagement. No cookies, persistent IDs, coordinates or key values. */
(() => {
  'use strict';
  const config = {
    life: ['main', '#life-play', '#life-generation,#life-operation', '#life-world', '#life-reset,#life-clear', '#life-shifts button', '#life-preset,#life-numbers,#life-speed'],
    sandbox: ['main', '#sand-play', '#sand-step', '#sand-world', '#sand-reset,#sand-clear', '#sand-inspect,#sand-data', '#sand-gravity,#sand-diagonals,#sand-spread,#sand-preset'],
    snake: ['snake-lab', '#snake-play', '#snake-step', '', '#snake-restart', '#snake-board button,#snake-matrix button', '[data-turn]'],
    tetris: ['tetris-lab', '#tetris-play', '#tetris-step', '', '#tetris-restart,#tetris-demo', '#tetris-data button,#tetris-game button', '#tetris-layer,[data-action]'],
    flight: ['arena', '#arena-play', '#arena-step', '', '#arena-restart,#arena-next,[data-level]', '#arena-canvas,[data-matrix]', '#arena-object,#arena-vertex,#arena-grid,#arena-collisions,[data-control],#arena-fire'],
    raycast: ['ray-lab', '#ray-play', '#ray-step', '', '#ray-reset', '#ray-map,#ray-view,#ray-index', '#ray-fov,#ray-count,#ray-floor,#ray-numbers,[data-ray-control]'],
    xonix: ['xon-lab', '#xon-play,#xon-auto', '#xon-wave,#xon-apply', '', '#xon-restart,#xon-next,[data-demo]', '#xon-regions button', '#xon-layer,[data-xon-direction]'],
    faces: ['main', '', '', '', '#new-round', '#bit-person', '[data-feature],[data-face]'],
    edges: ['main', '', '', '#edge-input button', '#edge-reset', '', '#edge-pattern,#edge-axis,#edge-numbers'],
    index: ['main', '', '#apply', '#matrix button', '#reset', '', '#operation,input[name=color]']
  };
  const name = location.pathname.split('/').pop().replace(/\.html$/, '') || 'index';
  const cfg = config[name], params = new URLSearchParams(location.search);
  if (!cfg || navigator.webdriver || navigator.doNotTrack === '1' || navigator.globalPrivacyControl || params.get('analytics') === 'off') return;
  const root = document.getElementById(cfg[0]);
  if (!root || !crypto.randomUUID) return;
  const session = crypto.randomUUID(), sent = new Set(), pending = new Set();
  const endpoint = 'https://matrix-game-events.vanflek.workers.dev/event';
  let first = null, last = -Infinity, lastCount = -Infinity, actions = 0, active = 0, previous = performance.now(), busy = false, failures = 0, retryAt = 0;
  const visible = () => !document.hidden && document.hasFocus();
  function queue(event) {
    if (!sent.has(event)) { pending.add(event); flush(); }
  }
  async function flush() {
    if (busy || !pending.size || failures >= 6 || performance.now() < retryAt) return;
    busy = true;
    const events = [...pending];
    try {
      const response = await fetch(endpoint, { method: 'POST', mode: 'cors', credentials: 'omit', referrerPolicy: 'no-referrer', keepalive: true,
        headers: {'Content-Type': 'text/plain'}, body: JSON.stringify({v: 1, game: name, session, events, test: params.get('activity_test') === '1'}) });
      if (!response.ok) throw new Error('Unavailable');
      events.forEach(event => { sent.add(event); pending.delete(event); });
      failures = 0;
    } catch (_) {
      failures++; retryAt = performance.now() + Math.min(60000, 2000 * 2 ** failures);
      // Analytics must never interrupt a game. Retries are bounded and deduplicated.
    }
    busy = false;
  }
  function action(kind, event) {
    if (!event.isTrusted || !visible()) return;
    const now = performance.now();
    last = now;
    if (event.repeat || now - lastCount < 400) return;
    if (first === null) { first = now; previous = now; }
    lastCount = now; actions++;
    // Defer networking until the game's own event handler has completed.
    queueMicrotask(() => { queue('interacted'); queue(kind); });
  }
  function matches(target, selector) { return selector && target.closest(selector); }
  root.addEventListener('click', e => {
    const target = e.target.closest ? e.target : e.target.parentElement;
    if (!target || target.closest(':disabled,[aria-disabled=true]')) return;
    if (matches(target, cfg[1])) { if (target.closest('button').getAttribute('aria-pressed') !== 'true') action('play', e); }
    else if (matches(target, cfg[2])) action('step', e);
    else if (matches(target, cfg[3])) { if (name !== 'sandbox') action('edit', e); }
    else if (matches(target, cfg[4])) action('restart', e);
    else if (matches(target, cfg[5])) action('inspect', e);
    else if (name === 'faces' && target.closest('[data-feature]')) action('question', e);
    else if (name === 'faces' && target.closest('[data-face]')) action('guess', e);
    else if (matches(target, cfg[6]) && target.closest('button')) action('control', e);
    else if (name === 'sandbox' && target.closest('#sand-gate')) action('edit', e);
  }, true);
  document.addEventListener('visibilitychange', () => { previous = performance.now(); });
  window.addEventListener('focus', () => { previous = performance.now(); });
  root.addEventListener('change', e => { if (matches(e.target, cfg[6])) action('rule', e); }, true);
  root.addEventListener('input', e => { if (matches(e.target, cfg[6]) || e.target.matches('#ray-index')) action('inspect', e); }, true);
  root.addEventListener('pointerdown', e => {
    if (e.button !== 0) return;
    if (name === 'sandbox' && matches(e.target, cfg[3])) action('edit', e);
    else if (e.target.closest('[data-control],[data-ray-control],[data-xon-direction]')) action('control', e);
  }, true);
  root.addEventListener('keydown', e => {
    if (e.ctrlKey || e.altKey || e.metaKey || e.target.closest('input,select,textarea,button,a,summary,[contenteditable=true]')) return;
    const allowed = {
      snake: ['ArrowUp','ArrowDown','ArrowLeft','ArrowRight'],
      tetris: ['ArrowUp','ArrowDown','ArrowLeft','ArrowRight'],
      flight: ['ArrowUp','ArrowDown','ArrowLeft','ArrowRight','KeyW','KeyA','KeyS','KeyD','Space','KeyP','KeyR','Enter'],
      raycast: ['ArrowUp','ArrowDown','ArrowLeft','ArrowRight','KeyW','KeyA','KeyS','KeyD','KeyP','Enter'],
      xonix: ['ArrowUp','ArrowDown','ArrowLeft','ArrowRight','KeyP','KeyC','Enter'],
      sandbox: ['ArrowUp','ArrowDown','ArrowLeft','ArrowRight','Space','KeyI']
    };
    if (allowed[name]?.includes(e.code)) action('control', e);
  }, true);
  setInterval(() => {
    const now = performance.now(), elapsed = Math.min(1500, now - previous); previous = now;
    if (first !== null && visible() && now - last < 60000) active += elapsed;
    if (actions >= 3 && active >= 5000) queue('engaged');
    if (actions >= 3 && active >= 30000) queue('active30');
    if (actions >= 3 && active >= 120000) queue('active120');
    if (pending.size && !busy) flush();
  }, 1000);
  // No load event is sent: ordinary page views stay in Cloudflare Web Analytics.
})();
