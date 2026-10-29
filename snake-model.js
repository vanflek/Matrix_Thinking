/* Same board data drives both representations. Coordinates are [row, column]. */
(function(root){
class SnakeModel {
 constructor(size=10,random=Math.random){this.size=size;this.random=random;this.reset();}
 reset(){this.body=[[5,4],[5,3],[5,2]];this.direction=[0,1];this.queued=null;this.apple=[5,7];this.state='ready';this.score=0;this.steps=0;this.last=null;}
 turn(d){const vectors={up:[-1,0],down:[1,0],left:[0,-1],right:[0,1]};const v=vectors[d];if(!v||this.queued||['lost','won'].includes(this.state))return false;if(v[0]===-this.direction[0]&&v[1]===-this.direction[1])return false;this.queued=v;return true;}
 spawnApple(){const free=[];for(let r=0;r<this.size;r++)for(let c=0;c<this.size;c++)if(!this.body.some(p=>p[0]===r&&p[1]===c))free.push([r,c]);this.apple=free.length?free[Math.min(free.length-1,Math.floor(this.random()*free.length))]:null;}
 step(){if(['lost','won'].includes(this.state))return null;
 const previous=this.body[0].slice(),tail=this.body.at(-1).slice();
 if(this.queued)this.direction=this.queued;this.queued=null;
 const raw=previous.map((n,i)=>n+this.direction[i]),head=raw.map(n=>(n+this.size)%this.size);
 const wrapped=raw.some((n,i)=>n!==head[i]),ate=this.apple&&head.every((n,i)=>n===this.apple[i]);
 const occupied=ate?this.body:this.body.slice(0,-1);
 if(occupied.some(p=>p.every((n,i)=>n===head[i]))){this.state='lost';this.last={collision:true,head};return this.last;}
 this.body.unshift(head);if(!ate)this.body.pop();else{this.score++;this.spawnApple();}
 this.steps++;this.state=this.apple?'active':'won';
 this.last={head,previous,tail,ate:!!ate,wrapped,delta:this.direction.slice()};return this.last;
 }
 matrix(){const a=Array.from({length:this.size},()=>Array(this.size).fill(0));this.body.forEach(([r,c],i)=>a[r][c]=i?1:3);if(this.apple)a[this.apple[0]][this.apple[1]]=2;return a;}
}
if(typeof module!=='undefined'&&module.exports)module.exports=SnakeModel;else root.SnakeModel=SnakeModel;
})(typeof globalThis!=='undefined'?globalThis:this);

