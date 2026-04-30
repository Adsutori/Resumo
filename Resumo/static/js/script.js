/* ============================================================
   RESUMO — script.js
   Features: Lucide icons, navbar scroll, mobile menu,
             smooth scroll, dark/light theme, i18n (EN / PL)
   ============================================================ */

/* ============================================================
   DOM READY — wire up all features once HTML is parsed
   ============================================================ */
document.addEventListener('DOMContentLoaded', () => {
  initLucide();
  initNavbarScroll();
  initMobileMenu();
  initSmoothScroll();
  initScrollReveal();
  initStatsCounter();
});

/* ============================================================
   LUCIDE ICONS
   Call createIcons() to replace all data-lucide attributes
   with inline SVGs. Re-call after any DOM mutation that adds
   new data-lucide elements (e.g. hamburger icon swap).
   ============================================================ */
function initLucide() {
  if (typeof lucide !== 'undefined') {
    lucide.createIcons();
  } else {
    // Lucide CDN not yet loaded — retry once after short delay
    setTimeout(() => {
      if (typeof lucide !== 'undefined') lucide.createIcons();
    }, 300);
  }
}

/* ============================================================
   NAVBAR — scroll shadow
   Adds .scrolled class when page is scrolled > 10px,
   triggering the box-shadow defined in CSS.
   ============================================================ */
function initNavbarScroll() {
  const navbar = document.querySelector('.navbar');
  if (!navbar) return;

  function onScroll() {
    navbar.classList.toggle('scrolled', window.scrollY > 10);
  }

  // Throttle via requestAnimationFrame for smooth performance
  let ticking = false;
  window.addEventListener('scroll', () => {
    if (!ticking) {
      requestAnimationFrame(() => {
        onScroll();
        ticking = false;
      });
      ticking = true;
    }
  }, { passive: true });

  // Run once on load (page may already be scrolled on refresh)
  onScroll();
}

/* ============================================================
   MOBILE MENU — open / close
   Toggles .is-open on #mobile-menu panel.
   Keeps aria-expanded / aria-hidden in sync.
   Swaps hamburger icon between menu ↔ x.
   ============================================================ */
function initMobileMenu() {
  const hamburger  = document.getElementById('hamburger-btn');
  const mobileMenu = document.getElementById('mobile-menu');
  if (!hamburger || !mobileMenu) return;

  // All tappable items inside the mobile menu
  const mobileLinks = mobileMenu.querySelectorAll('.mobile-link, .btn');

  /* ── Toggle on hamburger click ── */
  hamburger.addEventListener('click', (e) => {
    e.stopPropagation(); // prevent immediate outside-click close
    const isOpen = mobileMenu.classList.toggle('is-open');
    setMenuState(isOpen);
  });

  /* ── Close when a menu item is clicked ── */
  mobileLinks.forEach(link => {
    link.addEventListener('click', () => closeMenu());
  });

  /* ── Close on outside click ── */
  document.addEventListener('click', (e) => {
    const navbar = document.querySelector('.navbar');
    if (navbar && !navbar.contains(e.target)) closeMenu();
  });

  /* ── Close on Escape key ── */
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      closeMenu();
      hamburger.focus(); // return focus to trigger for a11y
    }
  });

  /* ── Helpers ── */
  function closeMenu() {
    if (!mobileMenu.classList.contains('is-open')) return;
    mobileMenu.classList.remove('is-open');
    setMenuState(false);
  }

  function setMenuState(isOpen) {
    hamburger.setAttribute('aria-expanded', String(isOpen));
    mobileMenu.setAttribute('aria-hidden',  String(!isOpen));
    swapHamburgerIcon(isOpen);
  }

  function swapHamburgerIcon(isOpen) {
    const icon = hamburger.querySelector('[data-lucide]');
    if (!icon) return;
    icon.setAttribute('data-lucide', isOpen ? 'x' : 'menu');
    if (typeof lucide !== 'undefined') lucide.createIcons();
  }
}

/* ============================================================
   SMOOTH SCROLL
   Intercepts all <a href="#..."> clicks, scrolls to target
   with an offset equal to the fixed navbar height + breathing room.
   Also updates the URL hash cleanly via history.pushState.
   ============================================================ */
function initSmoothScroll() {
  // Read navbar height from CSS custom property (stays in sync with CSS)
  const navbarHeight = parseInt(
    getComputedStyle(document.documentElement)
      .getPropertyValue('--navbar-height') || '64',
    10
  );
  const OFFSET = navbarHeight + 16; // 16px extra breathing room

  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', (e) => {
      const targetId = anchor.getAttribute('href');
      if (!targetId || targetId === '#') return;

      const target = document.querySelector(targetId);
      if (!target) return;

      e.preventDefault();

      const targetTop = target.getBoundingClientRect().top
                      + window.scrollY
                      - OFFSET;

      window.scrollTo({ top: targetTop, behavior: 'smooth' });

      // Update URL without triggering a jump
      history.pushState(null, '', targetId);
    });
  });
}

/* ============================================================
   AUTH PAGES — password toggle + strength meter
   Runs only if relevant elements exist on the page
   ============================================================ */

// ── Show / hide password ──
document.querySelectorAll('.form-input__toggle-pw').forEach(btn => {
  btn.addEventListener('click', () => {
    const targetId = btn.getAttribute('data-target');
    const input    = document.getElementById(targetId);
    if (!input) return;

    const isHidden = input.type === 'password';
    input.type     = isHidden ? 'text' : 'password';

    // Swap eye icon
    const icon = btn.querySelector('[data-lucide]');
    if (icon) {
      icon.setAttribute('data-lucide', isHidden ? 'eye-off' : 'eye');
      if (typeof lucide !== 'undefined') lucide.createIcons();
    }
  });
});

// ── Password strength meter (register page only) ──
const pw1Input     = document.getElementById('id_password1');
const strengthFill = document.getElementById('strength-fill');
const strengthLbl  = document.getElementById('strength-label');

if (pw1Input && strengthFill && strengthLbl) {
  pw1Input.addEventListener('input', () => {
    const val   = pw1Input.value;
    const score = getPasswordScore(val);

    const levels = [
      { label: '',         color: 'transparent', width: '0%'   },
      { label: 'Słabe',    color: '#ef4444',      width: '25%'  },
      { label: 'Średnie',  color: '#f59e0b',      width: '50%'  },
      { label: 'Dobre',    color: '#3b82f6',      width: '75%'  },
      { label: 'Silne',    color: '#22c55e',      width: '100%' },
    ];

    const level = levels[score];
    strengthFill.style.width           = level.width;
    strengthFill.style.backgroundColor = level.color;
    strengthLbl.textContent            = level.label;
    strengthLbl.style.color            = level.color;
  });
}

function getPasswordScore(pw) {
  if (!pw) return 0;
  let score = 0;
  if (pw.length >= 8)               score++;
  if (/[A-Z]/.test(pw))             score++;
  if (/[0-9]/.test(pw))             score++;
  if (/[^A-Za-z0-9]/.test(pw))      score++;
  return score;
}

/* ============================================================
   LANDING PAGE — Scroll Reveal + Stats Counter
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {
  initScrollReveal();
  initStatsCounter();
});

/* ── Scroll Reveal ── */
function initScrollReveal() {
  const elements = document.querySelectorAll('.reveal');
  if (!elements.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.12,
    rootMargin: '0px 0px -40px 0px'
  });

  elements.forEach(el => observer.observe(el));
}

/* ── Stats Counter ── */
function initStatsCounter() {
  const nums = document.querySelectorAll('.hero__stat-num[data-count]');
  if (!nums.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      const el     = entry.target;
      const target = parseInt(el.dataset.count, 10);
      const dur    = 1800;
      const start  = performance.now();

      function tick(now) {
        const elapsed  = now - start;
        const progress = Math.min(elapsed / dur, 1);
        // easeOutExpo
        const ease = progress === 1 ? 1 : 1 - Math.pow(2, -10 * progress);
        el.textContent = Math.floor(ease * target).toLocaleString();
        if (progress < 1) requestAnimationFrame(tick);
      }

      requestAnimationFrame(tick);
      observer.unobserve(el);
    });
  }, { threshold: 0.5 });

  nums.forEach(el => observer.observe(el));
}
