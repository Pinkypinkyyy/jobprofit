(function () {
  var nav = document.getElementById("pinkNav");
  var btn = document.getElementById("pinkBurger");
  if (nav && btn) {
    btn.addEventListener("click", function () {
      nav.classList.toggle("open");
      btn.setAttribute("aria-expanded", nav.classList.contains("open") ? "true" : "false");
    });
  }

  var copy = {
    hvac: "For HVAC firms we watch labour against the quoted hours, materials on the van, and whether a call-out actually covered the next tax bill.",
    electrical: "For electrical businesses we watch quoted jobs versus hours on the tools, subcontractors, and cash sitting in unfinished work.",
    construction: "For construction services we watch the job, not the building. Labour, subcontractors and materials, read while you can still change the next quote."
  };
  var trades = document.querySelectorAll(".trade");
  var live = document.getElementById("liveLine");
  var figs = document.querySelectorAll(".pair figure");
  function setTrade(key) {
    trades.forEach(function (t) {
      t.classList.toggle("is-on", t.getAttribute("data-trade") === key);
    });
    figs.forEach(function (f, i) {
      var on = (key === "hvac" && i === 0) || (key === "electrical" && i === 1) || key === "construction";
      f.classList.toggle("is-on", on);
    });
    if (live && copy[key]) live.textContent = copy[key];
  }
  trades.forEach(function (t) {
    t.addEventListener("click", function () {
      setTrade(t.getAttribute("data-trade"));
    });
  });
  figs.forEach(function (f) {
    f.addEventListener("click", function () {
      var key = f.getAttribute("data-trade");
      if (key) setTrade(key);
    });
  });

  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (!reduce) {
    var nodes = document.querySelectorAll(".pcol, .feat, .tier, .stepc, .funnel .card, .meet, .pair figure");
    nodes.forEach(function (el) { el.classList.add("reveal"); });
    if ("IntersectionObserver" in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) {
            e.target.classList.add("is-in");
            io.unobserve(e.target);
          }
        });
      }, { threshold: 0.16 });
      document.querySelectorAll(".reveal").forEach(function (el) { io.observe(el); });
    } else {
      document.querySelectorAll(".reveal").forEach(function (el) { el.classList.add("is-in"); });
    }
  }

  var bar = document.getElementById("bookBar");
  if (bar) {
    window.addEventListener("scroll", function () {
      var y = window.scrollY || 0;
      var nearFoot = document.documentElement.scrollHeight - window.innerHeight - y < 280;
      bar.classList.toggle("show", y > 520 && !nearFoot && window.innerWidth > 940);
    }, { passive: true });
  }

  document.querySelectorAll(".tier").forEach(function (card) {
    card.addEventListener("click", function () {
      document.querySelectorAll(".tier").forEach(function (c) { c.classList.remove("is-on"); });
      card.classList.add("is-on");
    });
  });
})();
