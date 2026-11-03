'use strict';

const navigation = document.querySelector('.navigation');
const toggle = document.querySelector('.menu-toggle');
const mobile = window.matchMedia('(max-width: 1100px)');

function setMenu(open, restoreFocus = false) {
  navigation.classList.toggle('is-open', open);
  toggle.setAttribute('aria-expanded', String(open));
  toggle.querySelector('.menu-label').textContent = open ? 'Fermer' : 'Menu';
  if (mobile.matches) navigation.inert = !open;
  else navigation.inert = false;
  document.body.classList.toggle('menu-open', open && mobile.matches);
  if (restoreFocus) toggle.focus();
}

if (navigation && toggle) {
  // Progressive enhancement: all navigation links remain available without JS.
  document.documentElement.classList.add('has-menu');
  setMenu(false);
  toggle.addEventListener('click', () => setMenu(toggle.getAttribute('aria-expanded') !== 'true'));
  navigation.addEventListener('click', event => {
    if (event.target.closest('a')) setMenu(false);
  });
  document.addEventListener('keydown', event => {
    if (toggle.getAttribute('aria-expanded') !== 'true' || !mobile.matches) return;
    if (event.key === 'Escape') setMenu(false, true);
    if (event.key === 'Tab') {
      const links = [...navigation.querySelectorAll('a')];
      const last = links[links.length - 1];
      if (event.shiftKey && document.activeElement === toggle) {
        event.preventDefault(); last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault(); toggle.focus();
      }
    }
  });
  mobile.addEventListener('change', () => setMenu(false));
}

const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
const search = document.querySelector('#project-query');
if (search) {
  const rows = [...document.querySelectorAll('[data-project]')];
  const normalize = value => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLocaleLowerCase('fr').replace(/[^a-z0-9]+/g, ' ').trim();
  const index = rows.map(row => normalize(row.textContent));
  const updateSearch = () => {
    const words = normalize(search.value).split(' ').filter(Boolean);
    let visible = 0;
    rows.forEach((row, i) => {
      row.hidden = !words.every(word => index[i].includes(word));
      if (!row.hidden) visible++;
    });
    document.querySelector('#project-count').textContent = `${visible} référence${visible > 1 ? 's' : ''} sur ${rows.length}`;
    document.querySelector('#project-empty').hidden = visible !== 0;
  };
  document.querySelector('.project-search').hidden = false;
  search.addEventListener('input', updateSearch);
  updateSearch();
}

if ('IntersectionObserver' in window && !reducedMotion.matches) {
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      }
    });
  }, {threshold: 0.08});
  document.querySelectorAll('[data-reveal]').forEach(element => {
    element.classList.add('will-reveal');
    observer.observe(element);
  });
  // A keyboard user must never focus invisible content.
  document.addEventListener('focusin', event => {
    event.target.closest('.will-reveal')?.classList.add('is-visible');
  });
  reducedMotion.addEventListener('change', event => {
    if (event.matches) {
      observer.disconnect();
      document.querySelectorAll('.will-reveal').forEach(el => el.classList.add('is-visible'));
    }
  });
}
