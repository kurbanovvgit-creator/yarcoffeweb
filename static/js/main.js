/* Yarcoffee — main runtime
   Self-contained, vanilla JS. No frameworks, no CDN. */

(function () {
  "use strict";

  /* ---------- Loader: hide as soon as DOM is ready, never block on slow assets ---------- */
  let loaderHidden = false;
  function hideLoader() {
    if (loaderHidden) return;
    loaderHidden = true;
    const loader = document.querySelector("[data-loader]");
    if (!loader) return;
    requestAnimationFrame(() => loader.classList.add("is-hidden"));
    setTimeout(() => loader && loader.parentNode && loader.parentNode.removeChild(loader), 900);
  }

  setTimeout(hideLoader, 250);
  document.addEventListener("DOMContentLoaded", () => setTimeout(hideLoader, 250));
  window.addEventListener("load", () => setTimeout(hideLoader, 100));
  setTimeout(hideLoader, 3500);

  /* ---------- Sticky nav state on scroll ---------- */
  const nav = document.querySelector("[data-nav]");
  const onScroll = () => {
    if (!nav) return;
    if (window.scrollY > 40) nav.classList.add("is-scrolled");
    else nav.classList.remove("is-scrolled");
  };
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ---------- Mobile menu toggle ---------- */
  const burger = document.querySelector("[data-burger]");
  const mobile = document.querySelector("[data-mobile-menu]");
  const mobileBackdrop = document.querySelector("[data-mobile-backdrop]");

  const setMobileMenu = (open) => {
    if (!mobile || !burger) return;
    mobile.classList.toggle("is-open", open);
    burger.classList.toggle("is-open", open);
    burger.setAttribute("aria-expanded", open ? "true" : "false");
    mobile.setAttribute("aria-hidden", open ? "false" : "true");
    if (nav) nav.classList.toggle("is-menu-open", open);
    document.body.classList.toggle("is-nav-open", open);
    if (mobileBackdrop) {
      mobileBackdrop.classList.toggle("is-open", open);
      mobileBackdrop.hidden = !open;
    }
    document.documentElement.style.overflow = open ? "hidden" : "";
    document.body.style.overflow = open ? "hidden" : "";
    if (burger.dataset.labelOpen) {
      burger.setAttribute(
        "aria-label",
        open ? burger.dataset.labelClose || "Close menu" : burger.dataset.labelOpen
      );
    }
  };

  if (burger && mobile) {
    burger.dataset.labelOpen = burger.getAttribute("aria-label") || "Menu";
    burger.addEventListener("click", (e) => {
      e.stopPropagation();
      setMobileMenu(!mobile.classList.contains("is-open"));
    });
    if (mobileBackdrop) mobileBackdrop.addEventListener("click", () => setMobileMenu(false));
    mobile.querySelectorAll("a").forEach((a) => a.addEventListener("click", () => setMobileMenu(false)));
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && mobile.classList.contains("is-open")) setMobileMenu(false);
    });
    window.addEventListener("resize", () => {
      if (window.innerWidth > 900 && mobile.classList.contains("is-open")) setMobileMenu(false);
    });
  }

  /* ---------- Reveal on scroll (IntersectionObserver) ---------- */
  const reveals = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && reveals.length) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.15, rootMargin: "0px 0px -50px 0px" }
    );
    reveals.forEach((el) => io.observe(el));
  } else {
    reveals.forEach((el) => el.classList.add("is-visible"));
  }

  /* ---------- Letter-by-letter animation for [data-split] elements ---- */
  document.querySelectorAll("[data-split]").forEach((el) => {
    const text = el.textContent.trim();
    el.classList.add("split-letters");
    el.textContent = "";
    [...text].forEach((ch, i) => {
      const span = document.createElement("span");
      span.className = "char";
      span.style.animationDelay = `${i * 30 + 200}ms`;
      span.textContent = ch === " " ? "\u00A0" : ch;
      el.appendChild(span);
    });
  });

  /* ---------- Smooth in-page scrolling ---------- */
  document.querySelectorAll('a[href^="#"]').forEach((link) => {
    link.addEventListener("click", (e) => {
      const id = link.getAttribute("href");
      if (id.length > 1) {
        const target = document.querySelector(id);
        if (target) {
          e.preventDefault();
          target.scrollIntoView({ behavior: "smooth", block: "start" });
        }
      }
    });
  });

  /* ---------- Lightbox for gallery tiles ---------- */
  const lb = document.querySelector("[data-lightbox]");
  if (lb) {
    const lbImg = lb.querySelector("img");
    const tiles = [...document.querySelectorAll("[data-lightbox-trigger]")];
    let idx = 0;

    const open = (i) => {
      idx = i;
      lbImg.src = tiles[i].dataset.src || tiles[i].querySelector("img").src;
      lb.classList.add("is-open");
      document.body.style.overflow = "hidden";
    };
    const close = () => {
      lb.classList.remove("is-open");
      document.body.style.overflow = "";
    };
    const next = () => open((idx + 1) % tiles.length);
    const prev = () => open((idx - 1 + tiles.length) % tiles.length);

    tiles.forEach((tile, i) => tile.addEventListener("click", () => open(i)));
    lb.querySelector("[data-lb-close]").addEventListener("click", close);
    lb.querySelector("[data-lb-next]").addEventListener("click", next);
    lb.querySelector("[data-lb-prev]").addEventListener("click", prev);
    lb.addEventListener("click", (e) => {
      if (e.target === lb) close();
    });
    document.addEventListener("keydown", (e) => {
      if (!lb.classList.contains("is-open")) return;
      if (e.key === "Escape") close();
      if (e.key === "ArrowRight") next();
      if (e.key === "ArrowLeft") prev();
    });
  }

  /* ---------- Menu category filter (anchor scroll) ---------- */
  document.querySelectorAll("[data-menu-tab]").forEach((tab) => {
    tab.addEventListener("click", (e) => {
      e.preventDefault();
      const slug = tab.dataset.menuTab;
      document.querySelectorAll("[data-menu-tab]").forEach((t) => t.classList.remove("is-active"));
      tab.classList.add("is-active");
      const target = document.getElementById("cat-" + slug);
      if (target) {
        const y = target.getBoundingClientRect().top + window.scrollY - 120;
        window.scrollTo({ top: y, behavior: "smooth" });
      }
    });
  });
})();
