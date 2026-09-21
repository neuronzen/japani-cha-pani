/* ==========================================================================
   জাপানি চা পানি — সাইট স্ক্রিপ্ট
   ফিচার: মোবাইল মেনু, মেনু ফিল্টার, অর্ডার তালিকা (কার্ট), ফর্ম ভ্যালিডেশন
           এবং হোয়াটসঅ্যাপে অর্ডার পাঠানো।
   ========================================================================== */
(function () {
  "use strict";

  /* -------------------- কনফিগ (মালিক এখানে বদলাবেন) -------------------- */
  var SHOP = {
    whatsapp: "8801677725711",        // দেশের কোডসহ, + ছাড়া (হটলাইন: ০১৬৭৭-৭২৫৭১১)
    currency: "৳"
  };

  /* -------------------- হেল্পার -------------------- */
  var BN_DIGITS = ["০", "১", "২", "৩", "৪", "৫", "৬", "৭", "৮", "৯"];

  function toBn(value) {
    return String(value).replace(/\d/g, function (d) { return BN_DIGITS[+d]; });
  }
  function money(amount) {
    return SHOP.currency + " " + toBn(amount);
  }
  function $(sel, root) { return (root || document).querySelector(sel); }
  function $$(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }

  /* -------------------- হেডার: স্ক্রল ইফেক্ট -------------------- */
  var header = $("#site-header");
  function onScroll() {
    if (!header) return;
    header.classList.toggle("is-stuck", window.scrollY > 12);
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
      if (window.innerWidth > 980) closeNav();
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

  // প্রতিটি ক্যাটাগরির সংখ্যা স্বয়ংক্রিয়ভাবে হিসাব করে ট্যাবে বসানো
  tabs.forEach(function (tab) {
    var key = tab.getAttribute("data-filter");
    var count = key === "all" ? dishes.length : dishes.filter(function (d) { return d.getAttribute("data-cat") === key; }).length;
    var badge = $(".tab__count", tab);
    if (badge) badge.textContent = "(" + toBn(count) + ")";
  });

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

  /* -------------------- অর্ডার তালিকা (কার্ট) -------------------- */
  var STORE_KEY = "jcp_order_v1";
  var cart = [];

  try {
    var saved = JSON.parse(localStorage.getItem(STORE_KEY) || "[]");
    if (Array.isArray(saved)) {
      cart = saved.filter(function (i) { return i && i.name && typeof i.price === "number"; });
    }
  } catch (e) { cart = []; }

  var fab = $("#cart-fab");
  var panel = $("#cart-panel");
  var itemsEl = $("#cart-items");
  var countEl = $("#cart-count");
  var totalEl = $("#cart-total");
  var closeBtn = $("#cart-close");
  var checkoutBtn = $("#cart-checkout");

  function save() {
    try { localStorage.setItem(STORE_KEY, JSON.stringify(cart)); } catch (e) {}
  }
  function cartCount() {
    return cart.reduce(function (n, i) { return n + i.qty; }, 0);
  }
  function cartTotal() {
    return cart.reduce(function (n, i) { return n + i.qty * i.price; }, 0);
  }

  function render() {
    if (!itemsEl) return;
    itemsEl.innerHTML = "";

    if (!cart.length) {
      itemsEl.innerHTML =
        '<li class="cart-empty"><span>🛒</span>তালিকা এখনো ফাঁকা।<br>মেনু থেকে পছন্দের আইটেম যোগ করে নিন।</li>';
    } else {
      cart.forEach(function (item, idx) {
        var li = document.createElement("li");
        li.className = "cart-item";
        li.innerHTML =
          '<span class="cart-item__name">' + item.name +
          "<small>" + money(item.price) + " × " + toBn(item.qty) + " = " + money(item.price * item.qty) + "</small></span>" +
          '<span class="qty">' +
          '<button type="button" data-qty="-1" data-idx="' + idx + '" aria-label="কমান">−</button>' +
          "<span>" + toBn(item.qty) + "</span>" +
          '<button type="button" data-qty="1" data-idx="' + idx + '" aria-label="বাড়ান">+</button>' +
          "</span>" +
          '<button type="button" class="cart-close" data-remove="' + idx + '" aria-label="' + item.name + ' মুছুন">🗑</button>';
        itemsEl.appendChild(li);
      });
    }

    if (countEl) countEl.textContent = toBn(cartCount());
    if (totalEl) totalEl.textContent = money(cartTotal());
    save();
  }

  function addItem(name, price, silent) {
    var found = cart.filter(function (i) { return i.name === name && i.price === price; })[0];
    if (found) { found.qty += 1; } else { cart.push({ name: name, price: price, qty: 1 }); }
    render();
    if (!silent) flashFab();
  }

  function flashFab() {
    if (!fab) return;
    fab.animate(
      [{ transform: "scale(1)" }, { transform: "scale(1.09)" }, { transform: "scale(1)" }],
      { duration: 380, easing: "ease-out" }
    );
  }

  // মেনুর "+ যোগ করুন" বাটন
  $$(".dish").forEach(function (dish) {
    var btn = $("[data-add]", dish);
    if (!btn) return;
    btn.addEventListener("click", function () {
      var name = dish.getAttribute("data-name");
      var price = parseInt(dish.getAttribute("data-price"), 10) || 0;
      addItem(name, price);
      var old = btn.textContent;
      btn.textContent = "✓ যোগ হয়েছে";
      btn.classList.add("is-added");
      setTimeout(function () {
        btn.textContent = old;
        btn.classList.remove("is-added");
      }, 1300);
    });
  });

  // কম্বো অফার বাটন
  $$("[data-combo]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var name = "কম্বো: " + btn.getAttribute("data-combo");
      var amt = parseInt(btn.getAttribute("data-combo-amt"), 10) || 0;
      addItem(name, amt);
      openPanel(true);
    });
  });

  // কার্ট লিস্টে +/- ও ডিলিট (ইভেন্ট ডেলিগেশন)
  if (itemsEl) {
    itemsEl.addEventListener("click", function (e) {
      var t = e.target.closest ? e.target.closest("button") : null;
      if (!t) return;
      if (t.hasAttribute("data-qty")) {
        var i = +t.getAttribute("data-idx");
        var dir = +t.getAttribute("data-qty");
        if (cart[i]) {
          cart[i].qty += dir;
          if (cart[i].qty <= 0) cart.splice(i, 1);
        }
        render();
      } else if (t.hasAttribute("data-remove")) {
        cart.splice(+t.getAttribute("data-remove"), 1);
        render();
      }
    });
  }

  function openPanel(open) {
    if (!panel) return;
    panel.classList.toggle("is-open", open);
    if (fab) fab.setAttribute("aria-expanded", String(open));
  }
  if (fab) {
    fab.addEventListener("click", function () {
      openPanel(!panel.classList.contains("is-open"));
    });
  }
  if (closeBtn) closeBtn.addEventListener("click", function () { openPanel(false); });
  document.addEventListener("click", function (e) {
    if (!panel || !panel.classList.contains("is-open")) return;
    if (panel.contains(e.target) || (fab && fab.contains(e.target))) return;
    // কম্বো বাটনে ক্লিক করে প্যানেল খোলা হয় — সেই একই ক্লিকে আবার বন্ধ হবে না
    if (e.target.closest && e.target.closest("[data-combo]")) return;
    openPanel(false);
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") { openPanel(false); closeNav(); }
  });

  /* -------------------- অর্ডার ফর্ম -------------------- */
  var form = $("#order-form");
  var msgBox = $("#form-msg");
  var orderField = $("#corder");

  function cartToText() {
    if (!cart.length) return "";
    return cart.map(function (i) {
      return toBn(i.qty) + " × " + i.name + " — " + money(i.price * i.qty);
    }).join("\n") + "\nসর্বমোট: " + money(cartTotal());
  }

  // কার্ট → ফর্ম
  if (checkoutBtn) {
    checkoutBtn.addEventListener("click", function () {
      if (orderField) {
        orderField.value = cartToText().split("\nসর্বমোট:")[0];
        var evt = new Event("input", { bubbles: true });
        orderField.dispatchEvent(evt);
      }
      openPanel(false);
      if (form) {
        form.scrollIntoView({ behavior: "smooth", block: "center" });
        setTimeout(function () { var f = $("#cname"); if (f) f.focus({ preventScroll: true }); }, 620);
      }
    });
  }

  function setError(field, on) {
    var wrap = field.closest(".field");
    if (wrap) wrap.classList.toggle("has-error", on);
    return !on;
  }

  function buildMessage(data) {
    var lines = [];
    lines.push("আসসালামু আলাইকুম, জাপানি চা পানি 👋");
    lines.push("আমি অর্ডার করতে চাই।");
    lines.push("");
    lines.push("👤 নাম: " + data.name);
    lines.push("📞 মোবাইল: " + data.phone);
    lines.push("🚚 ধরন: " + data.mode);
    if (data.address) lines.push("📍 ঠিকানা: " + data.address);
    lines.push("");
    lines.push("🧾 অর্ডার তালিকা:");
    if (cart.length) {
      cart.forEach(function (i) {
        lines.push("• " + toBn(i.qty) + " × " + i.name + " = " + money(i.price * i.qty));
      });
      lines.push("সর্বমোট: " + money(cartTotal()));
      if (data.order) lines.push("📝 অতিরিক্ত: " + data.order);
    } else {
      lines.push(data.order);
    }
    if (data.note) { lines.push(""); lines.push("🗒 নির্দেশনা: " + data.note); }
    lines.push("");
    lines.push("অনুগ্রহ করে অর্ডারটি কনফার্ম করুন। ধন্যবাদ!");
    return lines.join("\n");
  }

  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();

      var name = $("#cname");
      var phone = $("#cphone");
      var addr = $("#caddr");
      var note = $("#cnote");
      var modeEl = form.querySelector("input[name='mode']:checked");

      var ok = true;
      ok = setError(name, !name.value.trim()) && ok;
      var phoneClean = phone.value.replace(/[\s\-()]/g, "");
      ok = setError(phone, !/^(?:\+?88)?01[3-9]\d{8}$/.test(phoneClean)) && ok;
      ok = setError(orderField, !orderField.value.trim() && cart.length === 0) && ok;

      if (!ok) {
        if (msgBox) {
          msgBox.className = "form-msg is-bad";
          msgBox.textContent = "⚠️ অনুগ্রহ করে লাল দাগ দেওয়া ঘরগুলো ঠিক করে আবার চেষ্টা করুন।";
        }
        var firstBad = $(".field.has-error input, .field.has-error textarea");
        if (firstBad) firstBad.focus();
        return;
      }

      var data = {
        name: name.value.trim(),
        phone: phoneClean,
        address: addr ? addr.value.trim() : "",
        order: orderField.value.trim(),
        note: note ? note.value.trim() : "",
        mode: modeEl ? modeEl.value : "হোম ডেলিভারি"
      };

      var url = "https://wa.me/" + SHOP.whatsapp + "?text=" + encodeURIComponent(buildMessage(data));
      var win = window.open(url, "_blank", "noopener");

      if (msgBox) {
        msgBox.className = "form-msg is-ok";
        msgBox.innerHTML =
          "✅ ধন্যবাদ " + data.name + "! আপনার অর্ডার মেসেজ তৈরি হয়েছে — হোয়াটসঅ্যাপে <b>Send</b> চাপলেই আমরা পেয়ে যাব।" +
          (win ? "" : ' <a href="' + url + '" target="_blank" rel="noopener">হোয়াটসঅ্যাপ নিজে থেকে না খুললে এখানে ক্লিক করুন</a>');
      }

      // মালিকের সুবিধার জন্য ফর্মের অবস্থাও সেভ থাকবে (আগামী ভিজিটে),
      // তবে কার্ট খালি করা হয় যাতে ভুলে দুবার অর্ডার না যায়।
      try { localStorage.setItem("jcp_last_order", msgBox ? msgBox.textContent : ""); } catch (e2) {}
    });

    // ইনপুট দিলে এরর দাগ সরে যায়
    $$("#order-form input, #order-form textarea").forEach(function (el) {
      el.addEventListener("input", function () {
        var wrap = el.closest(".field");
        if (wrap) wrap.classList.remove("has-error");
      });
    });
  }

  /* -------------------- স্ক্রল রিভিল অ্যানিমেশন -------------------- */
  var reveals = $$(".reveal");
  function revealAll() {
    reveals.forEach(function (el) { el.classList.add("is-in"); });
  }
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
      // সেফটি নেট: ৫ সেকেন্ড পরেও কোনো অংশ লুকানো থাকলে জোর করে দেখানো হবে
      setTimeout(revealAll, 5000);
    } else {
      revealAll();
    }
  }

  /* -------------------- ফুটার বছর -------------------- */
  var yearEl = $("#year");
  if (yearEl) yearEl.textContent = toBn(new Date().getFullYear()) + " খ্রিস্টাব্দ";

  /* -------------------- প্রথম রেন্ডার -------------------- */
  render();
})();
