const canvas = document.getElementById('board');// "board" is the canvas' id
const ctx = canvas.getContext('2d');/* object for drawing */

const SIZE = 720;
const GRID = 15;
const CELL = SIZE / GRID;
const TOKEN_R = CELL * 0.32;

const PLAYERS = [
  {id:0,name:'RED', color:'#ef4444', avatar:'', startIndex:0},
  {id:1,name:'BLACK', color:'#000000', avatar:'', startIndex:13},
  {id:2,name:'YELLOW', color:'#ffff00', avatar:'', startIndex:26},
  {id:3,name:'BROWN', color:'#8b4513', avatar:'', startIndex:39},
];


// Basic main path for 52 steps (same arrangement as earlier)
const MAIN_PATH = [
  [6,0],[7,0],[8,0],[8,1],[8,2],[8,3],[8,4],[8,5],[9,6],[10,6],[11,6],[12,6],[13,6],[14,6],
  [14,7],[14,8],[13,8],[12,8],[11,8],[10,8],[9,8],[8,9],[8,10],[8,11],[8,12],[8,13],[8,14],
  [7,14],[6,14],[6,13],[6,12],[6,11],[6,10],[6,9],[5,8],[4,8],[3,8],[2,8],[1,8],[0,8],
  [0,7],[0,6],[1,6],[2,6],[3,6],[4,6],[5,6],[6,5],[6,4],[6,3],[6,2],[6,1]
];


const HOME_PATH = {
  0:[[7,1],[7,2],[7,3],[7,4],[7,5]],
  1:[[13,7],[12,7],[11,7],[10,7],[9,7]],
  2:[[7,13],[7,12],[7,11],[7,10],[7,9]],
  3:[[1,7],[2,7],[3,7],[4,7],[5,7]]
};


const BASE_SLOTS = {
  0:[[1.5,1.5],[3.5,1.5],[1.5,3.5],[3.5,3.5]],
  1:[[10.5,1.5],[12.5,1.5],[10.5,3.5],[12.5,3.5]],
  2:[[10.5,10.5],[12.5,10.5],[10.5,12.5],[12.5,12.5]],
  3:[[1.5,10.5],[3.5,10.5],[1.5,12.5],[3.5,12.5]]
}


// indexes of "MAIN_PATH" list
const ENTRY_INDEX = {0:42,1:3,2:16,3:29};
const SAFE = [50,11,24,37];



function cellCenter(x,y)
{
  return [x*CELL + CELL/2, y*CELL + CELL/2];
}


function newTokens(){
  return [
    {pos:'base',steps:0},
    {pos:'base',steps:0},
    {pos:'base',steps:0},
    {pos:'base',steps:0}
  ];
}



//draw the lines of the board
function drawGrid(){
  ctx.strokeStyle='#e6edf3';
  ctx.lineWidth=1;

  for(let i=0;i<=GRID;i++){
      ctx.beginPath();
      ctx.moveTo(i*CELL,0);
      ctx.lineTo(i*CELL,SIZE);
      ctx.stroke();
      ctx.beginPath();
      ctx.moveTo(0,i*CELL);
      ctx.lineTo(SIZE,i*CELL);
      ctx.stroke();
  }
}


//draw the squared houses of the player's 4 pieces
function drawHomeQuads(){
  const quads = [
    {x:0,y:0,w:6,h:6,color:'rgba(255,0,0)'},
    {x:9,y:0,w:6,h:6,color:'rgba(0,0,0)'},
    {x:9,y:9,w:6,h:6,color:'rgba(255,255,0)'},
    {x:0,y:9,w:6,h:6,color:'rgba(139,69,19)'}
  ];
  for(const q of quads){
    ctx.fillStyle=q.color;
    ctx.fillRect(q.x*CELL, q.y*CELL, q.w*CELL, q.h*CELL);
  }
}


function drawMainPath(){
  // draw path squares for visibility
  for(let i=0;i<MAIN_PATH.length;i++){
    console.log(i);
    const [x,y]=MAIN_PATH[i];
    console.log([x,y]);
    const [cx,cy]=cellCenter(x,y);
    ctx.fillStyle='#ffffff';
    ctx.strokeStyle='#cbd5e1';
    ctx.lineWidth=1;
    ctx.beginPath();
    ctx.rect(cx-CELL*0.4, cy-CELL*0.4, CELL*0.8, CELL*0.8);
    ctx.fill();
    ctx.stroke();

    // small index mark

    ctx.fillStyle='#94a3b8';
    ctx.font='10px sans-serif';
    ctx.textAlign='center';
    ctx.textBaseline='middle';
    //ctx.fillText("X: " + x + "" + "Y:" + y + "(" + i + ")", cx, cy);
  }
}



//Safe boxes for the player()
function drawSafeTiles(){
  SAFE.forEach(idx=>{
    const [x,y]=MAIN_PATH[idx];
    ctx.fillStyle='#10b981';
    ctx.globalAlpha=0.12;
    const [cx,cy]=cellCenter(x,y);
    ctx.beginPath();
    ctx.arc(cx,cy,CELL*0.36,0,Math.PI*2);
    ctx.fill();
    ctx.globalAlpha=1;

    ctx.font='10px sans-serif';
    ctx.textAlign='center';
    ctx.textBaseline='middle';
    ctx.fillText("Safe", cx, cy);
  });
}


function drawEntryHighlights(){
  for(const p of PLAYERS){
    const e = ENTRY_INDEX[p.id];
    const [x,y]=MAIN_PATH[e];
    ctx.fillStyle = p.color;
    ctx.globalAlpha=0.12;
    const [cx,cy]=cellCenter(x,y);
    ctx.beginPath();
    ctx.arc(cx,cy,CELL*0.36,0,Math.PI*2);
    ctx.fill();
    ctx.globalAlpha=1;

    ctx.font='10px sans-serif';
    ctx.textAlign='center';
    ctx.textBaseline='middle';
    ctx.fillText("Start", cx, cy);

}}


function drawHomePath(){
  for(const p of PLAYERS){
    const h = HOME_PATH[p.id];
    for(const home_path of h){
      const [x,y]=home_path;
      ctx.fillStyle = p.color;
      ctx.globalAlpha=0.12;
      const [cx,cy]=cellCenter(x,y);
      ctx.beginPath();
      ctx.arc(cx,cy,CELL*0.36,0,Math.PI*2);
      ctx.fill();
      ctx.globalAlpha=1;

      ctx.font='10px sans-serif';
      ctx.textAlign='center';
      ctx.textBaseline='middle';
      ctx.fillText("Home", cx, cy);
    }
}}



function tokenScreenPos(p, idx){
  const t = p.tokens[idx];
  if(t.pos==='base'){
   const slot=BASE_SLOTS[p.id][idx];
   const [cx,cy]=cellCenter(slot[0],slot[1]);
   return {x:cx,y:cy};
  }

  if(t.pos==='home'){
    const [cx,cy]=cellCenter(7,7);
    return {x:cx + (idx-1.5)*CELL*0.12, y:cy + (p.id-1.5)*CELL*0.12};
  }

  if(t.pos.type==='main'){
    const [mx,my]=MAIN_PATH[t.pos.index];
    const [cx,cy]=cellCenter(mx,my);
    return {x:cx,y:cy};
  }

  if(t.pos.type==='home'){
    const path = HOME_PATH[p.id];
    const stepIdx = t.steps-1;
    const [hx,hy]=path[stepIdx];
    const [cx,cy]=cellCenter(hx,hy);
    return {x:cx,y:cy};
  }

  return{x:SIZE/2,y:SIZE/2};
}



function drawTokens(){
  for(const p of state.players){
    for(let i=0;i<4;i++){
      const pos = tokenScreenPos(p,i);
      ctx.beginPath(); 
      ctx.arc(pos.x,pos.y,TOKEN_R,0,Math.PI*2);
      ctx.fillStyle=p.color;
      ctx.fill();
      ctx.lineWidth=3;
      ctx.strokeStyle='#fff';
      ctx.stroke();
      ctx.fillStyle='rgba(255,255,255,0.95)';
      ctx.beginPath();
      ctx.arc(pos.x,pos.y,TOKEN_R*0.5,0,Math.PI*2);
      ctx.fill();
      ctx.fillStyle='#0f172a';
      ctx.font=`${Math.floor(TOKEN_R*0.7)}px sans-serif`;
      ctx.textAlign='center';
      ctx.textBaseline='middle';
      ctx.fillText(String(i+1), pos.x, pos.y);
    }
  }
}




function draw(){
  ctx.clearRect(0,0,SIZE,SIZE);
  drawGrid();
  drawHomeQuads();
  drawMainPath();
  drawSafeTiles();
  drawEntryHighlights();
  drawHomePath();
  drawTokens();
}


let state = null;
function newGame(){
  state = {
    players: PLAYERS.map(p => ({...p, tokens:newTokens(), finished:0})),
    current:0,
    dice:null,
    rolled:false,
    winner:null
  };
  draw();
}

newGame();