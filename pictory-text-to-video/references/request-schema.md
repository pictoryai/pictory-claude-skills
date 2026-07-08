# Pictory Storyboard Render API — Request Body Reference

Complete reference for `POST /pictoryapis/v2/video/storyboard/render`. Anything not
listed here is silently stripped from the request by the API — do not invent fields.

## Top-level structure

```jsonc
{
  "videoName": "my-video",             // string; used for output file name/title
  "videoWidth": 1920,                  // optional; must be provided together with videoHeight
  "videoHeight": 1080,
  "aspectRatio": "16:9",               // "1:1" | "16:9" | "9:16" | "4:5"
  "language": "en",                    // script language (see Languages below)
  "saveProject": true,                 // also save as an editable Pictory project
  "webhook": "https://...",            // optional callback on completion (max 500 chars)
  "webhookInput": {},                  // optional payload echoed to the webhook
  "backgroundMusic": { ... },          // see Background music
  "voiceOver": { ... },                // see Voice-over
  "logo": { ... },                     // see Logo
  "avatar": { ... },                   // AI avatar; requires voiceOver.enabled=true
  "subtitleStyle": { ... },            // fontStyle object applied to all subtitles
  "scenes": [ ... ]                    // REQUIRED (unless templateId is used); min 1 scene
}
```

Other top-level fields (advanced / account-specific): `templateId` + `variables`,
`smartLayoutName`/`smartLayoutId`, `brandId` | `brandName` (not both),
`visualLibraryId` + `visualSelectionPreference` (`prefer-stock`, `prefer-user-library`,
`stock-only`, `user-library-only`), `destinations` (vimeo/s3 export), `awsConnectionId`,
`vimeoConnectionId`, `projectMetadata`, `storyboardVersion`.

**Leave `storyboardVersion` unset.** The service auto-routes to the v3 engine when a
scene uses `elements`, `aiVisual`, `colorOverlay`, `maxSubtitleLines`, smart layouts,
avatars, or audio scenes. Setting any explicit value other than `"v3"` forces the v2
engine and breaks those features.

**Validation rules**
- `videoWidth` and `videoHeight` must be provided together (or use `aspectRatio` alone).
- `brandId` and `brandName` are mutually exclusive.
- `subtitleStyleId` and `subtitleStyleName` are mutually exclusive.
- `avatar` requires `voiceOver.enabled: true`.
- Unknown fields are silently stripped — typos disappear rather than erroring.

## Scenes

Each scene must have **exactly one content source** — `story`, `storyCoPilot`, `blogUrl`,
`pptUrl`, `audioUrl`, or `videoUrl` — **or** a `background` with a visual/color (a
visual-only scene with no narration text).

```jsonc
{
  "story": "Narration / subtitle text for this scene.",   // max 15,000 chars
  "isSSMLStory": false,                 // only with story; enables SSML markup
  "createSceneOnNewLine": false,        // split into sub-scenes on newlines
  "createSceneOnEndOfSentence": false,  // split into sub-scenes per sentence
  "maxSubtitleLines": 2,                // 1-4; NOT allowed with smartLayout
  "highlightKeywords": true,            // keyword highlighting in subtitles (defaults ON)
  "hideSubtitles": false,               // narrate without showing subtitle text
  "minimumDuration": 5,                 // manual duration (seconds): IS the duration for
                                        // visual-only scenes; with narration the scene
                                        // still extends to fit the audio
  "endPauseDuration": 0.5,              // trailing pause in seconds
  "sceneTransition": "fade",            // transition INTO this scene (see Transitions)
  "subtitleStyle": { ... },             // fontStyle override for this scene
  "background": { ... },               // see Background
  "voiceOver": { ... },                // scene-level override
  "backgroundMusic": { "enabled": false }, // scene-level on/off only
  "elements": [ ... ]                  // 1-20 overlay elements (see Elements)
}
```

Scene-level validation:
- `caption` requires `story` and is incompatible with `createSceneOnNewLine` / `createSceneOnEndOfSentence`.
- `audioUrl`/`videoUrl` scenes require `audioLanguage` (e.g. `en-US`); `transcript` and
  `mediaRepurposeSettings` are only allowed with `audioUrl`/`videoUrl`.
- Scene `voiceOver` cannot have both `aiVoices` and `externalVoice`.

`storyCoPilot` (AI writes the script for the scene):

```jsonc
{
  "storyCoPilot": {
    "prompt": "30-second video about ocean plastic pollution",  // required, max 5000
    "videoType": "Explainer",   // Explainer | Marketing | Internal Communication | Tutorial | Product
    "duration": 30,             // 1-600 seconds
    "platform": "YouTube",      // YouTube | TikTok | Instagram | Facebook | LinkedIn | Twitter
    "tone": "informative"       // professional|casual|friendly|informative|persuasive|exciting|educational|humorous|serious|conversational
  }
}
```

## Background

Exactly **one** of `visualUrl`, `color`, or `aiVisual` (or none of those plus a
`searchFilter` for stock search). `type` ("video" | "image") is required with `aiVisual`.

```jsonc
"background": {
  // Option A — direct URL
  "visualUrl": "https://.../clip.mp4",
  "type": "video",
  "clips": [{ "start": 3, "end": 9 }],       // trim; only with visualUrl + type video

  // Option B — solid color
  "color": "rgb(15, 23, 42)",

  // Option C — stock library search (best default for realistic footage).
  // The service picks the best-matching asset and automatically avoids reusing an
  // asset another scene already took (no manual dedup needed). If no visual can be
  // found at all, the job fails with SCENE_BACKGROUND_VISUAL_NOT_FOUND.
  "searchFilter": {
    "query": "aerial coastline waves crashing",   // free-text semantic search
    "keywords": ["ocean", "coastline"],           // 1-10 keywords, 2-100 chars each
    "category": "Nature/Landscapes",              // optional taxonomy filter (see Categories)
    "libraries": ["story_blocks", "getty"]        // optional
  },

  // Option D — AI-generated visual
  "aiVisual": {
    "prompt": "cinematic drone shot of a turquoise coastline at golden hour",  // max 500
    "model": "veo3.1",            // see AI models
    "mediaStyle": "photorealistic",  // photorealistic|artistic|cartoon|minimalist|vintage|futuristic
    "videoDuration": "8s"         // video models only; model-specific values
  },
  "type": "video",                 // REQUIRED with aiVisual

  // Extras (combinable with any option)
  "colorOverlay": { "color": "rgb(0,0,0)", "opacity": 0.45 },  // tint for text legibility
  "settings": {
    "loop": true,                 // loop video to fill scene duration
    "mute": true,                 // mute background video's own audio
    "zoomAndPan": true,           // auto motion (any background)
    "kenBurnsEffect": true,       // image backgrounds only; NOT with zoomAndPan
    "videoKenBurns": {            // explicit zoom path
      "start": { "zoom": 1.0, "centerX": 0.5, "centerY": 0.5 },
      "end":   { "zoom": 1.2, "centerX": 0.6, "centerY": 0.4 }
    }
  },
  "motionGraphics": { "enabled": true, "prompt": "...", "style": "..." }  // animated graphics bg
}
```

`aiVisual` extra fields: `visualContinuity` (bool, chain scene visuals),
`firstFrameImageUrl` (video only, exclusive with `referenceImageUrls`),
`referenceImageUrls` (video, 1-2 URLs), `referenceImageUrl` (image only).

**`mediaStyle` rule:** set it for **image** models — it is always applied. For **video**
models it only has an effect when `prompt` is *omitted* (the auto-generated prompt uses
it); on a video with an explicit `prompt` it is ignored, so do not set it there — write
the style into the prompt text instead ("cinematic", "cartoon", "vintage film grain", …).

**AI generation behavior:** insufficient AI credits fail the whole job upfront
(`INSUFFICIENT_CREDITS`). If a single scene's generation fails, its credits are not
charged and the scene **silently keeps its stock/original background** — check the
finished video when using many AI scenes. Credits are charged per image and per
video-second (rate depends on the model).

Also on scenes: `backgroundBrolls` (array of background objects with optional
`brollClip: {start,end}` — b-roll cuts over the base background) and `backgroundCorpus`
(array of `{visualUrl, type: "image", prefer}` — a pool the engine picks from).

## Elements (scene overlays)

1-20 per scene. `type`: `"shape" | "text" | "video" | "image"`.

**Positioning (all element types):** either a `position` preset — `top-left`, `top-center`,
`top-right`, `center-left`, `center` / `center-center`, `center-right`, `bottom-left`,
`bottom-center`, `bottom-right` — **or** explicit `top` / `left` percentage strings
(`"0%"`–`"100%"`, measured from the top-left corner of the frame). Never both.
`width` (percentage of frame width) is independent and always allowed.

### Text element

```jsonc
{
  "type": "text",
  "text": "OCEANS IN CRISIS",          // required, max 2000 chars
  "textVariant": "heading",            // heading | subheading | body — ALWAYS set this
  "style": { ... },                    // fontStyle (below)
  "top": "12%", "left": "8%", "width": "60%"
}
```

`textVariant` seeds the element's defaults, which `style`/`top`/`left`/`width` then
override: `heading` → fontSize 66, center-center, width 90%; `subheading` → 42,
top-center, 90%; `body` → 20, center-center, 37%. An element without a variant falls
back to `body` — so a title that omits `fontSize` renders at 20px.

### Shape element

```jsonc
{
  "type": "shape",
  "name": "rectangle",                 // see Shape catalog
  "fill": "rgba(255, 200, 40, 1)",
  "stroke": "rgb(255,255,255)",
  "strokeWidth": 0,
  "borderRadius": 12,                  // rectangle rounding
  "top": "70%", "left": "8%", "width": "24%"
}
```

Shape rendering notes: `stroke`/`strokeWidth` only take effect on the basic shapes
(`rectangle`, `circle`, `line`); `borderRadius` only on `rectangle`. Featured shapes
(badges, arrows, checkmarks, …) accept a `fill` recolor only — other style fields are
accepted by validation but have no visual effect. Basic `rectangle`/`circle` render 1:1
(rendered height = width × frame aspect); `line` is a thin 300:16 bar; featured shapes
keep their source artwork's own aspect ratio (not necessarily square).

### Media element (video / image)

Exactly **one** of `visualUrl`, `searchFilter`, or `aiVisual`:

```jsonc
{
  "type": "image",
  "searchFilter": { "query": "smiling scientist portrait" },  // query only for elements
  // or "visualUrl": "https://...",
  // or "aiVisual": { "prompt": "...", "model": "seedream3.0", "mediaStyle": "minimalist" },
  "colorOverlay": { "color": "rgb(10,10,40)", "opacity": 0.3 },
  "settings": { "loop": true, "mute": true },   // type "video" only; both default true
  "position": "center-right", "width": "38%"
}
```

Media element rendering notes: the box takes the **source media's real aspect ratio**
(16:9 is only a fallback when dimensions can't be read); there is no height field and no
crop control. `width` defaults to 30% and may auto-shrink to fit the frame from the
given `top`/`left`. A media element whose visual can't be resolved (no stock match,
failed generation) is **silently dropped** from the scene rather than failing the render.

## fontStyle object

Used by `subtitleStyle` (global + scene) and text-element `style`.

```jsonc
{
  "fontFamily": "Montserrat",          // from Fonts list; or provide fontUrl + any fontFamily
  "fontUrl": "https://.../font.ttf",   // custom font (then fontFamily is free-form, required)
  "fontSize": 64,                      // integer ≥ 1 (canvas px; see design guide for scale)
  "color": "rgb(255,255,255)",
  "backgroundColor": "rgba(0,0,0,0.6)",  // text box background; "rgba(0,0,0,0)" hides the default translucent strip
  "keywordColor": "rgb(255,200,40)",   // highlighted-keyword color (subtitles)
  "shadowColor": "rgb(0,0,0)",
  "shadowWidth": "2%",
  "position": "bottom-center",         // 9-grid preset (no "center" alias here — use "center-center")
  "alignment": "left",                 // left | center | right
  "decorations": ["bold"],            // bold | underline | italics | linethrough
  "case": "uppercase",                 // uppercase | lowercase | capitalize | smallcapitalize
  "paragraphWidth": "80%",
  "showBoxBackground": true,           // false hides the text background; on scene text elements supported only on environments with the style_utility fix (older ones ignore it — use transparent backgroundColor instead)
  "showBullet": false, "bulletSize": 12, "bulletFillColor": "rgb(255,200,40)",  // subtitle styles only
  "animations": [                      // 1-2 entries (one entry + one exit)
    { "name": "fade", "type": "entry", "speed": "medium" },
    { "name": "fade", "type": "exit",  "speed": "fast" }
  ]
}
```

**Text animations:** `name`: `none`, `fade`, `drift`, `wipe`, `text reveal`, `elastic`,
`typewriter`, `blur`, `bulletin`. `type`: `entry` | `exit`. `speed`: `slow` | `medium` |
`fast` | `custom` (with `customSpeedValue` ≥ 0.5). Optional: `direction`
(`up`/`down`/`left`/`right`), `writingStyle` (`character`/`word`/`line`/`paragraph`),
`futureWords` (`hidden`/`subtle`/`prominent`, only for `fade`/`blur`).

## Voice-over

```jsonc
"voiceOver": {
  "enabled": true,
  "aiVoices": [{
    "speaker": "Adison",               // voice name from the voices API
    "speed": 100,                      // 50-200, default 100
    "amplificationLevel": 0,           // -1 to 1
    "premiumVoiceSettings": {          // ElevenLabs voices only
      "modelId": "eleven_multilingual_v2",  // eleven_v3|eleven_multilingual_v2|eleven_flash_v2_5|eleven_turbo_v2_5|eleven_turbo_v2|eleven_flash_v2|eleven_multilingual_v1|eleven_monolingual_v1
      "stability": "60%", "similarityBoost": "75%", "style": "20%",
      "useSpeakerBoost": true
    }
  }]
  // OR "externalVoice": { "voiceUrl": "https://...", "syncVoice": true, "amplificationLevel": 0 }
}
```

`aiVoices` and `externalVoice` are mutually exclusive (globally and per-scene).

**Behavior notes:**
- Omitting `voiceOver` entirely produces a **silent video** — there is no implicit
  default narrator; subtitle timing is then estimated from text length. Always include
  a `voiceOver` block (with `enabled: false` for deliberately silent videos).
- Multiple `aiVoices` **rotate across scenes** (scene *i* uses voice *i* mod N) — useful
  for dialog-style videos, surprising otherwise. Use exactly one voice for a single
  narrator.
- If a speaker name can't be resolved (numeric id → name, case-insensitive → provider
  voice id), the job fails with an "invalid speaker" error.

## Background music

```jsonc
"backgroundMusic": {
  "enabled": true,
  "autoMusic": true,                   // Pictory picks a matching track
  // OR "musicUrl": "https://.../track.mp3",   (autoMusic and musicUrl are exclusive)
  "volume": 0.12,                      // 0-1 — ALWAYS SET THIS: omitted = full volume (1.0)
  "clips": [{ "start": 0, "end": 30 }] // optional, max 10
}
```

If `volume` is omitted, a newly added track plays at **full volume** and will drown the
narration — always set it explicitly (0.08-0.15 under voice-over). Scene-level
`backgroundMusic` accepts only `{ "enabled": bool }` (mute music for that scene); track
and volume cannot be changed per scene.

## Logo & avatar

```jsonc
"logo":   { "url": "https://.../logo.png", "position": "top-right", "width": "10%" },
"avatar": { "avatarId": "...", "position": "bottom-right", "width": "25%",
            "borderRadius": "50%", "backgroundColor": "rgba(0,0,0,0)", "hide": false }
```

Scene-level `avatar` override: `position` | `top`/`left`, `width`, `hide`,
`backgroundColor`, `borderRadius`, `borderColor`, `borderThickness`.

## Value formats

- **Colors:** `rgb(r,g,b)`, `rgba(r,g,b,a)`, or hex (`#RGB`, `#RRGGBB`, `#RRGGBBAA` — hex
  is normalized to rgba server-side). `colorOverlay.color` drops any alpha; use `opacity`.
- **Percentages:** strings `"0%"` to `"100%"` (integers only, no decimals).
- **colorOverlay:** `{ color, opacity }`, opacity 0-1, default 0.4.

## AI models

| Type | Model | Durations | Aspect ratios | Notes |
|---|---|---|---|---|
| image | `seedream3.0` | — | 1:1, 16:9, 9:16 | supports `referenceImageUrl` editing |
| image | `flux-schnell` | — | 1:1, 16:9, 9:16 | fast, no reference editing |
| image | `nanobanana` | — | 1:1 | supports reference editing |
| video | `veo3.1` | 4s, 6s, 8s | 16:9, 9:16 | highest quality |
| video | `veo3.1_fast` | 4s, 6s, 8s | 16:9, 9:16 | faster/cheaper |
| video | `pixverse5.5` | 5s, 8s, 10s | 16:9, 9:16, 1:1, 3:4, 4:3 | most aspect ratios |

`videoDuration` must match the model's allowed values and is forbidden for image models.

## Transitions

`none`, `wipeup`, `wipedown`, `wipeleft`, `wiperight`, `smoothleft`, `smoothright`,
`radial`, `circlecrop`, `hblur`, `fade`

## Fonts

Anton, Archivo Narrow, Arial, Averia Libre, Barlow, Barlow Black, Bebas Neue, Calibri,
Caprasimo, Capriola, Carter One, Caveat, Chakra Petch, Chewy, Comfortaa, Courier Prime,
Dancing Script, Dangrek, Delius Unicase, DM Sans, Grandstander, Gruppo, Heartbeat,
Helvetica, Helvetica Neue Medium, JM Modern, Josefin Sans, Julius Sans One, Laisha, Lato,
Lato Extrabold, Lexend, LT Wave, Manrope, Merriweather, Montserrat, Moon dance, Mustard,
Notosans, Opensans, Optik, Party Confetti, Patua One, Playfair Display, Plus Jakarta Sans,
Poppins, Poppins Extrabold, Proxima Nova, Quicksand, Raleway, Raleway Black, Raleway Thin,
Roboto, Rokkitt, Rowdies, Russo One, Satisfy, Sora, Source Sans Pro, Space Grotesk,
Space mono, Special Elite, Strive, Titillium Web, Titillium Web Black, Ubuntu, Unbounded,
Work Sans, Noto Sans JP, Noto Serif JP, Noto Sans Tamil, Noto Sans Devanagari,
Noto Serif Devanagari

## Shape catalog (`elements[].name`)

Basic: `rectangle`, `circle`, `line`

Featured: `badge-1`…`badge-8`, `quote-1`…`quote-6`, `arrow-1`…`arrow-19`,
`geometry-1`…`geometry-8`, `geometry-10`, `doodle-1`…`doodle-12`, `star-1`…`star-6`,
`cross-1`…`cross-8`, `checkmark-1`…`checkmark-6`, `data-device-1`…`data-device-8`,
`blob-1`…`blob-9`, `word-1`…`word-9`, `line-1`…`line-17`, `speech-bubble-2`…`speech-bubble-7`,
`square-1`…`square-5`, `heart-1`…`heart-3`, `thumbs-up`, `gift`, `leaves`, `paperplane`,
`idea-bulb`, `pill`

## Languages

Script `language`: ar, zh, nl, en, fr, de, hi, id, it, ja, ko, mr, pl, pt, ru, es, ta, tr, ur, vi

`audioLanguage` (audio/video repurpose scenes): en-US, en-AU, en-GB, en-IN, en-IE, en-AB,
en-WL, fr-CA, fr-FR, de-CH, de-DE, it-IT, es-ES, es-US, nl-NL, pt-BR, ja-JP, ko-KR, ru-RU,
hi-IN, ta-IN, mr-IN

## Visual search categories (`background.searchFilter.category`)

Aerial (+ Coastal_and_Marine, Infrastructure, Natural_Landscapes, Urban_Landscapes),
Animals (+ Farm_Animals, Marine_Life, Pets, Wildlife),
Business_and_Professions (+ Business_Concepts, Office_Work, Professions),
Effects (+ Chemical_Reactions, Explosions, Fire_and_Smoke, Glitches, Lighting_Effects, Particles),
Food_and_Beverage (+ Beverages, Food_Preparation, Meals),
Graphics (+ Backgrounds, Effects, Patterns),
Historical (+ Eras, Events, Figures),
Holidays_and_Celebrations (+ Cultural_Celebrations, Festivals, Life_Events),
Lifestyle (+ Health_and_Fitness, Hobbies, Home_and_Family),
Medical,
Nature (+ Landscapes, Plants_and_Trees, Sunrises_and_Sunsets, Waterfalls, Weather),
People (+ Activities, Groups, Portraits),
Places_and_Landmarks (+ Rural_Areas, Tourist_Attractions, Urban_Areas),
Sports_and_Recreation (+ Individual_Sports, Outdoor_Activities, Team_Sports),
Technology (+ Devices, Innovation)

Subcategory syntax: `"Parent/Child"`, e.g. `"Nature/Sunrises_and_Sunsets"`.
