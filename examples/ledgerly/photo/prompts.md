# Промпты для фото (Flux) — Ledgerly, кампания «Чистовик»

Четыре кадра одной серии: одно и то же рабочее место фрилансера утром, вечером, крупно в руках и сверху. База собрана скриптом `prompt_pack.py` из `brand.json` + `shots.json`, потом доведена руками. Что поправлено и почему:
- **Свет и объектив — свои для каждого кадра.** Общий суффикс из `brand.json` говорил «утренний свет» даже для вечернего P02 и давал сразу два фокусных расстояния. Теперь в каждом кадре один источник света и один объектив.
- **Ничего «запрещённого» не названо.** У Flux нет negative prompt, поэтому если написать «avoid coins», монеты как раз могут появиться. Список «нельзя» из `brand.json → imagery.avoid` переписан в позитивные формулировки: «real lived-in room» вместо «not a corporate office», «blank glowing screen» вместо «no fake text».
- **Бренд-суффикс в конце каждого промпта одинаковый, слово в слово.** Именно он держит серию в одном цвете и настроении.

## Бренд-суффикс (не менять внутри серии)
```
Matte film look with lifted blacks and fine natural grain, warm paper-white highlights, restrained true-to-life colour. Palette of warm off-white paper, ink black and graphite grey, with one muted deep green and one highlighter yellow as the only accents. Calm, precise, quietly warm mood. Documentary realism, real lived-in space, tactile paper and wood textures, screens show only soft blank light.
```

## Настройки (проверьте актуальную документацию вашего Flux-сервиса)
- Модель: FLUX 1.1 [pro] / [pro] Ultra (Ultra нужна для 21:9 и для raw-режима, если он есть в вашем сервисе). FLUX [dev] тоже подойдёт, но держите guidance около 3–3.5: при большем значении картинка становится «пластиковой».
- Каждый кадр генерируйте 4–8 раз и выбирайте вариант с самыми чистыми руками и самым ровным местом под текст.
- Для единства серии: возьмите лучший P01 как reference (Redux/Kontext, если доступны) для P02 и P03, тогда стол, кружка и маркер совпадут.
- Если на экране ноутбука или телефона появился текст или цифры, перегенерируйте или закрасьте: интерфейс Ledgerly вставляется на монтаже/вёрстке.

---

## P01 — Герой / OG-картинка / реклама · 16:9
**Задача:** «утро, всё под контролем». **Место под текст:** левая треть (заголовок «Ваши деньги. Начисто.»).
```
An editorial photograph of a freelancer's wooden desk on a quiet weekday morning. An open silver laptop whose screen is a soft, blank, out-of-focus pale glow; beside it a paper notebook open on fine ruled lines, a yellow highlighter with its cap off lying across the page, a ceramic cup of black coffee, a small green plant in a clay pot. A small home studio by a tall window, light plaster wall. Composition: all objects grouped in the right two thirds of the frame, the left third is calm empty plaster wall and bare desk surface, camera slightly above desk height, horizon level. Light: soft morning daylight from a window on the left, gentle long shadows falling to the right, about 4800K. Lens: 35mm at f/4, natural perspective, everything on the desk in focus, wall softly falling off. Matte film look with lifted blacks and fine natural grain, warm paper-white highlights, restrained true-to-life colour. Palette of warm off-white paper, ink black and graphite grey, with one muted deep green and one highlighter yellow as the only accents. Calm, precise, quietly warm mood. Documentary realism, real lived-in space, tactile paper and wood textures, screens show only soft blank light.
```
Вывод: 2400×1350 (герой), кроп 1200×630 под OG.

## P02 — Разворот «Налог отложен. Можно спать.» · 21:9
**Задача:** облегчение, конец дня. **Место под текст:** левая половина в мягкой тени.
```
An editorial photograph of the same freelancer's wooden desk late in the evening, work finished. The silver laptop is closed; the paper notebook lies open on fine ruled lines with a single line marked by one clean yellow highlighter stroke; a phone rests face down; an empty ceramic coffee cup; a small green plant. A warm desk lamp is the only light. Home studio at night, the tall window behind is a deep ink-blue darkness with no city lights. Composition: wide and low, the still life sits in the right half, the left half is a calm, softly graded shadow area of wall and desk, desk edge on the lower third. Light: a single warm tungsten desk lamp from the right, about 3200K, soft pool of light on the notebook, gentle falloff into shadow. Lens: 50mm at f/2.8, focus on the highlighted line, background gently soft. Matte film look with lifted blacks and fine natural grain, warm paper-white highlights, restrained true-to-life colour. Palette of warm off-white paper, ink black and graphite grey, with one muted deep green and one highlighter yellow as the only accents. Calm, precise, quietly warm mood. Documentary realism, real lived-in space, tactile paper and wood textures, screens show only soft blank light.
```
Вывод: 2400×1029, WebP, `loading="lazy"`; на мобильных кроп 4:5 по правой половине.

## P03 — Пост в ленту «Оплачен» · 4:5
**Задача:** момент «деньги пришли, и это спокойно». **Место под текст:** верхняя левая треть.
**Кастинг:** иллюстратор(ка) 28–38 лет, руки без маникюра-«салона», можно с тонким кольцом и следами графита на пальцах; трикотажный рукав цвета овсянки. Лица в кадре нет.
```
An editorial close-up photograph of a freelance illustrator's hands holding a phone just above a wooden desk covered with loose pencil sketches on off-white paper. The phone screen is a soft, blank, glowing pale panel. The thumb rests calmly beside the screen, a quiet moment of relief. Oatmeal knit sleeve, a little graphite smudge on one finger, natural unretouched skin with real texture. Same small home studio in the morning. Composition: the hands enter from the lower right, the phone sits on the right golden-ratio point, the upper left third is calm, softly blurred paper and desk for a caption; no face in frame. Light: soft morning daylight from a window on the left, about 4800K, gentle shadow under the hands. Lens: 50mm at f/2.8, focus on the thumb and phone edge, sketches falling softly out of focus. Matte film look with lifted blacks and fine natural grain, warm paper-white highlights, restrained true-to-life colour. Palette of warm off-white paper, ink black and graphite grey, with one muted deep green and one highlighter yellow as the only accents. Calm, precise, quietly warm mood. Documentary realism, real lived-in space, tactile paper and wood textures, screens show only soft blank light.
```
Вывод: 1080×1350. На вёрстке поверх экрана телефона кладётся реальный push «Счёт № 0047 оплачен · 45 000 ₽».

## P04 — Обложка Stories/Reels «Черновик → Чистовик» · 9:16
**Задача:** главный образ кампании в одном кадре. **Безопасные зоны:** верхние 14% и нижние 20% пустые (интерфейс платформы), подпись «Черновик» снизу и «Чистовик» сверху вставляются в монтаже.
```
An editorial top-down photograph, strictly overhead at 90 degrees, of a warm off-white paper-textured tabletop split into two halves along a gentle diagonal. The lower half is a lively chaos: crumpled paper receipts, scattered square sticky notes in muted off-white and pale yellow, a loose phone cable, a pencil stub. The upper half is perfect order: a single clean sheet of ruled ledger paper with fine graphite lines and one confident yellow highlighter stroke across one line, the yellow highlighter lying neatly parallel to the sheet edge. The top 14 percent and the bottom 20 percent of the frame are empty tabletop. Light: soft even daylight from the upper left, very gentle short shadows that give the paper texture. Lens: 35mm at f/5.6, everything sharp edge to edge, no perspective distortion. Matte film look with lifted blacks and fine natural grain, warm paper-white highlights, restrained true-to-life colour. Palette of warm off-white paper, ink black and graphite grey, with one muted deep green and one highlighter yellow as the only accents. Calm, precise, quietly warm mood. Documentary realism, real lived-in space, tactile paper and wood textures, screens show only soft blank light.
```
Вывод: 1080×1920. Этот кадр — первый кадр (reference / first frame) для шота S02 ролика в Kling.

---

<details><summary>Исходный вывод скрипта (до ручной доводки)</summary>

Сгенерирован командой
`python3 scripts/prompt_pack.py brand.json photo/shots.json … --models flux`
Сохранён ниже для прозрачности. Используйте промпты выше.

```
P01: An editorial photograph of a freelancer's wooden desk in the morning: an open silver laptop whose screen shows a soft out-of-focus light interface with neat rows, a paper notebook with fine ruled lines, a yellow highlighter with its cap off, a ceramic cup of black coffee, a small green plant in a small home studio by a tall window, light plaster wall. Composition: objects grouped in the right two thirds, calm empty wall and desk surface in the left third for a headline, camera slightly above desk height. Light and look: soft morning window light from the side, gentle long shadows, warm daylight around 4800K, 35mm and 50mm, f/2.8 to f/4, natural perspective, slightly above eye level, matte film look, lifted blacks, warm paper highlights, restrained saturation, natural skin texture, no teal-orange, palette of warm off-white paper, ink black, graphite grey, a single muted green, a single highlighter yellow, mood: precise, warm, wry. Avoid stock smiles, corporate office, cold blue light, coins and piggy banks, 3D renders, glossy gradients, readable fake text on screens, neon, lens flare. Aspect ratio 16:9.
```
</details>
