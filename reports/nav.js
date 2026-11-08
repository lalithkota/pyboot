(function () {
  const baseUrl = document.currentScript.src.replace(/\/nav\.js$/, '');

  fetch(`${baseUrl}/manifest.json`)
    .then((res) => res.json())
    .then((data) => {
      const h1 = document.querySelector('h1');
      if (!h1) return;

      const select = document.createElement('select');
      select.style.cssText = 'margin-top: 8px; margin-bottom: 12px; font-size: 14px; padding: 4px 8px; cursor: pointer; display: inline-block;';

      data.reports.forEach((item) => {
        const url = `${baseUrl}/${item.path}`;
        const option = new Option(item.label, url);
        if (window.location.pathname.includes(`/${item.path}/`)) {
          option.selected = true;
        }
        select.add(option);
      });

      select.onchange = (e) => (window.location.href = e.target.value);
      h1.appendChild(select);
    })
    .catch((err) => console.error('Coverage nav error:', err));
})();
