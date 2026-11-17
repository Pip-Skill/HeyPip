# Промпты для Midjourney — Lumen & Loom

Три кадра, которые закрывают плейсхолдеры сайта: `hero` (герой), `street` (полноширинная пауза), `detail` (секция «Ателье»). ID совпадают с подписями плейсхолдеров в `site/index.html`.

Сырой вывод `scripts/prompt_pack.py` лежит в `prompts.generated.md`. Ниже — отредактированные вручную версии: слова настроения переведены на английский (Midjourney хуже понимает русский), объектив и ракурс приведены к каждому кадру (а не «35 и 50mm» сразу), свет «через ставни» оставлен только для интерьера, список `--no` сокращён до того, что модель реально делает по умолчанию.

**Общий хвост серии (не менять между кадрами — так кадры выглядят одной съёмкой):**
`hard low late-afternoon Lisbon sun, matte sun-bleached film look, warm whites, lifted blacks, fine 35mm grain, muted saturation, palette of limewash white, raw flax, charcoal and deep indigo, precise, sunlit, unhurried`

**Общий `--no`:** `studio backdrop, soft diffused light, glossy fabric, retouched skin, smiling at camera, teal and orange, lens flare, text, logo`

---

## 1. hero — герой сайта, 4:5

Задача: показать ручной труд за 1 секунду. Пустая полосатая стена слева сверху — место под заголовок на мобильном и в соцсетях.

```
editorial photograph, weathered hands of a seamstress in her fifties pinning the collar of an unfinished raw linen shirt laid flat on a scarred oak cutting table, tailor's chalk, steel shears and a spool of natural thread nearby, small atelier room in Lisbon, limewashed wall and a tall window with half-closed wooden shutters casting crisp diagonal stripes of shadow across the table and wall, 50mm lens, f/2.8, high three-quarter angle looking down, hands and shirt in the lower right two thirds, upper left third is empty shadow-striped wall, linen visibly creased and textured, hard low late-afternoon Lisbon sun, matte sun-bleached film look, warm whites, lifted blacks, fine 35mm grain, muted saturation, palette of limewash white, raw flax, charcoal and deep indigo, precise, sunlit, unhurried --ar 4:5 --style raw --no studio backdrop, soft diffused light, glossy fabric, retouched skin, smiling at camera, teal and orange, lens flare, text, logo
```

## 2. street — полноширинная пауза, 16:9

Задача: вещь живёт в городе, а не на вешалке. Лицо не видно (не нужен релиз модели для ИИ-референса; для продакшна — реальная модель). Левая половина пустая под подпись.

```
editorial photograph, a man in his late thirties in a loose undyed linen shirt with rolled sleeves and charcoal linen trousers walking uphill away from the camera, shirt creased and lifting slightly in the breeze, narrow cobbled calçada street in Alfama, Lisbon, pale limestone walls, one deep indigo painted wooden door, empty street, 35mm lens, f/4, eye-level, wide frame, figure small in the right third, face not visible, long diagonal building shadow cutting across the cobbles, left half is sunlit empty wall, hard low late-afternoon Lisbon sun, matte sun-bleached film look, warm whites, lifted blacks, fine 35mm grain, muted saturation, palette of limewash white, raw flax, charcoal and deep indigo, precise, sunlit, unhurried --ar 16:9 --style raw --no studio backdrop, soft diffused light, glossy fabric, retouched skin, smiling at camera, teal and orange, lens flare, text, logo, tourists, tram, azulejo tiles
```

## 3. detail — секция «Ателье», 4:5

Задача: доказательство качества — французский шов и ярлык с номером. Номер на ярлыке ИИ нарисует неразборчиво — в финале вписать «N.º 48 · 017/40» вручную или снять реальный ярлык.

```
editorial macro photograph, inside of an indigo-dyed linen dress turned out to show a hand-finished French seam, a small undyed cotton label attached with visible hand stitches, the label carries a short handwritten ink number, fabric resting on a worn oak table, a single narrow stripe of hard sunlight from a shuttered window crossing the seam, 100mm macro lens, f/2.8, very shallow depth of field, seam running diagonally from lower left to upper right, top third falls into soft shadow, individual linen slubs visible, hard low late-afternoon Lisbon sun, matte sun-bleached film look, warm whites, lifted blacks, fine 35mm grain, muted saturation, palette of limewash white, raw flax, charcoal and deep indigo, precise, sunlit, unhurried --ar 4:5 --style raw --no studio backdrop, soft diffused light, glossy fabric, teal and orange, lens flare, logo, printed text
```

---

**Как пользоваться.** Генерируйте серией в один день и с одной версией модели. Хороший первый кадр можно закрепить как стилевой референс (`--sref`) для двух остальных — проверьте актуальный синтаксис в документации Midjourney, флаги меняются. Для продакшна используйте эти промпты как ТЗ фотографу, а не как финальные изображения; ИИ-изображения на сайте помечайте, если этого требует площадка.
