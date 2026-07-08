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
          "style": { "fontFamily": "Anton", "fontSize": 56, "color": "rgb(15,23,42)" },
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
          "style": { "fontFamily": "Anton", "fontSize": 56, "color": "rgb(15,23,42)" },
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
          "style": { "fontFamily": "Anton", "fontSize": 56, "color": "rgb(15,23,42)" },
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
          "style": { "fontFamily": "DM Sans", "fontSize": 26, "color": "rgb(15,23,42)",
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
          "prompt": "soft golden sunrise light streaming through bedroom curtains, dust particles floating, slow push-in, dreamy cinematic",
          "model": "pixverse5.5",
          "mediaStyle": "photorealistic",
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
          "prompt": "steaming coffee cup on windowsill at dawn, city waking up in background, shallow depth of field, warm tones",
          "model": "pixverse5.5",
          "mediaStyle": "photorealistic",
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
          "prompt": "person stretching by open window in morning light, silhouette, lens flare, cinematic slow motion feel",
          "model": "pixverse5.5",
          "mediaStyle": "photorealistic",
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
consistent `mediaStyle` + `visualContinuity` keeps the look coherent. The `Joanna`
speaker is illustrative — verify against `GET /v1/voiceovers/tracks`.
