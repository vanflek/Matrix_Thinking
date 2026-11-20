const fs = require('fs'), vm = require('vm'), assert = require('assert/strict');
const path = require('path'), base = path.resolve(__dirname, '..');
const release = process.env.ACTIVITY_RELEASE ? path.resolve(process.env.ACTIVITY_RELEASE) : path.join(base,'dist');
const code = fs.readFileSync(path.join(release,'game-activity.js'),'utf8');
function browser(options={}) {
  let now=0, focus=true, hidden=false, fail=false, interval;
  const listeners={}, docListeners={}, winListeners={}, requests=[];
  const root={addEventListener:(type,fn)=>listeners[type]=fn,querySelector:()=>null};
  const document={getElementById:()=>root, hasFocus:()=>focus, get hidden(){return hidden;},addEventListener:(t,f)=>docListeners[t]=f};
  const navigator={webdriver:false, ...options.navigator};
  vm.runInNewContext(code,{document,navigator,window:{addEventListener:(t,f)=>winListeners[t]=f},crypto:require('crypto').webcrypto,
    location:{pathname:options.pathname||'/life.html',search:options.search||''},URLSearchParams,Set,performance:{now:()=>now},queueMicrotask,
    setInterval:fn=>interval=fn,fetch:async(url,req)=>{requests.push(JSON.parse(req.body));if(fail)throw Error('offline');return {ok:true};}});
  const drain=()=>new Promise(r=>setImmediate(r));
  const target=(id,attrs={})=>({closest(selector){
    if(selector==='button')return this;
    if(selector==='[data-activity-event]')return attrs.event?this:null;
    if(selector==='a[download]')return attrs.download?this:null;
    return selector.split(',').some(s=>s.trim()===id)?this:null;
  },getAttribute:name=>name==='data-activity-event'?attrs.event:'false',matches:()=>false});
  return {requests,async click(id,trusted=true,attrs={}){listeners.click?.({target:target(id,attrs),isTrusted:trusted});await drain();},
    async input(id){listeners.input?.({target:target(id),isTrusted:true});await drain();},
    async pointer(id,button=0){listeners.pointerdown?.({target:target(id),button,isTrusted:true});await drain();},
    async key(id,code){listeners.keydown?.({target:target(id),code,isTrusted:true});await drain();},
    async time(seconds){for(let i=0;i<seconds;i++){now+=1000;interval?.();await drain();}},
    focus(value){focus=value;winListeners.focus?.();},hide(value){hidden=value;docListeners.visibilitychange?.();},offline(value){fail=value;}};
}
const events=b=>b.requests.flatMap(r=>r.events);
(async()=>{
  let b=browser();await b.time(120);assert.equal(b.requests.length,0,'page load and animation are not engagement');
  await b.click('#life-play',false);assert.equal(b.requests.length,0,'synthetic events ignored');
  await b.click('#life-play');await b.time(1);assert(events(b).includes('interacted'));assert(events(b).includes('play'));
  await b.click('#life-generation');await b.time(1);await b.click('#life-world');await b.time(5);
  assert(events(b).includes('engaged'));
  await b.time(25);assert(events(b).includes('active30'));assert(!events(b).includes('active120'));
  await b.click('#life-world');await b.time(1);assert.equal(events(b).filter(e=>e==='edit').length,1,'one action category per page');
  b=browser();await b.click('#life-play');await b.time(1);await b.click('#life-generation');await b.time(1);await b.click('#life-world');
  b.hide(true);await b.time(150);assert(!events(b).includes('active30'),'hidden time excluded');
  b.hide(false);b.focus(false);await b.time(150);assert(!events(b).includes('active30'),'unfocused time excluded');
  for(const option of [{navigator:{doNotTrack:'1'}},{navigator:{globalPrivacyControl:true}},{navigator:{webdriver:true}},{search:'?analytics=off'}]){
    b=browser(option);await b.click('#life-play');await b.time(60);assert.equal(b.requests.length,0,'privacy/automation opt-out');
  }
  b=browser();b.offline(true);await b.click('#life-play');await b.time(1800);assert(b.requests.length<=6,'bounded offline retries');
  b=browser({pathname:'/microbit.html',search:'?activity_test=1'});
  await b.time(40);assert.equal(b.requests.length,0,'micro:bit page load is not an experiment');
  await b.click('a');await b.click('#mb-a',false);assert.equal(b.requests.length,0,'source links and synthetic micro:bit clicks ignored');
  await b.click('#mb-a');await b.time(1);await b.click('#mb-b[data-mb-action="step"]');await b.time(1);await b.click('#mb-shake');await b.time(5);
  assert(events(b).includes('step'));assert(events(b).includes('restart'));assert(events(b).includes('engaged'));
  await b.click('#mb-b[data-mb-action="reset"]');await b.time(1);await b.click('#mb-matrix button');await b.time(1);await b.click('[data-mb-lesson]');
  assert(events(b).includes('inspect'));assert(events(b).includes('control'));
  await b.time(30);assert(events(b).includes('active30'));assert(!events(b).includes('active120'));
  assert(b.requests.every(r=>r.game==='microbit'&&r.test===true),'micro:bit QA stays test-only');
  for(const option of [{navigator:{doNotTrack:'1'}},{navigator:{globalPrivacyControl:true}},{navigator:{webdriver:true}},{search:'?analytics=off'}]){
    b=browser({...option,pathname:'/microbit.html'});await b.click('#mb-a');await b.time(60);assert.equal(b.requests.length,0,'micro:bit respects privacy opt-out');
  }
  for (const [name, controls] of Object.entries({fruit:['#fruit-count','[data-stage]','#fruit-world'],garden:['#g-fence','[data-stage]','#g-world'],motion:['#mo-col','#mo-frame','#mo-mask'],roll:['[data-direction]','[data-tool]','#ro-reset'],scale:['[data-zs-factor]','[data-zs-op="right"]','[data-zs-op="duck"]'],kron:['[data-zs-factor]','[data-zs-op="right"]','[data-zs-op="duck"]']})) {
    b=browser({pathname:`/${name}.html`,search:'?activity_test=1'});
    await b.time(120);assert.equal(b.requests.length,0,`${name}: loading alone is not interaction`);
    for(const id of controls){if(id.includes('count')||id.includes('fence')||id.includes('col'))await b.input(id);else await b.click(id);await b.time(2);}
    await b.time(5);assert(events(b).includes('engaged'),`${name}: three genuine controls qualify`);
    assert(b.requests.every(r=>r.game===name&&r.test===true));
    for (const option of [{navigator:{doNotTrack:'1'}},{navigator:{globalPrivacyControl:true}},{navigator:{webdriver:true}},{search:'?analytics=off'}]) {
      const excluded=browser({...option,pathname:`/${name}.html`});await excluded.click(controls[1]);await excluded.time(10);assert.equal(excluded.requests.length,0,`${name}: privacy exclusion`);
    }
  }
  b=browser({pathname:'/roll.html'});await b.pointer('#ro-world',2);await b.time(1);await b.key('#ro-world','ArrowRight');assert(events(b).includes('edit'));assert(events(b).includes('control'));
  b=browser({pathname:'/kron.html'});await b.pointer('#zs-source-canvas',2);await b.time(1);await b.key('#zs-source-canvas','ArrowRight');await b.time(1);await b.click('#kr-compare');assert(events(b).includes('edit'));assert(events(b).includes('control'));
  b=browser({pathname:'/motion.html'});await b.pointer('#mo-current');await b.time(1);assert(events(b).includes('edit'));
  b=browser({pathname:'/garden.html'});await b.pointer('#g-handle');await b.time(1);assert(events(b).includes('control'));
  for (const name of ['fruit','garden','motion','roll','microbit-pycharm','sandbox','scale','kron']) {
    b=browser({pathname:`/${name}.html`});await b.click('a',false,{download:true});assert.equal(b.requests.length,0);
    await b.click('a',true,{download:true});await b.time(1);await b.click('a',true,{download:true});await b.time(1);
    assert.equal(events(b).filter(e=>e==='download_code').length,1,`${name}: one download milestone per session`);
    assert(!events(b).includes('engaged'),'one download is not sustained use');
    assert(b.requests.every(r=>Object.keys(r).sort().join(',')==='events,game,session,test,v'),'no file URLs or extra data');
  }
  b=browser({pathname:'/garden.html'});await b.click('#g-csv',true,{event:'download_data'});await b.click('#g-copy',true,{event:'copy_code'});await b.time(1);
  assert(events(b).includes('download_data'));assert(events(b).includes('copy_code'),'distinct resource milestones survive debounce');
  b=browser({pathname:'/roll.html'});await b.click('[data-direction]');await b.time(1);await b.click('[data-tool]');await b.time(1);await b.click('#ro-reset');
  for(let i=0;i<13;i++){await b.time(10);await b.click('[data-direction]');}
  assert(events(b).includes('active120'),'continued input reaches two active minutes');
  const workerPath=process.env.ACTIVITY_RELEASE?path.join(release,'activity-backend/worker.js'):path.join(__dirname,'worker.js');
  const worker=(await import('data:text/javascript;base64,'+Buffer.from(fs.readFileSync(workerPath,'utf8')).toString('base64'))).default;
  const writes=[];const DB={prepare:sql=>({bind:(...args)=>({sql,args,run:async()=>({success:true})}),first:async()=>null}),batch:async rows=>writes.push(...rows)};
  const request=(body,origin='https://matrixthinking.org')=>new Request('https://example.test/event',{method:'POST',headers:{Origin:origin},body:JSON.stringify(body)});
  const payload={v:1,game:'life',session:require('crypto').randomUUID(),events:['interacted','play','play'],test:true};
  assert.equal((await worker.fetch(request(payload),{DB},{waitUntil(){}})).status,204);assert.equal(writes.length,2,'duplicate batch event removed');
  assert.deepEqual(writes[0].args.slice(1),['life',payload.session,'interacted',1]);
  for(const game of ['fruit','garden','motion','roll','microbit-pycharm','scale','kron']){
    assert.equal((await worker.fetch(request({...payload,game,events:['download_code','copy_code','download_data']}),{DB},{waitUntil(){}})).status,204,`${game}: backend accepts new scope`);
  }
  assert.equal((await worker.fetch(request({...payload,game:'unknown'}),{DB},{waitUntil(){}})).status,400);
  assert.equal((await worker.fetch(request({...payload,events:['arbitrary_private_value']}),{DB},{waitUntil(){}})).status,400);
  const microbitPayload={...payload,game:'microbit',events:['interacted','step','restart','engaged'],session:require('crypto').randomUUID()};
  assert.equal((await worker.fetch(request(microbitPayload),{DB},{waitUntil(){}})).status,204,'collector accepts micro:bit actions');
  assert(writes.some(row=>row.args[1]==='microbit'&&row.args[3]==='step'&&row.args[4]===1));
  assert.equal((await worker.fetch(request(payload,'https://other.test'),{DB},{})).status,404);
  for(const bad of [{...payload,game:'unexpected'},{...payload,events:['typed-personal-data']},{...payload,session:'email@example.com'},{...payload,test:'false'}])
    assert.equal((await worker.fetch(request(bad),{DB},{})).status,400);
  const res=await worker.fetch(new Request('https://example.test/report'),{DB},{});assert.equal(res.status,404,'no public stats endpoint');
  assert.equal((await worker.fetch(request(payload),{DB:{batch:async()=>{throw Error('down');}}},{})).status,503);
  console.log('PASS: interaction milestones, deduplication, hidden/idle/opt-out exclusions, offline bounds, collector validation and private reports.');
})().catch(e=>{console.error(e);process.exitCode=1;});
