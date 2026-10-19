(function(){
  // rule: every new page opens at the top, never at a remembered scroll spot
  try{ if('scrollRestoration' in history) history.scrollRestoration='manual'; }catch(e){}
  function top(){ if(!location.hash){ var h=document.documentElement,b=h.style.scrollBehavior; h.style.scrollBehavior='auto'; window.scrollTo(0,0); h.style.scrollBehavior=b; } }
  top(); window.addEventListener('pageshow',top);
})();
(function(){
  var $=function(id){return document.getElementById(id)};

  // live open status in gym time (America/New_York), 4AM to 12AM daily
  try{
    var h=+new Intl.DateTimeFormat('en-US',{hour:'numeric',hourCycle:'h23',timeZone:'America/New_York'}).format(new Date());
    var day=new Intl.DateTimeFormat('en-US',{weekday:'long',timeZone:'America/New_York'}).format(new Date());
    var open=h>=4;
    var st=$('status'),tx=$('status-text');
    if(st){ if(open){st.classList.add('open');tx.textContent='Open now in Vineland · until midnight';} else tx.textContent='Opens at 4AM · Vineland, NJ'; }
    var ce=$('closer-eyebrow'); if(ce&&!open) ce.textContent='Doors open at 4AM';
    var row=document.querySelector('.hours tr[data-day="'+day+'"]'); if(row) row.classList.add('today');
  }catch(e){}

  // nav glass on scroll
  var nav=$('nav');
  function onScroll(){nav&&nav.classList.toggle('scrolled',window.scrollY>20)}
  window.addEventListener('scroll',onScroll,{passive:true});onScroll();

  // mobile menu
  var mb=$('menu-btn'),links=$('links');
  if(mb){mb.addEventListener('click',function(){var o=links.classList.toggle('show');mb.setAttribute('aria-expanded',o)});}

  // photo strips from the real upload library
  var g=['DSC08375','DSC08540','DSC06057','DSC08343','Copy-of-DSC00769','DSC08545','DSC06010','DSC08335','DSC08331-1','DSC08347','DSC08673','DSC08620','DSC05819-2','DSC05866','DSC05884-1','DSC05973'];
  function fill(el,list){
    if(!el)return;
    list.concat(list).forEach(function(n,i){
      var d=document.createElement('div');d.className='ph';
      var im=new Image();im.loading='lazy';im.alt=i<list.length?'Training at Animal Paradise Gyms, Vineland NJ':'';
      im.src='https://animalparadisegyms.com/wp-content/uploads/2026/10/'+n+'-720x520.jpg';
      im.onerror=function(){im.remove()};d.appendChild(im);el.appendChild(d);
    });
  }


  // count-up once numbers scroll into view (final values already in the HTML)
  if('IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion:reduce)').matches){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){
      if(!e.isIntersecting)return;io.unobserve(e.target);
      var el=e.target,to=+el.dataset.count,t0=null;
      function step(t){if(!t0)t0=t;var p=Math.min((t-t0)/1100,1);el.textContent=Math.round(to*(1-Math.pow(1-p,3)));if(p<1)requestAnimationFrame(step)}
      requestAnimationFrame(step);
    })},{threshold:.6});
    [].forEach.call(document.querySelectorAll('[data-count]'),function(el){io.observe(el)});
  }

  // membership finder
  var f=$('finder');
  if(f){
    var P={
      silver:{n:'Silver',p:'$70',w:'No contract, cancel when you like. Full gym, sauna, posing room and 4 studio classes.',id:'13656dbde8fd436bb689e32c16b63056'},
      gold:{n:'Gold',p:'$60',w:'Our best value. Full gym, sauna, studio classes and 5% off at the cafe and supps store.',id:'9ebe7a5348c7495fae488912433d9c65'},
      premium:{n:'Premium',p:'$70',w:'Everything in Gold plus the Hibernation Station recovery room, towel service and 10% off.',id:'81293d61d2af47cebc834aec823432e4'},
      platinum:{n:'Platinum',p:'$70',w:'Everything in Gold plus the women-only Lioness Den, towel service and 10% off.',id:'563c3fc6a6954a9ca216624c35a4378a'},
      diamond:{n:'Diamond',p:'$80',w:'All access: Lioness Den, Hibernation Station, towel service, 2hr daycare and 10% off.',id:'8c6f6ea07fe0440cb83468ca56c58cdb'}
    };
    var pick=function(){
      var den=f.den.value,term=f.term.value,rec=f.rec.value,k;
      if(term==='m')k='silver';else if(den==='y')k=rec==='y'?'diamond':'platinum';else k=rec==='y'?'premium':'gold';
      var t=P[k];
      $('f-tier').textContent=t.n;
      $('f-price').innerHTML=t.p+' <small>a month'+(k==='silver'?', no contract':', 12 months')+'</small>';
      $('f-why').textContent=(term==='m'&&(den==='y'||rec==='y')?'The Lioness Den and recovery room come with 12-month plans. Month to month, Silver is your plan. ':'')+t.w;
      var j=$('f-join');j.textContent='Join '+t.n+' online';
      j.href='https://onlinejoin.abcfitness.com/signup/plan?club=31857&planId='+t.id;
      [].forEach.call(document.querySelectorAll('.plan'),function(el){el.classList.toggle('match',el.dataset.tier===k)});
    };
    f.addEventListener('change',pick);f.addEventListener('submit',function(e){e.preventDefault()});pick();
  }

  // lead forms: post to the GHL inbound webhook, fire the Meta Lead event, then go to /thank-you/
  var HOOK=(window.APG_WEBHOOK||'');
  [].forEach.call(document.querySelectorAll('form[data-lead]'),function(fm){
    var nm=fm.querySelector('input[data-name]'),ms=fm.querySelector('.msg'),btn=fm.querySelector('button[type=submit]');
    fm.addEventListener('submit',function(e){
      e.preventDefault();ms.hidden=false;
      var data={form:fm.dataset.form||'free-tour',form_location:fm.id||'',page:location.pathname,source:'website'};if(fm.dataset.coach)data.coach=fm.dataset.coach;
      [].forEach.call(fm.querySelectorAll('input,select,textarea'),function(el){
        if(!el.id)return;var k=el.id.split('-').pop();data[k]=(el.value||'').trim();
      });
      if(!data.name){ms.textContent='Add your name so we know who to expect.';nm.focus();return;}
      if(!data.phone&&!data.email){ms.textContent='Add a phone number or email so we can confirm your time.';return;}
      var parts=data.name.split(' ');data.first_name=parts.shift();data.last_name=parts.join(' ');
      if(!HOOK){ms.textContent='Thanks '+data.first_name+'. (Preview: this form is not connected yet.)';return;}
      btn.disabled=true;ms.textContent='Sending...';
      var body=new URLSearchParams(data);
      fetch(HOOK,{method:'POST',mode:'no-cors',body:body}).catch(function(){}).then(function(){
        if(fm.dataset.inline){btn.disabled=false;ms.textContent=fm.dataset.inline.replace('{name}',data.first_name);fm.reset();return;}
        try{if(window.fbq)fbq('track','Lead',{content_name:data.form});}catch(_){}
        try{(window.dataLayer=window.dataLayer||[]).push({event:'generate_lead',form:data.form});}catch(_){}
        setTimeout(function(){location.href='/thank-you/'},250);
      });
    });
  });
})();

// muted clips play only while on screen, so they cost nothing until someone scrolls to them
(function(){
  var vs=[].slice.call(document.querySelectorAll('video[data-autoplay]')); if(!vs.length) return;
  var reduce=matchMedia('(prefers-reduced-motion:reduce)').matches;
  if(reduce||!('IntersectionObserver' in window)){vs.forEach(function(v){v.controls=true});return;}
  var io=new IntersectionObserver(function(es){es.forEach(function(e){
    var v=e.target;
    if(e.isIntersecting){ if(v.preload!=='auto') v.preload='auto'; var p=v.play(); if(p&&p.catch) p.catch(function(){v.controls=true}); }
    else v.pause();
  })},{threshold:.35});
  vs.forEach(function(v){io.observe(v)});
})();

// blog topic filter
(function(){
  var chips=[].slice.call(document.querySelectorAll('.chip[data-cat]')); if(!chips.length) return;
  chips.forEach(function(c){c.addEventListener('click',function(){
    chips.forEach(function(x){x.setAttribute('aria-pressed',x===c)});
    var cat=c.dataset.cat;
    [].forEach.call(document.querySelectorAll('#post-grid .pcard'),function(card){card.hidden=!(cat==='all'||card.dataset.cat===cat)});
  })});
})();

// gallery: filter + full-screen viewer with keyboard and swipe
(function(){
  var grid=document.getElementById('ggrid'); if(!grid) return;
  var items=[].slice.call(grid.querySelectorAll('.gitem')), chips=[].slice.call(document.querySelectorAll('[data-gcat]'));
  chips.forEach(function(c){c.addEventListener('click',function(){
    chips.forEach(function(x){x.setAttribute('aria-pressed',x===c)});
    items.forEach(function(it){it.hidden=!(c.dataset.gcat==='all'||it.dataset.cat===c.dataset.gcat)});
  })});
  var lb=document.getElementById('lb'),img=document.getElementById('lb-img'),cap=document.getElementById('lb-cap'),cur=0,last=null;
  function vis(){return items.filter(function(it){return !it.hidden})}
  function show(it){var i=it.querySelector('img');img.src=i.src;img.alt=i.alt;cap.textContent=it.querySelector('.gcap b').textContent;cur=vis().indexOf(it)}
  function open(it){last=it;show(it);lb.hidden=false;document.body.style.overflow='hidden';lb.querySelector('.lb-x').focus()}
  function close(){lb.hidden=true;document.body.style.overflow='';if(last)last.focus()}
  function step(d){var v=vis();if(!v.length)return;cur=(cur+d+v.length)%v.length;show(v[cur])}
  items.forEach(function(it){it.addEventListener('click',function(){open(it)})});
  lb.querySelector('.lb-x').addEventListener('click',close);
  lb.querySelector('.lb-prev').addEventListener('click',function(){step(-1)});
  lb.querySelector('.lb-next').addEventListener('click',function(){step(1)});
  lb.addEventListener('click',function(e){if(e.target===lb)close()});
  document.addEventListener('keydown',function(e){if(lb.hidden)return;if(e.key==='Escape')close();if(e.key==='ArrowRight')step(1);if(e.key==='ArrowLeft')step(-1)});
  var x0=null;lb.addEventListener('touchstart',function(e){x0=e.touches[0].clientX},{passive:true});
  lb.addEventListener('touchend',function(e){if(x0===null)return;var dx=e.changedTouches[0].clientX-x0;if(Math.abs(dx)>40)step(dx<0?1:-1);x0=null});
})();

// parent consent waiver: signature pad + submit to /api/waiver
(function(){
  var fm=document.getElementById('sign'),cv=document.getElementById('sig'); if(!fm||!cv) return;
  var ctx=cv.getContext('2d'),drawn=false,down=false,last=null,wrap=cv.parentNode;
  try{document.getElementById('w-today').textContent=new Date().toLocaleDateString('en-US',{dateStyle:'long'});}catch(e){}
  function size(){
    var keep=drawn?cv.toDataURL():null,r=cv.getBoundingClientRect(),d=Math.max(window.devicePixelRatio||1,1);
    cv.width=Math.round(r.width*d);cv.height=Math.round(r.height*d);
    ctx.setTransform(d,0,0,d,0,0);ctx.lineWidth=2.4;ctx.lineCap='round';ctx.lineJoin='round';ctx.strokeStyle='#14120f';
    if(keep){var im=new Image();im.onload=function(){ctx.drawImage(im,0,0,r.width,r.height)};im.src=keep;}
  }
  size(); var rw=cv.getBoundingClientRect().width;
  window.addEventListener('resize',function(){var w=cv.getBoundingClientRect().width;if(Math.abs(w-rw)>2){rw=w;size();}});
  function pt(e){var r=cv.getBoundingClientRect();return{x:e.clientX-r.left,y:e.clientY-r.top}}
  cv.addEventListener('pointerdown',function(e){e.preventDefault();down=true;last=pt(e);cv.setPointerCapture(e.pointerId);ctx.beginPath();ctx.arc(last.x,last.y,1.1,0,6.3);ctx.fillStyle='#14120f';ctx.fill();mark();});
  cv.addEventListener('pointermove',function(e){if(!down)return;e.preventDefault();var p=pt(e);ctx.beginPath();ctx.moveTo(last.x,last.y);ctx.lineTo(p.x,p.y);ctx.stroke();last=p;mark();});
  ['pointerup','pointercancel','pointerleave'].forEach(function(t){cv.addEventListener(t,function(){down=false})});
  function mark(){if(!drawn){drawn=true;wrap.classList.add('signed');wrap.classList.remove('bad');}}
  document.getElementById('sig-clear').addEventListener('click',function(){ctx.clearRect(0,0,cv.width,cv.height);drawn=false;wrap.classList.remove('signed');});

  var ms=fm.querySelector('.msg'),btn=fm.querySelector('button[type=submit]');
  function err(t,first){ms.hidden=false;ms.classList.add('err');ms.textContent=t;if(first){first.scrollIntoView({behavior:'smooth',block:'center'});if(first.focus)first.focus({preventScroll:true});}}
  fm.addEventListener('input',function(e){var f=e.target.closest('.field,.agree');if(f)f.classList.remove('bad')});
  fm.addEventListener('submit',function(e){
    e.preventDefault();
    [].forEach.call(fm.querySelectorAll('.bad'),function(x){x.classList.remove('bad')});
    var data={},bad=[];
    [].forEach.call(fm.elements,function(el){
      if(!el.name)return;
      if(el.type==='radio'){if(el.checked)data[el.name]=el.value;return;}
      if(el.type==='checkbox'){data[el.name]=el.checked;return;}
      data[el.name]=(el.value||'').trim();
    });
    [].forEach.call(fm.querySelectorAll('[required]'),function(el){
      var ok=el.type==='radio'?!!data[el.name]:el.type==='checkbox'?el.checked:!!data[el.name];
      if(el.type==='email'&&ok)ok=/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data[el.name]);
      if(!ok){var f=el.closest('.field,.agree');if(f&&bad.indexOf(f)<0){f.classList.add('bad');bad.push(f);}}
    });
    if(!drawn){wrap.classList.add('bad');bad.push(wrap);}
    if(bad.length){err(bad.length===1&&bad[0]===wrap?'Please sign in the signature box.':'Please complete the highlighted fields.',bad[0].querySelector('input')||bad[0]);return;}
    data.signature=cv.toDataURL('image/png');
    btn.disabled=true;btn.textContent='Saving your waiver...';ms.hidden=true;ms.classList.remove('err');
    fetch('/api/waiver',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify(data)})
      .then(function(r){return r.json().catch(function(){return{ok:false}})})
      .then(function(res){
        if(!res.ok){btn.disabled=false;btn.textContent='Sign waiver';
          var first=null;(res.missing||[]).forEach(function(k){var el=fm.querySelector('[name="'+k+'"]');var f=k==='signature'?wrap:el&&el.closest('.field,.agree');if(f){f.classList.add('bad');first=first||f;}});
          err(res.error||'Something went wrong. Please try again or call (856) 839-4536.',first);return;}
        try{(window.dataLayer=window.dataLayer||[]).push({event:'waiver_signed'});}catch(_){}
        var done=document.getElementById('wv-done');fm.hidden=true;document.getElementById('waiver').hidden=true;
        var sk=document.querySelector('.wv-skip');if(sk)sk.hidden=true;done.hidden=false;
        done.scrollIntoView({behavior:'smooth',block:'start'});
      })
      .catch(function(){btn.disabled=false;btn.textContent='Sign waiver';err('No connection. Please check your internet and try again.');});
  });
})();
