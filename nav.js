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

  // Services dropdown: hover opens it on a computer; the arrow button opens it
  // for touch and keyboard. On phones the CSS shows the list inside the menu.
  var drop = document.querySelector(".navdrop");
  var tog = drop && drop.querySelector(".navdrop-toggle");
  function setDrop(open) {
    if (!drop || !tog) return;
    drop.classList.toggle("is-open", open);
    tog.setAttribute("aria-expanded", open ? "true" : "false");
  }
  if (drop && tog) {
    tog.addEventListener("click", function () {
      setDrop(!drop.classList.contains("is-open"));
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") setDrop(false);
    });
    document.addEventListener("click", function (e) {
      if (!drop.contains(e.target)) setDrop(false);
    });
  }

  var copy = {
    hvac: "Air con and refrigeration. Quoted hours versus hours on the job.",
    electrical: "Electrical. Hours on the tools versus the quote.",
    construction: "Fit-out and maintenance. Not house builders."
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
      t.setAttribute("aria-pressed", on ? "true" : "false");
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
      t.addEventListener("click", function () {
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

  var hoursForm = document.getElementById("hoursCheck");
  var hoursOut = document.getElementById("hoursResult");
  var hoursLine = document.getElementById("hoursResultLine");
  if (hoursForm && hoursOut && hoursLine) {
    hoursForm.addEventListener("submit", function (e) {
      e.preventDefault();
      var quoted = parseFloat(hoursForm.quoted.value);
      var tools = parseFloat(hoursForm.tools.value);
      var rate = parseFloat(hoursForm.rate.value);
      if (!(quoted > 0) || !(tools > 0) || !(rate > 0)) return;
      var extra = Math.max(0, Math.round((tools - quoted) * 10) / 10);
      var dollars = Math.round(extra * rate);
      if (extra <= 0) {
        hoursLine.textContent =
          "That job landed on quote. The leak is often the next job, or the bank. Book 15 minutes if the quotes and the tax still do not match.";
      } else {
        hoursLine.textContent =
          "That job ran " + extra + " hours over. At $" + rate +
          " an hour, about $" + dollars +
          " never made the next quote.";
      }
      hoursOut.hidden = false;
      hoursOut.scrollIntoView({ behavior: "smooth", block: "nearest" });
      try {
        if (typeof gtag === "function") gtag("event", "generate_lead", { method: "hours-check" });
      } catch (err) {}
    });
  }

  var crewForm = document.getElementById("crewCheck");
  var crewOut = document.getElementById("crewResult");
  var crewLine = document.getElementById("crewResultLine");
  if (crewForm && crewOut && crewLine) {
    crewForm.addEventListener("submit", function (e) {
      e.preventDefault();
      var techs = parseFloat(crewForm.techs.value);
      var leak = parseFloat(crewForm.leak.value);
      var rate = parseFloat(crewForm.rate.value);
      if (!(techs > 0) || !(leak >= 0) || !(rate > 0)) return;
      var week = Math.round(techs * leak * rate);
      var year = week * 52;
      var money = function (n) {
        return "$" + n.toLocaleString("en-AU");
      };
      if (leak === 0) {
        crewLine.textContent =
          "No unbilled hours in that week. The leak is often the next job, or the bank after GST, PAYG, super and wages. Book 15 minutes if those still do not match.";
      } else {
        crewLine.textContent =
          techs +
          " people, " +
          leak +
          " unbilled hours each, at $" +
          rate +
          " an hour. That is " +
          money(week) +
          " a week, about " +
          money(year) +
          " a year, that never made a quote. Job Profit is $19,800 + GST a year.";
      }
      crewOut.hidden = false;
      crewOut.scrollIntoView({ behavior: "smooth", block: "nearest" });
      try {
        if (typeof gtag === "function") gtag("event", "generate_lead", { method: "hours-check-crew" });
      } catch (err) {}
    });
  }

  var form = document.getElementById("enquiryForm");
  var ok = document.getElementById("enquiryOk");
  var formShownAt = Date.now();
  if (form) {
    var params = new URLSearchParams(window.location.search);
    if (params.get("sent") === "1" && ok) {
      form.hidden = true;
      ok.hidden = false;
      ok.scrollIntoView({ behavior: "smooth", block: "center" });
    }
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (form.querySelector("[name=_gotcha]").value) return;
      if (Date.now() - formShownAt < 4000) return;
      var btn = form.querySelector("button[type=submit]");
      var btnLabel = btn ? btn.textContent : "";
      if (btn) {
        btn.disabled = true;
        btn.textContent = "Sending…";
      }
      var data = {};
      new FormData(form).forEach(function (value, key) {
        data[key] = value;
      });
      delete data._gotcha;
      fetch(form.getAttribute("data-ajax") || form.action, {
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
          if (ok) ok.scrollIntoView({ behavior: "smooth", block: "center" });
          if (typeof window.spLead === "function") window.spLead("form");
        })
        .catch(function () {
          var labels = {
            name: "Name", business: "Business", email: "Email", phone: "Phone",
            trade: "Work", revenue: "Revenue", staff: "Staff", hurt: "Hurting",
            position: "Current position", vision: "12-month vision",
            message: "Message"
          };
          var body = Object.keys(data)
            .filter(function (k) { return k.charAt(0) !== "_" && data[k]; })
            .map(function (k) { return (labels[k] || k) + ": " + data[k]; })
            .join("\n");
          window.location.href =
            "mailto:admin@pinktax.com.au?subject=" +
            encodeURIComponent("Service Profit intake") +
            "&body=" +
            encodeURIComponent(body);
        })
        .finally(function () {
          if (btn) {
            btn.disabled = false;
            btn.textContent = btnLabel;
          }
        });
    });
  }
})();
