/* ============================================================
   RESUMO — script.js
   Vanilla JS only. No jQuery. No frameworks.
   ============================================================ */

/* === LUCIDE ICONS INIT === */
// Must run after DOM is ready; Lucide replaces data-lucide attributes
document.addEventListener('DOMContentLoaded', () => {
  if (typeof lucide !== 'undefined') {
    lucide.createIcons();
  }

  initNavbar();
  initMobileMenu();
  initSmoothScroll();
});

/* ============================================================
   NAVBAR — Scroll shadow
   Adds .scrolled class to navbar when page is scrolled
   ============================================================ */
function initNavbar() {
  const navbar = document.querySelector('.navbar');
  if (!navbar) return;

  const onScroll = () => {
    if (window.scrollY > 10) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
  };

  // Throttle scroll handler for performance
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

  // Run once on load in case page is already scrolled
  onScroll();
}

/* ============================================================
   MOBILE MENU — Toggle open/close
   Toggles .is-open on the mobile menu panel
   Updates aria-expanded and aria-hidden for accessibility
   ============================================================ */
function initMobileMenu() {
  const hamburger  = document.getElementById('hamburger-btn');
  const mobileMenu = document.getElementById('mobile-menu');
  const mobileLinks = document.querySelectorAll('.mobile-link, .mobile-menu .btn');

  if (!hamburger || !mobileMenu) return;

  // Toggle menu open/close
  hamburger.addEventListener('click', () => {
    const isOpen = mobileMenu.classList.toggle('is-open');
    hamburger.setAttribute('aria-expanded', String(isOpen));
    mobileMenu.setAttribute('aria-hidden', String(!isOpen));

    // Swap hamburger icon: menu ↔ x
    const icon = hamburger.querySelector('[data-lucide]');
    if (icon) {
      icon.setAttribute('data-lucide', isOpen ? 'x' : 'menu');
      lucide.createIcons(); // re-render updated icon
    }
  });

  // Close menu when a link inside it is clicked
  mobileLinks.forEach(link => {
    link.addEventListener('click', () => {
      closeMobileMenu(hamburger, mobileMenu);
    });
  });

  // Close menu on outside click
  document.addEventListener('click', (e) => {
    const navbar = document.querySelector('.navbar');
    if (navbar && !navbar.contains(e.target)) {
      closeMobileMenu(hamburger, mobileMenu);
    }
  });

  // Close menu on Escape key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      closeMobileMenu(hamburger, mobileMenu);
      hamburger.focus(); // return focus to trigger
    }
  });
}

function closeMobileMenu(hamburger, mobileMenu) {
  if (!mobileMenu.classList.contains('is-open')) return;

  mobileMenu.classList.remove('is-open');
  hamburger.setAttribute('aria-expanded', 'false');
  mobileMenu.setAttribute('aria-hidden', 'true');

  const icon = hamburger.querySelector('[data-lucide]');
  if (icon) {
    icon.setAttribute('data-lucide', 'menu');
    lucide.createIcons();
  }
}

/* ============================================================
   SMOOTH SCROLL — Anchor links
   Handles all <a href="#..."> clicks with offset for fixed navbar
   ============================================================ */
function initSmoothScroll() {
  const NAVBAR_HEIGHT = parseInt(
    getComputedStyle(document.documentElement)
      .getPropertyValue('--navbar-height') || '64',
    10
  );

  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', (e) => {
      const targetId = anchor.getAttribute('href');
      if (!targetId || targetId === '#') return;

      const target = document.querySelector(targetId);
      if (!target) return;

      e.preventDefault();

      const targetTop = target.getBoundingClientRect().top
                      + window.scrollY
                      - NAVBAR_HEIGHT
                      - 16; // extra breathing room

      window.scrollTo({
        top: targetTop,
        behavior: 'smooth',
      });

      // Update URL hash without jumping
      history.pushState(null, '', targetId);
    });
  });
}
