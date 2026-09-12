(function () {
  var nav = document.getElementById("pinkNav");
  var btn = document.getElementById("pinkBurger");

  function setMenu(open) {
    if (!nav || !btn) return;
    nav.classList.toggle("open", open);
    btn.setAttribute("aria-expanded", open ? "true" : "false");
  }

  if (nav && btn) {
    btn.addEventListener("click", function () {
      setMenu(!nav.classList.contains("open"));
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") setMenu(false);
    });
    document.addEventListener("click", function (e) {
      if (!nav.classList.contains("open")) return;
      if (nav.contains(e.target)) return;
      setMenu(false);
    });
  }

  var copy = {
    hvac: "HVAC: labour against quoted hours, materials on the job, and whether the call-out covered the next tax bill.",
    electrical: "Electrical: quoted jobs versus hours on the tools, subcontractors, and cash in unfinished work.",
    construction: "Construction services: the job, not the building. Labour, subcontractors and materials while you can still change the next quote."
  };
  var labels = { hvac: "HVAC", electrical: "Electrical", construction: "Construction services" };
  var trades = document.querySelectorAll(".trade");
  var live = document.getElementById("liveLine");
  var shots = document.querySelectorAll("#stage img");
  var cap = document.getElementById("stageCap");

  function setTrade(key) {
    trades.forEach(function (t) {
      var on = t.getAttribute("data-trade") === key;
      t.classList.toggle("is-on", on);
    });
    shots.forEach(function (img) {
      var on = img.getAttribute("data-trade") === key;
      img.classList.toggle("is-on", on);
      if (on) {
        img.removeAttribute("aria-hidden");
        img.removeAttribute("inert");
      } else {
        img.setAttribute("aria-hidden", "true");
        img.setAttribute("inert", "");
      }
    });
    if (live && copy[key]) live.textContent = copy[key];
    if (cap && labels[key]) cap.textContent = labels[key];
  }

  if (trades.length) {
    setTrade("hvac");
    trades.forEach(function (t) {
      t.addEventListener("mouseenter", function () {
        setTrade(t.getAttribute("data-trade"));
      });
      t.addEventListener("focus", function () {
        setTrade(t.getAttribute("data-trade"));
      });
    });
  }

  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (!reduce) {
    var nodes = document.querySelectorAll(".pcol, .feat, .tier, .stepc, .funnel .card, .meet");
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

  document.querySelectorAll("[data-event]").forEach(function (el) {
    el.addEventListener("click", function () {
      try {
        var row = {
          t: Date.now(),
          e: el.getAttribute("data-event"),
          href: el.getAttribute("href") || ""
        };
        var prev = JSON.parse(sessionStorage.getItem("spEvents") || "[]");
        prev.push(row);
        sessionStorage.setItem("spEvents", JSON.stringify(prev.slice(-50)));
        if (typeof gtag === "function") {
          gtag("event", "select_content", { content_id: row.e });
        }
      } catch (err) {}
    });
  });

  var form = document.getElementById("enquiryForm");
  var ok = document.getElementById("enquiryOk");
  if (form) {
    var params = new URLSearchParams(window.location.search);
    if (params.get("sent") === "1" && ok) {
      form.hidden = true;
      ok.hidden = false;
    }
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (form.querySelector("[name=_gotcha]").value) return;
      var btn = form.querySelector("button[type=submit]");
      if (btn) {
        btn.disabled = true;
        btn.textContent = "Sending…";
      }
      var data = {
        name: form.name.value,
        email: form.email.value,
        phone: form.phone.value,
        trade: form.trade.value,
        message: form.message.value,
        _subject: "Service Profit enquiry",
        _template: "table",
        _captcha: "false"
      };
      fetch("https://formsubmit.co/ajax/admin@pinktax.com.au", {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify(data)
      })
        .then(function (res) {
          if (!res.ok) throw new Error("send-failed");
          return res.json();
        })
        .then(function () {
          form.hidden = true;
          if (ok) ok.hidden = false;
          if (typeof window.spLead === "function") window.spLead("form");
        })
        .catch(function () {
          var body =
            "Name: " + data.name +
            "\nEmail: " + data.email +
            "\nPhone: " + data.phone +
            "\nTrade: " + data.trade +
            "\n\n" + data.message;
          window.location.href =
            "mailto:admin@pinktax.com.au?subject=" +
            encodeURIComponent("Service Profit enquiry") +
            "&body=" +
            encodeURIComponent(body);
        })
        .finally(function () {
          if (btn) {
            btn.disabled = false;
            btn.textContent = "Send the enquiry";
          }
        });
    });
  }
})();
