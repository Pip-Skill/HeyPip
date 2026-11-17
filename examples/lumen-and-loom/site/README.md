# Сайт Lumen & Loom

**Запуск:** откройте `index.html` в браузере (нужен интернет: Tailwind v4 через CDN `@tailwindcss/browser` и Google Fonts). Для продакшна соберите Tailwind CLI с `../tokens/tokens.tailwind.css`.

**Токены:** все цвета, шрифты, шкалы — из `../tokens/tokens.css`, сгенерированного из `../brand.json`. В `index.html` блок `@theme inline` только связывает имена утилит (`bg-bg`, `text-accent`, `text-6xl`) с переменными — значений там нет. Меняете цвет → правите `brand.json` → `python3 scripts/build_tokens.py brand.json tokens`.

**Копирайт:** весь текст — в `index.html`. Неизвестные факты в квадратных скобках: `[ЦЕНА]`, `[АДРЕС]`, `[ГРАММАТУРА]`, `[N]`, `[ИНТЕГРАЦИЯ]` — найдите `[` и заполните.

**Фото:** плейсхолдеры `.ph` с ID кадров (`hero`, `street`, `detail`, карточки вещей). Замените на `<img src width height alt loading="lazy">` (герой — `fetchpriority="high"` без lazy). Промпты — `../photo/prompts.md`.

**Форма:** лист ожидания с валидацией и состояниями; отправка — заглушка, подключите сервис рассылки в месте `[ИНТЕГРАЦИЯ]`.
