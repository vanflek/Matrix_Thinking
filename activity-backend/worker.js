const ORIGINS = new Set(['https://matrixthinking.org', 'https://www.matrixthinking.org', 'https://vanflek.github.io']);
const GAMES = new Set(['index','snake','tetris','flight','raycast','xonix','faces','life','edges','sandbox']);
const EVENTS = new Set(['interacted','engaged','active30','active120','play','step','edit','restart','inspect','control','rule','question','guess']);
export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url), origin = request.headers.get('Origin');
    const headers = {'Cache-Control':'no-store', 'Vary':'Origin'};
    if (ORIGINS.has(origin)) Object.assign(headers, {'Access-Control-Allow-Origin':origin,'Access-Control-Allow-Methods':'POST, OPTIONS','Access-Control-Allow-Headers':'Content-Type'});
    if (url.pathname === '/health' && request.method === 'GET') {
      try { await env.DB.prepare('SELECT 1 FROM game_daily LIMIT 1').first(); return Response.json({ready:true}, {headers}); }
      catch (_) { return Response.json({ready:false}, {status:503,headers}); }
    }
    if (url.pathname !== '/event' || !ORIGINS.has(origin)) return new Response(null,{status:404,headers});
    if (request.method === 'OPTIONS') return new Response(null,{status:204,headers});
    if (request.method !== 'POST') return new Response(null,{status:405,headers});
    if (Number(request.headers.get('Content-Length')) > 2048) return new Response(null,{status:413,headers});
    try {
      const text = await request.text();
      if (text.length > 2048) return new Response(null,{status:413,headers});
      const body = JSON.parse(text);
      if (body.v !== 1 || !GAMES.has(body.game) || !/^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(body.session) ||
          !Array.isArray(body.events) || body.events.length < 1 || body.events.length > EVENTS.size || body.events.some(e => !EVENTS.has(e)) || typeof body.test !== 'boolean') return new Response(null,{status:400,headers});
      const day = new Date().toISOString().slice(0,10);
      await env.DB.batch([...new Set(body.events)].map(event => env.DB.prepare('INSERT OR IGNORE INTO game_events(day,game,session,event,test) VALUES(?,?,?,?,?)').bind(day,body.game,body.session,event,body.test?1:0)));
      // Short-lived random page IDs are used only for deduplication; retain totals.
      if (Math.random() < .02) {
        const cutoff = new Date(Date.now()-14*86400000).toISOString().slice(0,10);
        ctx.waitUntil(env.DB.prepare('DELETE FROM game_events WHERE day < ?').bind(cutoff).run());
      }
      return new Response(null,{status:204,headers});
    } catch (_) { return new Response(null,{status:503,headers}); }
  }
};
