(function () {
  "use strict";
  var data = JSON.parse(document.getElementById("showcase-data").textContent);
  var reading = window.RTReading;
  var state = reading.get(), lang = state.lang, theme = state.theme;
  var selected = data.cases.pairs.findIndex(function (p) { return p.id === state.topic; });
  if (selected < 0) selected = 0;
  var detail = state.detail || "diff";
  var params = new URLSearchParams(location.search);
  if (params.get("view") === "readme") document.body.classList.add("capture-readme");
  if (params.get("view") === "method") document.body.classList.add("capture-method");
  function node(tag, className, text) {
    var e = document.createElement(tag);
    if (className) e.className = className;
    if (text !== undefined) e.textContent = text;
    return e;
  }
  function highlighted(text, needles) {
    var fragment = document.createDocumentFragment(), cursor = 0;
    (needles || []).map(function (needle) { return {start:text.indexOf(needle),word:needle}; })
      .filter(function (s) { return s.start >= 0; }).sort(function (a,b) { return a.start-b.start; })
      .forEach(function (s) {
        if (s.start < cursor) return;
        fragment.append(document.createTextNode(text.slice(cursor,s.start)),node("mark","",s.word));
        cursor = s.start+s.word.length;
      });
    fragment.append(document.createTextNode(text.slice(cursor)));
    return fragment;
  }
  function link(label, href) {
    var a = node("a", "", label + " ↗");
    a.href = href; a.setAttribute("data-preserve-reading", ""); return a;
  }
  function excerpt(pair, side) {
    var words = data.i18n[lang], text = pair[lang], after = side === "after";
    var el = node("article", "excerpt" + (after ? " revised" : ""));
    var label = node("h4", "excerpt-label", words[after ? "final" : "initial"]);
    label.append(node("span", "", words.summaryLabel));
    var copy = node("blockquote", "excerpt-copy");
    copy.append(highlighted(text[side], after ? text.highlights : text.before_highlights));
    el.append(label, copy, node("p", "excerpt-note", text[side + "_note"]),
      link(words.passage, pair[after ? "revised_url" : "original_url"]));
    return el;
  }
  function choices(items, className) {
    var list = node("dl", className);
    items.forEach(function (item) { list.append(node("dt", "", item.label), node("dd", "", item.text)); });
    return list;
  }
  function renderDetail(pair) {
    var text = pair[lang], words = data.i18n[lang], panel = document.getElementById("case-panel");
    panel.dataset.detail = detail; panel.setAttribute("aria-labelledby", "detail-" + detail);
    document.querySelectorAll("[data-detail][role='tab']").forEach(function (button) {
      var active = button.dataset.detail === detail;
      button.setAttribute("aria-selected", String(active)); button.tabIndex = active ? 0 : -1;
      button.textContent = words[{diff:"detailDiff",reason:"detailReason",review:"detailReview"}[button.dataset.detail]];
    });
    if (detail === "diff") {
      var change = node("div", "case-difference");
      change.append(node("h4", "", words.changeHeading), choices(text.changes, "case-change-list"));
      panel.replaceChildren(excerpt(pair, "before"), excerpt(pair, "after"), change);
    } else if (detail === "reason") {
      var reason = node("div", "case-reasoning");
      text.reasons.forEach(function (item) {
        var section = node("section", "reason-section");
        section.append(node("h4", "", item.heading), node("p", "", item.body)); reason.append(section);
      });
      var trade = node("section", "reason-tradeoffs");
      trade.append(node("h4", "", words.tradeoffHeading), choices(text.tradeoffs, "case-tradeoffs")); reason.append(trade);
      var sources = node("div", "reason-sources"); sources.append(node("span", "", words.supportingSources));
      text.sources.forEach(function (item) { sources.append(link(item.label, item.url)); }); reason.append(sources);
      panel.replaceChildren(reason);
    } else {
      var review = node("div", "case-review"), history = node("div", "review-history");
      text.history.forEach(function (item) {
        var stage = node("article", "review-stage"); stage.append(node("h4", "", item.stage), node("p", "", item.body)); history.append(stage);
      });
      var decisions = node("div", "review-decisions");
      text.decisions.forEach(function (item) {
        var article = node("article", "review-decision");
        article.append(node("h4", "", item.finding), node("p", "decision-choice", item.decision), node("p", "", item.basis)); decisions.append(article);
      });
      review.append(history, decisions, node("p", "review-note", text.review_note), link(text.review_link, pair.review_url));
      panel.replaceChildren(review);
    }
  }
  function renderCase() {
    var pair = data.cases.pairs[selected], text = pair[lang];
    document.querySelectorAll("[data-case]").forEach(function (button) {
      var n = Number(button.dataset.case), active = n === selected;
      button.setAttribute("aria-selected", String(active)); button.tabIndex = active ? 0 : -1;
      button.textContent = data.cases.pairs[n][lang].label;
    });
    document.getElementById("case-content").setAttribute("aria-labelledby", "topic-" + pair.id);
    document.getElementById("case-context").textContent = text.context;
    document.getElementById("case-context").hidden = !text.context;
    document.getElementById("case-title").replaceChildren.apply(document.getElementById("case-title"), text.title.split(/(Claude Code|Codex CLI)/).map(function (part) { return /^(Claude Code|Codex CLI)$/.test(part) ? node("span", "case-program", part) : document.createTextNode(part); }));
    document.getElementById("case-why").textContent = text.why;
    document.querySelector(".case-detail-tabs").setAttribute("aria-label", data.i18n[lang].detailAria);
    renderDetail(pair);
    var evidence = document.getElementById("evidence-source"); evidence.textContent = data.i18n[lang].sourcesLabel + " ↗";
    reading.set({lang:lang, theme:theme, topic:pair.id, detail:detail}, true);
  }
  function renderTheme() {
    document.documentElement.dataset.theme = theme;
    var button = document.getElementById("theme-toggle");
    button.textContent = data.i18n[lang][theme === "light" ? "themeDark" : "themeLight"];
    button.setAttribute("aria-label",data.i18n[lang].themeAction);
    button.setAttribute("aria-pressed",String(theme === "dark"));
  }
  function renderLanguage() {
    document.documentElement.lang = lang === "zh" ? "zh-CN" : "en";
    document.querySelectorAll("[data-i18n]").forEach(function (e) {
      var text = data.i18n[lang][e.dataset.i18n]; if (text !== undefined) e.textContent = text;
    });
    document.querySelector("[data-nav-aria]").setAttribute("aria-label",data.i18n[lang].navAria);
    document.querySelector(".case-choices").setAttribute("aria-label",data.i18n[lang].topicsAria);
    document.querySelector(".language-switch").setAttribute("aria-label",lang === "zh" ? "语言" : "Language");
    document.querySelectorAll(".language-switch [data-language]").forEach(function (button) {
      button.setAttribute("aria-pressed",String(button.dataset.language === lang));
    });
    document.getElementById("research-prompt").textContent = data.prompts[lang];
    document.getElementById("hero-quote").replaceChildren(highlighted(data.cases.hero[lang].quote,data.cases.hero[lang].highlights));
    document.getElementById("copy-status").textContent = "";
    document.querySelectorAll("[data-report-link]").forEach(function (e) { e.href = "case-study/report."+(lang === "zh" ? "zh-CN" : "en")+".html"; });
    document.querySelectorAll("[data-method-link]").forEach(function (e) { e.href = "framework"+(lang === "zh" ? ".zh-CN" : "")+".html"; });
    document.querySelectorAll("[data-record-language]").forEach(function (e) {
      if (lang !== "en") return;
      var labels = {sources:"Source records (Chinese)",claims:"Claim records (Chinese)",reviews:"Review records (Chinese)"};
      var span = e.querySelector("span"); if (span) span.textContent = labels[e.dataset.recordLanguage];
    });
    document.querySelectorAll("[data-usage-link]").forEach(function (e) {
      var url = new URL(e.href);
      url.pathname = url.pathname.replace(/usage-modes(?:\.zh-CN)?\.md/,"usage-modes"+(lang === "zh" ? ".zh-CN" : "")+".md");
      if (url.hash) url.hash = lang === "zh" ? (e.dataset.i18n === "mcpLink" ? "#单独接入-mcp" : "#安装插件") : (e.dataset.i18n === "mcpLink" ? "#connect-mcp-separately" : "#install-the-plugin");
      e.href = url.href;
    });
    document.querySelectorAll("[data-eval-link]").forEach(function (e) { e.href = "https://github.com/rrrrrredy/research-toolkit/blob/main/docs/evaluation-status"+(lang === "zh" ? ".zh-CN" : "")+".md"; });
    document.querySelectorAll("[data-agent-link]").forEach(function (e) {
      var file = "https://github.com/rrrrrredy/research-toolkit/blob/main/agents/README"+(lang === "zh" ? ".zh-CN" : "")+".md";
      var anchor = e.dataset.i18n === "textLink" ? (lang === "zh" ? "#只能在聊天中使用时" : "#chat-only-use") : (lang === "zh" ? "#直接读取使用" : "#use-without-installation");
      e.href = file+anchor;
    });
    var skillGuide = document.querySelector("[data-i18n='skillLink']");
    skillGuide.href = "https://github.com/rrrrrredy/research-toolkit/blob/main/agents/README"+(lang === "zh" ? ".zh-CN" : "")+".md"+(lang === "zh" ? "#安装后重复使用" : "#install-for-repeated-use");
    var fallback = document.querySelector("[data-i18n='fallbackGuide']");
    fallback.href = "https://github.com/rrrrrredy/research-toolkit/blob/main/agents/README"+(lang === "zh" ? ".zh-CN" : "")+".md"+(lang === "zh" ? "#直接读取使用" : "#use-without-installation");
    var video = document.querySelector("video"), source = video.querySelector("source");
    video.poster = "assets/readme-preview."+(lang === "zh" ? "zh-CN" : "en")+".png";
    var file = "assets/case-walkthrough"+(lang === "zh" ? ".zh-CN" : "")+".mp4";
    if (source.getAttribute("src") !== file) { source.setAttribute("src",file); video.load(); }
    document.title = lang === "zh" ? "Research Toolkit · 面向 AI Agent 的研究工具箱" : "Research Toolkit · Research methods and tools for AI agents";
    document.querySelector('meta[name="description"]').content = data.i18n[lang].lede;
    renderTheme(); renderCase();
  }
  document.querySelectorAll("[data-case]").forEach(function (button) {
    button.addEventListener("click",function () { selected = Number(button.dataset.case); renderCase(); });
  });
  var topicLayout = matchMedia("(min-width:1001px)");
  function topicOrientation() {
    document.querySelector(".case-choices").setAttribute("aria-orientation",topicLayout.matches ? "vertical" : "horizontal");
  }
  topicOrientation(); topicLayout.addEventListener("change",topicOrientation);
  document.querySelector(".case-choices").addEventListener("keydown",function (event) {
    var buttons = Array.from(this.querySelectorAll("[data-case]")), current = buttons.indexOf(document.activeElement), next;
    if (current < 0) return;
    if (event.key === "ArrowRight" || (topicLayout.matches && event.key === "ArrowDown")) next = (current+1)%buttons.length;
    else if (event.key === "ArrowLeft" || (topicLayout.matches && event.key === "ArrowUp")) next = (current+buttons.length-1)%buttons.length;
    else if (event.key === "Home") next = 0;
    else if (event.key === "End") next = buttons.length-1;
    else return;
    event.preventDefault(); selected = next; renderCase(); buttons[next].focus();
  });
  var details = Array.from(document.querySelectorAll("[data-detail][role='tab']"));
  details.forEach(function (button) {
    button.addEventListener("click", function () { detail = button.dataset.detail; renderCase(); });
  });
  document.querySelector(".case-detail-tabs").addEventListener("keydown", function (event) {
    var current = details.indexOf(document.activeElement), next;
    if (current < 0) return;
    if (event.key === "ArrowRight") next = (current + 1) % details.length;
    else if (event.key === "ArrowLeft") next = (current + details.length - 1) % details.length;
    else if (event.key === "Home") next = 0;
    else if (event.key === "End") next = details.length - 1;
    else return;
    event.preventDefault(); detail = details[next].dataset.detail; renderCase(); details[next].focus();
  });
  document.querySelectorAll(".language-switch [data-language]").forEach(function (button) {
    button.addEventListener("click",function () {
      if (lang === button.dataset.language) return;
      lang = button.dataset.language; renderLanguage();
    });
  });
  document.getElementById("theme-toggle").addEventListener("click",function () { theme = theme === "light" ? "dark" : "light"; reading.set({theme:theme},true); renderTheme(); });
  document.getElementById("copy-request").addEventListener("click",async function () {
    try {
      if (!navigator.clipboard) throw new Error("Clipboard unavailable");
      await navigator.clipboard.writeText(data.prompts[lang]);
      this.textContent = lang === "zh" ? "已复制" : "Copied";
      document.getElementById("copy-status").textContent = lang === "zh" ? "请求已复制，发送前请替换 [日期]。" : "Request copied. Replace [DATE] before sending.";
    } catch (_) {
      var range = document.createRange(); range.selectNodeContents(document.getElementById("research-prompt"));
      var selection = window.getSelection(); selection.removeAllRanges(); selection.addRange(range);
      document.getElementById("copy-status").textContent = lang === "zh" ? "请选中并复制请求。" : "Select and copy the request.";
    }
  });
  renderLanguage();
})();
