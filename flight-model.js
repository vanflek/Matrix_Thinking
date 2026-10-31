(function(root,factory){const api=factory();if(typeof module==='object'&&module.exports)module.exports=api;else root.WireframeGame=api;})(typeof globalThis!=='undefined'?globalThis:this,function(){'use strict';
const rad=a=>a*Math.PI/180,clamp=(x,a,b)=>Math.max(a,Math.min(b,x));
// Module 21's local aircraft vertices and edge indices, unchanged.
const planeV=[[45,0,1],[105,0,1],[90,15,1],[60,15,1],[0,90,1],[-30,90,1],[0,15,1],[-45,15,1],[-60,30,1],[-75,30,1],[-75,-30,1],[-60,-30,1],[-45,-15,1],[0,-15,1],[-30,-90,1],[0,-90,1],[60,-15,1],[90,-15,1],[90,0,1],[0,0,1]];
const planeE=[[1,2],[2,3],[3,4],[4,5],[5,6],[6,7],[7,8],[8,9],[9,10],[10,11],[11,12],[12,13],[13,14],[14,15],[15,16],[16,17],[17,1],[1,18],[18,3],[18,16],[18,19],[3,0],[16,0],[3,19],[16,19],[6,13],[19,6],[19,13],[7,12]];
const starV=[[30,0,1],[10,7.5,1],[0,30,1],[-7.5,10,1],[-30,0,1],[-10,-7.5,1],[0,-30,1],[7.5,-10,1],[0,0,1]],starE=[[0,1],[1,2],[2,3],[3,4],[4,5],[5,6],[6,7],[7,0],[8,0],[8,2],[8,4],[8,6],[1,5],[3,7]];
const hunterV=[[34,0,1],[-20,24,1],[-7,0,1],[-20,-24,1],[0,0,1]],hunterE=[[0,1],[1,2],[2,3],[3,0],[4,0],[4,1],[4,3]];
const bossV=[[65,0,1],[38,37,1],[0,52,1],[-38,37,1],[-65,0,1],[-38,-37,1],[0,-52,1],[38,-37,1],[0,0,1]],bossE=[[0,1],[1,2],[2,3],[3,4],[4,5],[5,6],[6,7],[7,0],[0,8],[2,8],[4,8],[6,8],[1,5],[3,7]];
const bulletV=[[12,0,1],[0,3,1],[-8,0,1],[0,-3,1]],bulletE=[[0,1],[1,2],[2,3],[3,0],[0,2]];
const levels=[{title:'Crossing paths',subtitle:'The book’s six enemies: diagonal motion and independent orbits.'},{title:'Orbital guard',subtitle:'Armoured orbiters, moving formations, and aimed enemy fire.'},{title:'Vector swarm',subtitle:'Pursuers and a shielded command ship with a radial attack.'}];
const mul=(a,b)=>a.map(row=>b[0].map((_,j)=>row.reduce((s,v,k)=>s+v*b[k][j],0)));const mv=(m,v)=>m.map(row=>row.reduce((s,x,i)=>s+x*v[i],0));
function matrices(o){const c=Math.cos(rad(o.angle)),q=Math.sin(rad(o.angle));const S=[[o.sx,0,0],[0,o.sy,0],[0,0,1]],R=[[c,-q,0],[q,c,0],[0,0,1]],T=[[1,0,o.x],[0,1,o.y],[0,0,1]];return {S,R,T,M:mul(T,mul(R,S))};}
const world=o=>o.v.map(v=>mv(matrices(o).M,v));const screen=v=>[384+v[0],384-v[1]];
function object(id,type,x,y,angle=0){const geom=type==='player'?[planeV,planeE]:type==='hunter'?[hunterV,hunterE]:type==='boss'?[bossV,bossE]:[starV,starE];return {id,type,x,y,oldX:x,oldY:y,angle,sx:type==='player'?.5:1,sy:type==='player'?.5:1,v:geom[0],e:geom[1],r:type==='player'?21:type==='boss'?62:34,hp:type==='boss'?10:type==='guard'?2:1,maxHp:type==='boss'?10:type==='guard'?2:1,spin:60,phase:angle,fireAt:2.5};}
function create(level=0){level=clamp(level,0,2);const s={level,player:object('player','player',0,-245,90),enemies:[],bullets:[],hostile:[],effects:[],time:0,score:0,lives:3,invulnerable:1.5,status:'ready',cooldown:0,serial:0,message:levels[level].subtitle,lastEvent:'',shots:0};
if(level===0){[-250,250].forEach((x,i)=>{const e=object('diagonal-'+i,'spinner',x,250);Object.assign(e,{motion:'bounce',vx:i?-120:120,vy:-120,spin:i?-70:70});s.enemies.push(e);});for(let i=0;i<4;i++){const e=object('orbiter-'+i,'spinner',0,0,i*90);Object.assign(e,{motion:'orbit',cx:0,cy:40,orbit:185,phase:i*90,orbitSpeed:i%2?-34:34,spin:i%2?-65:65});positionOrbit(e);s.enemies.push(e);}}
if(level===1){for(let i=0;i<6;i++){const e=object('guard-'+i,i%3===0?'guard':'spinner',0,0,i*60);Object.assign(e,{motion:'orbit',cx:0,cy:60,orbit:i%2?240:150,phase:i*60,orbitSpeed:i%2?-26:35,spin:50,fireAt:3+i*.6});positionOrbit(e);s.enemies.push(e);}for(let i=0;i<2;i++){const e=object('sweeper-'+i,'guard',i?-250:250,220);Object.assign(e,{motion:'sweep',phase:i*Math.PI,spin:-45,fireAt:4+i});s.enemies.push(e);}}
if(level===2){for(let i=0;i<4;i++){const e=object('hunter-'+i,'hunter',-255+i*170,230+(i%2)*55,270);Object.assign(e,{motion:'hunt',speed:55+i*4,spin:0,fireAt:5+i});s.enemies.push(e);}const e=object('command','boss',0,160);Object.assign(e,{motion:'boss',spin:18,fireAt:3});s.enemies.push(e);}return s;}
function positionOrbit(e){e.x=e.cx+e.orbit*Math.cos(rad(e.phase));e.y=e.cy+e.orbit*Math.sin(rad(e.phase));}
function shot(s){const p=s.player,a=rad(p.angle),nose=world(p)[1];s.bullets.push({id:'shot-'+s.serial++,x:nose[0]+12*Math.cos(a),y:nose[1]+12*Math.sin(a),vx:520*Math.cos(a),vy:520*Math.sin(a),angle:p.angle,r:9});s.shots++;}
function hostileShot(s,e,angle){const a=rad(angle);s.hostile.push({x:e.x,y:e.y,vx:135*Math.cos(a),vy:135*Math.sin(a),angle,r:6});}
function segmentDistance(ax,ay,bx,by){const dx=bx-ax,dy=by-ay,l=dx*dx+dy*dy,t=l?clamp(-(ax*dx+ay*dy)/l,0,1):0;return Math.hypot(ax+t*dx,ay+t*dy);}
function swept(a,b,r){return segmentDistance((a.oldX??a.x)-(b.oldX??b.x),(a.oldY??a.y)-(b.oldY??b.y),a.x-b.x,a.y-b.y)<=r;}
function hurt(s){if(s.invulnerable>0)return;s.lives--;s.invulnerable=1.4;s.lastEvent='Shield hit';s.effects.push({x:s.player.x,y:s.player.y,life:.5,max:.5,color:'#1265da'});if(s.lives<=0){s.status='lost';s.message='Aircraft lost. Restart this level and try a different approach.';}}
function step(s,input,dt,fireCount=0){if(s.status!=='playing')return s;dt=clamp(dt,0,.05);s.time+=dt;s.invulnerable=Math.max(0,s.invulnerable-dt);s.cooldown=Math.max(0,s.cooldown-dt);const p=s.player;p.oldX=p.x;p.oldY=p.y;p.angle=(p.angle+((input.turnLeft?1:0)-(input.turnRight?1:0))*120*dt+360)%360;const a=rad(p.angle),f=[Math.cos(a),Math.sin(a)],l=[-f[1],f[0]];let x=f[0]*((input.forward?1:0)-(input.backward?1:0))+l[0]*((input.left?1:0)-(input.right?1:0)),y=f[1]*((input.forward?1:0)-(input.backward?1:0))+l[1]*((input.left?1:0)-(input.right?1:0));const len=Math.hypot(x,y);if(len){p.x+=x/len*220*dt;p.y+=y/len*220*dt;}p.x=clamp(p.x,-329.5,329.5);p.y=clamp(p.y,-329.5,329.5);
for(let i=0;i<fireCount;i++)shot(s);if(input.auto&&s.cooldown<=0){shot(s);s.cooldown=.18;}
for(const b of [...s.bullets,...s.hostile]){b.oldX=b.x;b.oldY=b.y;b.x+=b.vx*dt;b.y+=b.vy*dt;}
for(const e of s.enemies){e.oldX=e.x;e.oldY=e.y;e.angle=(e.angle+e.spin*dt+360)%360;
if(e.motion==='bounce'){e.x+=e.vx*dt;e.y+=e.vy*dt;for(const[k,v]of [['x','vx'],['y','vy']])if(Math.abs(e[k])>347){e[k]=clamp(e[k],-347,347);e[v]*=-1;}}
if(e.motion==='orbit'){e.phase+=e.orbitSpeed*dt;positionOrbit(e);}
if(e.motion==='sweep'){e.x=270*Math.cos(s.time*.65+e.phase);e.y=100+120*Math.sin(s.time*.9+e.phase);}
if(e.motion==='hunt'){const dx=p.x-e.x,dy=p.y-e.y,d=Math.hypot(dx,dy)||1;e.x+=dx/d*e.speed*dt;e.y+=dy/d*e.speed*dt;e.angle=Math.atan2(dy,dx)*180/Math.PI;}
if(e.motion==='boss'){e.x=210*Math.sin(s.time*.32);e.y=145+65*Math.sin(s.time*.65);}
if(s.level>0&&s.time>=e.fireAt){if(e.type==='boss'){for(let j=0;j<8;j++)hostileShot(s,e,s.time*25+j*45);e.fireAt=s.time+(e.hp<=4?1.5:2.6);}else{hostileShot(s,e,Math.atan2(p.y-e.y,p.x-e.x)*180/Math.PI);e.fireAt=s.time+(e.motion==='hunt'?5:4);}}
}
const spent=new Set();for(const b of s.bullets){for(const e of s.enemies){if(e.hp<=0)continue;if(swept(b,e,b.r+e.r)){e.hp--;spent.add(b);s.effects.push({x:b.x,y:b.y,life:.3,max:.3,color:'#d69c14'});if(e.hp===0){s.score+=e.type==='boss'?1000:e.maxHp>1?200:100;s.lastEvent=e.type==='boss'?'Command ship destroyed':'Enemy destroyed';}break;}}}
s.bullets=s.bullets.filter(b=>!spent.has(b)&&Math.abs(b.x)<425&&Math.abs(b.y)<425);s.enemies=s.enemies.filter(e=>e.hp>0);
const hitHostile=new Set();for(const b of s.hostile)if(swept(b,p,b.r+p.r)){if(s.invulnerable<=0)hurt(s);hitHostile.add(b);}s.hostile=s.hostile.filter(b=>!hitHostile.has(b)&&Math.abs(b.x)<425&&Math.abs(b.y)<425);
for(const e of s.enemies)if(swept(e,p,e.r+p.r))hurt(s);s.effects=s.effects.filter(e=>(e.life-=dt)>0);
if(s.status==='playing'&&s.enemies.length===0){s.status=s.level===2?'won':'cleared';s.message=s.level===2?'Command sector secured. You control the world through its data.':'Sector cleared. Inspect the final state, then continue to the next level.';}return s;}
return {planeV,planeE,starV,starE,bulletV,bulletE,levels,create,step,world,screen,matrices,mul,mv,swept,segmentDistance};});
