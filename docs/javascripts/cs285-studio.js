(function () {
  "use strict";
  var root = document.documentElement, path = location.pathname.toLowerCase(), body, key = "shoug-theme";
  var subjects = [
    { re:/logic-and-proof/, id:"logic", name:"Logic & Proofs", mark:"⊢" },
    { re:/basic-structures/, id:"structures", name:"Sets & Structures", mark:"∈" },
    { re:/number-theory/, id:"crypto", name:"Number Theory & Cryptography", mark:"≡" },
    { re:/induction-and-recursion/, id:"induction", name:"Induction & Recursion", mark:"∞" },
    { re:/advanced-counting/, id:"advanced-counting", name:"Advanced Counting", mark:"Σ" },
    { re:/\/counting\.html/, id:"counting", name:"Counting Principles", mark:"n!" },
    { re:/relations\.html/, id:"relations", name:"Relations", mark:"R" },
    { re:/cheat-sheet/, id:"reference", name:"Discrete Math Cheat Sheet", mark:"ƒ" }
  ];
  function subject() { for (var i=0;i<subjects.length;i+=1) if (subjects[i].re.test(path)) return subjects[i]; return {id:"core",name:"Discrete Mathematics",mark:"∴"}; }
  function read() { try { var v=localStorage.getItem(key)||localStorage.getItem("theme"); if (/^(light|dark)$/.test(v)) return v; } catch(e) {} return matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light"; }
  function icon(mode) { return mode==="dark"?'<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M2 12h2m16 0h2M5 5l1.4 1.4m11.2 11.2L19 19M5 19l1.4-1.4M17.6 6.4 19 5"/></svg>':'<svg viewBox="0 0 24 24"><path d="M20.2 15.3A8.5 8.5 0 1 1 8.7 3.8a7 7 0 0 0 11.5 11.5Z"/></svg>'; }
  function apply(mode,save) { root.dataset.theme=mode; root.style.colorScheme=mode; if(body){body.dataset.theme=mode;body.classList.toggle("shoug-light-mode",mode==="light");body.classList.toggle("shoug-dark-mode",mode==="dark");} var b=document.getElementById("cs285-theme");if(b){b.innerHTML=icon(mode);b.setAttribute("aria-label","Switch to "+(mode==="dark"?"light":"dark")+" mode");} if(save)try{localStorage.setItem(key,mode);localStorage.setItem("theme",mode);}catch(e){} }
  apply(read(),false);
  function setup(){
    body=document.body;if(!body)return;var s=subject(), reference=s.id==="reference", shell=!!body.querySelector(".app-layout,.layout-wrapper,.academic-sidebar,.sidebar"), embedded=window.parent!==window;
    body.classList.add("cs285-content",shell?"cs285-shell":(reference?"cs285-reference":"cs285-breakdown"),"cs285-topic-"+s.id);if(embedded)body.classList.add("cs285-embedded");body.dataset.topic=s.id;
    var bar=document.createElement("header");bar.className="cs285-bar";
    bar.innerHTML='<a class="cs285-brand" href="/academics/computer-science/cs285/"><span class="cs285-mark">'+s.mark+'</span><span><small>CS285 · '+(reference?'reference':'study guide')+'</small>'+s.name+'</span></a><nav aria-label="CS285 material"><a href="/academics/computer-science/cs285/slide-breakdowns/">Breakdowns</a><a href="/academics/computer-science/cs285/extra-resources/">Resources</a><a href="/academics/computer-science/cs285/slides/">Slides</a></nav><button id="cs285-theme" type="button"></button>';
    if(!embedded){body.insertBefore(bar,body.firstChild);bar.querySelector("button").onclick=function(){apply(root.dataset.theme==="dark"?"light":"dark",true);};}apply(read(),false);requestAnimationFrame(function(){body.classList.add("cs285-ready");});
  }
  if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",setup,{once:true});else setup();
})();
