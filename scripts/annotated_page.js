(function(){
  var root=document.documentElement, body=document.body, K=body.getAttribute('data-key')||'annotated';
  function store(k,v){try{localStorage.setItem(k,v)}catch(e){}}
  function read(k){try{return localStorage.getItem(k)}catch(e){return null}}
  // theme toggle (shared key with the rest of the site)
  var tbtn=document.getElementById('t-theme');
  function paintTheme(){tbtn.textContent=root.getAttribute('data-theme')==='dark'?'Light':'Dark'}
  tbtn.addEventListener('click',function(){var t=root.getAttribute('data-theme')==='dark'?'light':'dark';root.setAttribute('data-theme',t);store('shoug-theme',t);paintTheme()});
  window.addEventListener('storage',function(ev){if(ev.key==='shoug-theme'&&ev.newValue){root.setAttribute('data-theme',ev.newValue);paintTheme()}});
  paintTheme();
  // global toggles
  function setPressed(b,on){b.setAttribute('aria-pressed',on?'true':'false')}
  var bn=document.getElementById('t-notes'), bh=document.getElementById('t-hl'), ba=document.getElementById('t-ans');
  function setCardNotes(card,show){var b=card.querySelector('.note-toggle');if(!b)return;card.classList.toggle('notes-hidden',!show);b.textContent=show?'Hide notes':'Show notes';b.setAttribute('aria-expanded',show?'true':'false')}
  bn.addEventListener('click',function(){var on=bn.getAttribute('aria-pressed')!=='true';setPressed(bn,on);
    document.querySelectorAll('.card[data-slide]').forEach(function(c){setCardNotes(c,on)});store(K+'-notes',on?'1':'0')});
  bh.addEventListener('click',function(){var on=bh.getAttribute('aria-pressed')!=='true';setPressed(bh,on);body.classList.toggle('no-hl',!on);store(K+'-hl',on?'1':'0')});
  ba.addEventListener('click',function(){var on=ba.getAttribute('aria-pressed')!=='true';setPressed(ba,on);
    document.querySelectorAll('.exam details').forEach(function(d){d.open=on})});
  document.querySelectorAll('.note-toggle').forEach(function(b){b.addEventListener('click',function(){var c=b.closest('.card');setCardNotes(c,c.classList.contains('notes-hidden'))})});
  // overview show/hide (control lives inside the overview)
  var ob=document.querySelector('.ov-toggle'), ovb=document.getElementById('ov-body');
  function setOv(show){ovb.hidden=!show;ob.textContent=show?'Hide overview':'Show overview';ob.setAttribute('aria-expanded',show?'true':'false');store(K+'-ov',show?'1':'0')}
  ob.addEventListener('click',function(){setOv(ovb.hidden)});
  if(read(K+'-ov')==='0')setOv(false);
  if(read(K+'-notes')==='0')bn.click();
  if(read(K+'-hl')==='0')bh.click();
  // highlight <-> note linking
  function link(card,n,on){card.querySelectorAll('[data-n="'+n+'"]').forEach(function(el){el.classList.toggle('on',on)})}
  document.querySelectorAll('.card[data-slide]').forEach(function(card){
    card.querySelectorAll('.notes li[data-n]').forEach(function(li){var n=li.getAttribute('data-n');
      li.addEventListener('mouseenter',function(){link(card,n,true)});li.addEventListener('mouseleave',function(){link(card,n,false)})});
    card.querySelectorAll('rect.hl:not(.free)').forEach(function(r){var n=r.getAttribute('data-n');
      r.addEventListener('mouseenter',function(){link(card,n,true)});r.addEventListener('mouseleave',function(){link(card,n,false)});
      r.addEventListener('click',function(){if(card.classList.contains('notes-hidden'))setCardNotes(card,true);var li=card.querySelector('.notes li[data-n="'+n+'"]');
        if(li){li.scrollIntoView({behavior:'smooth',block:'center'});li.classList.add('flash');setTimeout(function(){li.classList.remove('flash')},1600)}})});
  });
  // scroll / flip view: flip shows one card (overview or slide) at a time
  var cards=[].slice.call(document.querySelectorAll('main>.card')), bar=document.querySelector('.flipbar'),
      ms=document.getElementById('m-scroll'), mf=document.getElementById('m-flip'), jump=document.getElementById('f-jump'),
      fp=document.getElementById('f-prev'), fn=document.getElementById('f-next'), cur=0;
  cards.forEach(function(c,i){var o=document.createElement('option');var h=c.querySelector('h3');
    o.value=i;o.textContent=(c.dataset.slide?c.dataset.slide+' · ':'')+(c.dataset.slide?(h?h.textContent:''):'Overview');jump.appendChild(o)});
  function indexOf(id){for(var i=0;i<cards.length;i++){if(cards[i].id===id)return i}return -1}
  function show(i,noScroll){cur=Math.max(0,Math.min(cards.length-1,i));
    cards.forEach(function(c,k){c.classList.toggle('current',k===cur)});
    jump.value=cur;fp.disabled=cur===0;fn.disabled=cur===cards.length-1;
    try{history.replaceState(null,'','#'+cards[cur].id)}catch(e){}
    if(!noScroll)window.scrollTo(0,0)}
  function setMode(flip){body.classList.toggle('flip',flip);bar.hidden=!flip;setPressed(mf,flip);setPressed(ms,!flip);store(K+'-mode',flip?'flip':'scroll');
    if(flip){var top=0;for(var i=0;i<cards.length;i++){if(cards[i].getBoundingClientRect().bottom>90){top=i;break}}show(top)}
    else{cards[cur].scrollIntoView()}}
  ms.addEventListener('click',function(){if(body.classList.contains('flip'))setMode(false)});
  mf.addEventListener('click',function(){if(!body.classList.contains('flip'))setMode(true)});
  fp.addEventListener('click',function(){show(cur-1)});fn.addEventListener('click',function(){show(cur+1)});
  jump.addEventListener('change',function(){show(+jump.value)});
  document.addEventListener('keydown',function(ev){if(!body.classList.contains('flip')||ev.altKey||ev.ctrlKey||ev.metaKey)return;
    var t=ev.target.tagName;if(t==='INPUT'||t==='SELECT'||t==='TEXTAREA')return;
    if(ev.key==='ArrowRight'||ev.key==='PageDown'){show(cur+1);ev.preventDefault()}
    else if(ev.key==='ArrowLeft'||ev.key==='PageUp'){show(cur-1);ev.preventDefault()}});
  var sx=null,sy=null;
  document.addEventListener('touchstart',function(ev){if(ev.touches.length===1){sx=ev.touches[0].clientX;sy=ev.touches[0].clientY}},{passive:true});
  document.addEventListener('touchend',function(ev){if(sx===null||!body.classList.contains('flip'))return;
    var dx=ev.changedTouches[0].clientX-sx,dy=ev.changedTouches[0].clientY-sy;sx=null;
    if(Math.abs(dx)>70&&Math.abs(dx)>2*Math.abs(dy))show(cur+(dx<0?1:-1))},{passive:true});
  // in-page links (contents list, "seen again") go to the right card in flip mode
  document.addEventListener('click',function(ev){var a=ev.target.closest&&ev.target.closest('a[href^="#"]');
    if(!a||!body.classList.contains('flip'))return;var i=indexOf(a.getAttribute('href').slice(1));if(i>=0){ev.preventDefault();show(i)}});
  var start=indexOf(location.hash.slice(1));
  if(read(K+'-mode')==='flip'){body.classList.add('flip');bar.hidden=false;setPressed(mf,true);setPressed(ms,false);show(start>=0?start:0)}
})();
