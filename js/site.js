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

const siteSearch = document.querySelector('[data-site-search]');
if (siteSearch) {
  const form = siteSearch.querySelector('form');
  const input = form.querySelector('input');
  const panel = siteSearch.querySelector('#site-search-results');
  const list = panel.querySelector('[data-search-results-list]');
  const status = panel.querySelector('[data-search-status]');
  const more = panel.querySelector('[data-search-more]');
  let indexPromise;
  let matched = [];
  let shown = 6;
  let revision = 0;
  let timer;

  function loadIndex() {
    if (!indexPromise) {
      indexPromise = fetch('data/search-index.json').then(response => {
        if (!response.ok) throw new Error('Search index unavailable');
        return response.json();
      }).then(entries => entries.map(entry => ({
        ...entry,
        searchText: `${entry.title} ${entry.category} ${entry.description} ${entry.text}`.toLocaleLowerCase(),
      }))).catch(error => { indexPromise = null; throw error; });
    }
    return indexPromise;
  }
  function closeSearch() {
    revision++;
    clearTimeout(timer);
    panel.hidden = true;
    input.setAttribute('aria-expanded', 'false');
  }
  function openSearch() {
    panel.hidden = false;
    input.setAttribute('aria-expanded', 'true');
    fitSearchPanel();
  }
  function fitSearchPanel() {
    const viewportHeight = window.visualViewport?.height ?? innerHeight;
    const available = viewportHeight - siteSearch.getBoundingClientRect().bottom - 24;
    panel.style.maxHeight = `${Math.max(180, Math.min(510, available))}px`;
  }
  function renderResults() {
    list.replaceChildren();
    matched.slice(0, shown).forEach(result => {
      if (!/^[\w.-]+\.html(?:#[\w-]+)?$/.test(result.url)) return;
      const item = document.createElement('li');
      const anchor = document.createElement('a');
      anchor.href = result.url;
      [['search-result-category', result.category], ['search-result-title', result.title], ['search-result-description', result.description]].forEach(([className, text]) => {
        const span = document.createElement('span');
        span.className = className;
        span.textContent = text;
        anchor.append(span);
      });
      item.append(anchor);
      list.append(item);
    });
    more.hidden = shown >= matched.length;
    status.textContent = matched.length ? `${matched.length} ${matched.length === 1 ? 'result' : 'results'} for “${input.value.trim()}”` : 'No matches. Try “privacy”, “AI”, or a researcher’s name.';
  }
  async function search() {
    const query = input.value.toLocaleLowerCase().trim();
    if (!query) { closeSearch(); return; }
    const request = ++revision;
    openSearch();
    status.textContent = 'Searching LERSAIS…';
    more.hidden = true;
    list.replaceChildren();
    try {
      const entries = await loadIndex();
      if (request !== revision) return;
      const terms = query.split(/\s+/).filter(Boolean);
      matched = entries.filter(entry => terms.every(term => entry.searchText.includes(term))).map(entry => {
        const title = entry.title.toLocaleLowerCase();
        const description = entry.description.toLocaleLowerCase();
        return { ...entry, score: (title === query ? 100 : 0) + terms.reduce((score, term) => score + (title.includes(term) ? 12 : 0) + (description.includes(term) ? 3 : 0), 0) };
      }).sort((a, b) => b.score - a.score);
      shown = 6;
      renderResults();
    } catch {
      if (request !== revision) return;
      status.textContent = 'Search is unavailable right now. Please try again or use the navigation above.';
    }
  }
  input.addEventListener('input', () => {
    clearTimeout(timer);
    // Invalidate an earlier request immediately, before the next debounce runs.
    revision++;
    if (!input.value.trim()) { closeSearch(); return; }
    timer = setTimeout(search, 140);
  });
  input.addEventListener('focus', () => { if (input.value.trim() && panel.hidden) search(); });
  form.addEventListener('submit', event => {
    event.preventDefault();
    clearTimeout(timer);
    const url = new URL(location.href);
    if (input.value.trim()) url.searchParams.set('q', input.value.trim());
    else url.searchParams.delete('q');
    history.replaceState(null, '', url);
    search();
  });
  more.addEventListener('click', () => {
    const previousShown = shown;
    shown += 6;
    renderResults();
    list.querySelectorAll('a')[previousShown]?.focus();
  });
  panel.querySelector('[data-search-close]').addEventListener('click', () => {
    input.focus();
    closeSearch();
  });
  siteSearch.addEventListener('keydown', event => {
    if (event.key === 'Escape') {
      event.preventDefault();
      input.focus();
      closeSearch();
    } else if (event.key === 'ArrowDown' && event.target === input && !panel.hidden) {
      event.preventDefault();
      list.querySelector('a')?.focus();
    }
  });
  document.addEventListener('click', event => { if (!siteSearch.contains(event.target)) closeSearch(); });
  siteSearch.addEventListener('focusout', event => {
    if (event.relatedTarget && !siteSearch.contains(event.relatedTarget)) closeSearch();
  });
  window.addEventListener('resize', () => { if (!panel.hidden) fitSearchPanel(); });
  window.visualViewport?.addEventListener('resize', () => { if (!panel.hidden) fitSearchPanel(); });
  const initialQuery = new URLSearchParams(location.search).get('q');
  if (initialQuery) { input.value = initialQuery; search(); }
}

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
