---
name: pictory-text-to-video
description: Create professional videos from text using the Pictory API. Use when the user wants to create, render, or generate a video from a topic, script, blog post, or brief — plans scenes, designs layouts with text/shape/media elements, adds voice-over, music, and stock or AI-generated visuals, then submits the render job and polls until the video URL is ready.
---

# Pictory Video Creation

Turn a text brief into a rendered video by authoring a storyboard request for
`POST /v2/video/storyboard/render`, submitting it, and polling the job until the video
URL is ready. You are the video's writer, art director, and editor — the API only
executes what the request body describes, so the quality of the video is the quality of
your request.

## Reference files

Read these before building the request — do not work from memory:

- **references/design-guide.md** — creative direction (concept, motif, mood), story
  arcs, narration pacing, palettes, typography, layout recipes, visual selection, audio.
  Read this FIRST, always.
- **references/request-schema.md** — every field, enum, and validation rule of the
  request body. Read before writing JSON.
- **references/api-endpoints.md** — auth, render/poll endpoints, visual/music/voice
  search APIs, discovery endpoints, pitfalls.
- **references/examples.md** — five complete, valid request bodies (designed 16:9
  explainer; AI-background 9:16 short; product teaser with AI-generated image/video
  elements; two tutorial diagrams with connected shape blocks — horizontal pipeline
  and vertical layer stack).

## Prerequisites

1. **API key** — read from the `PICTORY_API_KEY` environment variable
   (`echo ${PICTORY_API_KEY:+set}`). If unset, ask the user for their key (from
   https://app.pictory.ai/api-access) and have them export it. Never print the key.
2. **Base URL** — `PICTORY_API_BASE_URL` env var if set, otherwise the default in
   `scripts/pictory_api.py` (Pictory production, `https://api.pictory.ai/pictoryapis`).
   Set `PICTORY_API_BASE_URL` in `.env` only when a non-production environment is needed.

## Workflow

### Step 1 — Gather the brief

From the user's message, establish: topic/script, target platform & aspect ratio,
approximate length, language, and tone. If not stated, ask — one batched question
covering the open choices, typically:

- **Aspect ratio / platform** (16:9 YouTube, 9:16 Shorts/Reels, 1:1 feed)
- **Voice-over?** (AI voice yes/no; any gender/style preference)
- **Background music?** (auto-picked vs a mood/genre preference vs none)
- **AI-generated visuals?** — stock footage is free; AI images are cheap; AI *video*
  costs real credits (≈1.6-20 credits/sec). Default to stock unless the user opts in.
- Anything brand-specific (colors, logo URL, brand kit)

Sensible defaults if the user says "you decide": 16:9, ~45-60s, voice-over on, autoMusic
at low volume, stock visuals, `saveProject: true`.

### Step 2 — Write the script and scene plan

Follow references/design-guide.md: pick the arc for the topic shape, write per-scene
narration at **~2.5 words/second** against each scene's duration budget, and keep
on-screen text down to headlines. Show the user a compact scene plan (scene number,
narration one-liner, visual concept, layout type) before building the full JSON — for
short videos or an explicit "just do it", proceed directly.

### Step 3 — Build the request body

Author the full JSON against references/request-schema.md:

- One palette + one font pairing for the whole video; every text-over-footage scene gets
  a `colorOverlay`; designed scenes set `hideSubtitles: true`; vary layouts scene to scene.
- Every text element declares a `textVariant` (`heading`/`subheading`/`body`) as its
  semantic base; percentages (`top`/`left`/`width`) are integer strings like `"11%"`.
- Stock visuals via `background.searchFilter.query` with action-first queries (the
  render engine picks the asset). Optionally sanity-check queries with
  `scripts/pictory_api.py search "<query>"` to confirm good footage exists.
- AI visuals via `aiVisual` only if the user opted in (Step 1).
- Voice: use a known-good default speaker (e.g. `Martin` for English) or list options
  with `scripts/pictory_api.py voices --language en`. Never invent speaker names,
  avatar/brand/template IDs — discover them (see api-endpoints.md).
- Music: `{"enabled": true, "autoMusic": true, "volume": 0.12}` unless the user wants a
  specific mood — then pick a track via `scripts/pictory_api.py music --mood <Mood>` and
  pass its `audioUrl` as `musicUrl`.

Save the payload to a file (e.g. `video-request.json` in the scratchpad), run the
design-guide quality checklist against it, then run
`python3 scripts/pictory_api.py lint video-request.json` — it mechanically verifies
text wrap lines, on-shape label centering, chip sizing, and transparent label
backgrounds. Fix every finding before submitting.

### Step 4 — Render and poll

```bash
python3 scripts/pictory_api.py render-and-wait video-request.json
```

Or separately: `render` (prints jobId) then `poll <jobId>`. Polling checks
`GET /v1/jobs/{jobId}` every 30 seconds with a 30-minute maximum, printing a heartbeat
line on every poll (status, render progress, elapsed time) so the user can see the
system is still working. Renders typically take a few minutes (longer with AI visuals).
Relay those progress updates to the user rather than going silent; if the 30-minute
timeout is hit (exit code 4), give the user the jobId so the job can be polled again
later — the render may still complete server-side.

### Step 5 — Deliver

When the job completes, give the user:

- **`data.videoURL`** — the rendered MP4 (plus `videoShareURL` / `thumbnail` if useful)
- Duration (`videoDuration`) and, if AI visuals were used, `aiCreditsUsed`
- The saved project note (if `saveProject: true`, it's editable at app.pictory.ai)
- Offer one round of concrete revisions (rewording a scene, different visual, new voice)
  — apply edits to the same payload file and re-render.

## Error handling

- **400 INVALID_REQUEST_BODY** — the response's `fields[]` names each bad field; fix the
  payload and resubmit. Remember: unknown fields are silently *stripped*, so a typo'd
  field won't error — it just won't apply.
- **Job `failed`** — `data.error_message` is specific (e.g. an invalid speaker name);
  fix and resubmit.
- **401** — bad/missing key; re-check `PICTORY_API_KEY`.
- Common traps: `Bearer` prefix (don't), `brandId`+`brandName` together,
  `subtitleStyleId`+`subtitleStyleName` together, avatar without `voiceOver.enabled`,
  `videoWidth` without `videoHeight`, narration overshooting scene duration budgets.
