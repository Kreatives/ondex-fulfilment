// Gedeelde interacties voor de losse Ondex-pagina's.
(function () {
  var prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Mobiel menu
  var toggle = document.querySelector("[data-nav-toggle]");
  var links = document.querySelector(".nav-links");
  if (toggle && links) {
    toggle.addEventListener("click", function () {
      var open = links.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    links.addEventListener("click", function (e) {
      if (e.target.tagName === "A") {
        links.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
      }
    });
  }

  // Diensten-dropdown in de navigatie
  var drop = document.querySelector(".nav-drop");
  if (drop) {
    var dropBtn = drop.querySelector("button");
    dropBtn.addEventListener("click", function (e) {
      e.stopPropagation();
      var open = drop.classList.toggle("open");
      dropBtn.setAttribute("aria-expanded", open ? "true" : "false");
    });
    document.addEventListener("click", function (e) {
      if (!drop.contains(e.target)) {
        drop.classList.remove("open");
        dropBtn.setAttribute("aria-expanded", "false");
      }
    });
  }

  // Reveal-on-scroll
  var revealEls = [].slice.call(document.querySelectorAll("[data-reveal]"));
  if (prefersReduced || !("IntersectionObserver" in window)) {
    revealEls.forEach(function (el) { el.classList.add("is-visible"); });
  } else {
    var revObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          var el = entry.target;
          var delay = el.getAttribute("data-reveal-delay");
          if (delay) el.style.transitionDelay = delay + "ms";
          el.classList.add("is-visible");
          revObserver.unobserve(el);
        }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -8% 0px" });
    revealEls.forEach(function (el) { revObserver.observe(el); });
  }

  // Count-up voor stat-cijfers
  var counters = [].slice.call(document.querySelectorAll("[data-count]"));
  var runCounter = function (el) {
    var target = parseFloat(el.getAttribute("data-count"));
    var decimals = (el.getAttribute("data-count").split(".")[1] || "").length;
    var prefix = el.getAttribute("data-prefix") || "";
    var suffix = el.getAttribute("data-suffix") || "";
    if (prefersReduced) {
      el.textContent = prefix + target.toFixed(decimals).replace(".", ",") + suffix;
      return;
    }
    var start = null;
    var duration = 1400;
    var step = function (ts) {
      if (!start) start = ts;
      var p = Math.min((ts - start) / duration, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      var val = (target * eased).toFixed(decimals).replace(".", ",");
      el.textContent = prefix + val + suffix;
      if (p < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  };
  if (counters.length) {
    if (!("IntersectionObserver" in window)) {
      counters.forEach(runCounter);
    } else {
      var cObserver = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) { runCounter(entry.target); cObserver.unobserve(entry.target); }
        });
      }, { threshold: 0.6 });
      counters.forEach(function (el) { cObserver.observe(el); });
    }
  }

  // Scrollspy voor de diensten-timeline: markeer de stap die in beeld is
  var steps = [].slice.call(document.querySelectorAll("[data-flow-step]"));
  if (steps.length && "IntersectionObserver" in window) {
    var flowObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          steps.forEach(function (s) { s.classList.remove("is-active"); });
          entry.target.classList.add("is-active");
        }
      });
    }, { threshold: 0.6, rootMargin: "-30% 0px -30% 0px" });
    steps.forEach(function (s) { flowObserver.observe(s); });
  }

  // Tabs (image links, tekst rechts)
  var tabGroups = [].slice.call(document.querySelectorAll("[data-tabs]"));
  tabGroups.forEach(function (group) {
    var tabs = [].slice.call(group.querySelectorAll(".tab"));
    var panels = [].slice.call(group.querySelectorAll(".tab-panel"));
    function activate(id) {
      tabs.forEach(function (t) {
        var on = t.getAttribute("data-tab") === id;
        t.classList.toggle("is-active", on);
        t.setAttribute("aria-selected", on ? "true" : "false");
      });
      panels.forEach(function (p) {
        var on = p.getAttribute("data-panel") === id;
        p.hidden = !on;
        if (on) {
          p.classList.remove("is-animating");
          void p.offsetWidth;
          p.classList.add("is-animating");
        }
      });
    }
    tabs.forEach(function (t) {
      t.addEventListener("click", function () { activate(t.getAttribute("data-tab")); });
    });
  });

  // Jaartal in de footer
  var yearEl = document.querySelector("[data-year]");
  if (yearEl) yearEl.textContent = new Date().getFullYear();
})();
