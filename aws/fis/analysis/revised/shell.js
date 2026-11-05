(function () {
  'use strict';
  const modes = ['initial', 'suggested'];
  const labels = { initial: 'Initial FIS experiment interface', suggested: 'Suggested assessment workflow interface' };
  const buttons = Array.from(document.querySelectorAll('[data-mode]'));
  function select(mode, updateHash) {
    if (!modes.includes(mode)) mode = 'initial';
    for (const name of modes) {
      const active = name === mode;
      document.getElementById(name + '-panel').hidden = !active;
      const button = document.getElementById(name + '-tab');
      button.setAttribute('aria-selected', String(active));
      button.tabIndex = active ? 0 : -1;
    }
    const frame = document.getElementById(mode + '-frame');
    if (!frame.getAttribute('src')) frame.src = frame.dataset.src;
    document.getElementById('standalone-link').href = mode + '/index.html';
    document.getElementById('mode-announcement').textContent = labels[mode] + ' selected.';
    document.title = 'FIS assessment workspace · ' + (mode === 'initial' ? 'Initial' : 'Suggested');
    if (updateHash && location.hash !== '#' + mode) location.hash = mode;
  }
  buttons.forEach(button => {
    button.addEventListener('click', () => select(button.dataset.mode, true));
    button.addEventListener('keydown', event => {
      if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
      event.preventDefault();
      const index = modes.indexOf(button.dataset.mode);
      const next = event.key === 'Home' ? 0 : event.key === 'End' ? modes.length - 1 : (index + (event.key === 'ArrowRight' ? 1 : -1) + modes.length) % modes.length;
      select(modes[next], true);
      document.getElementById(modes[next] + '-tab').focus();
    });
  });
  window.addEventListener('hashchange', () => select(location.hash.slice(1), false));
  select(location.hash.slice(1), false);
}());
