(function(root){
const shapes=[[[1,1,1,1]],[[2,2],[2,2]],[[0,3,0],[3,3,3]],[[4,0],[4,0],[4,4]],[[0,5],[0,5],[5,5]],[[0,6,6],[6,6,0]],[[7,7,0],[0,7,7]]];
class TetrisModel{
constructor(random=Math.random){this.random=random;this.reset();}
reset(){this.field=Array.from({length:20},()=>Array(10).fill(0));this.lines=0;this.score=0;this.over=false;this.bag=[];this.before=null;this.after=null;this.spawn();this.message='Move, rotate, or take one downward step. The first piece is a T.';}
spawn(){if(!this.bag.length){const rest=[0,1,3,4,5,6];for(let i=rest.length-1;i>0;i--){const j=Math.floor(this.random()*(i+1));[rest[i],rest[j]]=[rest[j],rest[i]];}this.bag=[2,...rest];}this.shape=shapes[this.bag.shift()].map(r=>r.slice());this.row=0;this.col=Math.floor((10-this.shape[0].length)/2);if(!this.fits()){this.over=true;this.message='Game over: the next piece cannot enter the field. Restart to try again.';}}
fits(shape=this.shape,row=this.row,col=this.col){return shape.every((line,r)=>line.every((v,c)=>!v||(row+r>=0&&row+r<20&&col+c>=0&&col+c<10&&!this.field[row+r][col+c])));}
move(dc){if(this.over)return false;if(!this.fits(this.shape,this.row,this.col+dc)){this.message='Move rejected: a wall or settled cell blocks the piece.';return false;}this.col+=dc;this.message='Column changes by '+dc+'. The piece matrix stays the same.';return true;}
rotate(){if(this.over)return false;const next=this.shape[0].map((_,c)=>this.shape.map(row=>row[this.shape[0].length-1-c]));this.before=this.shape.map(r=>r.slice());this.after=next.map(r=>r.slice());if(!this.fits(next)){this.message='Rotation rejected: the rotated matrix overlaps a wall or settled cell. Move away and try again.';return false;}this.shape=next;this.message='Counterclockwise rotation, like np.rot90(matrix, 1) in the book. Cell IDs and their colors are preserved.';return true;}
step(){if(this.over)return;if(this.fits(this.shape,this.row+1)){this.row++;this.message='One downward step: row = row + 1. The piece matrix stays the same.';return;}this.lock();}
lock(){this.shape.forEach((line,r)=>line.forEach((v,c)=>{if(v)this.field[this.row+r][this.col+c]=v;}));const kept=this.field.filter(row=>!row.every(Boolean)),cleared=20-kept.length;this.field=[...Array.from({length:cleared},()=>Array(10).fill(0)),...kept];this.lines+=cleared;this.score+=[0,100,300,500,800][cleared];this.spawn();if(!this.over)this.message=cleared?'Locked the piece. Removed '+cleared+' full row(s); rows above shifted down. Added empty rows at the top.':'The next step was blocked. The piece moved into the fixed layer, keeping its IDs and colors. A new piece entered the active layer.';}
drop(){if(this.over)return;while(this.fits(this.shape,this.row+1))this.row++;this.lock();}
demo(){this.reset();this.field[19]=Array(10).fill(1);for(let c=3;c<7;c++)this.field[19][c]=0;this.shape=[[1,1,1,1]];this.row=18;this.col=3;this.message='Predict: the I piece fits the four-cell gap. Step once to fill it; step again to lock it and clear the row.';}
activeMatrix(){const a=Array.from({length:20},()=>Array(10).fill(0));if(!this.over)this.shape.forEach((line,r)=>line.forEach((v,c)=>{if(v)a[this.row+r][this.col+c]=v;}));return a;}
matrix(){const a=this.field.map(r=>r.slice());if(!this.over)this.shape.forEach((line,r)=>line.forEach((v,c)=>{if(v)a[this.row+r][this.col+c]=v;}));return a;}
}
if(typeof module!=='undefined'&&module.exports)module.exports=TetrisModel;else root.TetrisModel=TetrisModel;
})(typeof globalThis!=='undefined'?globalThis:this);
