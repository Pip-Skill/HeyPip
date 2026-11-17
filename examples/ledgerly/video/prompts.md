# Промпты для видео (Kling) — Ledgerly, Reels «Черновик → Чистовик»

Четыре генерируемых шота: S01, S02, S03, S05. S04 и S06 — моушн-графика, их не генерируем: интерфейс и логотип нейросеть исказит. ID совпадают со `script.md` и `storyboard.html`.

База собрана `prompt_pack.py` из `brand.json` + `shots.json`, потом доведена руками:
- свет и объектив свои для каждого шота (вечерний S05 больше не получает «утреннее окно»);
- в каждом шоте одно движение камеры, а движение в кадре описано отдельно;
- negative prompt сокращён до того, что реально может испортить именно этот шот;
- бренд-суффикс `Look:` одинаковый во всех шотах, слово в слово.

## Настройки Kling (проверьте актуальные опции в вашей версии)
- Режим: **Image-to-Video**, где указан стартовый кадр (лучше держит серию). Иначе Text-to-Video.
- Качество: Professional / High Quality, 1080p, 9:16.
- Длительность генерации: **5 с** (берём лучший отрезок 1,5–3 с на монтаже).
- CFG / relevance: около 0.5. Если рука «плывёт», поднимите до 0.6–0.7.
- Делайте 3–4 дубля на шот. Для рук выбирайте дубль с пятью пальцами и без «резиновых» суставов.
- Не просите текст в кадре: титры и UI добавляются в монтаже шрифтами бренда.

## Бренд-суффикс (`Look:`, не менять)
```
matte film look with lifted blacks and fine natural grain, warm paper-white highlights, restrained true-to-life colour, palette of warm off-white paper, ink black and graphite grey with one highlighter yellow accent, calm precise quietly warm mood, documentary realism, real tactile paper textures
```

---

## S01 — Хук: черновик · 0:00.0–0:01.5 в монтаже
**Стартовый кадр:** нижняя половина P04 (кроп 9:16 по зоне хаоса) или Text-to-Video.
```
Scene: strictly overhead view of a messy pile of crumpled paper receipts, scattered square pale-yellow and off-white sticky notes, a loose phone cable and a pencil stub on a warm off-white paper-textured tabletop. A real human hand enters from the top of frame and drops one more crumpled receipt onto the pile.
Camera: strictly overhead at 90 degrees, a quick but smooth push-in toward the centre of the pile, no rotation.
Action: the receipt falls, lands and bounces once, two sticky notes slide a few centimetres, the paper settles; the hand exits the frame upward.
Light: soft even daylight from the upper left, short gentle shadows, about 4800K. Lens: 35mm, f/5.6, everything sharp.
Look: matte film look with lifted blacks and fine natural grain, warm paper-white highlights, restrained true-to-life colour, palette of warm off-white paper, ink black and graphite grey with one highlighter yellow accent, calm precise quietly warm mood, documentary realism, real tactile paper textures
Duration: 5s · Aspect: 9:16
Negative: text, letters, numbers, logos, coins, money bills, extra fingers, deformed hand, motion blur smear, flicker, cold blue light, 3D render
```
**В монтаже:** берём 1,5 с, где чек приземляется (удар — на 0:00.3).

## S02 — Фирменная склейка: черновик → чистовик · 0:01.5–0:04.5
**Стартовый кадр:** P04 целиком, но с хаосом поверх всего листа. Если генерируете кадр отдельно: тот же промпт P04, где мусор накрывает весь кадр. **Конечный кадр (если в вашей версии Kling есть end frame):** P04 без мусора — только чистый лист.
```
Scene: strictly overhead view of a warm off-white paper-textured tabletop covered with crumpled receipts and sticky notes; underneath lies a single clean sheet of ruled ledger paper with fine graphite lines and one confident yellow highlighter stroke, a yellow highlighter lying neatly parallel to the sheet.
Camera: locked-off, perfectly static overhead camera, no movement at all.
Action: one flat open hand enters from the top and sweeps everything downward and out of the bottom of the frame in a single smooth continuous motion; the receipts and notes slide away; the clean ruled sheet and the highlighter stay perfectly still and are fully revealed; the hand exits; stillness.
Light: soft even daylight from the upper left, short gentle shadows, about 4800K. Lens: 35mm, f/5.6, everything sharp.
Look: matte film look with lifted blacks and fine natural grain, warm paper-white highlights, restrained true-to-life colour, palette of warm off-white paper, ink black and graphite grey with one highlighter yellow accent, calm precise quietly warm mood, documentary realism, real tactile paper textures
Duration: 5s · Aspect: 9:16
Negative: text, letters, handwriting, numbers, logos, paper morphing, the sheet moving, extra fingers, deformed hand, camera shake, flicker
```
**В монтаже:** 3,0 с: взмах 1,2 с → чистый лист держим 1,8 с, на 0:03.0 появляется титр. Если взмах в генерации медленный, ускорьте до 130–150% (бумага это прощает).

## S03 — Оплата пришла · 0:04.5–0:07.0
**Стартовый кадр:** P03 (переразметьте его в 9:16 или сгенерируйте P03 сразу в 9:16 тем же промптом).
```
Scene: close-up of a freelance illustrator's hands holding a phone just above a wooden desk covered with loose pencil sketches on off-white paper; the phone screen is a soft blank pale glowing panel with nothing on it; oatmeal knit sleeve, a small graphite smudge on one finger, natural skin texture.
Camera: slow, precise push-in of about ten percent, perfectly smooth, no handheld shake.
Action: the blank screen brightens slightly as if a notification has arrived; the thumb relaxes and comes to rest beside the screen; a tiny calm settle of the hands; nothing else moves.
Light: soft morning daylight from a window on the left, about 4800K, gentle shadow under the hands. Lens: 50mm, f/2.8, focus on the thumb and phone edge, sketches softly out of focus.
Look: matte film look with lifted blacks and fine natural grain, warm paper-white highlights, restrained true-to-life colour, palette of warm off-white paper, ink black and graphite grey with one highlighter yellow accent, calm precise quietly warm mood, documentary realism, real tactile paper textures
Duration: 5s · Aspect: 9:16
Negative: text on screen, user interface, icons, numbers, face, extra fingers, deformed hands, glossy plastic skin, screen glare, flicker
```
**В монтаже:** трекинг экрана (4 точки, у пустого экрана они стабильны), сверху кладётся push Ledgerly из `motion-brief.md`.

## S05 — Можно спать · 0:10.0–0:12.5
**Стартовый кадр:** P02, кроп 9:16 по правой половине (натюрморт с лампой).
```
Scene: a silver laptop open on a wooden desk late at night, its screen a soft blank glow; next to it an open ruled notebook with one line marked by a yellow highlighter stroke, an empty ceramic cup, a small green plant and a warm desk lamp; the tall window behind is deep ink-blue darkness.
Camera: locked-off, slightly above desk height, no movement.
Action: a hand enters from the right and slowly, gently closes the laptop lid; the screen glow fades out as the lid shuts; the hand withdraws; only the warm lamp light remains on the notebook; stillness.
Light: a single warm tungsten desk lamp from the right, about 3200K, soft pool of light, gentle falloff into shadow. Lens: 50mm, f/2.8, focus on the notebook.
Look: matte film look with lifted blacks and fine natural grain, warm paper-white highlights, restrained true-to-life colour, palette of warm off-white paper, ink black and graphite grey with one highlighter yellow accent, calm precise quietly warm mood, documentary realism, real tactile paper textures
Duration: 5s · Aspect: 9:16
Negative: text, numbers, logos, neon, blue screen light on the face, person's face, extra fingers, deformed hand, flicker, lamp flicker
```
**В монтаже:** 2,5 с: крышка закрывается к 0:11.5, оставшаяся секунда — тишина и лампа под титром «Можно спать.»

---

<details><summary>Исходный вывод скрипта для S01 (до доводки)</summary>

```
Scene: overhead view of a messy pile of crumpled paper receipts and scattered pale yellow sticky notes on a warm off-white tabletop; a hand drops one more crumpled receipt onto the pile, home studio tabletop, daylight
Camera: strictly overhead, fast but smooth push-in toward the pile
Action: the receipt lands and bounces once, two sticky notes slide slightly, paper settles
Look: soft morning window light from the side, gentle long shadows, warm daylight around 4800K, 35mm and 50mm, f/2.8 to f/4, natural perspective, slightly above eye level, matte film look, lifted blacks, warm paper highlights, restrained saturation, natural skin texture, no teal-orange, palette of warm off-white paper, ink black, graphite grey, a single muted green, a single highlighter yellow, mood: precise, warm, wry
Duration: 5s · Aspect: 9:16
Negative: stock smiles, corporate office, cold blue light, coins and piggy banks, 3D renders, glossy gradients, readable fake text on screens, neon, lens flare, on-screen text, logos, warping faces, flicker
```
</details>
