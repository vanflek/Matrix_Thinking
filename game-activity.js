/* Aggregate lab engagement. No cookies, persistent IDs, coordinates or key values. */
(() => {
  'use strict';
  const config = {
    scale: ['main', '', '[data-zs-op="left"],[data-zs-op="right"],[data-zs-op="up"],[data-zs-op="down"]', '', '[data-zs-op="duck"],[data-zs-op="clear"]', '#zs-source-matrix button,#zs-output-matrix button,#zs-output-canvas', '[data-zs-factor],[data-zs-tool],[data-zs-op="rotate"]'],
    kron: ['main', '', '[data-zs-op="left"],[data-zs-op="right"],[data-zs-op="up"],[data-zs-op="down"]', '', '[data-zs-op="duck"],[data-zs-op="clear"]', '#zs-source-matrix button,#zs-output-matrix button,#zs-output-canvas', '[data-zs-factor],[data-zs-tool],[data-zs-op="rotate"],#kr-compare'],
    fruit: ['main', '', '', '', '', '#fruit-world,#fruit-matrix-table', '#fruit-count,#fruit-price,[data-stage],[data-example]'],
    garden: ['main', '', '#g-lesson-next,#g-lesson-back', '', '#g-reset', '#g-world,#g-table', '#g-fence,#g-minimum,#g-width,#g-length,[data-example],[data-stage],[data-lesson],#g-best'],
    motion: ['main', '#mo-play', '#mo-frame,#mo-capture', '', '#mo-reset', '#mo-previous,#mo-difference,#mo-mask,#mo-table', '[data-scene],#mo-threshold,#mo-row,#mo-col,#mo-probe-row,#mo-probe-col,#mo-matrix-choice,#mo-light,#mo-noise,#mo-brightness'],
    roll: ['main', '', '[data-direction]', '', '#ro-reset,[data-preset]', '#ro-matrix button', '[data-tool]'],
    'microbit-pycharm': ['main', '', '', '', '', '', ''],
    microbit: ['main', '', '#mb-a,#mb-b[data-mb-action="step"],[data-mb-tilt]', '', '#mb-shake,#mb-b[data-mb-action="reset"]', '#mb-matrix button', '[data-mb-lesson]'],
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
    queueMany([event]);
  }
  function queueMany(events) {
    events.forEach(event => { if (!sent.has(event)) pending.add(event); });
    flush();
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
    if (event.repeat) return;
    // Preserve distinct milestones even when one gesture emits multiple DOM events.
    queueMicrotask(() => queueMany(['interacted', kind]));
    if (now - lastCount < 400) return;
    if (first === null) { first = now; previous = now; }
    lastCount = now; actions++;
  }
  function matches(target, selector) { return selector && target.closest(selector); }
  root.addEventListener('click', e => {
    const target = e.target.closest ? e.target : e.target.parentElement;
    if (!target || target.closest(':disabled,[aria-disabled=true]')) return;
    const resource = target.closest('[data-activity-event]');
    if (resource) { action(resource.getAttribute('data-activity-event'), e); return; }
    const download = target.closest('a[download]');
    if (download) { action('download_code', e); return; }
    if (matches(target, cfg[1])) { if (target.closest('button')?.getAttribute('aria-pressed') !== 'true') action('play', e); }
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
    if (e.button !== 0 && !(['roll','scale','kron'].includes(name) && e.button === 2)) return;
    if (['scale','kron'].includes(name) && e.target.closest('#zs-source-canvas')) {
      const inspect = root.querySelector('[data-zs-tool="inspect"][aria-pressed="true"]');
      action(inspect && e.button === 0 ? 'inspect' : 'edit', e);
    }
    else if (name === 'roll' && e.target.closest('#ro-world')) {
      const inspect = root.querySelector('[data-tool="inspect"][aria-pressed="true"]');
      action(inspect && e.button === 0 ? 'inspect' : 'edit', e);
    }
    else if (name === 'motion' && e.target.closest('#mo-current')) action('edit', e);
    else if (name === 'garden' && e.target.closest('#g-handle')) action('control', e);
    else if (name === 'sandbox' && matches(e.target, cfg[3])) action('edit', e);
    else if (e.target.closest('[data-control],[data-ray-control],[data-xon-direction]')) action('control', e);
  }, true);
  root.addEventListener('keydown', e => {
    if (['scale','kron'].includes(name) && !e.ctrlKey && !e.altKey && !e.metaKey && e.target.closest('#zs-source-matrix button,#zs-output-matrix button') && ['ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].includes(e.code)) { action('inspect',e); return; }
    if (e.ctrlKey || e.altKey || e.metaKey || e.target.closest('input,select,textarea,button,a,summary,[contenteditable=true]')) return;
    const allowed = {
      snake: ['ArrowUp','ArrowDown','ArrowLeft','ArrowRight'],
      tetris: ['ArrowUp','ArrowDown','ArrowLeft','ArrowRight'],
      flight: ['ArrowUp','ArrowDown','ArrowLeft','ArrowRight','KeyW','KeyA','KeyS','KeyD','Space','KeyP','KeyR','Enter'],
      raycast: ['ArrowUp','ArrowDown','ArrowLeft','ArrowRight','KeyW','KeyA','KeyS','KeyD','KeyP','Enter'],
      xonix: ['ArrowUp','ArrowDown','ArrowLeft','ArrowRight','KeyP','KeyC','Enter'],
      sandbox: ['ArrowUp','ArrowDown','ArrowLeft','ArrowRight','Space','KeyI'],
      scale: ['ArrowUp','ArrowDown','ArrowLeft','ArrowRight','Space','KeyC','KeyR','Digit1','Digit2','Digit3'],
      kron: ['ArrowUp','ArrowDown','ArrowLeft','ArrowRight','Space','KeyC','KeyR','Digit1','Digit2','Digit3'],
      roll: ['ArrowUp','ArrowDown','ArrowLeft','ArrowRight','Space','KeyC','KeyR'],
      motion: ['ArrowUp','ArrowDown','ArrowLeft','ArrowRight'],
      fruit: ['ArrowUp','ArrowDown','ArrowLeft','ArrowRight','Home','End','Enter','Space'],
      garden: ['ArrowUp','ArrowDown','ArrowLeft','ArrowRight','Home','End','Enter','Space']
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


