/* ==========================================================================
   জাপানি চা পানি — সাইট স্ক্রিপ্ট (ডাইন-ইন সংস্করণ)
   ফিচার: মোবাইল মেনু, মেনু ক্যাটাগরি ফিল্টার, অ্যাক্টিভ নেভ লিংক,
           স্ক্রল অ্যানিমেশন। অনলাইন অর্ডার/কার্ট নেই — দোকানে এসে খেতে হয়।
   ========================================================================== */
(function () {
  "use strict";

  function $(sel, root) { return (root || document).querySelector(sel); }
  function $$(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }

  /* -------------------- হেডার: স্ক্রল ইফেক্ট -------------------- */
  var header = $("#site-header");
  function onScroll() {
    if (header) header.classList.toggle("is-stuck", window.scrollY > 12);
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* -------------------- মোবাইল মেনু -------------------- */
  var burger = $("#burger");
  var nav = $("#main-nav");
  function closeNav() {
    if (!nav) return;
    nav.classList.remove("is-open");
    if (burger) {
      burger.classList.remove("is-open");
      burger.setAttribute("aria-expanded", "false");
      burger.setAttribute("aria-label", "মেনু খুলুন");
    }
    document.body.style.overflow = "";
  }
  if (burger && nav) {
    burger.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      burger.classList.toggle("is-open", open);
      burger.setAttribute("aria-expanded", String(open));
      burger.setAttribute("aria-label", open ? "মেনু বন্ধ করুন" : "মেনু খুলুন");
      document.body.style.overflow = open ? "hidden" : "";
    });
    $$("a", nav).forEach(function (a) { a.addEventListener("click", closeNav); });
    window.addEventListener("resize", function () {
      if (window.innerWidth > 1050) closeNav();
    });
  }

  /* -------------------- অ্যাক্টিভ নেভ লিংক -------------------- */
  var navLinks = $$("#main-nav a[href^='#']");
  var sections = navLinks
    .map(function (a) { return document.getElementById(a.getAttribute("href").slice(1)); })
    .filter(Boolean);
  if ("IntersectionObserver" in window && sections.length) {
    var navObs = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        navLinks.forEach(function (a) {
          a.classList.toggle("is-active", a.getAttribute("href") === "#" + en.target.id);
        });
      });
    }, { rootMargin: "-45% 0px -50% 0px" });
    sections.forEach(function (s) { navObs.observe(s); });
  }

  /* -------------------- মেনু ফিল্টার -------------------- */
  var tabs = $$(".tab");
  var dishes = $$(".dish");

  function filterMenu(key) {
    dishes.forEach(function (d) {
      var show = key === "all" || d.getAttribute("data-cat") === key;
      d.classList.toggle("is-hidden", !show);
    });
    tabs.forEach(function (t) {
      var on = t.getAttribute("data-filter") === key;
      t.classList.toggle("is-active", on);
      t.setAttribute("aria-selected", String(on));
    });
  }
  tabs.forEach(function (tab) {
    tab.addEventListener("click", function () { filterMenu(tab.getAttribute("data-filter")); });
  });
  // ফুটারের ক্যাটাগরি লিংক → ট্যাব সিলেক্ট করে মেনুতে স্ক্রল
  $$("[data-jump]").forEach(function (link) {
    link.addEventListener("click", function () { filterMenu(link.getAttribute("data-jump")); });
  });

  /* -------------------- স্ক্রল রিভিল অ্যানিমেশন -------------------- */
  var reveals = $$(".reveal");
  function revealAll() { reveals.forEach(function (el) { el.classList.add("is-in"); }); }
  if (reveals.length) {
    document.documentElement.classList.add("js-ready");
    if ("IntersectionObserver" in window) {
      var rObs = new IntersectionObserver(function (entries, obs) {
        entries.forEach(function (en, i) {
          if (!en.isIntersecting) return;
          en.target.style.transitionDelay = Math.min(i * 70, 280) + "ms";
          en.target.classList.add("is-in");
          obs.unobserve(en.target);
        });
      }, { rootMargin: "0px 0px -8% 0px", threshold: 0.06 });
      reveals.forEach(function (el) { rObs.observe(el); });
      setTimeout(revealAll, 5000);   // সেফটি নেট
    } else {
      revealAll();
    }
  }

  /* -------------------- ফুটার বছর -------------------- */
  var BN = ["০", "১", "২", "৩", "৪", "৫", "৬", "৭", "৮", "৯"];
  function toBn(v) { return String(v).replace(/\d/g, function (d) { return BN[+d]; }); }
  var yearEl = $("#year");
  if (yearEl) yearEl.textContent = toBn(new Date().getFullYear());

  /* -------------------- আজ খোলা কি না (টপবারে ছোট তথ্য) -------------------- */
  var liveTag = $(".topbar .dot-live");
  if (liveTag) {
    var h = new Date().getHours();
    var open = h >= 7 && h < 23;      // প্রতিদিন সকাল ৭টা – রাত ১১টা
    var parent = liveTag.parentElement;
    if (parent && !open) {
      parent.innerHTML = '<span class="dot-live" style="background:#f97316"></span> এখন বন্ধ — সকাল ৭টায় খুলবে';
    }
  }
})();
