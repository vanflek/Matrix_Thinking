(function(root){
const features=['Glasses','Hat','Curly hair','Dark hair','Smile'];
const names=['Ada','Ben','Cleo','Dev','Eli','Faye','Gus','Hope','Ira','Jade','Kai','Luz','Milo','Nia','Otis','Pia','Quinn','Rae','Sol','Tess','Uma','Val','Wren','Zoe','Arlo','Bea','Cory','Dana','Emery','Finn','Gray','Hazel'];
const people=names.map((name,i)=>({name,bits:Array.from({length:5},(_,j)=>(i>>j)&1)}));
// Mix the six columns while keeping every character distinct.
people.forEach((p,i)=>p.bits=[i&1,(i>>1)&1,(i>>2)&1,(i>>3)&1,(i>>4)&1]);
function create(secret=Math.floor(Math.random()*32)){return {secret,mask:people.map(()=>1),history:[],phase:'playing',selected:null};}
function ask(s,j){if(s.phase!=='playing'||s.history.some(h=>h.j===j))return false;let answer=people[s.secret].bits[j];let before=s.mask.slice(),match=people.map(p=>+(p.bits[j]===answer));s.mask=s.mask.map((v,i)=>v&match[i]);s.selected=j;s.history.push({j,answer,before,match,after:s.mask.slice()});return true;}
function guess(s,i){if(s.phase!=='playing')return false;s.phase=i===s.secret?'won':'lost';return true;}
const api={features,people,create,ask,guess};if(typeof module!=='undefined')module.exports=api;else root.FaceLab=api;
})(typeof globalThis!=='undefined'?globalThis:this);