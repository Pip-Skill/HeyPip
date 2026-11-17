// Ledgerly — лендинг. Без зависимостей.
(function () {
  var root = document.documentElement;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  root.classList.add('js');

  // Вход героя: один раз, ≤ 600ms суммарно
  requestAnimationFrame(function () { requestAnimationFrame(function () { root.classList.add('loaded'); }); });

  // Цифра «Ваше» досчитывается один раз (≤ 600ms), при reduced motion — сразу итог
  var hl = document.querySelector('[data-count]');
  if (hl && !reduce) {
    var target = parseInt(hl.getAttribute('data-count'), 10);
    var fmt = function (n) { return n.toLocaleString('ru-RU').replace(/\s/g, ' ') + ' ₽'; };
    var final = hl.textContent;
    hl.setAttribute('aria-label', final);
    var start = null, dur = 600, delay = 500;
    setTimeout(function () {
      requestAnimationFrame(function step(t) {
        if (!start) start = t;
        var p = Math.min((t - start) / dur, 1);
        var eased = 1 - Math.pow(1 - p, 3);
        hl.textContent = fmt(Math.round(target * eased / 10) * 10);
        if (p < 1) requestAnimationFrame(step); else hl.textContent = final;
      });
    }, delay);
  }

  // Тема: системная по умолчанию, ручной выбор запоминается
  var btn = document.getElementById('theme-toggle');
  var saved = null;
  try { saved = localStorage.getItem('ledgerly-theme'); } catch (e) {}
  var isDark = function () {
    var t = root.getAttribute('data-theme');
    if (t) return t === 'dark';
    return window.matchMedia('(prefers-color-scheme: dark)').matches;
  };
  if (saved) root.setAttribute('data-theme', saved);
  var sync = function () { btn.setAttribute('aria-pressed', String(isDark())); };
  sync();
  btn.addEventListener('click', function () {
    var next = isDark() ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    try { localStorage.setItem('ledgerly-theme', next); } catch (e) {}
    sync();
  });

  // Форма регистрации: валидация, отправка, успех
  var form = document.getElementById('signup');
  var input = document.getElementById('email');
  var err = document.getElementById('email-error');
  var ok = document.getElementById('signup-success');
  var submit = form.querySelector('button[type="submit"]');
  var valid = function (v) { return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v); };
  var setError = function (on) {
    err.hidden = !on;
    input.setAttribute('aria-invalid', on ? 'true' : 'false');
  };
  input.addEventListener('input', function () { if (!err.hidden && valid(input.value.trim())) setError(false); });
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var v = input.value.trim();
    if (!valid(v)) { setError(true); input.focus(); return; }
    setError(false);
    submit.setAttribute('aria-busy', 'true');
    submit.disabled = true;
    submit.textContent = 'Отправляем…';
    // [ПОДКЛЮЧИТЬ API РЕГИСТРАЦИИ]. Ошибка сети: «Не получилось отправить. Попробуйте ещё раз через минуту.»
    setTimeout(function () {
      form.hidden = true;
      ok.textContent = 'Письмо ушло на ' + v + '. Откройте его — там ссылка для входа.';
      ok.hidden = false;
    }, 700);
  });
})();
