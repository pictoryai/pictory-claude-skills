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

Scale (relative to the ~1080p canvas):

- Hero/title: 64-90, `"case": "uppercase"`, `"decorations": ["bold"]`
- Giant stat numeral: 120-160 (accent color)
- Section heading: 48-66
- Subheading/kicker: 28-42 (muted color or accent, uppercase for kickers/eyebrows)
- Body/support: 20-28, max ~2 short lines
- Set `"alignment"` to match the layout (left for left-anchored text blocks)

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

> **Known engine issue (as of July 2026).** Explicit `top`/`left` on **shape and text**
> elements are currently ignored at render time: the service seeds a preset anchor
> (shapes → `top-right`; `heading`/`body` text → `center-center`; `subheading` →
> `top-center`) and never clears it, and the renderer gives the preset precedence
> (text-to-video-service `apply_scene_elements/index.js` `applyPosition`; avinya
> `DataMapper.ts` `transformElement`). Media elements honor `top`/`left` correctly.
> **Until the fix ships, design each scene with at most one element per anchor slot** —
> one `subheading` kicker (top), one `heading` (center), one accent shape (top-right) —
> and move list/checklist detail into the narration. Multi-row recipes below (checklist,
> numbered chip with overlay digit, stat hero, split layout, frosted panel) will collapse
> into overlapping center text until then.

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

**Stat hero** — solid `background.color` or heavy overlay; giant numeral + caption:

```jsonc
"elements": [
  { "type": "text", "text": "94%", "textVariant": "heading",
    "style": { "fontFamily": "Anton", "fontSize": 150, "color": "rgb(250,204,21)",
               "animations": [{ "name": "elastic", "type": "entry", "speed": "medium" }] },
    "top": "28%", "left": "10%", "width": "40%" },
  { "type": "text", "text": "of breaches start with a phishing email", "textVariant": "body",
    "style": { "fontFamily": "DM Sans", "fontSize": 34, "color": "rgb(255,255,255)", "alignment": "left" },
    "top": "62%", "left": "10%", "width": "50%" }
]
```

**Split layout** — text left, media element right (media defaults to 16:9 box):

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
    "style": { "fontFamily": "Anton", "fontSize": 56, "color": "rgb(15,23,42)" },
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
    "style": { "fontFamily": "Montserrat", "fontSize": 44, "color": "rgb(15,23,42)",
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
    "style": { "fontFamily": "DM Sans", "fontSize": 30, "color": "rgb(8,8,12)", "decorations": ["bold"],
               "alignment": "center" },
    "top": "58%", "left": "40%", "width": "20%" }
]
```

Layering note: elements render in array order — put backdrop shapes before the text that
sits on them. Vary layouts scene to scene; two identical consecutive layouts is the
ceiling.

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
cinematic teal-orange grade"). Use `mediaStyle` to lock the look and keep it consistent
across the video's AI scenes; set `visualContinuity: true` for scene-to-scene coherence.

**Motion:** image backgrounds get `"settings": { "kenBurnsEffect": true }` (or an
explicit `videoKenBurns` zoom path); video backgrounds get `"settings": { "loop": true,
"mute": true }`. Stock clips shorter than the scene need `loop: true`.

## 8. Audio and transitions

**Voice-over.** One consistent voice per video. `speed` 95-105 for explainers, up to 115
for energetic shorts. ElevenLabs voices (via `premiumVoiceSettings`) sound best for
premium content. Defaults if the user has no preference: `Martin` (en). Discover
options via the voices endpoint (api-endpoints.md).

**Music.** `{ "enabled": true, "autoMusic": true, "volume": 0.12 }` is a solid default —
keep volume 0.08-0.15 under narration so the voice stays intelligible; up to 0.3+ only
for music-forward videos with no voice-over. For a curated track, search the music API
by mood/purpose and pass its `audioUrl` as `musicUrl`.

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
- [ ] Layouts vary scene to scene; safe areas respected; bottom clear where subtitles show
- [ ] `hideSubtitles: true` on designed scenes with text elements
- [ ] Search queries are action-first and unique per scene
- [ ] Music volume ≤ 0.15 with voice-over; single consistent voice
- [ ] Transitions subtle and consistent
- [ ] `videoName`, `aspectRatio`, `saveProject` set
