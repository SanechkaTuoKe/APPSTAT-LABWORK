(()=>{
const $=s=>document.querySelector(s),$$=s=>Array.from(document.querySelectorAll(s));
const drawer=$('#drawer'),mask=$('.mobile-mask'),menubtn=$('.menu-toggle');
function openMenu(open){
 if(!drawer)return;
 drawer.classList.toggle('open',open);
 drawer.setAttribute('aria-hidden', String(!open));
 mask.hidden=!open;
 menubtn?.setAttribute('aria-expanded',String(open));
 document.body.classList.toggle('menu-open',open);
 if(open) drawer.querySelector('.drawer-close')?.focus();
 else menubtn?.focus();
}
menubtn?.addEventListener('click',()=>openMenu(!drawer.classList.contains('open')));
$('.drawer-close')?.addEventListener('click',()=>openMenu(false));
mask?.addEventListener('click',()=>openMenu(false));
$$('.drawer a').forEach(a=>a.addEventListener('click',()=>openMenu(false)));
$$('.nav-expand').forEach(b=>b.addEventListener('click',()=>{
 const child=document.getElementById(b.getAttribute('aria-controls'));
 if(!child)return;
 child.hidden=!child.hidden;
 b.setAttribute('aria-expanded',String(!child.hidden));
}));
// Within-page navigation follows only the current page's real subsection headings.
const idx=$('#local-index'),mobileIdx=$('#local-index-mobile');
if(idx||mobileIdx){
 const headings=$$('.article-body .toc-heading');
 headings.forEach((h,i)=>{
  if(!h.id)h.id='section-'+i;
  for(const el of [idx,mobileIdx]){
   if(!el)continue;
   const a=document.createElement('a');a.textContent=h.textContent.trim();a.href='#'+h.id;for(const level of ['level-chapter','level-subsection','level-nested'])if(h.classList.contains(level))a.classList.add(level);
   el.append(a);
   a.addEventListener('click',()=>{const d=$('.section-index-mobile');if(d)d.open=false;});
  }
 });
 const links=$$('#local-index a,#local-index-mobile a');
 if('IntersectionObserver' in window){
  const io=new IntersectionObserver(entries=>{
   entries.forEach(e=>{if(e.isIntersecting)links.forEach(a=>a.classList.toggle('active',a.hash==='#'+e.target.id));});
  },{rootMargin:'-120px 0px -65% 0px'});
  headings.forEach(h=>io.observe(h));
 }
}
// Each tall plot is divided into selectable original rows; selection changes displayed chart and enlarged image.
$$('.chart-viewer').forEach(view=>{
 const tabs=Array.from(view.querySelectorAll('[role="tab"]'));
 const btn=view.querySelector('.chart-expand'),im=btn?.querySelector('img');
 tabs.forEach((tab,i)=>tab.addEventListener('click',()=>{
  tabs.forEach((other,j)=>{const on=i===j;other.setAttribute('aria-selected',String(on));other.tabIndex=on?0:-1;});
  btn.dataset.img=tab.dataset.image;
  im.src=tab.dataset.image;
  im.alt=tab.textContent;
 }));
});
const lightbox=$('.lightbox'),lbImg=lightbox?.querySelector('img'),lbViewport=lightbox?.querySelector('.lightbox-viewport');
let zoom=1,lastTrigger=null;
function updateZoom(){
 if(!lightbox||!lbImg||!lbViewport)return;
 const bw=lbViewport.clientWidth-25,bh=lbViewport.clientHeight-25;
 const nw=lbImg.naturalWidth||bw,nh=lbImg.naturalHeight||bh;
 const scale=Math.min(1,bw/nw,bh/nh);
 lbImg.style.width=Math.max(1,Math.round(nw*scale*zoom))+'px';
 lbImg.style.height='auto';
 lightbox.querySelector('.zoom-label').textContent=Math.round(zoom*100)+'%';
 lightbox.querySelector('.zoom-out').disabled=zoom<=1;
 lightbox.querySelector('.zoom-in').disabled=zoom>=3;
}
function showImage(btn){
 if(!lightbox)return;lastTrigger=btn;zoom=1;
 lbImg.src=btn.dataset.img;lbImg.alt=btn.querySelector('img')?.alt||'График исследования';
 lightbox.hidden=false;document.body.classList.add('modal-open');
 lbImg.onload=()=>{updateZoom();lbViewport.scrollTo(0,0)};
 requestAnimationFrame(updateZoom);
 lightbox.querySelector('.lightbox-close').focus();
}
function hideImage(){
 if(!lightbox||lightbox.hidden)return;
 lightbox.hidden=true;document.body.classList.remove('modal-open');
 if(lastTrigger)lastTrigger.focus();
}
$$('.chart-expand').forEach(btn=>btn.addEventListener('click',()=>showImage(btn)));
$('.lightbox-close')?.addEventListener('click',hideImage);
lightbox?.addEventListener('click',e=>{if(e.target===lightbox)hideImage();});
$('.zoom-in')?.addEventListener('click',()=>{zoom=Math.min(3,zoom+0.5);updateZoom()});
$('.zoom-out')?.addEventListener('click',()=>{zoom=Math.max(1,zoom-0.5);updateZoom()});
window.addEventListener('resize',()=>{if(lightbox&&!lightbox.hidden)updateZoom()});
document.addEventListener('keydown',e=>{
 if(e.key==='Escape'){
  if(lightbox&&!lightbox.hidden)hideImage(); else if(drawer?.classList.contains('open'))openMenu(false);
 }
});
const topbtn=$('.back-to-top');
if(topbtn){
 window.addEventListener('scroll',()=>topbtn.classList.toggle('visible',window.scrollY>650),{passive:true});
 topbtn.addEventListener('click',()=>window.scrollTo({top:0,behavior:'smooth'}));
}
// Rayleigh generator. F(r)=1-exp[-r²/(2σ²)]; r=σ sqrt[-2ln(1-u)].
const drawSection=$('#interactive-rayleigh');if(!drawSection)return;
const sigmaInput=$('#sigma'),seedInput=$('#seed'),sampleInput=$('#samples');let sample=[];let histHover=[];
const fmt=n=>Number(n).toFixed(6);
function randFromSeed(seed){let a=(seed>>>0);return function(){a=(a+0x6D2B79F5)>>>0;let t=a;t=Math.imul(t^(t>>>15),t|1);t^=t+Math.imul(t^(t>>>7),t|61);return ((t^(t>>>14))>>>0)/4294967296;}}
function chartSetup(canvas){const ctx=canvas.getContext('2d');const w=canvas.width,h=canvas.height;ctx.clearRect(0,0,w,h);ctx.fillStyle='#0b1730';ctx.fillRect(0,0,w,h);const L=64,T=25,R=18,B=48;ctx.font='13px Manrope, sans-serif';ctx.textAlign='left';return {ctx,w,h,L,T,R,B,cw:w-L-R,ch:h-T-B};}
function makeGrid(p,maxY,maxX){const {ctx,L,T,cw,ch}=p;ctx.save();ctx.strokeStyle='#284268';ctx.fillStyle='#98accd';ctx.lineWidth=1;for(let i=0;i<=4;i++){let y=T+ch*i/4;ctx.beginPath();ctx.moveTo(L,y);ctx.lineTo(L+cw,y);ctx.stroke();ctx.fillText((maxY*(1-i/4)).toFixed(maxY>10?1:2),9,y+4);}for(let i=0;i<=4;i++){let x=L+cw*i/4;ctx.fillText((maxX*i/4).toFixed(2),x-10,T+ch+23);}ctx.restore();}
function paint(){let n=Math.floor(+sampleInput.value),sigma=Math.min(1,Math.max(.0001,+sigmaInput.value||.05630)),seed=Math.floor(+seedInput.value||0);sampleInput.value=n;sigmaInput.value=sigma;$('#samples-n').textContent=n;let rng=randFromSeed(seed);let arr=Array.from({length:n},()=>sigma*Math.sqrt(-2*Math.log1p(-Math.min(.999999999999,rng()))));sample=arr;
let sorted=[...arr].sort((a,b)=>a-b),mean=arr.reduce((a,b)=>a+b,0)/n,variance=arr.reduce((a,b)=>a+(b-mean)**2,0)/(n-1);$('#mean-out').textContent=fmt(mean);$('#variance-out').textContent=fmt(variance);
// Median and the 95% quantile use linear interpolation, as in NumPy.
const quantile=(values,p)=>{const t=(values.length-1)*p,lo=Math.floor(t),hi=Math.ceil(t);return values[lo]+(values[hi]-values[lo])*(t-lo);};
$('#median-out').textContent=fmt(quantile(sorted,.5));$('#quantile-out').textContent=fmt(quantile(sorted,.95));
let oneRng=randFromSeed(seed),u=oneRng(),value=sigma*Math.sqrt(-2*Math.log1p(-u));$('#u-out').textContent=fmt(u);$('#value-out').textContent=fmt(value);$('#check-out').textContent=fmt(1-Math.exp(-value*value/(2*sigma*sigma)));
const maxX=Math.max(sorted[n-1]*1.02,sigma*4),binCount=42,binWidth=maxX/binCount,bins=Array(binCount).fill(0);for(let x of arr)bins[Math.min(binCount-1,Math.floor(x/binWidth))]++;const dens=bins.map(v=>v/n/binWidth),maxY=Math.max(...dens)*1.18;
const p=chartSetup($('#hist-chart'));makeGrid(p,maxY,maxX);histHover=[];p.ctx.fillStyle='#49d6ff';for(let i=0;i<binCount;i++){const bw=p.cw/binCount;const bh=(dens[i]/maxY)*p.ch;const x=p.L+bw*i,y=p.T+p.ch-bh;p.ctx.fillRect(x+.4,y,bw-1,bh);histHover.push({x,y,w:bw,h:bh,value:dens[i],bin:i*binWidth});}
const q=chartSetup($('#cdf-chart'));makeGrid(q,1,maxX);q.ctx.beginPath();q.ctx.lineWidth=3;q.ctx.strokeStyle='#8b5cf6';for(let i=0;i<=300;i++){let x=maxX*i/300,y=1-Math.exp(-(x*x)/(2*sigma*sigma));let px=q.L+i/300*q.cw,py=q.T+q.ch*(1-y);i===0?q.ctx.moveTo(px,py):q.ctx.lineTo(px,py);}q.ctx.stroke();let px=q.L+value/maxX*q.cw,py=q.T+q.ch*(1-u);q.ctx.strokeStyle='#ff4ecd';q.ctx.setLineDash([5,6]);q.ctx.beginPath();q.ctx.moveTo(px,q.T+q.ch);q.ctx.lineTo(px,py);q.ctx.lineTo(q.L,py);q.ctx.stroke();q.ctx.setLineDash([]);q.ctx.fillStyle='#ffcd78';q.ctx.beginPath();q.ctx.arc(px,py,6,0,2*Math.PI);q.ctx.fill();}
$('#generate').addEventListener('click',paint);sampleInput.addEventListener('input',()=>{$('#samples-n').textContent=sampleInput.value;paint();});$('#save-csv').addEventListener('click',()=>{const txt='r_def\n'+sample.map(x=>x.toFixed(10)).join('\n');const a=document.createElement('a');let url=URL.createObjectURL(new Blob([txt],{type:'text/csv;charset=utf-8'}));a.href=url;a.download='r_def.csv';a.click();setTimeout(()=>URL.revokeObjectURL(url),500);});
let hist=$('#hist-chart'),panel=hist.closest('.plot-panel'),tooltip=document.createElement('div');tooltip.className='plot-tooltip';panel.appendChild(tooltip);hist.addEventListener('mousemove',e=>{let r=hist.getBoundingClientRect(),x=(e.clientX-r.left)*hist.width/r.width;let bar=histHover.find(p=>x>=p.x&&x<p.x+p.w);if(!bar){tooltip.classList.remove('show');return;}tooltip.textContent=bar.bin.toFixed(4)+' : '+bar.value.toFixed(3);tooltip.style.left=Math.min(r.width-125,(e.clientX-r.left)+12)+'px';tooltip.style.top=Math.max(12,e.clientY-r.top-17)+'px';tooltip.classList.add('show');});hist.addEventListener('mouseleave',()=>tooltip.classList.remove('show'));paint();
})();