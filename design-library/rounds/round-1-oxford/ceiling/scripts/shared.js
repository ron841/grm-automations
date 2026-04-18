// Shared: gap tag toggle + scroll reveal + persistence
(function () {
  // Gap tag toggle
  const btn = document.createElement('button');
  btn.className = 'gap-toggle';
  btn.innerHTML = 'Gap annotations · off';
  document.body.appendChild(btn);

  const saved = localStorage.getItem('oxf-gaps');
  if (saved === 'on') {
    document.body.classList.add('gaps-on');
    btn.classList.add('on');
    btn.innerHTML = 'Gap annotations · on';
  }

  btn.addEventListener('click', () => {
    const on = document.body.classList.toggle('gaps-on');
    btn.classList.toggle('on', on);
    btn.innerHTML = 'Gap annotations · ' + (on ? 'on' : 'off');
    localStorage.setItem('oxf-gaps', on ? 'on' : 'off');
  });

  // Scroll reveal
  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (e.isIntersecting) {
        e.target.classList.add('in');
        io.unobserve(e.target);
      }
    });
  }, { threshold: 0.12 });
  document.querySelectorAll('.reveal').forEach((el) => io.observe(el));

  // Active nav
  const path = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-list a').forEach((a) => {
    const href = a.getAttribute('href');
    if (href === path || (path === '' && href === 'index.html')) a.classList.add('active');
  });
})();
