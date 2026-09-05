// Progressive enhancement: all content and links also work without JavaScript.
document.documentElement.classList.add('js');

const menuButton = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#site-nav');
function closeMenu() {
  navigation.classList.remove('is-open');
  menuButton.setAttribute('aria-expanded', 'false');
  menuButton.setAttribute('aria-label', 'Open navigation');
}
menuButton?.addEventListener('click', () => {
  const open = menuButton.getAttribute('aria-expanded') !== 'true';
  menuButton.setAttribute('aria-expanded', String(open));
  menuButton.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
  navigation.classList.toggle('is-open', open);
});
navigation?.addEventListener('click', event => {
  if (event.target.closest('a')) closeMenu();
});
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && menuButton?.getAttribute('aria-expanded') === 'true') {
    closeMenu();
    menuButton.focus();
  }
});
document.addEventListener('click', event => {
  if (!event.target.closest('.site-header') && navigation?.classList.contains('is-open')) closeMenu();
});
const desktop = matchMedia('(min-width: 901px)');
desktop.addEventListener('change', () => { if (desktop.matches) closeMenu(); });

document.querySelectorAll('[data-filter-scope]').forEach(scope => {
  const input = scope.querySelector('[data-search]');
  const buttons = [...scope.querySelectorAll('[data-filter]')];
  const items = [...scope.querySelectorAll('[data-filter-item]')];
  const searchable = items.map(item => item.textContent.toLocaleLowerCase().replace(/\s+/g, ' '));
  let category = 'all';
  function filter() {
    const terms = input.value.toLocaleLowerCase().trim().split(/\s+/).filter(Boolean);
    let count = 0;
    items.forEach((item, i) => {
      const matches = (category === 'all' || item.dataset.category === category) && terms.every(term => searchable[i].includes(term));
      item.hidden = !matches;
      if (matches) count++;
    });
    buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.filter === category)));
    scope.querySelectorAll('[data-result-group]').forEach(group => {
      group.hidden = ![...group.querySelectorAll('[data-filter-item]')].some(item => !item.hidden);
    });
    scope.querySelector('[data-empty]').hidden = count > 0;
    scope.querySelector('[data-result-count]').textContent = `${count} ${count === 1 ? 'result' : 'results'} found.`;
  }
  buttons.forEach(button => button.addEventListener('click', () => {
    category = button.dataset.filter;
    filter();
  }));
  input.addEventListener('input', filter);
  scope.querySelector('[data-reset]').addEventListener('click', () => {
    category = 'all';
    input.value = '';
    filter();
    input.focus();
  });
  function revealHash() {
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)); } catch { return; }
    if (!id) return;
    const target = document.getElementById(id);
    if (!target || !scope.contains(target)) return;
    category = 'all';
    input.value = '';
    filter();
    const details = target.querySelector('.profile-details');
    if (details) details.open = true;
    requestAnimationFrame(() => target.scrollIntoView({ block: 'start' }));
  }
  filter();
  revealHash();
  window.addEventListener('hashchange', revealHash);
});

const gallery = document.querySelector('.gallery-dialog');
if (gallery && typeof gallery.showModal === 'function') {
  const photos = [...document.querySelectorAll('[data-gallery-image]')];
  let current = 0;
  let opener;
  function renderPhoto() {
    const source = photos[current];
    const image = gallery.querySelector('figure img');
    const thumbnail = source.querySelector('img');
    image.src = source.getAttribute('href');
    image.alt = source.dataset.caption;
    image.width = Number(thumbnail.getAttribute('width'));
    image.height = Number(thumbnail.getAttribute('height'));
    gallery.querySelector('figcaption').textContent = source.dataset.caption;
    gallery.querySelector('[data-gallery-count]').textContent = `${current + 1} / ${photos.length}`;
  }
  function step(direction) {
    current = (current + direction + photos.length) % photos.length;
    renderPhoto();
  }
  photos.forEach((photo, index) => photo.addEventListener('click', event => {
    if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    current = index;
    opener = photo;
    renderPhoto();
    gallery.showModal();
    document.body.classList.add('dialog-open');
  }));
  gallery.querySelector('.dialog-close').addEventListener('click', () => gallery.close());
  gallery.querySelector('[data-gallery-prev]').addEventListener('click', () => step(-1));
  gallery.querySelector('[data-gallery-next]').addEventListener('click', () => step(1));
  gallery.addEventListener('keydown', event => {
    if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
      event.preventDefault();
      step(event.key === 'ArrowLeft' ? -1 : 1);
    }
  });
  gallery.addEventListener('click', event => {
    if (event.target !== gallery) return;
    const rect = gallery.getBoundingClientRect();
    if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) gallery.close();
  });
  gallery.addEventListener('close', () => {
    document.body.classList.remove('dialog-open');
    opener?.focus();
  });
}

document.querySelectorAll('[data-year]').forEach(node => { node.textContent = new Date().getFullYear(); });
