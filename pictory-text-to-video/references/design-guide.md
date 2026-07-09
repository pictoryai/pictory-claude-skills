# Video Design Guide — Designer-Level Scenes with the Render API

How to turn a text brief into a video that looks art-directed rather than auto-generated.
All JSON fragments use the request vocabulary from request-schema.md.

## 1. The process

1. **Write the script first.** Split it into scenes; each scene's `story` is its narration.
2. **Choose the arc and length** to fit the topic (§2).
3. **Pick one palette and one font pairing** for the whole video (§4, §5) — consistency
   within a video, variety between videos.
4. **Design each scene**: background + color overlay + 2-5 elements from the layout
   recipes (§6). Vary layouts across scenes.
5. **Add voice-over, music, transitions** (§8).

### Creative direction — find the concept before the layouts

The most common failure mode of generated videos is sameness: every video the same arc,
same length, same palette, same five numbered points. Treat these as levers that
**change between videos**, not constants — and pick a *concept* before picking layouts:

- **Lead with a creative device, not a template.** Options to rotate: cold-open on the
  most surprising stat; open with a question the video answers; myth-bust ("everyone
  believes X — here's why it's wrong"); before/after contrast; a day-in-the-life
  micro-story; countdown ("3 things nobody tells you about…"); a single recurring
  metaphor (chess for strategy, weather for market mood, a race for performance).
- **Give the video a motif.** One accent shape, color, or visual idea that recurs —
  e.g. the same `circle` chip counting beats, the accent color only ever on the one
  word that matters, every background shot from above. A motif reads as intentional
  design; random variety reads as noise.
- **Three adjectives first.** Write down three adjectives for the video's mood
  ("urgent, technical, confident" vs "warm, playful, personal") and let them drive
  every choice: palette, font pairing, animation speed, music mood, transition style,
  and whether visuals are stock footage, AI-photoreal, or AI-stylized.
- **Mismatch on purpose, occasionally.** A serious topic with a light palette, or a
  playful topic shot in premium executive style, is memorable when the script supports
  it. Deliberate contrast is a tool; accidental contrast is a mistake.
- **Let the topic pick the visual world.** Finance → macro shots of hands, ledgers,
  skylines; developer tools → screen glow, terminals, dark UI; wellness → morning
  light, slow motion, negative space. Name the visual world in one line before writing
  search queries — every query should live inside it.

If the user asks for consistency with a previous video, replicate its choices exactly;
variety is the default, consistency is on request.

## 2. Story structure and pacing

**Arc.** Default shape: hook → 3-5 content beats → recap or key takeaway → CTA/outro.
But match the structure to the topic — do not force every topic into "five numbered
rules":

| Topic feels like | Structure |
|---|---|
| Ranked list of peer points | Numbered beats with chip/badge scenes |
| One big idea | Hook → idea hero → 2-3 supporting angles → CTA |
| A story | Setup → tension → turn → resolution |
| Myth vs fact | Alternating myth/fact card scenes |
| Q&A / FAQ | Question card → answer scene, repeated |
| Data-heavy | Rapid-fire stat-hero scenes |
| Comparison | Before/after or two-column scenes |

**Length.** Teaser ~15-20s (3-4 scenes), standard ~45-60s (6-9 scenes), deep dive
90-120s. Don't default everything to 60s.

**Narration pacing — critical.** Voice-over reads at **~2.5 words/second**, and the
engine *extends scene duration to fit the narration audio*. Overlong narration is the
top cause of videos running 2x their intended length.

- 5s scene → ~12 words; 8s → ~20 words; 10s → ~25 words; 15s → ~37 words.
- Hook/title scenes: 8-10s. Content beats: 10-13s. Checklist items: 5-6s.
  Stat scenes: 8-10s. Quote: 8-10s. CTA/outro: 6-8s.
- On-screen text must be **shorter** than the narration — narration carries the detail,
  on-screen text is the headline (≤8 words for headings).
- Use `minimumDuration` for scenes whose narration is very short (or absent) so the
  visual has time to land; add `endPauseDuration` (0.3-0.6s) for breathing room.
- TTS spell-outs in `story` text so the voice reads them correctly: IT → I.T.,
  AI → A.I., MFA → M.F.A., URL → U.R.L., CEO → C.E.O., GDPR → G.D.P.R.

## 3. Two rendering modes — pick per video

**A. Subtitle-driven (fast, classic).** Scenes have `story`, subtitles are shown and
styled via `subtitleStyle`, backgrounds come from `searchFilter`. Good for narration-led
explainers from long text. Use `createSceneOnEndOfSentence: true` to auto-split,
`maxSubtitleLines: 2`, `highlightKeywords: true` with a `keywordColor`.

**B. Designed scenes (art-directed).** Each scene sets `hideSubtitles: true` and carries
its message with **text/shape/media elements** — narration still comes from `story`.
This is the mode for title cards, stat heroes, quote cards, CTAs, listicles. Most
high-quality videos mix both: designed hook/stat/CTA scenes, subtitle-driven body scenes.

Any scene with `elements` is routed to the v3 engine automatically — never set
`storyboardVersion` yourself.

## 4. Color system

Pick **one palette per video**, chosen by topic mood. Each palette defines: `bg` (scene
background / overlay tint), `text` (primary), `accent` (highlights, keywords, shapes),
`muted` (secondary text), and 3-5 card colors for chips/badges. Proven combinations
(WCAG-AA audited, from Pictory's design system):

| Palette | bg | text | accent | muted | mood |
|---|---|---|---|---|---|
| Tech/Cyber | `rgb(15,23,42)` | `rgb(255,255,255)` | `rgb(34,211,238)` | `rgb(148,163,184)` | modern, technical |
| Creative | `rgb(10,10,15)` | `rgb(255,255,255)` | `rgb(244,114,182)` | `rgb(161,161,170)` | bold, artistic |
| Executive | `rgb(24,28,36)` | `rgb(255,255,255)` | `rgb(234,179,8)` | `rgb(156,163,175)` | premium, authoritative |
| Health | `rgb(11,52,86)` | `rgb(255,255,255)` | `rgb(110,231,183)` | `rgb(148,163,184)` | calm, trustworthy |
| Education | `rgb(30,27,75)` | `rgb(255,255,255)` | `rgb(250,204,21)` | `rgb(165,180,252)` | energetic, friendly |
| Safety | `rgb(28,25,23)` | `rgb(255,255,255)` | `rgb(251,146,60)` | `rgb(168,162,158)` | urgent, high-contrast |
| Finance | `rgb(6,46,55)` | `rgb(255,255,255)` | `rgb(234,179,8)` | `rgb(148,163,184)` | trust, stability |
| Product | `rgb(8,8,12)` | `rgb(255,255,255)` | `rgb(34,211,238)` | `rgb(161,161,170)` | electric, launch-y |
| Light/Support | `rgb(252,250,247)` | `rgb(15,42,55)` | `rgb(15,118,110)` | `rgb(100,116,139)` | warm, approachable |
| Sales | `rgb(15,23,42)` | `rgb(255,255,255)` | `rgb(251,146,60)` | `rgb(148,163,184)` | energetic pitch |

Chip/badge card colors that read well on the dark palettes: `rgb(251,113,133)` rose,
`rgb(167,139,250)` violet, `rgb(34,211,238)` cyan, `rgb(251,191,36)` amber,
`rgb(52,211,153)` emerald, `rgb(96,165,250)` blue. Text on these light chips should be
the palette `bg` color, not white.

**Color overlays (the legibility workhorse).** Any text over video/photo needs a
`colorOverlay` in the palette bg color:

- Full-bleed background with text on top: opacity **0.45-0.55**
- Background where the visual should stay prominent (text in a corner): **0.3-0.35**
- Solid-color mood scenes (no footage): use `background.color` directly
- Frosted-glass panel: light overlay (~0.25) on the background **plus** a white
  `rectangle` shape `fill: "rgba(255,255,255,0.88)"` behind dark text

## 5. Typography

One pairing per video — a display font for headings, a workhorse for everything else:

| Pairing | Heading font | Body/support font | Vibe |
|---|---|---|---|
| Impact | Bebas Neue or Anton | DM Sans | punchy, social |
| Modern | Space Grotesk | Manrope | tech, product |
| Corporate | Montserrat | Lato | professional |
| Editorial | Playfair Display | Source Sans Pro | elegant, premium |
| Friendly | Poppins Extrabold | Poppins | warm, consumer |
| Bold geo | Unbounded | Work Sans | futuristic |

**Always set `textVariant` on text elements** (`heading` / `subheading` / `body`). It is
the semantic base layer: the engine seeds font size, anchor position, and width from the
variant (heading=66/center/90%, subheading=42/top-center/90%, body=20/center/37%), and
your explicit `style` / `top` / `left` / `width` override only what the design changes.
Text without a variant is treated as `body` — so an undeclared title that omits
`fontSize` renders at 20px.

Scale (px on the default 1080p output):

- Hero/title: 64-90, `"case": "uppercase"`, `"decorations": ["bold"]`
- Giant stat numeral: 120-160 (accent color)
- Section heading: 48-66
- Subheading/kicker: 28-42 (muted color or accent, uppercase for kickers/eyebrows)
- Body/support: 20-28, max ~2 short lines
- Set `"alignment"` to match the layout (left for left-anchored text blocks)

**Line-wrap budget — check every text element.** The renderer measures text at
`fontSize × 4/3` px against a reference frame **1280 px** wide (16:9; **720 px** for
9:16), so one line holds roughly **width% × 1750 / fontSize characters** on 16:9
(width% × 980 / fontSize on 9:16) — about 15% fewer for bold or wide glyphs (M, W).
Text over budget wraps and grows the element *downward*, which is the top cause of
elements overlapping whatever sits below them. Check headings, chip/pill labels, and
diagram block labels against the budget: shorten the text, shrink the font, or widen
the element. Each rendered line is ≈ `fontSize × 1.6 / 720` of frame height (~11% at
fontSize 48) — reserve that much vertical room below any heading you *intend* to run
to two lines, and never place another element inside it.

**Text animations:** default entry `fade` at `slow`/`medium` speed so viewers can read;
add exit `fade` `fast` when the element should clear before the scene ends. `typewriter`
or `text reveal` for hero titles, `drift` (direction up) for kickers, `elastic` for
stats. Max 2 animations (one entry + one exit). **Shape elements do not animate** —
if a label must animate, make it a text element.

## 6. Layout recipes (elements)

Coordinates: `top`/`left` are percentages from the frame's top-left; `width` is percent
of frame width. Percentage strings must be **integers** (`"11%"`, never `"10.5%"`).
**Safe area:** keep elements 5-8% from edges; keep the bottom ~20% clear
on any scene showing subtitles (subtitles render bottom-center). All recipes below assume
16:9 and `hideSubtitles: true`; rebalance vertically for 9:16 (stack, larger fonts).

> **Fallback rule.** If a rendered video comes back with shape/text elements ignoring
> their `top`/`left` and collapsing onto default anchors (shapes → top-right,
> headings/body → center, subheadings → top-center), the target environment does not
> support explicit coordinates on those element types yet. Redesign with one element
> per anchor slot — one `subheading` (top), one `heading` (center), one shape
> (top-right) — and let media elements, which always honor `top`/`left`, carry the
> composition. Otherwise, use explicit coordinates freely.

**Hero / title card** — full-bleed visual, overlay 0.5, kicker + title + accent bar:

```jsonc
"elements": [
  { "type": "shape", "name": "rectangle", "fill": "rgb(34,211,238)",
    "top": "38%", "left": "8%", "width": "6%" },                      // accent bar
  { "type": "text", "text": "CYBERSECURITY BASICS", "textVariant": "subheading",
    "style": { "fontFamily": "DM Sans", "fontSize": 30, "color": "rgb(34,211,238)",
               "case": "uppercase", "alignment": "left",
               "animations": [{ "name": "drift", "type": "entry", "speed": "medium", "direction": "up" }] },
    "top": "44%", "left": "8%", "width": "60%" },
  { "type": "text", "text": "Five habits that stop 90% of attacks", "textVariant": "heading",
    "style": { "fontFamily": "Space Grotesk", "fontSize": 72, "color": "rgb(255,255,255)",
               "decorations": ["bold"], "alignment": "left",
               "animations": [{ "name": "text reveal", "type": "entry", "speed": "medium" }] },
    "top": "52%", "left": "8%", "width": "78%" }
]
```

**Stat hero** — solid `background.color` or heavy overlay; numeral on a backdrop chip +
caption (numbers always sit on a shape — see Standout elements below):

```jsonc
"elements": [
  { "type": "shape", "name": "rectangle", "fill": "rgb(250,204,21)", "borderRadius": 20,
    "top": "26%", "left": "8%", "width": "30%" },
  { "type": "text", "text": "94%", "textVariant": "heading",
    "style": { "backgroundColor": "rgba(0,0,0,0)", "fontFamily": "Anton", "fontSize": 150, "color": "rgb(30,27,75)", "alignment": "center",
               "animations": [{ "name": "elastic", "type": "entry", "speed": "medium" }] },
    "top": "32%", "left": "8%", "width": "30%" },
  { "type": "text", "text": "of breaches start with a phishing email", "textVariant": "body",
    "style": { "fontFamily": "DM Sans", "fontSize": 34, "color": "rgb(255,255,255)", "alignment": "left" },
    "top": "62%", "left": "10%", "width": "50%" }
]
```

**Split layout** — text left, media element right (the media box takes the source
clip's own aspect ratio; there is no crop control, so budget the space accordingly):

```jsonc
"background": { "color": "rgb(24,28,36)" },
"elements": [
  { "type": "text", "text": "Meet the new dashboard", "textVariant": "heading",
    "style": { "fontFamily": "Montserrat", "fontSize": 54, "color": "rgb(255,255,255)",
               "decorations": ["bold"], "alignment": "left" },
    "top": "30%", "left": "7%", "width": "40%" },
  { "type": "text", "text": "Every metric, one screen, zero spreadsheets.", "textVariant": "body",
    "style": { "fontFamily": "Lato", "fontSize": 26, "color": "rgb(156,163,175)", "alignment": "left" },
    "top": "48%", "left": "7%", "width": "36%" },
  { "type": "video", "searchFilter": { "query": "analytics dashboard on laptop screen close up" },
    "settings": { "loop": true, "mute": true },
    "top": "22%", "left": "50%", "width": "44%" }
]
```

**Numbered beat / chip scene** — badge chip + heading, footage behind (overlay 0.45):

```jsonc
"elements": [
  { "type": "shape", "name": "circle", "fill": "rgb(251,191,36)",
    "top": "20%", "left": "8%", "width": "7%" },
  { "type": "text", "text": "1", "textVariant": "body",
    "style": { "backgroundColor": "rgba(0,0,0,0)", "fontFamily": "Anton", "fontSize": 56, "color": "rgb(15,23,42)" },
    "top": "22%", "left": "11%", "width": "3%" },
  { "type": "text", "text": "Use a password manager", "textVariant": "heading",
    "style": { "fontFamily": "Space Grotesk", "fontSize": 58, "color": "rgb(255,255,255)",
               "decorations": ["bold"], "alignment": "left",
               "animations": [{ "name": "wipe", "type": "entry", "speed": "medium", "direction": "right" }] },
    "top": "38%", "left": "8%", "width": "70%" }
]
```

**Quote card** — solid bg, quote shape + italic serif text + attribution:

```jsonc
"background": { "color": "rgb(30,27,75)" },
"elements": [
  { "type": "shape", "name": "quote-1", "fill": "rgb(250,204,21)",
    "top": "18%", "left": "8%", "width": "8%" },
  { "type": "text", "text": "The best time to fix security was yesterday. The second best is today.",
    "textVariant": "heading",
    "style": { "fontFamily": "Playfair Display", "fontSize": 46, "color": "rgb(255,255,255)",
               "decorations": ["italics"], "alignment": "left" },
    "top": "34%", "left": "8%", "width": "72%" },
  { "type": "text", "text": "— HEAD OF SECURITY, ACME", "textVariant": "body",
    "style": { "fontFamily": "DM Sans", "fontSize": 24, "color": "rgb(165,180,252)", "case": "uppercase" },
    "top": "68%", "left": "8%", "width": "50%" }
]
```

**Checklist scene** — 2-4 rows of checkmark + item (5-6s narration per item):

```jsonc
"elements": [
  { "type": "shape", "name": "checkmark-2", "fill": "rgb(52,211,153)", "top": "30%", "left": "10%", "width": "4%" },
  { "type": "text", "text": "Enable two-factor authentication", "textVariant": "body",
    "style": { "fontFamily": "DM Sans", "fontSize": 34, "color": "rgb(255,255,255)", "alignment": "left" },
    "top": "31%", "left": "16%", "width": "60%" },
  { "type": "shape", "name": "checkmark-2", "fill": "rgb(52,211,153)", "top": "45%", "left": "10%", "width": "4%" },
  { "type": "text", "text": "Update software monthly", "textVariant": "body",
    "style": { "fontFamily": "DM Sans", "fontSize": 34, "color": "rgb(255,255,255)", "alignment": "left" },
    "top": "46%", "left": "16%", "width": "60%" }
]
```

**Frosted panel** — content card floating over footage:

```jsonc
"background": { "searchFilter": { "query": "modern office people walking motion blur" },
                "colorOverlay": { "color": "rgb(15,23,42)", "opacity": 0.25 } },
"elements": [
  { "type": "shape", "name": "rectangle", "fill": "rgba(255,255,255,0.88)", "borderRadius": 24,
    "top": "22%", "left": "26%", "width": "48%" },
  { "type": "text", "text": "3 things to remember", "textVariant": "heading",
    "style": { "backgroundColor": "rgba(0,0,0,0)", "fontFamily": "Montserrat", "fontSize": 44, "color": "rgb(15,23,42)",
               "decorations": ["bold"], "alignment": "center" },
    "top": "32%", "left": "30%", "width": "40%" }
]
```

**CTA / outro** — solid bg or brand color, one line + pill button mock:

```jsonc
"background": { "color": "rgb(8,8,12)" },
"elements": [
  { "type": "text", "text": "Start your free trial", "textVariant": "heading",
    "style": { "fontFamily": "Unbounded", "fontSize": 60, "color": "rgb(255,255,255)",
               "decorations": ["bold"], "alignment": "center",
               "animations": [{ "name": "fade", "type": "entry", "speed": "slow" }] },
    "top": "36%", "left": "10%", "width": "80%" },
  { "type": "shape", "name": "pill", "fill": "rgb(34,211,238)", "top": "56%", "left": "40%", "width": "20%" },
  { "type": "text", "text": "pictory.ai", "textVariant": "body",
    "style": { "backgroundColor": "rgba(0,0,0,0)", "fontFamily": "DM Sans", "fontSize": 30, "color": "rgb(8,8,12)", "decorations": ["bold"],
               "alignment": "center" },
    "top": "58%", "left": "40%", "width": "20%" }
]
```

**Diagrams / connected blocks (tutorials)** — build flowcharts and pipelines from
shapes: `rectangle` blocks (1:1 aspect — rendered height ≈ element width × frame
width ÷ frame height) with `body` labels on top, connected by thin `line` shapes
(300:16 bar) horizontally or a chain of small `circle` dots vertically. Shapes cannot
animate, so animate the *diagram state across scenes*: redraw the identical diagram at
identical coordinates each scene and change only the fills — upcoming = dark fill +
muted stroke, active = accent fill + dark label, done = a second accent (e.g. emerald)
— with `"sceneTransition": "none"` so consecutive scenes read as one diagram lighting
up step by step. Labels sitting on a colored block get the default translucent text
strip behind them — hide it with `"backgroundColor": "rgba(0,0,0,0)"` in the label's
`style` (`showBoxBackground: false` is the documented equivalent once supported by the
target environment). Full worked payloads: examples.md Examples 4 (horizontal pipeline,
16:9) and 5 (vertical layer stack, 9:16).

Layering note: elements render in array order — put backdrop shapes before the text that
sits on them. Vary layouts scene to scene; two identical consecutive layouts is the
ceiling.

### Standout elements — micro-components that grab attention

Small element combinations that make key information pop. Build each by layering: the
backdrop shape goes **first** in the `elements` array, the text on top goes after, with
coordinates that sit the text inside the shape (text `top` ≈ shape `top` + 1-2%).

**Rule: text on a shape never keeps the default text strip.** Every label that sits on
a chip, badge, pill, or block gets `"backgroundColor": "rgba(0,0,0,0)"` in its `style` —
the shape *is* the background, and the engine's translucent text box would land on top
of the fill. (Text floating directly on footage or a scene color keeps the strip — there
it earns its keep as legibility backing.) All snippets below and examples.md follow this.

**Rule for numbers: never render a crucial number as plain text.** Whenever a scene
shows or highlights a number — a step count, percentage, price, metric, deadline — put
a **background shape** behind it and the numeral as **`body` text on top of the shape**.
The shape gives the number a frame the eye lands on; use the palette accent as fill and
the palette `bg` color for the numeral (dark-on-bright reads best):

```jsonc
// Number chip — step counts, ranks ("1", "2", "#3")
{ "type": "shape", "name": "circle", "fill": "rgb(251,191,36)",
  "top": "20%", "left": "8%", "width": "11%" },
{ "type": "text", "text": "1", "textVariant": "body",
  "style": { "backgroundColor": "rgba(0,0,0,0)", "fontFamily": "Anton", "fontSize": 56, "color": "rgb(15,23,42)", "alignment": "center" },
  "top": "22%", "left": "8%", "width": "11%" }
```

```jsonc
// Stat badge — percentages, money, KPIs ("94%", "$1.2M", "3x")
{ "type": "shape", "name": "rectangle", "fill": "rgb(34,211,238)", "borderRadius": 16,
  "top": "30%", "left": "10%", "width": "22%" },
{ "type": "text", "text": "94%", "textVariant": "body",
  "style": { "backgroundColor": "rgba(0,0,0,0)", "fontFamily": "Anton", "fontSize": 84, "color": "rgb(15,23,42)", "alignment": "center",
             "animations": [{ "name": "elastic", "type": "entry", "speed": "medium" }] },
  "top": "38%", "left": "10%", "width": "22%" }
```

Give the shape and its text the **same `left`/`width`** with `alignment: "center"` so
the numeral stays centered in the chip at any width. Multiple numbers in one scene →
repeat the pair at different coordinates, rotating chip colors from the palette's card
colors.

**Vertical centering formula (empirical).** A single-line label's optical center sits
≈ `fontSize / 7.2` percent of frame height below the element's `top` on 16:9
(`fontSize / 12.8` on 9:16). To center a label on a shape:

1. Shape height H% = shape width% × 16/9 (on 16:9; × 9/16 on 9:16) ÷ the shape's own
   aspect ratio (rectangle/circle = 1:1, pill ≈ 3.2:1, line = 300:16).
2. Label `top` = shapeTop + H/2 − fontSize/7.2 (16:9) or − fontSize/12.8 (9:16),
   rounded to an integer.

Example: 9:16 circle chip at top 16% / width 16% → H = 9%, center 20.5%; a fontSize-60
numeral goes at top = 20.5 − 60/12.8 ≈ **16%** (level with the chip's own top — the
naive "chip top + 1-2%" placement sits visibly low). The snippets below follow this.

**Chip size follows the font.** Size the chip so its rendered height is ≈ 2.5× the
numeral's cap height (cap height ≈ fontSize/7.2 [16:9] or fontSize/12.8 [9:16] percent
of frame height). For circles that reduces to: **width ≈ fontSize/5 on 16:9,
fontSize/3 on 9:16**. Smaller chips crowd the digit; larger ones read as empty
badges. A fontSize-56 numeral therefore takes an 11%-wide circle on 16:9, a
fontSize-40 numeral an 8%-wide one.

**Multi-line labels and the elements below.** Always count lines before placing
anything: n = ceil(chars ÷ wrap budget from §5). A label's glyph block is
capHeight + (n−1) × lineHeight tall, where lineHeight ≈ fontSize/4.5 (16:9) or
fontSize/8 (9:16) percent of frame height. Then:

- shape height must be ≥ 2.2 × capHeight + (n−1) × lineHeight;
- label `top` = shapeCenter − capHeight − (n−1)/2 × lineHeight (n=1 reduces to the
  single-line formula above);
- anything placed below must clear max(shape bottom, label top + n × lineHeight)
  plus a 2-3% margin.

On-shape labels should stay single-line — reword before resizing. **Mechanical check:
run `python3 scripts/pictory_api.py lint payload.json` before every submit** — it
computes wrap lines for every text element and validates on-shape label centering,
shape sizing, and transparent label backgrounds against these formulas.

Other standout components, most-used first:

| Component | Use for | Construction |
|---|---|---|
| Promo badge | "NEW", "-50%", "FREE" | `badge-1`…`badge-8` shape (accent fill) + short uppercase `body` text on top |
| CTA button mock | closers, offers | `pill` shape + `body` label on top, palette `bg`-colored text |
| Kicker / eyebrow | section context above a title | `subheading` text, uppercase, accent color, fontSize 24-30 |
| Accent bar | anchoring a title's left edge | thin `rectangle`, accent fill, width 5-6% |
| Checkmark row | do's, benefits | `checkmark-1`…`checkmark-6` (green fill) + `body` text to its right |
| Cross row | don'ts, myths | `cross-1`…`cross-8` (red/rose fill) + `body` text to its right |
| Arrow callout | pointing at a media element | `arrow-1`…`arrow-19`, accent fill, placed between text and target |
| Quote mark | testimonials | `quote-1`…`quote-6`, accent fill, above-left of italic quote text |
| Speech bubble | tips, persona voice | `speech-bubble-2`…`speech-bubble-7` + short `body` text inside |
| Idea marker | insights, pro tips | `idea-bulb` or `star-1`…`star-6` (amber fill) + `body` tip text beside it |
| Keyword pop | one hot word in subtitles | not an element: `highlightKeywords: true` + `keywordColor` in subtitleStyle |

```jsonc
// Promo badge
{ "type": "shape", "name": "badge-3", "fill": "rgb(244,114,182)",
  "top": "12%", "left": "78%", "width": "12%" },
{ "type": "text", "text": "NEW", "textVariant": "body",
  "style": { "backgroundColor": "rgba(0,0,0,0)", "fontFamily": "DM Sans", "fontSize": 30, "color": "rgb(10,10,15)",
             "decorations": ["bold"], "case": "uppercase", "alignment": "center" },
  "top": "16%", "left": "78%", "width": "12%" }
```

```jsonc
// Do / don't rows (myth-vs-fact, tips scenes)
{ "type": "shape", "name": "cross-2", "fill": "rgb(251,113,133)", "top": "34%", "left": "10%", "width": "4%" },
{ "type": "text", "text": "Reuse one password everywhere", "textVariant": "body",
  "style": { "fontFamily": "DM Sans", "fontSize": 32, "color": "rgb(148,163,184)",
             "decorations": ["linethrough"], "alignment": "left" },
  "top": "35%", "left": "16%", "width": "60%" },
{ "type": "shape", "name": "checkmark-2", "fill": "rgb(52,211,153)", "top": "50%", "left": "10%", "width": "4%" },
{ "type": "text", "text": "One unique password per account", "textVariant": "body",
  "style": { "fontFamily": "DM Sans", "fontSize": 32, "color": "rgb(255,255,255)", "alignment": "left" },
  "top": "51%", "left": "16%", "width": "60%" }
```

Restraint rule: **one standout component per scene carries the message; two is the
maximum.** A badge, a stat chip, and an arrow in the same frame compete and all lose.
Animate the standout (entry `elastic` or `fade`), keep everything else static — shapes
don't animate, so motion on the text is what draws the eye.

## 7. Visuals: stock search vs AI generation

**Stock (`searchFilter`) is the default** — free, fast, photoreal. Write queries that
describe the *behavior on camera*, not the abstract topic (3-6 words):

- Topic "pause before clicking links" → `"thoughtful professional pausing at laptop"`
- Topic "verify requests" → `"concerned woman phone call office"`
- Topic "growth" → `"rising line graph animation screen"`

Ask "what is the person DOING?" and describe what a camera sees. Add a `category` filter
when the taxonomy matches (e.g. `"Nature/Sunrises_and_Sunsets"`). Vary queries across
scenes — never reuse one query twice.

**AI visuals (`aiVisual`)** when stock can't deliver: specific fictional scenes, stylized
looks (cartoon/futuristic/vintage), brand-specific imagery, impossible shots. Costs AI
credits (video is expensive: veo3.1 ≈ 20 credits/sec) — always confirm with the user
before putting AI video in many scenes. Prompt like a cinematographer: subject + action
+ setting + lighting + camera ("slow dolly-in on a lone lighthouse at dusk, storm clouds,
cinematic teal-orange grade"). Set `visualContinuity: true` for scene-to-scene coherence.

**`mediaStyle` rule:** it applies to AI **images** always, but to AI **video** only when
`prompt` is omitted; on a prompted video it is silently ignored. So: for AI *images*,
set `mediaStyle` and keep it identical across the video. For AI *video* with a prompt,
do not set `mediaStyle` — write the style into the prompt text itself and repeat the
same style words across scenes ("…, cinematic, teal-orange grade" in every prompt).

**AI-generated media *elements*** — `aiVisual` works on scene `elements` too, not just
backgrounds, and media elements honor explicit `top`/`left` positioning. This is the
tool for product renders, mascots, stylized icons, and concept art placed *inside* a
designed layout (e.g. a floating product shot next to a headline). AI *images* are
billed per image (cheap — use freely once the user opts in); AI *video* elements are
billed per second of generated footage — reserve for one hero moment.
AI image elements are **opaque rectangles** — an isolated object generated on a white
studio background reads as a white card sitting on the scene. When placing an object
on a solid-color scene, name the scene's background color in the prompt ("centered on
a plain solid dark indigo background #1E1B4B"); full-bleed illustrations that fill
their own frame don't need this.
For a consistent character/product across scenes, generate with the same model +
`mediaStyle` and reuse tight prompt wording; `referenceImageUrl` (image models with
editing support, e.g. `seedream3.0`, `nanobanana`) can lock identity to a user-provided
image:

```jsonc
{ "type": "image",
  "aiVisual": { "prompt": "sleek smart lamp product render, floating, studio lighting, dark background, soft cyan rim light",
                "model": "seedream3.0", "mediaStyle": "futuristic" },
  "top": "55%", "left": "68%", "width": "26%" }
```

**Motion:** image backgrounds get `"settings": { "kenBurnsEffect": true }` (or an
explicit `videoKenBurns` zoom path); video backgrounds get `"settings": { "loop": true,
"mute": true }`. Stock clips shorter than the scene need `loop: true`.

## 8. Audio and transitions

**Voice-over.** Always include a `voiceOver` block — omitting it entirely produces a
**silent video** (there is no implicit default narrator). One consistent voice per
video: multiple `aiVoices` rotate scene-by-scene, which is a dialog device, not a
default. `speed` 95-105 for explainers, up to 115 for energetic shorts. ElevenLabs
voices (via `premiumVoiceSettings`) sound best for premium content. `Martin` (en) is a
safe pick if the user has no preference; discover options via the voices endpoint
(api-endpoints.md).

**Music.** `{ "enabled": true, "autoMusic": true, "volume": 0.12 }` is a solid default.
**Never omit `volume`** — an omitted volume plays the track at full loudness over the
narration. Keep 0.08-0.15 under voice-over; up to 0.3+ only for music-forward videos
with no narration. For a curated track, search the music API by mood/purpose and pass
its `audioUrl` as `musicUrl`.

**Transitions.** Less is more: `fade` or none for most cuts; `hblur` or `smoothleft` as
occasional punctuation at chapter boundaries; `circlecrop`/`radial` only for playful
content. Use one transition style consistently — don't rotate through the catalog.

## 9. Aspect ratio

- `16:9` — YouTube, presentations (default)
- `9:16` — TikTok/Reels/Shorts: bigger fonts (headings 70-90), stacked layouts,
  center-weighted composition, tighter word budgets
- `1:1` / `4:5` — feed posts

Element `top/left/width` percentages are relative to the frame, so re-derive layout for
each ratio rather than copying a 16:9 layout to 9:16.

## 10. Quality checklist (before submitting)

- [ ] Narration fits duration budget (~2.5 words/sec) for every scene
- [ ] One palette, one font pairing across all scenes
- [ ] Every text-over-footage scene has a colorOverlay (0.3-0.55)
- [ ] On-screen text ≤ 8-10 words per element; no paragraph dumps
- [ ] Every text element passes the line-wrap budget (chars ≤ width% × 1750 / fontSize
      on 16:9; × 980 on 9:16); intended two-line headings have vertical room below
- [ ] Crucial numbers sit on a backdrop shape (chip/badge) as body text, never plain,
      with the chip sized to the font (circle width ≈ fontSize/5 on 16:9, /3 on 9:16)
- [ ] Every text element sitting on a shape has `backgroundColor: "rgba(0,0,0,0)"`
- [ ] At most one or two standout components per scene
- [ ] Layouts vary scene to scene; safe areas respected; bottom clear where subtitles show
- [ ] `hideSubtitles: true` on designed scenes with text elements
- [ ] Search queries are action-first and unique per scene
- [ ] `voiceOver` block present (omitting it = silent video); single consistent voice
- [ ] `backgroundMusic.volume` set explicitly, ≤ 0.15 with voice-over
- [ ] Transitions subtle and consistent
- [ ] `videoName`, `aspectRatio`, `saveProject` set
- [ ] `scripts/pictory_api.py lint <payload>` passes
