/* ============================================================
   RESUMO — script.js
   Features: Lucide icons, navbar scroll, mobile menu,
             smooth scroll, dark/light theme, i18n (EN / PL)
   ============================================================ */

/* ============================================================
   TRANSLATIONS
   All UI strings in English and Polish.
   Keys match data-i18n attributes in index.html.
   ============================================================ */
const translations = {
  en: {
    /* ── Navbar ── */
    nav_how:       'How it works',
    nav_features:  'Features',
    nav_templates: 'Templates',
    nav_login:     'Log in',
    nav_signup:    'Sign up',

    /* ── Hero ── */
    hero_badge:         '100% free — no credit card needed',
    hero_title_line1:   'Your CV, done right.',
    hero_title_line2:   'In minutes.',
    hero_sub:           'Resumo helps you build a clean, professional CV that stands out — no design skills required, no hidden fees, ever.',
    hero_cta:           "Create your CV — it's free",
    hero_cta_secondary: 'See how it works',
    hero_social_proof:  'Trusted by <strong>12,000+</strong> job seekers worldwide',

    /* ── How it works ── */
    how_title:   'How it works',
    how_sub:     'Three steps from blank page to polished CV.',
    step1_title: 'Pick a template',
    step1_desc:  'Choose from clean, recruiter-tested layouts designed for readability.',
    step2_title: 'Fill in your details',
    step2_desc:  'Type directly into guided fields — experience, skills, education, and more.',
    step3_title: 'Download as PDF',
    step3_desc:  'Export a pixel-perfect PDF, ready to send to employers.',

    /* ── Features ── */
    features_title: 'What Resumo does',
    features_sub:   'Straightforward tools that actually help you get hired.',
    feat1_title:    'Live preview',
    feat1_desc:     "See your CV update in real time as you type — no guessing how it'll look.",
    feat2_title:    'Multiple templates',
    feat2_desc:     'Switch between layouts instantly without losing your content.',
    feat3_title:    'PDF export',
    feat3_desc:     'One-click export to a clean, ATS-friendly PDF document.',
    feat4_title:    'Auto-save',
    feat4_desc:     'Your progress is saved automatically — pick up where you left off.',
    feat5_title:    'Works on any device',
    feat5_desc:     'Edit your CV on desktop, tablet, or phone — fully responsive.',
    feat6_title:    'Private by default',
    feat6_desc:     "Your data stays yours. We don't sell or share your information.",

    /* ── Templates ── */
    tpl_title:  'Ready-made templates',
    tpl_sub:    'Designed to impress — just add your details.',
    tpl1_name:  'Classic',
    tpl1_tag:   'Clean & timeless',
    tpl2_name:  'Modern',
    tpl2_tag:   'Bold & structured',
    tpl3_name:  'Minimal',
    tpl3_tag:   'Simple & elegant',
    tpl_cta:    'Start with any template — free',

    /* ── CTA Banner ── */
    banner_title: 'Ready to build your CV?',
    banner_sub:   'No account needed to start. Sign up only when you want to save.',
    banner_cta:   'Get started now',

    /* ── Footer ── */
    footer_tagline: 'Free CV builder for everyone.',
    footer_privacy: 'Privacy',
    footer_terms:   'Terms',
    footer_copy:    '© 2026 Resumo. All rights reserved.',
  },

  pl: {
    /* ── Navbar ── */
    nav_how:       'Jak to działa',
    nav_features:  'Funkcje',
    nav_templates: 'Szablony',
    nav_login:     'Zaloguj się',
    nav_signup:    'Zarejestruj się',

    /* ── Hero ── */
    hero_badge:         '100% bezpłatnie — bez karty kredytowej',
    hero_title_line1:   'Twoje CV, zrobione dobrze.',
    hero_title_line2:   'W kilka minut.',
    hero_sub:           'Resumo pomaga Ci stworzyć przejrzyste, profesjonalne CV — bez umiejętności projektowania, bez ukrytych opłat.',
    hero_cta:           'Stwórz swoje CV — to darmowe',
    hero_cta_secondary: 'Zobacz jak to działa',
    hero_social_proof:  'Zaufało nam <strong>12 000+</strong> osób szukających pracy',

    /* ── How it works ── */
    how_title:   'Jak to działa',
    how_sub:     'Trzy kroki od pustej strony do gotowego CV.',
    step1_title: 'Wybierz szablon',
    step1_desc:  'Wybieraj spośród przejrzystych układów zaprojektowanych z myślą o rekruterach.',
    step2_title: 'Uzupełnij swoje dane',
    step2_desc:  'Wpisuj dane bezpośrednio w przygotowane pola — doświadczenie, umiejętności, wykształcenie i więcej.',
    step3_title: 'Pobierz jako PDF',
    step3_desc:  'Eksportuj idealnie dopasowany PDF, gotowy do wysłania do pracodawcy.',

    /* ── Features ── */
    features_title: 'Co robi Resumo',
    features_sub:   'Proste narzędzia, które naprawdę pomagają znaleźć pracę.',
    feat1_title:    'Podgląd na żywo',
    feat1_desc:     'Obserwuj, jak Twoje CV zmienia się w czasie rzeczywistym podczas pisania.',
    feat2_title:    'Wiele szablonów',
    feat2_desc:     'Przełączaj się między układami natychmiast, nie tracąc treści.',
    feat3_title:    'Eksport do PDF',
    feat3_desc:     'Eksport jednym kliknięciem do czystego, przyjaznego dla ATS dokumentu PDF.',
    feat4_title:    'Automatyczny zapis',
    feat4_desc:     'Twoje postępy są zapisywane automatycznie — wróć tam, gdzie skończyłeś.',
    feat5_title:    'Działa na każdym urządzeniu',
    feat5_desc:     'Edytuj CV na komputerze, tablecie lub telefonie — w pełni responsywne.',
    feat6_title:    'Prywatność domyślnie',
    feat6_desc:     'Twoje dane należą do Ciebie. Nie sprzedajemy ani nie udostępniamy ich.',

    /* ── Templates ── */
    tpl_title:  'Gotowe szablony',
    tpl_sub:    'Zaprojektowane, by zrobić wrażenie — wystarczy dodać swoje dane.',
    tpl1_name:  'Klasyczny',
    tpl1_tag:   'Czysty i ponadczasowy',
    tpl2_name:  'Nowoczesny',
    tpl2_tag:   'Wyrazisty i przejrzysty',
    tpl3_name:  'Minimalistyczny',
    tpl3_tag:   'Prosty i elegancki',
    tpl_cta:    'Zacznij od dowolnego szablonu — za darmo',

    /* ── CTA Banner ── */
    banner_title: 'Gotowy na stworzenie CV?',
    banner_sub:   'Nie potrzebujesz konta, żeby zacząć. Zarejestruj się tylko, gdy chcesz zapisać.',
    banner_cta:   'Zacznij teraz',

    /* ── Footer ── */
    footer_tagline: 'Darmowy kreator CV dla każdego.',
    footer_privacy: 'Prywatność',
    footer_terms:   'Regulamin',
    footer_copy:    '© 2026 Resumo. Wszelkie prawa zastrzeżone.',
  },
};

/* ============================================================
   BOOT — runs immediately (before DOMContentLoaded)
   Applies theme & language class to <html> before first paint
   to prevent any flash of wrong theme or language.
   ============================================================ */
(function boot() {
  /* ── Theme ── */
  const savedTheme  = localStorage.getItem('theme');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const isDark      = savedTheme === 'dark' || (!savedTheme && prefersDark);
  if (isDark) document.documentElement.classList.add('dark');

  /* ── Language ── */
  const savedLang = localStorage.getItem('lang') || 'en';
  document.documentElement.setAttribute('lang', savedLang);

  // Expose to DOMContentLoaded scope
  window.__initialLang = savedLang;
})();

/* ============================================================
   DOM READY — wire up all features once HTML is parsed
   ============================================================ */
document.addEventListener('DOMContentLoaded', () => {

  // 1. Render Lucide icons first — must happen before anything
  //    else reads icon elements (theme toggle visibility etc.)
  initLucide();

  // 2. Apply saved language to all [data-i18n] elements
  applyLanguage(window.__initialLang);

  // 3. Mark the correct lang button as active
  syncLangButtons(window.__initialLang);

  // 4. Wire up remaining features
  initNavbarScroll();
  initMobileMenu();
  initSmoothScroll();
  initThemeToggle();
  initLangSwitcher();
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
   THEME TOGGLE — dark / light
   Reads preference from localStorage on boot (handled above).
   On click: toggles html.dark, persists to localStorage,
   re-renders Lucide icons (sun/moon swap is CSS-driven,
   but createIcons ensures SVGs are always fresh).
   ============================================================ */
function initThemeToggle() {
  const btn = document.getElementById('theme-toggle');
  if (!btn) return;

  btn.addEventListener('click', () => {
    const html    = document.documentElement;
    const isDark  = html.classList.toggle('dark');

    // Persist preference
    localStorage.setItem('theme', isDark ? 'dark' : 'light');

    // Update aria-label for screen readers
    btn.setAttribute(
      'aria-label',
      isDark ? 'Switch to light mode' : 'Switch to dark mode'
    );

    // Re-render icons — CSS handles sun/moon visibility,
    // but a fresh createIcons() keeps SVGs clean after DOM changes
    if (typeof lucide !== 'undefined') lucide.createIcons();
  });

  // Set correct initial aria-label
  const isDarkNow = document.documentElement.classList.contains('dark');
  btn.setAttribute(
    'aria-label',
    isDarkNow ? 'Switch to light mode' : 'Switch to dark mode'
  );
}

/* ============================================================
   LANGUAGE SWITCHER — EN / PL
   On click: applies translations, updates active button state,
   persists choice to localStorage, updates <html lang="">.
   ============================================================ */
function initLangSwitcher() {
  const langBtns = document.querySelectorAll('.lang-btn');
  if (!langBtns.length) return;

  langBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const lang = btn.getAttribute('data-lang');
      if (!lang || !translations[lang]) return;

      // Apply translations to DOM
      applyLanguage(lang);

      // Update active button styling
      syncLangButtons(lang);

      // Persist & update html[lang] attribute
      localStorage.setItem('lang', lang);
      document.documentElement.setAttribute('lang', lang);
    });
  });
}

/* ============================================================
   APPLY LANGUAGE
   Loops through every [data-i18n] element and sets its
   innerHTML from the translations object.
   Uses innerHTML (not textContent) to support <strong> tags
   in strings like hero_social_proof.
   ============================================================ */
function applyLanguage(lang) {
  const dict = translations[lang];
  if (!dict) return;

  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (key && dict[key] !== undefined) {
      // Use innerHTML to allow inline HTML (e.g. <strong>)
      el.innerHTML = dict[key];
    }
  });
}

/* ============================================================
   SYNC LANG BUTTONS
   Adds .active to the button matching the current language,
   removes it from all others.
   ============================================================ */
function syncLangButtons(activeLang) {
  document.querySelectorAll('.lang-btn').forEach(btn => {
    const isActive = btn.getAttribute('data-lang') === activeLang;
    btn.classList.toggle('active', isActive);
    // Communicate state to screen readers
    btn.setAttribute('aria-pressed', String(isActive));
  });
}
