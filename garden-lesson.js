/* Readable NumPy lesson data; the browser illustrates, Python executes. */
(function(root){
'use strict';
const titles=['Create the whole candidate world','Describe every candidate before filtering','Mask the world by fence budget','Mask the same world by area','Intersect the masks','Collect the complete solution set'];
function formatArray(rows){
 if(!rows.length)return '[]';
 const size=String(Math.max(...rows.flat().map(v=>Math.abs(v)))).length;
 return '['+rows.map(r=>'['+r.map(v=>String(v).padStart(size)).join(' ')+']').join('\n ') + ']';
}
function steps(world){
 const {fence,minimum,n,cells,solutions}=world;
 const matrix=key=>Array.from({length:n},(_,i)=>cells.slice(i*n,(i+1)*n).map(c=>Number(c[key])));
 const named=(label,key)=>label+` · shape (${n}, ${n})\n`+formatArray(matrix(key));
 const sizes=Array.from({length:n},(_,i)=>i+1);
 const rows=solutions.map(c=>[c.width,c.length,c.perimeter,c.area]);
 return [
 {title:titles[0],stage:0,explanation:`First create all ${n} × ${n} = ${cells.length} pairs of side lengths from 1 to ${n} metres, including unsuitable gardens. These are candidates, not yet solutions: no mask has been applied. meshgrid builds this whole finite world. With indexing="ij", rows choose width and columns choose length; corresponding cells in the two arrays describe the same garden.`,code:`import numpy as np\n\nfence = ${fence}\nminimum = ${minimum}\nsizes = np.arange(1, fence // 2 + 1)\nwidth, length = np.meshgrid(\n    sizes, sizes, indexing="ij"\n)\n\nprint(width)\nprint(length)`,output:'sizes\n['+sizes.join(' ')+']\n\n'+named('width','width')+'\n\n'+named('length','length')},
 {title:titles[1],stage:0,explanation:'Arithmetic acts on corresponding cells of the two dimension arrays. Every candidate now has a perimeter and an area. We have calculated the whole world; no candidates have been removed yet.',code:'perimeter = 2 * (width + length)\narea = width * length\n\nprint(perimeter)\nprint(area)',output:named('perimeter · metres','perimeter')+'\n\n'+named('area · square metres','area')},
 {title:titles[2],stage:1,explanation:`Compare every perimeter with ${fence}. The Boolean result keeps the same ${n} × ${n} shape. ${world.fenceCount} cells are True. This condition allows unused fence and does not check the minimum area.`,code:'fence_ok = perimeter <= fence\n\nprint(fence_ok.astype(int))',output:named('fence_ok · 1 = True, 0 = False','fenceOk')+`\n\n${world.fenceCount} gardens pass the fence condition.`},
 {title:titles[3],stage:2,explanation:`Independently compare every area with ${minimum}. ${world.areaCount} cells are True. A garden can pass this test while needing too much fence, so this is not the final answer.`,code:'area_ok = area >= minimum\n\nprint(area_ok.astype(int))',output:named('area_ok · 1 = True, 0 = False','areaOk')+`\n\n${world.areaCount} gardens pass the area condition.`},
 {title:titles[4],stage:3,explanation:`The & operator combines corresponding Boolean cells. A cell is True only where both conditions hold. ${solutions.length} of the ${cells.length} candidates survive. We now know where all the solutions are.`,code:'mask = fence_ok & area_ok\n\nprint(mask.astype(int))\nprint(np.count_nonzero(mask))',output:named('mask · 1 = both conditions are True','valid')+`\n\nnp.count_nonzero(mask)\n${solutions.length}`},
 {title:titles[5],stage:4,explanation:`Apply the same Boolean mask to all four arrays. Each selection becomes a one-dimensional array, read row by row in the same order. column_stack places these four arrays beside each other: one row for each of the ${solutions.length} solutions. Rotated dimensions remain separate.`,code:'solutions = np.column_stack((\n    width[mask], length[mask],\n    perimeter[mask], area[mask],\n))\n\nprint(solutions)\nprint(solutions.shape)',output:`solutions · shape (${solutions.length}, 4)\nColumns: width, length, perimeter, area\n`+formatArray(rows)+'\n\nThe same mask selects four matching columns:\n'+['width','length','perimeter','area'].map(key=>key+'[mask] = ['+solutions.map(c=>c[key]).join(' ')+']').join('\n')+(solutions.length?'':'\n\nNo candidates pass both conditions. The result has zero rows and four columns.')}
 ];
}
const api={steps,formatArray};
if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.GardenLesson=api;
})(typeof globalThis!=='undefined'?globalThis:this);
