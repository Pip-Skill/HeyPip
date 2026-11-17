# Ledgerly — лендинг

**Запуск:** откройте `index.html` в браузере (сборка не нужна). Для публикации загрузите папку `site/` вместе с `../tokens/` — или скопируйте `tokens/tokens.css` рядом и поправьте путь в `<link>`.

**Файлы**
- `index.html` — разметка и весь текст. Плейсхолдеры в квадратных скобках (`[ЦЕНА]`, `[N]`, `[ОТЗЫВ 1]`, `[РЕЖИМЫ НАЛОГООБЛОЖЕНИЯ]`, `[ЮРЛИЦО]`, ссылки) — заменить до запуска: `grep -n "\[" index.html`.
- `styles.css` — только переменные из `tokens.css`, ни одного HEX.
- `main.js` — вход героя, досчёт цифры, тема, форма (подключите API в месте `[ПОДКЛЮЧИТЬ API РЕГИСТРАЦИИ]`).
- `favicon.svg` — временный знак. `og-image.png` (1200×630) — сделать из кадра P01 (см. `../photo/prompts.md`), заголовок «Ваши деньги. Начисто.» набрать Literata в левой трети.

**Фото:** блок `.photo-ph` (P02) заменить на `<img src="p02.webp" width="2400" height="1029" loading="lazy" alt="…">`, alt уже написан в `aria-label`.

**Изменить цвет/шрифт:** правьте `../brand.json`, затем
```
python3 <heypip>/scripts/check_contrast.py ../brand.json
python3 <heypip>/scripts/build_tokens.py ../brand.json ../tokens
```
Руками `tokens.css` не редактировать.
