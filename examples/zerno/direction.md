# Direction — Zerno: "Röstprotokoll" (Roast Log)

**Alternatives considered** (from `suggest_brand.py --alternatives 3`, plus my own reading):
1. *Bakery/Cafe → Vibrant & Block-based, Great Vibes + Cormorant* — rejected: a wedding-script display reads "Konditorei/boutique", wrong for a 14-seat roastery for neighbours, and block-colour vibrancy fights the one real story (the roast).
2. *Ticketing → Inter + Playfair, green accent* — mismatch from the matcher; nothing to keep.
3. *Interior → Swiss Modernism, Inter + Inter, stone accent* — the Swiss discipline is useful, the stone accent is mute. Kept the grid, dropped the rest.

**Chosen: "Röstprotokoll".** Why it wins: it is the only direction built on the one fact no other café in Neukölln can claim — *you can watch us roast, every Wednesday, in the room you're sitting in.* The brand looks like the roaster's own log: kraft paper, stamped ink, handwritten batch numbers, a temperature curve. It is crafted but strict — a ledger, not a scrapbook.

The idea in plain words: Zerno is the neighbourhood's roasting room. Everything we show is the working record — batch, date, origin, roast curve — written plainly, in German and Russian, like a note pinned by the door. Wednesday is the event; the rest of the week is the result.

## Positioning
- **Category:** independent neighbourhood coffee roastery-café (Kiezrösterei).
- **Difference:** roasts weekly *in the guest room*, Wednesdays, 14 seats — the neighbours see, smell and hear their coffee being made, and take it home the same week.
- **Character:** **neighbourly, exact, warm-smoky** (friendly people who keep a precise log).

| Is | Is not |
|---|---|
| a working room with a log book | a latte-art Instagram set |
| exact numbers (batch, °C, date) | vague "artisan passion" talk |
| bilingual as a neighbour talks | tourist-English menu |
| kraft, ink, ember | marble, gold, pastel |
| Wednesday as a ritual | "experience", "journey" |

## Visual language
- **Style family:** Organic / crafted leads (paper, stamp, hand-numbered marks), held by a **Swiss grid** underneath (flush-left, strict 12-col, big type contrast) so it never looks amateur.
- **Colour logic:** 70% **Kraft** `#EDE4D3` (paper bags, the log), 20% **Röstschwarz** `#1F1712` (ink, text), 7% **Röstbraun** `#6B4E3D` (secondary text, rules), 3% **Glut** (ember) `#A9361A` — the heat of the drum; used **only** for actions and the "Mittwoch / среда" marker. Dark mode = the room at roast time: near-black brown ground, kraft text, ember lifted to pass contrast.
- **Typography:** **Alegreya** (display, 700/800 — a calligraphic book serif with Cyrillic, feels hand-set without being a script) + **Golos Text** (text/UI, 400/500/600 — a neutral humanist grotesk designed with Cyrillic as a first-class script, handles ä/ö/ü/ß cleanly) + **IBM Plex Mono** (batch numbers, temperatures, times — the "log" voice). Ratio 1.333, body 18px: big jump between display and body.
- **Layout and rhythm:** 12-col, flush-left ragged-right, generous margins; sections separated by hairline rules like ruled paper; data in small mono tables (batch / origin / roast date). Sections breathe 96–128px.
- **Shape:** sharp — radius 2px (stamped labels, tickets). Borders, not shadows. One "stamp" element: a rotated-free rectangular ink border.
- **Imagery:** warm tungsten + daylight mix in a small room, grain visible, close on hands, drum, beans cooling in the tray, steam; neighbours not models; no flat-lay on marble.
- **Motion:** calm, 160/280/520ms, opacity and short translate; one signature: the roast-curve line draws once on scroll. Nothing loops.
- **Voice:** short declaratives, numbers instead of adjectives, neighbourly "ihr/du" in German (Kiez register), «вы» in Russian (friendly, not formal-stiff).
  - "Mittwochs rösten wir. Hier, im Raum." / «По средам жарим. Прямо здесь, в зале.»
  - "14 Plätze. Ein Röster. Dein Kiez." / «14 мест. Один ростер. Ваш район.»
  - "Charge 47 — geröstet am Mittwoch, getrunken bis Sonntag." / «Партия 47 — обжарена в среду, выпита к воскресенью.»

## What we refuse
1. Never a script/handwriting *font* — handwriting appears only as real marks (batch numbers), never as typeset copy.
2. Never "artisan", "passion", "Erlebnis", "experience", «крафтовый», «атмосферный».
3. Never ember red for decoration — it means "act" or "Wednesday", nothing else.
4. Never stock-photo baristas, marble, or latte-art close-ups as heroes.
5. Never English as a third language on the site; DE first, RU equal, no mixed-language headings.

## Risks
- *Kraft + brown looks dull/"bio-shop".* Guard: real contrast (near-black ink, not mid-brown text), one confident ember, big type.
- *Ledger detail reads as clutter.* Guard: mono data only in two places (roast log, opening hours); everything else is plain text.
- *Bilingual doubles the length.* Guard: language switch, not side-by-side columns; same structure in both.
- *No real photos yet.* Guard: shot list in brand.json imagery; placeholders are honest frames, not stock.
