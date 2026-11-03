'use strict';

const panel = document.querySelector('.menu-panel');
const toggle = document.querySelector('.menu-toggle');
const close = document.querySelector('.menu-close');
const backdrop = document.querySelector('.menu-backdrop');
const main = document.querySelector('main');
const footer = document.querySelector('.site-footer');
const brand = document.querySelector('.site-header .brand');
let open = false;

if (panel && toggle && close && backdrop) {
  document.documentElement.classList.add('menu-ready');
  panel.inert = true;
  function setMenu(value) {
    open = value;
    panel.inert = !value;
    backdrop.hidden = !value;
    toggle.setAttribute('aria-expanded', String(value));
    toggle.setAttribute('aria-label', value ? 'Fermer le menu' : 'Ouvrir le menu');
    document.body.classList.toggle('menu-open', value);
    main.inert = value;
    footer.inert = value;
    brand.inert = value;
    toggle.inert = value;
    if (value) {
      panel.setAttribute('role', 'dialog');
      panel.setAttribute('aria-modal', 'true');
      close.focus({ preventScroll: true });
    } else {
      panel.removeAttribute('role');
      panel.removeAttribute('aria-modal');
      toggle.focus({ preventScroll: true });
    }
  }
  toggle.addEventListener('click', () => setMenu(!open));
  close.addEventListener('click', () => setMenu(false));
  backdrop.addEventListener('click', () => setMenu(false));
  panel.addEventListener('click', event => {
    if (event.target.closest('a')) setMenu(false);
  });
  document.addEventListener('keydown', event => {
    if (!open) return;
    if (event.key === 'Escape') setMenu(false);
    if (event.key === 'Tab') {
      const items = [...panel.querySelectorAll('a, button')];
      const first = items[0];
      const last = items[items.length - 1];
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault(); last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault(); first.focus();
      }
    }
  });
}

const carousel = document.querySelector('.carousel');
if (carousel) {
  const slides = [...carousel.querySelectorAll('.carousel-slide')];
  const controls = carousel.querySelector('.carousel-controls');
  const counter = carousel.querySelector('.slide-counter');
  let active = 0;
  const update = () => {
    slides.forEach((slide, index) => { slide.hidden = index !== active; });
    counter.textContent = `${String(active + 1).padStart(2, '0')} / ${String(slides.length).padStart(2, '0')}`;
  };
  const move = delta => {
    active = (active + delta + slides.length) % slides.length;
    update();
  };
  controls.hidden = slides.length < 2;
  carousel.querySelector('.slide-prev').addEventListener('click', () => move(-1));
  carousel.querySelector('.slide-next').addEventListener('click', () => move(1));
  carousel.addEventListener('keydown', event => {
    if (event.key === 'ArrowLeft') { event.preventDefault(); move(-1); }
    if (event.key === 'ArrowRight') { event.preventDefault(); move(1); }
  });
  // Manual navigation only: no autoplay, gesture hijacking or motion dependency.
  update();
}
