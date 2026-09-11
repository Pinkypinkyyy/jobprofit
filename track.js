(function () {
  var GA = "G-8T6SXPNSCW";
  var GT = "GT-WVXQ29L2";
  var META = "";

  window.dataLayer = window.dataLayer || [];
  function gtag() {
    window.dataLayer.push(arguments);
  }
  window.gtag = gtag;
  gtag("js", new Date());
  gtag("config", GA);
  gtag("config", GT);

  var s = document.createElement("script");
  s.async = true;
  s.src = "https://www.googletagmanager.com/gtag/js?id=" + GA;
  document.head.appendChild(s);

  if (META) {
    !(function (f, b, e, v, n, t, s2) {
      if (f.fbq) return;
      n = f.fbq = function () {
        n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments);
      };
      if (!f._fbq) f._fbq = n;
      n.push = n;
      n.loaded = true;
      n.version = "2.0";
      n.queue = [];
      t = b.createElement(e);
      t.async = true;
      t.src = v;
      s2 = b.getElementsByTagName(e)[0];
      s2.parentNode.insertBefore(t, s2);
    })(window, document, "script", "https://connect.facebook.net/en_US/fbevents.js");
    window.fbq("init", META);
    window.fbq("track", "PageView");
  }

  window.spLead = function (method) {
    try {
      if (typeof gtag === "function") {
        gtag("event", "generate_lead", { method: method || "form" });
      }
      if (window.fbq) window.fbq("track", "Lead");
    } catch (err) {}
  };
})();
