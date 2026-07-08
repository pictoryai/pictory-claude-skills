# Complete Request Examples

## Example 1 — Designed explainer (16:9, ~60s, stock visuals, music + voice-over)

Brief: "Make a video about five habits that protect you from phishing."
Palette: Tech/Cyber. Fonts: Space Grotesk + DM Sans. Mixed designed/subtitle scenes.

Every text element declares a `textVariant` (`heading` / `subheading` / `body`) as its
semantic base — the engine seeds size, position, and width from the variant, and the
explicit `style` / `top` / `left` / `width` fields then override only what the design
needs. Note all `top`/`left`/`width` percentages are integers — decimals are rejected.

```json
{
  "videoName": "Five Anti-Phishing Habits",
  "language": "en",
  "aspectRatio": "16:9",
  "saveProject": true,
  "backgroundMusic": { "enabled": true, "autoMusic": true, "volume": 0.12 },
  "voiceOver": {
    "enabled": true,
    "aiVoices": [{ "speaker": "Martin", "speed": 100, "amplificationLevel": 0 }]
  },
  "scenes": [
    {
      "story": "Ninety four percent of breaches start with a single phishing email. These five habits shut the door.",
      "hideSubtitles": true,
      "minimumDuration": 9,
      "endPauseDuration": 0.4,
      "background": {
        "searchFilter": { "query": "hooded hacker typing dark room screen glow" },
        "colorOverlay": { "color": "rgb(15,23,42)", "opacity": 0.5 },
        "settings": { "loop": true, "mute": true }
      },
      "elements": [
        { "type": "shape", "name": "rectangle", "fill": "rgb(34,211,238)",
          "top": "38%", "left": "8%", "width": "6%" },
        { "type": "text", "text": "SECURITY BASICS", "textVariant": "subheading",
          "style": { "fontFamily": "DM Sans", "fontSize": 30, "color": "rgb(34,211,238)",
                     "case": "uppercase", "alignment": "left",
                     "animations": [{ "name": "drift", "type": "entry", "speed": "medium", "direction": "up" }] },
          "top": "44%", "left": "8%", "width": "60%" },
        { "type": "text", "text": "Five habits that stop phishing", "textVariant": "heading",
          "style": { "fontFamily": "Space Grotesk", "fontSize": 72, "color": "rgb(255,255,255)",
                     "decorations": ["bold"], "alignment": "left",
                     "animations": [{ "name": "text reveal", "type": "entry", "speed": "medium" }] },
          "top": "52%", "left": "8%", "width": "78%" }
      ]
    },
    {
      "story": "Habit one. Pause before you click. Hover over every link and read the real U.R.L. first.",
      "hideSubtitles": true,
      "sceneTransition": "fade",
      "background": {
        "searchFilter": { "query": "thoughtful professional pausing at laptop" },
        "colorOverlay": { "color": "rgb(15,23,42)", "opacity": 0.45 },
        "settings": { "loop": true, "mute": true }
      },
      "elements": [
        { "type": "shape", "name": "circle", "fill": "rgb(251,191,36)",
          "top": "20%", "left": "8%", "width": "7%" },
        { "type": "text", "text": "1", "textVariant": "body",
          "style": { "backgroundColor": "rgba(0,0,0,0)", "fontFamily": "Anton", "fontSize": 56, "color": "rgb(15,23,42)" },
          "top": "22%", "left": "11%", "width": "3%" },
        { "type": "text", "text": "Pause before you click", "textVariant": "heading",
          "style": { "fontFamily": "Space Grotesk", "fontSize": 58, "color": "rgb(255,255,255)",
                     "decorations": ["bold"], "alignment": "left",
                     "animations": [{ "name": "wipe", "type": "entry", "speed": "medium", "direction": "right" }] },
          "top": "38%", "left": "8%", "width": "70%" }
      ]
    },
    {
      "story": "Habit two. Verify unusual requests on a second channel. A thirty second phone call beats a thirty thousand dollar mistake.",
      "hideSubtitles": true,
      "sceneTransition": "fade",
      "background": {
        "searchFilter": { "query": "concerned woman making phone call office" },
        "colorOverlay": { "color": "rgb(15,23,42)", "opacity": 0.45 },
        "settings": { "loop": true, "mute": true }
      },
      "elements": [
        { "type": "shape", "name": "circle", "fill": "rgb(52,211,153)",
          "top": "20%", "left": "8%", "width": "7%" },
        { "type": "text", "text": "2", "textVariant": "body",
          "style": { "backgroundColor": "rgba(0,0,0,0)", "fontFamily": "Anton", "fontSize": 56, "color": "rgb(15,23,42)" },
          "top": "22%", "left": "11%", "width": "3%" },
        { "type": "text", "text": "Verify on a second channel", "textVariant": "heading",
          "style": { "fontFamily": "Space Grotesk", "fontSize": 58, "color": "rgb(255,255,255)",
                     "decorations": ["bold"], "alignment": "left",
                     "animations": [{ "name": "wipe", "type": "entry", "speed": "medium", "direction": "right" }] },
          "top": "38%", "left": "8%", "width": "70%" }
      ]
    },
    {
      "story": "Habit three. Turn on multi factor authentication everywhere. Even a stolen password becomes useless.",
      "hideSubtitles": true,
      "sceneTransition": "fade",
      "background": {
        "searchFilter": { "query": "smartphone security code login close up" },
        "colorOverlay": { "color": "rgb(15,23,42)", "opacity": 0.45 },
        "settings": { "loop": true, "mute": true }
      },
      "elements": [
        { "type": "shape", "name": "circle", "fill": "rgb(167,139,250)",
          "top": "20%", "left": "8%", "width": "7%" },
        { "type": "text", "text": "3", "textVariant": "body",
          "style": { "backgroundColor": "rgba(0,0,0,0)", "fontFamily": "Anton", "fontSize": 56, "color": "rgb(15,23,42)" },
          "top": "22%", "left": "11%", "width": "3%" },
        { "type": "text", "text": "Switch on M.F.A.", "textVariant": "heading",
          "style": { "fontFamily": "Space Grotesk", "fontSize": 58, "color": "rgb(255,255,255)",
                     "decorations": ["bold"], "alignment": "left",
                     "animations": [{ "name": "wipe", "type": "entry", "speed": "medium", "direction": "right" }] },
          "top": "38%", "left": "8%", "width": "70%" }
      ]
    },
    {
      "story": "Habits four and five. Report suspicious emails to your security team, and keep your software up to date.",
      "hideSubtitles": true,
      "sceneTransition": "fade",
      "background": { "color": "rgb(30,41,59)" },
      "elements": [
        { "type": "shape", "name": "checkmark-2", "fill": "rgb(52,211,153)",
          "top": "32%", "left": "12%", "width": "4%" },
        { "type": "text", "text": "Report suspicious emails", "textVariant": "body",
          "style": { "fontFamily": "DM Sans", "fontSize": 36, "color": "rgb(255,255,255)", "alignment": "left",
                     "animations": [{ "name": "fade", "type": "entry", "speed": "medium" }] },
          "top": "33%", "left": "18%", "width": "60%" },
        { "type": "shape", "name": "checkmark-2", "fill": "rgb(52,211,153)",
          "top": "48%", "left": "12%", "width": "4%" },
        { "type": "text", "text": "Update software monthly", "textVariant": "body",
          "style": { "fontFamily": "DM Sans", "fontSize": 36, "color": "rgb(255,255,255)", "alignment": "left",
                     "animations": [{ "name": "fade", "type": "entry", "speed": "medium" }] },
          "top": "49%", "left": "18%", "width": "60%" }
      ]
    },
    {
      "story": "Five small habits. One much safer inbox. Share this with your team today.",
      "hideSubtitles": true,
      "sceneTransition": "hblur",
      "minimumDuration": 7,
      "background": { "color": "rgb(15,23,42)" },
      "elements": [
        { "type": "text", "text": "Stay sharp. Stay safe.", "textVariant": "heading",
          "style": { "fontFamily": "Space Grotesk", "fontSize": 64, "color": "rgb(255,255,255)",
                     "decorations": ["bold"], "alignment": "center",
                     "animations": [{ "name": "fade", "type": "entry", "speed": "slow" }] },
          "top": "38%", "left": "10%", "width": "80%" },
        { "type": "shape", "name": "pill", "fill": "rgb(34,211,238)",
          "top": "58%", "left": "40%", "width": "20%" },
        { "type": "text", "text": "SHARE THIS VIDEO", "textVariant": "body",
          "style": { "backgroundColor": "rgba(0,0,0,0)", "fontFamily": "DM Sans", "fontSize": 26, "color": "rgb(15,23,42)",
                     "decorations": ["bold"], "alignment": "center" },
          "top": "60%", "left": "40%", "width": "20%" }
      ]
    }
  ]
}
```

## Example 2 — Subtitle-driven video with AI-generated backgrounds (9:16 short)

Brief: "A dreamy 20-second vertical video about morning routines, AI visuals, cinematic."
Subtitles carry the text (no `elements`, so no `textVariant` needed — that field only
exists on text elements); every background is AI-generated with a consistent style.

```json
{
  "videoName": "Morning Ritual",
  "language": "en",
  "aspectRatio": "9:16",
  "saveProject": true,
  "backgroundMusic": { "enabled": true, "autoMusic": true, "volume": 0.15 },
  "voiceOver": {
    "enabled": true,
    "aiVoices": [{ "speaker": "Joanna", "speed": 95, "amplificationLevel": 0 }]
  },
  "subtitleStyle": {
    "fontFamily": "Poppins Extrabold",
    "fontSize": 44,
    "color": "rgb(255,255,255)",
    "keywordColor": "rgb(251,191,36)",
    "position": "center-center",
    "alignment": "center"
  },
  "scenes": [
    {
      "story": "Your morning sets the tone for everything.",
      "highlightKeywords": true,
      "maxSubtitleLines": 2,
      "background": {
        "type": "video",
        "aiVisual": {
          "prompt": "soft golden sunrise light streaming through bedroom curtains, dust particles floating, slow push-in, dreamy cinematic, photorealistic",
          "model": "pixverse5.5",
          "videoDuration": "5s"
        },
        "colorOverlay": { "color": "rgb(20,10,30)", "opacity": 0.3 }
      }
    },
    {
      "story": "Five quiet minutes before the phone wins.",
      "highlightKeywords": true,
      "maxSubtitleLines": 2,
      "sceneTransition": "fade",
      "background": {
        "type": "video",
        "aiVisual": {
          "prompt": "steaming coffee cup on windowsill at dawn, city waking up in background, shallow depth of field, warm tones, dreamy cinematic, photorealistic",
          "model": "pixverse5.5",
          "videoDuration": "5s",
          "visualContinuity": true
        },
        "colorOverlay": { "color": "rgb(20,10,30)", "opacity": 0.3 }
      }
    },
    {
      "story": "Small rituals. Big days. Start tomorrow.",
      "highlightKeywords": true,
      "maxSubtitleLines": 2,
      "sceneTransition": "fade",
      "endPauseDuration": 0.6,
      "background": {
        "type": "video",
        "aiVisual": {
          "prompt": "person stretching by open window in morning light, silhouette, lens flare, slow motion, dreamy cinematic, photorealistic",
          "model": "pixverse5.5",
          "videoDuration": "5s",
          "visualContinuity": true
        },
        "colorOverlay": { "color": "rgb(20,10,30)", "opacity": 0.3 }
      }
    }
  ]
}
```

Notes on Example 2: AI video costs credits per second (pixverse5.5 ≈ 1.6/sec is the
economical choice; veo3.1 ≈ 20/sec is premium) — confirm with the user first. One
`mediaStyle` is ignored on prompted AI *videos* (it only applies to images, or to
videos when the prompt is omitted) — so the shared style words repeated in every prompt
("dreamy cinematic, photorealistic") plus `visualContinuity` keep the look coherent. The `Joanna`
speaker is illustrative — verify against `GET /v1/voiceovers/tracks`.

## Example 3 — Product launch teaser with AI-generated media elements (16:9, ~30s)

Brief: "A punchy teaser for Aura, a smart lamp that learns your routine. Futuristic,
premium." Palette: Product (electric dark). Fonts: Unbounded + Work Sans.

What this demonstrates that Examples 1-2 don't:

- **AI-generated media elements** — `aiVisual` on `elements[]`, not just backgrounds:
  AI *image* elements (product renders, `seedream3.0`, ≈2 credits each) placed inside
  designed layouts, plus one AI *video* element as a single hero moment (cost-conscious:
  element-level AI video is per-second).
- **A recurring motif** — the same product render style and cyan rim-light recurs in
  every scene, so the video reads as one designed piece.
- **Media-led composition** — the freely positioned AI media elements do the layout
  work while each scene keeps to one `subheading` + one `heading` in their natural
  anchor slots (media elements always honor `top`/`left`, so a media-led layout is the
  most robust composition — see the fallback rule in design-guide.md §6).

```json
{
  "videoName": "Aura Launch Teaser",
  "language": "en",
  "aspectRatio": "16:9",
  "saveProject": true,
  "backgroundMusic": { "enabled": true, "autoMusic": true, "volume": 0.15 },
  "voiceOver": {
    "enabled": true,
    "aiVoices": [{ "speaker": "Martin", "speed": 105, "amplificationLevel": 0 }]
  },
  "scenes": [
    {
      "story": "Meet Aura. The lamp that learns how you live, and lights your home before you ask.",
      "hideSubtitles": true,
      "minimumDuration": 8,
      "endPauseDuration": 0.4,
      "background": { "color": "rgb(8,8,12)" },
      "elements": [
        { "type": "text", "text": "INTRODUCING", "textVariant": "subheading",
          "style": { "fontFamily": "Work Sans", "fontSize": 28, "color": "rgb(34,211,238)",
                     "case": "uppercase",
                     "animations": [{ "name": "fade", "type": "entry", "speed": "medium" }] } },
        { "type": "text", "text": "The lamp that learns you", "textVariant": "heading",
          "style": { "fontFamily": "Unbounded", "fontSize": 66, "color": "rgb(255,255,255)",
                     "decorations": ["bold"],
                     "animations": [{ "name": "text reveal", "type": "entry", "speed": "medium" }] } },
        { "type": "image",
          "aiVisual": { "prompt": "sleek minimalist smart lamp product render, floating, studio lighting, dark background, soft cyan rim light",
                        "model": "seedream3.0", "mediaStyle": "futuristic" },
          "top": "58%", "left": "70%", "width": "24%" }
      ]
    },
    {
      "story": "It reads the room. Sunset warmth for dinner. Crisp daylight for deep work. All automatic.",
      "hideSubtitles": true,
      "sceneTransition": "fade",
      "background": {
        "searchFilter": { "query": "cozy living room evening warm lamp glow" },
        "colorOverlay": { "color": "rgb(8,8,12)", "opacity": 0.5 },
        "settings": { "loop": true, "mute": true }
      },
      "elements": [
        { "type": "text", "text": "Light that reads the room", "textVariant": "heading",
          "style": { "fontFamily": "Unbounded", "fontSize": 56, "color": "rgb(255,255,255)",
                     "decorations": ["bold"],
                     "animations": [{ "name": "wipe", "type": "entry", "speed": "medium", "direction": "right" }] } },
        { "type": "image",
          "aiVisual": { "prompt": "circular glowing dial interface with warm-to-cool color gradient, dark UI, cyan accents, minimal icon style",
                        "model": "seedream3.0", "mediaStyle": "futuristic" },
          "top": "62%", "left": "8%", "width": "18%" }
      ]
    },
    {
      "story": "Seven days is all Aura needs to learn your rhythm.",
      "hideSubtitles": true,
      "sceneTransition": "fade",
      "minimumDuration": 7,
      "background": { "color": "rgb(20,20,28)" },
      "elements": [
        { "type": "text", "text": "7 days to learn your rhythm", "textVariant": "heading",
          "style": { "fontFamily": "Unbounded", "fontSize": 58, "color": "rgb(255,255,255)",
                     "decorations": ["bold"],
                     "animations": [{ "name": "elastic", "type": "entry", "speed": "medium" }] } },
        { "type": "video",
          "aiVisual": { "prompt": "slow motion warm light particles drifting and reorganizing into a soft glowing waveform, dark background, cyan and amber, abstract, premium",
                        "model": "pixverse5.5", "videoDuration": "5s" },
          "settings": { "loop": true, "mute": true },
          "top": "60%", "left": "64%", "width": "30%" }
      ]
    },
    {
      "story": "Aura. Be first in line this spring.",
      "hideSubtitles": true,
      "sceneTransition": "hblur",
      "minimumDuration": 6,
      "endPauseDuration": 0.5,
      "background": { "color": "rgb(8,8,12)" },
      "elements": [
        { "type": "text", "text": "AURA — SPRING 2027", "textVariant": "subheading",
          "style": { "fontFamily": "Work Sans", "fontSize": 26, "color": "rgb(161,161,170)",
                     "case": "uppercase",
                     "animations": [{ "name": "fade", "type": "entry", "speed": "medium" }] } },
        { "type": "text", "text": "Be first in line", "textVariant": "heading",
          "style": { "fontFamily": "Unbounded", "fontSize": 64, "color": "rgb(34,211,238)",
                     "decorations": ["bold"],
                     "animations": [{ "name": "fade", "type": "entry", "speed": "slow" }] } },
        { "type": "image",
          "aiVisual": { "prompt": "sleek minimalist smart lamp product render glowing softly, floating, dark background, cyan rim light, three-quarter view",
                        "model": "seedream3.0", "mediaStyle": "futuristic" },
          "top": "56%", "left": "72%", "width": "22%" }
      ]
    }
  ]
}
```

Cost note: in-render AI visuals are billed per image and per video-second (rates vary
by model) — a few images plus one short clip is cheap, but still confirm AI usage with
the user first; insufficient credits fail the whole job upfront, and a scene whose
generation fails silently keeps its stock/original background. The repeated product-render prompt wording keeps the lamp looking like the same
object across scenes; for exact identity to a real product photo, use
`referenceImageUrl` with an editing-capable image model instead.

## Example 4 — Tutorial with a connected-blocks pipeline diagram (16:9, ~45s)

Brief: "A tutorial explaining how a CI/CD pipeline works." Palette: Tech/Cyber.
Fonts: Space Grotesk + Manrope.

The technique — a **flow diagram built from shapes**, "animated" across scenes:

- **Blocks** are `rectangle` shapes (1:1 aspect: rendered height = element width ×
  frame aspect, so a 14%-wide rectangle on 16:9 is ~25% of frame height) with `body`
  text labels layered on top (same `left`/`width`, `alignment: "center"`).
- **Connectors** are `line` shapes — a thin 300:16 horizontal bar, ideal between
  horizontally arranged blocks.
- Shapes cannot animate, so the diagram is animated **across scenes**: every scene
  redraws the same diagram at the same coordinates, changing only the **state colors**
  — upcoming = dark fill + muted stroke, active = cyan accent + dark label,
  done = emerald. `"sceneTransition": "none"` makes the redraws read as one continuous
  diagram lighting up step by step.

```json
{
  "videoName": "How a CICD Pipeline Works",
  "language": "en",
  "aspectRatio": "16:9",
  "saveProject": true,
  "backgroundMusic": { "enabled": true, "autoMusic": true, "volume": 0.1 },
  "voiceOver": {
    "enabled": true,
    "aiVoices": [{ "speaker": "Martin", "speed": 100, "amplificationLevel": 0 }]
  },
  "scenes": [
    {
      "story": "Every feature you use went down the same assembly line. It is called a pipeline, and it has three stations.",
      "hideSubtitles": true,
      "minimumDuration": 9,
      "background": { "color": "rgb(15,23,42)" },
      "elements": [
        { "type": "text", "text": "TUTORIAL — CI/CD BASICS", "textVariant": "subheading",
          "style": { "fontFamily": "Manrope", "fontSize": 26, "color": "rgb(34,211,238)",
                     "case": "uppercase", "alignment": "center",
                     "animations": [{ "name": "fade", "type": "entry", "speed": "medium" }] },
          "top": "6%", "left": "10%", "width": "80%" },
        { "type": "text", "text": "How code ships to production", "textVariant": "heading",
          "style": { "fontFamily": "Space Grotesk", "fontSize": 58, "color": "rgb(255,255,255)",
                     "decorations": ["bold"], "alignment": "center",
                     "animations": [{ "name": "text reveal", "type": "entry", "speed": "medium" }] },
          "top": "13%", "left": "10%", "width": "80%" },
        { "type": "shape", "name": "rectangle", "fill": "rgb(30,41,59)", "stroke": "rgb(148,163,184)",
          "strokeWidth": 2, "borderRadius": 20, "top": "36%", "left": "8%", "width": "14%" },
        { "type": "shape", "name": "line", "fill": "rgb(71,85,105)", "top": "48%", "left": "24%", "width": "17%" },
        { "type": "shape", "name": "rectangle", "fill": "rgb(30,41,59)", "stroke": "rgb(148,163,184)",
          "strokeWidth": 2, "borderRadius": 20, "top": "36%", "left": "43%", "width": "14%" },
        { "type": "shape", "name": "line", "fill": "rgb(71,85,105)", "top": "48%", "left": "59%", "width": "17%" },
        { "type": "shape", "name": "rectangle", "fill": "rgb(30,41,59)", "stroke": "rgb(148,163,184)",
          "strokeWidth": 2, "borderRadius": 20, "top": "36%", "left": "78%", "width": "14%" },
        { "type": "text", "text": "COMMIT", "textVariant": "body",
          "style": { "backgroundColor": "rgba(0,0,0,0)", "fontFamily": "Space Grotesk", "fontSize": 30, "color": "rgb(148,163,184)",
                     "decorations": ["bold"], "alignment": "center" },
          "top": "46%", "left": "8%", "width": "14%" },
        { "type": "text", "text": "BUILD", "textVariant": "body",
          "style": { "backgroundColor": "rgba(0,0,0,0)", "fontFamily": "Space Grotesk", "fontSize": 30, "color": "rgb(148,163,184)",
                     "decorations": ["bold"], "alignment": "center" },
          "top": "46%", "left": "43%", "width": "14%" },
        { "type": "text", "text": "DEPLOY", "textVariant": "body",
          "style": { "backgroundColor": "rgba(0,0,0,0)", "fontFamily": "Space Grotesk", "fontSize": 30, "color": "rgb(148,163,184)",
                     "decorations": ["bold"], "alignment": "center" },
          "top": "46%", "left": "78%", "width": "14%" }
      ]
    },
    {
      "story": "Station one. A developer pushes code, and the pipeline wakes up. Every change starts life as a commit.",
      "hideSubtitles": true,
      "sceneTransition": "none",
      "minimumDuration": 9,
      "background": { "color": "rgb(15,23,42)" },
      "elements": [
        { "type": "shape", "name": "rectangle", "fill": "rgb(34,211,238)",
          "borderRadius": 20, "top": "36%", "left": "8%", "width": "14%" },
        { "type": "shape", "name": "line", "fill": "rgb(71,85,105)", "top": "48%", "left": "24%", "width": "17%" },
        { "type": "shape", "name": "rectangle", "fill": "rgb(30,41,59)", "stroke": "rgb(148,163,184)",
          "strokeWidth": 2, "borderRadius": 20, "top": "36%", "left": "43%", "width": "14%" },
        { "type": "shape", "name": "line", "fill": "rgb(71,85,105)", "top": "48%", "left": "59%", "width": "17%" },
        { "type": "shape", "name": "rectangle", "fill": "rgb(30,41,59)", "stroke": "rgb(148,163,184)",
          "strokeWidth": 2, "borderRadius": 20, "top": "36%", "left": "78%", "width": "14%" },
        { "type": "text", "text": "COMMIT", "textVariant": "body",
          "style": { "backgroundColor": "rgba(0,0,0,0)", "fontFamily": "Space Grotesk", "fontSize": 30, "color": "rgb(15,23,42)",
                     "decorations": ["bold"], "alignment": "center" },
          "top": "46%", "left": "8%", "width": "14%" },
        { "type": "text", "text": "BUILD", "textVariant": "body",
          "style": { "backgroundColor": "rgba(0,0,0,0)", "fontFamily": "Space Grotesk", "fontSize": 30, "color": "rgb(148,163,184)",
                     "decorations": ["bold"], "alignment": "center" },
          "top": "46%", "left": "43%", "width": "14%" },
        { "type": "text", "text": "DEPLOY", "textVariant": "body",
          "style": { "backgroundColor": "rgba(0,0,0,0)", "fontFamily": "Space Grotesk", "fontSize": 30, "color": "rgb(148,163,184)",
                     "decorations": ["bold"], "alignment": "center" },
          "top": "46%", "left": "78%", "width": "14%" },
        { "type": "text", "text": "Step 1 — a push starts the pipeline", "textVariant": "body",
          "style": { "fontFamily": "Manrope", "fontSize": 32, "color": "rgb(255,255,255)", "alignment": "center",
                     "animations": [{ "name": "fade", "type": "entry", "speed": "medium" }] },
          "top": "72%", "left": "20%", "width": "60%" }
      ]
    },
    {
      "story": "Station two. Servers compile the code and run every test. If anything fails, the line stops right here.",
      "hideSubtitles": true,
      "sceneTransition": "none",
      "minimumDuration": 9,
      "background": { "color": "rgb(15,23,42)" },
      "elements": [
        { "type": "shape", "name": "rectangle", "fill": "rgb(52,211,153)",
          "borderRadius": 20, "top": "36%", "left": "8%", "width": "14%" },
        { "type": "shape", "name": "line", "fill": "rgb(34,211,238)", "top": "48%", "left": "24%", "width": "17%" },
        { "type": "shape", "name": "rectangle", "fill": "rgb(34,211,238)",
          "borderRadius": 20, "top": "36%", "left": "43%", "width": "14%" },
        { "type": "shape", "name": "line", "fill": "rgb(71,85,105)", "top": "48%", "left": "59%", "width": "17%" },
        { "type": "shape", "name": "rectangle", "fill": "rgb(30,41,59)", "stroke": "rgb(148,163,184)",
          "strokeWidth": 2, "borderRadius": 20, "top": "36%", "left": "78%", "width": "14%" },
        { "type": "text", "text": "COMMIT", "textVariant": "body",
          "style": { "backgroundColor": "rgba(0,0,0,0)", "fontFamily": "Space Grotesk", "fontSize": 30, "color": "rgb(15,23,42)",
                     "decorations": ["bold"], "alignment": "center" },
          "top": "46%", "left": "8%", "width": "14%" },
        { "type": "text", "text": "BUILD", "textVariant": "body",
          "style": { "backgroundColor": "rgba(0,0,0,0)", "fontFamily": "Space Grotesk", "fontSize": 30, "color": "rgb(15,23,42)",
                     "decorations": ["bold"], "alignment": "center" },
          "top": "46%", "left": "43%", "width": "14%" },
        { "type": "text", "text": "DEPLOY", "textVariant": "body",
          "style": { "backgroundColor": "rgba(0,0,0,0)", "fontFamily": "Space Grotesk", "fontSize": 30, "color": "rgb(148,163,184)",
                     "decorations": ["bold"], "alignment": "center" },
          "top": "46%", "left": "78%", "width": "14%" },
        { "type": "text", "text": "Step 2 — build and test everything", "textVariant": "body",
          "style": { "fontFamily": "Manrope", "fontSize": 32, "color": "rgb(255,255,255)", "alignment": "center",
                     "animations": [{ "name": "fade", "type": "entry", "speed": "medium" }] },
          "top": "72%", "left": "20%", "width": "60%" }
      ]
    },
    {
      "story": "Station three. The build rolls out to production, and users see the change in minutes. That is the whole pipeline.",
      "hideSubtitles": true,
      "sceneTransition": "none",
      "minimumDuration": 10,
      "endPauseDuration": 0.5,
      "background": { "color": "rgb(15,23,42)" },
      "elements": [
        { "type": "shape", "name": "rectangle", "fill": "rgb(52,211,153)",
          "borderRadius": 20, "top": "36%", "left": "8%", "width": "14%" },
        { "type": "shape", "name": "line", "fill": "rgb(34,211,238)", "top": "48%", "left": "24%", "width": "17%" },
        { "type": "shape", "name": "rectangle", "fill": "rgb(52,211,153)",
          "borderRadius": 20, "top": "36%", "left": "43%", "width": "14%" },
        { "type": "shape", "name": "line", "fill": "rgb(34,211,238)", "top": "48%", "left": "59%", "width": "17%" },
        { "type": "shape", "name": "rectangle", "fill": "rgb(34,211,238)",
          "borderRadius": 20, "top": "36%", "left": "78%", "width": "14%" },
        { "type": "text", "text": "COMMIT", "textVariant": "body",
          "style": { "backgroundColor": "rgba(0,0,0,0)", "fontFamily": "Space Grotesk", "fontSize": 30, "color": "rgb(15,23,42)",
                     "decorations": ["bold"], "alignment": "center" },
          "top": "46%", "left": "8%", "width": "14%" },
        { "type": "text", "text": "BUILD", "textVariant": "body",
          "style": { "backgroundColor": "rgba(0,0,0,0)", "fontFamily": "Space Grotesk", "fontSize": 30, "color": "rgb(15,23,42)",
                     "decorations": ["bold"], "alignment": "center" },
          "top": "46%", "left": "43%", "width": "14%" },
        { "type": "text", "text": "DEPLOY", "textVariant": "body",
          "style": { "backgroundColor": "rgba(0,0,0,0)", "fontFamily": "Space Grotesk", "fontSize": 30, "color": "rgb(15,23,42)",
                     "decorations": ["bold"], "alignment": "center" },
          "top": "46%", "left": "78%", "width": "14%" },
        { "type": "text", "text": "Step 3 — deploy to production", "textVariant": "body",
          "style": { "fontFamily": "Manrope", "fontSize": 32, "color": "rgb(255,255,255)", "alignment": "center",
                     "animations": [{ "name": "fade", "type": "entry", "speed": "medium" }] },
          "top": "72%", "left": "20%", "width": "60%" }
      ]
    }
  ]
}
```

## Example 5 — Tutorial with a vertical stacked-layers diagram (9:16, ~40s)

Brief: "Explain the three layers of a web app, vertical for Shorts." Palette: Education.
Fonts: Poppins Extrabold + Poppins. Same buildup technique, adapted to portrait:

- Blocks stack **vertically** (a 40%-wide rectangle on 9:16 is ~22% of frame height).
- Connectors are small `circle` dots in the gaps between blocks — a dotted chain reads
  as vertical flow without needing a vertical line shape.
- The active layer holds the accent color; inactive layers stay dimmed.

```json
{
  "videoName": "Three Layers of a Web App",
  "language": "en",
  "aspectRatio": "9:16",
  "saveProject": true,
  "backgroundMusic": { "enabled": true, "autoMusic": true, "volume": 0.1 },
  "voiceOver": {
    "enabled": true,
    "aiVoices": [{ "speaker": "Martin", "speed": 100, "amplificationLevel": 0 }]
  },
  "scenes": [
    {
      "story": "Every web app you have ever used is just three layers talking to each other. Let us peel them apart.",
      "hideSubtitles": true,
      "minimumDuration": 9,
      "background": { "color": "rgb(30,27,75)" },
      "elements": [
        { "type": "text", "text": "Every app has 3 layers", "textVariant": "heading",
          "style": { "fontFamily": "Poppins Extrabold", "fontSize": 52, "color": "rgb(255,255,255)",
                     "alignment": "center",
                     "animations": [{ "name": "text reveal", "type": "entry", "speed": "medium" }] },
          "top": "7%", "left": "10%", "width": "80%" },
        { "type": "shape", "name": "rectangle", "fill": "rgb(49,46,129)", "stroke": "rgb(165,180,252)",
          "strokeWidth": 2, "borderRadius": 28, "top": "18%", "left": "30%", "width": "40%" },
        { "type": "shape", "name": "circle", "fill": "rgb(250,204,21)", "top": "41%", "left": "48%", "width": "3%" },
        { "type": "shape", "name": "rectangle", "fill": "rgb(49,46,129)", "stroke": "rgb(165,180,252)",
          "strokeWidth": 2, "borderRadius": 28, "top": "44%", "left": "30%", "width": "40%" },
        { "type": "shape", "name": "circle", "fill": "rgb(250,204,21)", "top": "67%", "left": "48%", "width": "3%" },
        { "type": "shape", "name": "rectangle", "fill": "rgb(49,46,129)", "stroke": "rgb(165,180,252)",
          "strokeWidth": 2, "borderRadius": 28, "top": "70%", "left": "30%", "width": "40%" },
        { "type": "text", "text": "Frontend", "textVariant": "body",
          "style": { "backgroundColor": "rgba(0,0,0,0)", "fontFamily": "Poppins Extrabold", "fontSize": 40, "color": "rgb(165,180,252)",
                     "alignment": "center" },
          "top": "25%", "left": "30%", "width": "40%" },
        { "type": "text", "text": "A.P.I.", "textVariant": "body",
          "style": { "backgroundColor": "rgba(0,0,0,0)", "fontFamily": "Poppins Extrabold", "fontSize": 40, "color": "rgb(165,180,252)",
                     "alignment": "center" },
          "top": "51%", "left": "30%", "width": "40%" },
        { "type": "text", "text": "Database", "textVariant": "body",
          "style": { "backgroundColor": "rgba(0,0,0,0)", "fontFamily": "Poppins Extrabold", "fontSize": 40, "color": "rgb(165,180,252)",
                     "alignment": "center" },
          "top": "77%", "left": "30%", "width": "40%" }
      ]
    },
    {
      "story": "The frontend is everything you see and touch. Buttons, screens, animations. It runs right on your device.",
      "hideSubtitles": true,
      "sceneTransition": "none",
      "minimumDuration": 9,
      "background": { "color": "rgb(30,27,75)" },
      "elements": [
        { "type": "shape", "name": "rectangle", "fill": "rgb(250,204,21)",
          "borderRadius": 28, "top": "18%", "left": "30%", "width": "40%" },
        { "type": "shape", "name": "circle", "fill": "rgb(250,204,21)", "top": "41%", "left": "48%", "width": "3%" },
        { "type": "shape", "name": "rectangle", "fill": "rgb(49,46,129)", "stroke": "rgb(165,180,252)",
          "strokeWidth": 2, "borderRadius": 28, "top": "44%", "left": "30%", "width": "40%" },
        { "type": "shape", "name": "circle", "fill": "rgb(250,204,21)", "top": "67%", "left": "48%", "width": "3%" },
        { "type": "shape", "name": "rectangle", "fill": "rgb(49,46,129)", "stroke": "rgb(165,180,252)",
          "strokeWidth": 2, "borderRadius": 28, "top": "70%", "left": "30%", "width": "40%" },
        { "type": "text", "text": "Frontend", "textVariant": "body",
          "style": { "backgroundColor": "rgba(0,0,0,0)", "fontFamily": "Poppins Extrabold", "fontSize": 40, "color": "rgb(30,27,75)",
                     "alignment": "center" },
          "top": "25%", "left": "30%", "width": "40%" },
        { "type": "text", "text": "what users see", "textVariant": "body",
          "style": { "backgroundColor": "rgba(0,0,0,0)", "fontFamily": "Poppins", "fontSize": 24, "color": "rgb(30,27,75)",
                     "alignment": "center",
                     "animations": [{ "name": "fade", "type": "entry", "speed": "medium" }] },
          "top": "31%", "left": "30%", "width": "40%" },
        { "type": "text", "text": "A.P.I.", "textVariant": "body",
          "style": { "backgroundColor": "rgba(0,0,0,0)", "fontFamily": "Poppins Extrabold", "fontSize": 40, "color": "rgb(165,180,252)",
                     "alignment": "center" },
          "top": "51%", "left": "30%", "width": "40%" },
        { "type": "text", "text": "Database", "textVariant": "body",
          "style": { "backgroundColor": "rgba(0,0,0,0)", "fontFamily": "Poppins Extrabold", "fontSize": 40, "color": "rgb(165,180,252)",
                     "alignment": "center" },
          "top": "77%", "left": "30%", "width": "40%" }
      ]
    },
    {
      "story": "The A.P.I. is the messenger. It carries requests from the screen to the server, and brings the answers back.",
      "hideSubtitles": true,
      "sceneTransition": "none",
      "minimumDuration": 9,
      "background": { "color": "rgb(30,27,75)" },
      "elements": [
        { "type": "shape", "name": "rectangle", "fill": "rgb(49,46,129)", "stroke": "rgb(165,180,252)",
          "strokeWidth": 2, "borderRadius": 28, "top": "18%", "left": "30%", "width": "40%" },
        { "type": "shape", "name": "circle", "fill": "rgb(250,204,21)", "top": "41%", "left": "48%", "width": "3%" },
        { "type": "shape", "name": "rectangle", "fill": "rgb(250,204,21)",
          "borderRadius": 28, "top": "44%", "left": "30%", "width": "40%" },
        { "type": "shape", "name": "circle", "fill": "rgb(250,204,21)", "top": "67%", "left": "48%", "width": "3%" },
        { "type": "shape", "name": "rectangle", "fill": "rgb(49,46,129)", "stroke": "rgb(165,180,252)",
          "strokeWidth": 2, "borderRadius": 28, "top": "70%", "left": "30%", "width": "40%" },
        { "type": "text", "text": "Frontend", "textVariant": "body",
          "style": { "backgroundColor": "rgba(0,0,0,0)", "fontFamily": "Poppins Extrabold", "fontSize": 40, "color": "rgb(165,180,252)",
                     "alignment": "center" },
          "top": "25%", "left": "30%", "width": "40%" },
        { "type": "text", "text": "A.P.I.", "textVariant": "body",
          "style": { "backgroundColor": "rgba(0,0,0,0)", "fontFamily": "Poppins Extrabold", "fontSize": 40, "color": "rgb(30,27,75)",
                     "alignment": "center" },
          "top": "51%", "left": "30%", "width": "40%" },
        { "type": "text", "text": "the messenger", "textVariant": "body",
          "style": { "backgroundColor": "rgba(0,0,0,0)", "fontFamily": "Poppins", "fontSize": 24, "color": "rgb(30,27,75)",
                     "alignment": "center",
                     "animations": [{ "name": "fade", "type": "entry", "speed": "medium" }] },
          "top": "57%", "left": "30%", "width": "40%" },
        { "type": "text", "text": "Database", "textVariant": "body",
          "style": { "backgroundColor": "rgba(0,0,0,0)", "fontFamily": "Poppins Extrabold", "fontSize": 40, "color": "rgb(165,180,252)",
                     "alignment": "center" },
          "top": "77%", "left": "30%", "width": "40%" }
      ]
    },
    {
      "story": "The database is the memory. It stores every account, every post, every like. Three layers. One app.",
      "hideSubtitles": true,
      "sceneTransition": "none",
      "minimumDuration": 9,
      "endPauseDuration": 0.5,
      "background": { "color": "rgb(30,27,75)" },
      "elements": [
        { "type": "shape", "name": "rectangle", "fill": "rgb(49,46,129)", "stroke": "rgb(165,180,252)",
          "strokeWidth": 2, "borderRadius": 28, "top": "18%", "left": "30%", "width": "40%" },
        { "type": "shape", "name": "circle", "fill": "rgb(250,204,21)", "top": "41%", "left": "48%", "width": "3%" },
        { "type": "shape", "name": "rectangle", "fill": "rgb(49,46,129)", "stroke": "rgb(165,180,252)",
          "strokeWidth": 2, "borderRadius": 28, "top": "44%", "left": "30%", "width": "40%" },
        { "type": "shape", "name": "circle", "fill": "rgb(250,204,21)", "top": "67%", "left": "48%", "width": "3%" },
        { "type": "shape", "name": "rectangle", "fill": "rgb(250,204,21)",
          "borderRadius": 28, "top": "70%", "left": "30%", "width": "40%" },
        { "type": "text", "text": "Frontend", "textVariant": "body",
          "style": { "backgroundColor": "rgba(0,0,0,0)", "fontFamily": "Poppins Extrabold", "fontSize": 40, "color": "rgb(165,180,252)",
                     "alignment": "center" },
          "top": "25%", "left": "30%", "width": "40%" },
        { "type": "text", "text": "A.P.I.", "textVariant": "body",
          "style": { "backgroundColor": "rgba(0,0,0,0)", "fontFamily": "Poppins Extrabold", "fontSize": 40, "color": "rgb(165,180,252)",
                     "alignment": "center" },
          "top": "51%", "left": "30%", "width": "40%" },
        { "type": "text", "text": "Database", "textVariant": "body",
          "style": { "backgroundColor": "rgba(0,0,0,0)", "fontFamily": "Poppins Extrabold", "fontSize": 40, "color": "rgb(30,27,75)",
                     "alignment": "center" },
          "top": "77%", "left": "30%", "width": "40%" },
        { "type": "text", "text": "the memory", "textVariant": "body",
          "style": { "backgroundColor": "rgba(0,0,0,0)", "fontFamily": "Poppins", "fontSize": 24, "color": "rgb(30,27,75)",
                     "alignment": "center",
                     "animations": [{ "name": "fade", "type": "entry", "speed": "medium" }] },
          "top": "83%", "left": "30%", "width": "40%" }
      ]
    }
  ]
}
```

Diagram-technique notes (both examples): keep every block, connector, and label at
**identical coordinates in every scene** — only colors change; any drift breaks the
illusion of one continuous diagram. Compute block heights from the 1:1 shape aspect
(height ≈ element width × frame width / frame height) before placing labels. Narration
carries the explanation; block labels stay to one or two words. For branching
flowcharts, `arrow-1`…`arrow-19` shapes can replace `line` connectors — but verify the
arrow art's direction with a quick test render before building a whole video on it.
