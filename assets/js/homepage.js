/* Small, dependency-free enhancements. All research text is in the HTML. */
(() => {
  'use strict';

  const root = document.documentElement;
  const themeButton = document.querySelector('.theme-toggle');
  const systemTheme = window.matchMedia('(prefers-color-scheme: dark)');
  const currentTheme = () => root.dataset.theme || (systemTheme.matches ? 'dark' : 'light');
  const describeTheme = () => {
    themeButton.setAttribute('aria-label', `Switch to ${currentTheme() === 'dark' ? 'light' : 'dark'} theme`);
  };
  try {
    const saved = localStorage.getItem('theme');
    if (saved === 'light' || saved === 'dark') root.dataset.theme = saved;
  } catch (_) { /* Browsing with storage disabled still supports theme switching. */ }
  if (themeButton) {
    themeButton.hidden = false;
    describeTheme();
    themeButton.addEventListener('click', () => {
      const next = currentTheme() === 'dark' ? 'light' : 'dark';
      root.dataset.theme = next;
      try { localStorage.setItem('theme', next); } catch (_) { /* Optional preference. */ }
      describeTheme();
    });
    systemTheme.addEventListener('change', describeTheme);
  }

  function stopMedia(container) {
    container.querySelectorAll('video').forEach(video => video.pause());
    container.querySelectorAll('[data-youtube]').forEach(stage => {
      const frame = stage.querySelector('iframe');
      if (frame) frame.remove();
      const launch = stage.querySelector('[data-play-youtube]');
      if (launch) launch.hidden = false;
    });
  }

  document.querySelectorAll('[data-media-switcher]').forEach(switcher => {
    const tablist = switcher.querySelector('[role="tablist"]');
    const tabs = [...tablist.querySelectorAll('[role="tab"]')];
    const panels = [...switcher.querySelectorAll('[role="tabpanel"]')];
    function activate(tab, focus = false) {
      tabs.forEach(candidate => {
        const selected = candidate === tab;
        candidate.setAttribute('aria-selected', String(selected));
        candidate.tabIndex = selected ? 0 : -1;
      });
      panels.forEach(panel => {
        panel.hidden = panel.id !== tab.dataset.panel;
        if (panel.hidden) stopMedia(panel);
      });
      if (focus) tab.focus();
    }
    switcher.classList.add('is-enhanced');
    tablist.hidden = false;
    activate(tabs[0]);
    tabs.forEach((tab, index) => {
      tab.addEventListener('click', () => activate(tab));
      tab.addEventListener('keydown', event => {
        let next;
        if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
        else if (event.key === 'ArrowLeft') next = (index - 1 + tabs.length) % tabs.length;
        else if (event.key === 'Home') next = 0;
        else if (event.key === 'End') next = tabs.length - 1;
        else return;
        event.preventDefault();
        activate(tabs[next], true);
      });
    });
  });

  document.querySelectorAll('[data-play-youtube]').forEach(link => {
    link.addEventListener('click', event => {
      event.preventDefault();
      const stage = link.closest('[data-youtube]');
      if (stage.querySelector('iframe')) return;
      stopMedia(document);
      const frame = document.createElement('iframe');
      frame.src = `https://www.youtube-nocookie.com/embed/${encodeURIComponent(stage.dataset.youtube)}?autoplay=1&rel=0`;
      frame.title = `${stage.dataset.title} — video demonstration`;
      frame.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
      frame.referrerPolicy = 'strict-origin-when-cross-origin';
      frame.allowFullscreen = true;
      link.hidden = true;
      stage.appendChild(frame);
      frame.focus();
    });
  });

  const videos = [...document.querySelectorAll('video')];
  videos.forEach(video => {
    video.addEventListener('play', () => {
      videos.forEach(other => { if (other !== video) other.pause(); });
      document.querySelectorAll('[data-youtube]').forEach(stage => stopMedia(stage));
    });
  });
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => { if (!entry.isIntersecting) entry.target.pause(); });
    });
    videos.forEach(video => observer.observe(video));
  }
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) stopMedia(document);
  });

  const dialog = document.querySelector('.figure-dialog');
  if (dialog && typeof dialog.showModal === 'function') {
    const dialogImage = dialog.querySelector('.dialog-image');
    const original = dialog.querySelector('.original-figure');
    document.querySelectorAll('[data-zoom]').forEach(link => {
      link.addEventListener('click', event => {
        if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
        event.preventDefault();
        dialogImage.src = link.href;
        dialogImage.alt = link.querySelector('img').alt;
        original.href = link.href;
        dialog.showModal();
        document.body.classList.add('dialog-open');
      });
    });
    dialog.querySelector('.close-dialog').addEventListener('click', () => dialog.close());
    dialog.addEventListener('click', event => {
      if (event.target !== dialog) return;
      const rect = dialog.getBoundingClientRect();
      if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close();
    });
    dialog.addEventListener('close', () => {
      document.body.classList.remove('dialog-open');
      dialogImage.removeAttribute('src');
    });
  }
})();
