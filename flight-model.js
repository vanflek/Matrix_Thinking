(function(root,factory){const api=factory();if(typeof module==='object'&&module.exports)module.exports=api;else root.FlightModel=api;})(typeof globalThis!=='undefined'?globalThis:this,function(){
'use strict';
const vertices=[[0,0,2.6],[-.38,-.05,.7],[.38,-.05,.7],[-.32,0,-1.8],[.32,0,-1.8],[-2.6,-.1,-1],[2.6,-.1,-1],[-.7,0,-1.5],[.7,0,-1.5],[-.7,.7,-1.9],[.7,.7,-1.9],[0,.18,.4],[-.24,.35,-.3],[.24,.35,-.3],[-.22,-.15,-2],[.22,-.15,-2],[-.55,-.15,-2],[.55,-.15,-2]];
const edges=[[0,1],[0,2],[1,3],[2,4],[3,4],[1,5],[5,3],[2,6],[6,4],[3,7],[7,9],[9,3],[4,8],[8,10],[10,4],[0,11],[11,12],[11,13],[12,13],[12,3],[13,4],[3,14],[14,16],[16,3],[4,15],[15,17],[17,4]];
function create(){return {x:0,y:3,vx:0,vy:0,roll:0,pitch:0,distance:0,speed:9,time:0,next:0,passed:0,missed:0,status:'ready',gates:Array.from({length:8},(_,i)=>({x:[0,2.8,-2.5,1.8,-2.8,0,2.3,0][i],y:[3,4.2,2.2,4.3,3,2,4.2,3][i],z:42+i*26})),last:'Fly through eight openings. Three missed gates end the flight.'};}
const clamp=(x,a,b)=>Math.max(a,Math.min(b,x));
function gateFits(s,g){return Math.abs(s.x-g.x)<=1.7+1e-9&&Math.abs(s.y-g.y)<=1.2+1e-9;}
function advance(s,input,dt){if(s.status==='won'||s.status==='lost')return s;dt=clamp(dt,0,1/20);s.time+=dt;const tx=(input.right?1:0)-(input.left?1:0),ty=(input.up?1:0)-(input.down?1:0);s.vx+=(tx*4.8-s.vx)*Math.min(1,dt*9);s.vy+=(ty*3.8-s.vy)*Math.min(1,dt*9);s.x=clamp(s.x+s.vx*dt,-6,6);s.y=clamp(s.y+s.vy*dt,1,6);s.roll=-s.vx*.12;s.pitch=s.vy*.06;const old=s.distance;s.distance+=s.speed*dt;const g=s.gates[s.next];if(g&&old<g.z-4&&s.distance>=g.z-4){if(gateFits(s,g)){s.passed++;s.last='Gate '+(s.next+1)+' cleared. Position was inside the opening.';}else{s.missed++;s.last='Gate '+(s.next+1)+' missed. Align the blue aircraft marker with the yellow opening.';}s.next++;if(s.missed>=3){s.status='lost';s.last='Flight ended: three missed gates. Restart and try smaller movements.';}else if(s.next===s.gates.length){s.status='won';s.last='Course complete! '+s.passed+' of eight gates cleared.';}}return s;}
function transform(s){const c=Math.cos(s.roll),q=Math.sin(s.roll),p=Math.cos(s.pitch),r=Math.sin(s.pitch);return [[c,-q*p,q*r,s.x],[q,c*p,-c*r,s.y],[0,r,p,4],[0,0,0,1]];}
function multiply(m,v){return m.map(row=>row.reduce((sum,a,i)=>sum+a*v[i],0));}
function camera(v){return [v[0],v[1]-4,v[2]+14];}
function project(v,w,h,fov=65){if(v[2]<.5)return null;const f=w/2/Math.tan(fov*Math.PI/360);return [w/2+f*v[0]/v[2],h*.43-f*v[1]/v[2]];}
function clip(a,b,near=.5){if(a[2]<near&&b[2]<near)return null;if(a[2]<near||b[2]<near){const t=(near-a[2])/(b[2]-a[2]);const p=a.map((v,i)=>v+t*(b[i]-v));p[2]=near;if(a[2]<near)a=p;else b=p;}return [a,b];}
return {vertices,edges,create,advance,gateFits,transform,multiply,camera,project,clip};
});

