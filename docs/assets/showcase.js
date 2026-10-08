
(function(){
  "use strict";
  var data=JSON.parse(document.getElementById("showcase-data").textContent);
  var lang=new URLSearchParams(location.search).get("lang")==="zh"?"zh":"en";
  var selected=0, mode="review";
  var labels={
    en:{original:"Original",review:"Review notes",revised:"Revised",source:"Read source",reviewHeading:"WHY IT CHANGED",copy:"Copy request",copied:"Copied",fallback:"Select and copy the request below.",status:"Request copied. Replace [DATE] before sending.",report:"Read the full English report ↗"},
    zh:{original:"原稿",review:"修改说明",revised:"修订稿",source:"查看原文",reviewHeading:"为什么改",copy:"复制请求",copied:"已复制",fallback:"请选中并复制下方请求。",status:"已复制。发送前请替换 [日期]。",report:"阅读完整中文报告 ↗"}
  };
  function node(tag,className,text){
    var el=document.createElement(tag);if(className)el.className=className;if(text!==undefined)el.textContent=text;return el;
  }
  function excerpt(pair,side){
    var words=pair[lang], el=node("article","excerpt "+(side==="after"?"revised":""));
    var tag=node("p","excerpt-label",labels[lang][side==="before"?"original":"revised"]+" · "+words[side+"_tag"]);
    var quote=node("blockquote","",words[side]);
    var link=node("a","",labels[lang].source+" ↗");link.href=pair[side==="before"?"original_url":"revised_url"];
    el.append(tag,quote,link);return el;
  }
  function renderCase(){
    var pair=data.cases.pairs[selected], words=pair[lang];
    document.getElementById("case-title").textContent=words.title;
    document.querySelectorAll("[data-case]").forEach(function(el){
      var n=Number(el.dataset.case);el.setAttribute("aria-pressed",String(n===selected));
      el.replaceChildren(node("span","","0"+(n+1)),document.createTextNode(data.cases.pairs[n][lang].label));
    });
    document.querySelectorAll("[data-mode]").forEach(function(el){
      var active=el.dataset.mode===mode;el.textContent=labels[lang][el.dataset.mode];el.setAttribute("aria-selected",String(active));el.tabIndex=active?0:-1;
    });
    var panel=document.getElementById("case-panel");panel.replaceChildren();panel.setAttribute("aria-labelledby","tab-"+mode);
    var comparison=node("div","comparison"+(mode==="review"?"":" single"));
    if(mode==="original"||mode==="review")comparison.append(excerpt(pair,"before"));
    if(mode==="revised"||mode==="review")comparison.append(excerpt(pair,"after"));
    panel.append(comparison);
    if(mode==="review"){
      var note=node("aside","annotation");
      note.append(node("strong","",labels[lang].reviewHeading),node("p","",words.note),node("p","why",words.why));panel.append(note);
    }
    panel.append(node("p","version-note",words.version));
  }
  function renderLanguage(){
    document.documentElement.lang=lang==="zh"?"zh-CN":"en";
    document.querySelectorAll("[data-i18n]").forEach(function(el){var val=data.i18n[lang][el.dataset.i18n];if(val!==undefined)el.textContent=val;});
    document.querySelectorAll("[data-html]").forEach(function(el){el.innerHTML=data.i18n[lang][el.dataset.html];});
    document.getElementById("language-toggle").textContent=lang==="zh"?"English":"中文";
    document.getElementById("language-toggle").setAttribute("aria-label",lang==="zh"?"Switch to English":"切换为中文");
    document.getElementById("research-prompt").textContent=data.prompts[lang];
    document.getElementById("copy-request").textContent=labels[lang].copy;
    document.getElementById("copy-status").textContent="";
    var report="case-study/report."+(lang==="zh"?"zh-CN":"en")+".html";
    document.querySelectorAll("[data-report-link]").forEach(function(el){el.href=report;el.textContent=labels[lang].report;});
    document.getElementById("case-fallback").href="case-study/README"+(lang==="zh"?".zh-CN":"")+".md";
    document.title=lang==="zh"?"Research Toolkit · 从研究问题到有依据的报告":"Research Toolkit · From question to inspectable report";
    renderCase();
  }
  document.querySelectorAll("[data-case]").forEach(function(el){el.addEventListener("click",function(){selected=Number(el.dataset.case);renderCase();});});
  document.querySelectorAll("[data-mode]").forEach(function(el){el.addEventListener("click",function(){mode=el.dataset.mode;renderCase();});});
  document.querySelector(".case-tabs").addEventListener("keydown",function(event){
    var tabs=Array.from(this.querySelectorAll("[data-mode]")), i=tabs.indexOf(document.activeElement);
    if(i<0)return;var next;
    if(event.key==="ArrowRight")next=(i+1)%tabs.length;else if(event.key==="ArrowLeft")next=(i+tabs.length-1)%tabs.length;else if(event.key==="Home")next=0;else if(event.key==="End")next=tabs.length-1;else return;
    event.preventDefault();mode=tabs[next].dataset.mode;renderCase();tabs[next].focus();
  });
  document.getElementById("language-toggle").addEventListener("click",function(){
    lang=lang==="en"?"zh":"en";var url=new URL(location.href);if(lang==="zh")url.searchParams.set("lang","zh");else url.searchParams.delete("lang");history.replaceState(null,"",url);renderLanguage();
  });
  document.getElementById("copy-request").addEventListener("click",async function(){
    try{if(!navigator.clipboard)throw new Error("Clipboard unavailable");await navigator.clipboard.writeText(data.prompts[lang]);this.textContent=labels[lang].copied;document.getElementById("copy-status").textContent=labels[lang].status;}
    catch(error){var range=document.createRange();range.selectNodeContents(document.getElementById("research-prompt"));var selection=window.getSelection();selection.removeAllRanges();selection.addRange(range);document.getElementById("copy-status").textContent=labels[lang].fallback;}
  });
  renderLanguage();
})();

