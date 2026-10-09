(function () {
  "use strict";
  var params = new URLSearchParams(location.search);
  var savedTheme, savedLanguage;
  try {
    savedTheme = localStorage.getItem("research-toolkit.theme");
    savedLanguage = localStorage.getItem("research-toolkit.language");
  } catch (_) {}
  var isHome = !!document.getElementById("showcase-data") || /\/(?:index\.html)?$/.test(location.pathname);
  var lang = params.get("lang") === "zh" ? "zh" : params.get("lang") === "en" ? "en" :
    (isHome && ["en", "zh"].includes(savedLanguage) ? savedLanguage : document.documentElement.lang.indexOf("zh") === 0 ? "zh" : "en");
  var theme = ["light", "dark"].includes(params.get("theme")) ? params.get("theme") :
    ["light", "dark"].includes(savedTheme) ? savedTheme : matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  var topic = ["writing", "process", "versions", "analysis"].includes(params.get("case")) ? params.get("case") : "writing";
  var detail = ["diff", "reason", "review"].includes(params.get("detail")) ? params.get("detail") : "diff";
  var words = {
    en: {home:"Research Toolkit", archive:"Case archive", sources:"Source records (Chinese)", claims:"Claim records (Chinese)", scroll:"Scroll horizontally to read the table.", toc:"Contents", top:"Back to top", csv:"Download CSV", openSource:"Original source", notes:"Original Chinese notes", date:"Publication date", publisher:"Publisher", supports:"Use in the report", limits:"Limits", record:"Record details", contrary:"Counter-evidence", uncertainty:"Uncertainty", kind:"Claim type", grade:"Recorded evidence level"},
    zh: {home:"Research Toolkit", archive:"案例档案", sources:"来源资料", claims:"论点资料", scroll:"表格可横向滚动。", toc:"目录", top:"返回顶部", csv:"下载 CSV", openSource:"原始来源", notes:"中文原始记录", date:"发布日期", publisher:"发布者", supports:"报告中的用途", limits:"限制", record:"记录详情", contrary:"反证", uncertainty:"不确定性", kind:"论点类型", grade:"记录中的证据等级"}
  };
  function applyLinks() {
    document.querySelectorAll("a[data-preserve-reading],a[data-home-link],a[data-language]").forEach(function (a) {
      var href = a.getAttribute("href");
      if (!href || href[0] === "#") return;
      var url = new URL(href, location.href);
      if (url.origin !== location.origin) return;
      url.searchParams.set("lang", a.dataset.language || lang);
      url.searchParams.set("theme", theme);
      url.searchParams.set("case", topic);
      url.searchParams.set("detail", detail);
      url.searchParams.delete("mode");
      a.href = url.href;
    });
    document.querySelectorAll("[data-reader-label]").forEach(function (e) {
      var text = words[lang][e.dataset.readerLabel];
      if (text) e.textContent = text;
    });
  }
  function applyTheme() {
    document.documentElement.dataset.theme = theme;
    document.documentElement.classList.add("js");
  }
  function update(next, changeURL) {
    if (next.lang) lang = next.lang;
    if (next.theme) theme = next.theme;
    if (next.topic) topic = next.topic;
    if (next.detail) detail = next.detail;
    try {
      if (next.theme) localStorage.setItem("research-toolkit.theme", theme);
      if (next.lang) localStorage.setItem("research-toolkit.language", lang);
    } catch (_) {}
    applyTheme(); applyLinks();
    if (changeURL) {
      var url = new URL(location.href);
      url.searchParams.set("lang", lang);
      url.searchParams.set("theme", theme);
      url.searchParams.set("case", topic);
      url.searchParams.set("detail", detail);
      url.searchParams.delete("mode");
      history.replaceState(null, "", url);
    }
  }
  window.RTReading = {
    get: function () { return {lang:lang, theme:theme, topic:topic, detail:detail}; },
    set: update,
    links: applyLinks
  };
  applyTheme();
  function ready() {
    applyLinks();
    document.addEventListener("click", function (event) {
      var a = event.target.closest("a[data-language]");
      if (a) {
        try { localStorage.setItem("research-toolkit.language", a.dataset.language); } catch (_) {}
      }
    });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", ready);
  else ready();
})();
