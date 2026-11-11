(function () {
  const baseUrl = document.currentScript.src.replace(/\/nav\.js$/, '');

  fetch(`${baseUrl}/manifest.json`)
    .then((res) => res.json())
    .then((data) => {
      const h1 = document.querySelector('h1');
      if (!h1) return;

      const container = document.createElement('div');
      container.style.cssText = 'margin-top: 8px; margin-bottom: 12px;';

      const label = document.createElement('label');
      label.textContent = 'Current branch: ';

      const select = document.createElement('select');
      select.style.cssText = 'padding: 4px 8px; cursor: pointer;';

      data.reports.forEach((item) => {
        const url = `${baseUrl}/${item.path}`;
        const option = new Option(item.label, url);
        if (window.location.pathname.includes(`/${item.path}/`)) {
          option.selected = true;
        }
        select.add(option);
      });

      select.onchange = (e) => (window.location.href = e.target.value);

      label.appendChild(select);
      container.appendChild(label);
      h1.after(container);
    })
    .catch((err) => console.error('Coverage nav error:', err));
})();
