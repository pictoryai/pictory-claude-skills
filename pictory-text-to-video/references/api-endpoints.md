# Pictory API — Endpoints, Auth, and Job Polling

## Base URL

The base URL comes from the `PICTORY_API_BASE_URL` environment variable. Defaults:

`https://api.pictory.ai/pictoryapis`

Version prefixes are mixed and must be exact: render/preview/projects/transcription use
`/v2/`; jobs, media, music, voiceovers, aistudio, avatars, brands, styles, smartlayouts,
templates use `/v1/`.

## Authentication

Every request sends the raw API key in the `Authorization` header — **no `Bearer` prefix**:

```
Authorization: pictai_xxxxxxxxxxxxxxxx
Content-Type: application/json
```

Keys start with `pictai_` and come from https://app.pictory.ai/api-access. A 401 returns
`{"message": "Unauthorized"}`.

Read the key from the `PICTORY_API_KEY` environment variable. If it is not set, ask the
user for it — never invent or hard-code a key.

## Render a video

```
POST {base}/v2/video/storyboard/render
```

Body: the full storyboard request (see request-schema.md). Response:

```json
{ "success": true, "data": { "jobId": "265a7c1a-4985-4058-9208-68114f131a2b" } }
```

A 400 returns `{"code": "INVALID_REQUEST_BODY", "message": "...", "fields": [{"name": "scenes", "errors": "..."}]}` —
read `fields[]` to fix the payload and retry.

## Poll job status

```
GET {base}/v1/jobs/{jobId}
```

Poll every 30 seconds with a 30-minute cap — the helper script's defaults
(`--interval 30 --timeout 1800`) — and report a status heartbeat to the user on every
poll. Renders typically take a few minutes; AI-generated visuals add more.
`data.status` is `in-progress`, `completed`, or `failed`.

In progress:

```json
{ "job_id": "...", "success": true,
  "data": { "status": "in-progress", "renderProgress": 42,
            "renderProgressMessage": "Generating video", "renderState": "RUNNING" } }
```

Completed — the video URL is **`data.videoURL`**:

```json
{ "job_id": "...", "success": true,
  "data": { "status": "completed", "progress": 100,
            "videoURL": "https://.../video.mp4",
            "videoShareURL": "https://video.pictory.ai/...",
            "thumbnail": "https://.../thumb.jpg",
            "srtFile": "...", "vttFile": "...", "txtFile": "...",
            "videoDuration": 65.6, "aiCreditsUsed": 48 } }
```

Failed:

```json
{ "job_id": "...", "success": false,
  "data": { "status": "failed", "error_code": "TEXT_TO_VIDEO_FAILED",
            "error_message": "The AI voice speaker [Timm] is invalid..." } }
```

An unknown job returns `error_code: "5000"`, `error_message: "JOB_NOT_FOUND"`.

Alternative to polling: pass a `webhook` URL in the render body; Pictory POSTs the result
there on completion.

## Preview-first flow (optional)

1. `POST {base}/v2/video/storyboard` — same body as render; creates a preview job.
2. Poll `GET {base}/v1/jobs/{jobId}` until completed; review the storyboard.
3. `PUT {base}/v2/video/render/{storyboardJobId}` — render the reviewed preview
   (body optional: `{ "webhook": "..." }`). The path param is the **preview job id**.

Use this when the user wants to check scenes before spending render credits.

## Visual search (stock footage/images)

```
GET {base}/v1/media/search?keyword={query}&language=en[&category={category}]
```

Response items: `assetId`, `mediaType` (`video` | `image`), `duration`,
`mediaDescription`, `preview.url` / `preview.jpg` (watermarked, token-expiring),
`searchLibrary` (`story_blocks` | `getty`).

Use this to *verify* that good stock exists for a query, or to show the user options.
For the actual render, prefer putting the query in the scene's
`background.searchFilter.query` — the service picks the best full-resolution asset for
each scene and automatically avoids reusing an asset another scene already took.
Do **not** paste watermarked preview URLs into `visualUrl`.

## Music search

```
POST {base}/v1/music/search
```

Body (all optional): `query`, `page` (≥1), `pageSize` (20-100), `sort`
(`latest`|`shuffle`|`featured`), array filters `genreGroup`, `genre`, `mood`,
`instrument`, `purpose` (each with a `not*` negation variant), `minDuration`,
`maxDuration` (seconds). Filter values are case-sensitive; get exact values from:

- `GET {base}/v1/music/moods`
- `GET {base}/v1/music/genres`
- `GET {base}/v1/music/genres/groups`
- `GET {base}/v1/music/instruments`
- `GET {base}/v1/music/purposes`

Result items include `id`, `title`, `audioUrl`, `duration`, `genres[]`, `moods[]`,
`purposes[]`. To use a track in a render, pass its `audioUrl` as
`backgroundMusic.musicUrl`. Simpler default: `backgroundMusic: { enabled: true, autoMusic: true }`.

## Voices

```
GET {base}/v1/voiceovers/tracks
```

Returns voice objects: `id` (numeric), `name` (e.g. `Joanna`), `voice` (provider id),
`gender`, `accent`, `language` (e.g. `en-US`), `engine` (`neural`/`standard`/...),
`service` (`aws` | `google` | `elevenlabs`), `sample` (mp3 preview URL).

`voiceOver.aiVoices[].speaker` accepts a numeric track id, a voice **name**
(e.g. `"Brian"`), or a provider voice id (e.g. an ElevenLabs voice UUID).
`premiumVoiceSettings` only works with `service: "elevenlabs"` voices.

Documented default voices by language when the user has no preference: en `Martin`,
nl `Tim`, fr `Gabriel`, de `Wilbur`, it `Marco`, pt `Aurelio`, es `Hugo`. For other
languages, list the tracks and pick a native voice.

## Standalone AI visual generation (AI Studio)

Usually unnecessary — in-render `aiVisual` on backgrounds/elements is preferred because
the render pipeline handles generation, billing, and placement. Standalone endpoints
exist for pre-generating assets:

- `POST {base}/v1/aistudio/images` — body: `prompt` (5-5000 chars), `model`
  (`seedream3.0` default, `flux-schnell`, `nanobanana`, `nanobanana-pro`), `aspectRatio`,
  `style`, `referenceImageUrl`, `webhook`. Returns a `jobId`; completed job has `data.url`.
- `POST {base}/v1/aistudio/videos` — body: `prompt`, `model` (`pixverse5.5` default,
  `veo3.1`, `veo3.1_fast`), `aspectRatio`, `duration`, one of `firstFrameImageUrl` |
  `extendVideoUrl` | `referenceImageUrls`, `webhook`.

AI credit costs — images: flux-schnell 0.6, seedream3.0 2, nanobanana 4 per image.
Video: veo3.1 20/sec, veo3.1_fast 10/sec, pixverse5.5 1.6/sec. Mention rough cost when
the user requests many AI-generated scenes.

## Discovery endpoints — never invent these IDs

| Field | Endpoint |
|---|---|
| `avatar.avatarId` | `GET {base}/v1/avatars` |
| `brandId` / `brandName` | `GET {base}/v1/brands/video` |
| `templateId` | `GET {base}/v2/projects` or `GET {base}/v1/templates` |
| `smartLayoutId` / `smartLayoutName` | `GET {base}/v1/smartlayouts` |
| `subtitleStyleId` / `subtitleStyleName` | `GET {base}/v1/styles` |
| `voiceOver.aiVoices[].speaker` | `GET {base}/v1/voiceovers/tracks` |

Other useful endpoints: `GET {base}/v1/quota`, `GET {base}/v1/aicredits/usage`,
`POST {base}/v1/media/generateurl` (signed upload URL for user files),
`GET {base}/v1/jobs` (list jobs).

## Common pitfalls

- **No `Bearer` prefix** on the Authorization header — the raw key is the value.
- `videoName` is required on render requests.
- `brandId` + `brandName` together → rejected. Same for `subtitleStyleId` + `subtitleStyleName`.
- `avatar.avatarId` is set once at the **top level**; per-scene `avatar` is
  position/style overrides only.
- Renders are not saved to My Projects unless `saveProject: true`.
- Any scene with `elements` (or `aiVisual`, `colorOverlay`, `maxSubtitleLines`, smart
  layouts, avatars) is routed to the v3 storyboard engine automatically — do not set
  `storyboardVersion` manually; any explicit value other than `"v3"` forces v2 and
  breaks those features.
- Omitting `voiceOver` entirely renders a **silent** video — there is no default narrator.
- Omitting `backgroundMusic.volume` plays the music at **full volume** — always set it.
- Unknown/misspelled fields are silently stripped by validation, not rejected.
