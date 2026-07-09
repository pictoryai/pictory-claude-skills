#!/usr/bin/env python3
"""Pictory API helper: submit renders, poll jobs, search visuals/music/voices.

Uses only the Python standard library. Configuration via environment:
  PICTORY_API_KEY       (required) raw API key, starts with "pictai_"
  PICTORY_API_BASE_URL  (optional) default: https://api.pictory.ai/pictoryapis (production);
                        set it in .env only to target another environment (e.g. dev)

Commands:
  render <payload.json>              Submit a render job, print jobId
  poll <jobId> [--interval N] [--timeout N]
                                     Poll a job until completed/failed
                                     (default: every 30s, 30 min max; prints a
                                     status heartbeat on every poll)
  render-and-wait <payload.json> [--interval N] [--timeout N]
                                     Submit then poll; prints final video URL
  search <keyword> [--category C]    Stock visual search (videos + images)
  voices [--language L] [--service S]
                                     List AI voice-over speakers
  music [--query Q] [--mood M] [--purpose P] [--max N]
                                     Search background music tracks
  music-options                      List valid music moods/genres/purposes
  lint <payload.json>                Check text wrap lines, on-shape label centering,
                                     and shape sizing before submitting (16:9, 9:16)

Exit codes: 0 success, 1 API/HTTP error or lint findings, 2 usage error,
3 job failed, 4 timeout.
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

DEFAULT_BASE_URL = "https://api.pictory.ai/pictoryapis"


def _load_dotenv():
    """Populate os.environ from a .env file so no shell `source` is needed (Windows-safe).

    Looks in CWD, then walks up from the script location; real env vars win over .env.
    """
    candidates = [os.path.join(os.getcwd(), ".env")]
    here = os.path.dirname(os.path.abspath(__file__))
    for _ in range(5):
        candidates.append(os.path.join(here, ".env"))
        here = os.path.dirname(here)
    for path in candidates:
        if not os.path.isfile(path):
            continue
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, value = line.partition("=")
                os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))
        return


_load_dotenv()


def _base_url():
    return os.environ.get("PICTORY_API_BASE_URL", DEFAULT_BASE_URL).rstrip("/")


def _api_key():
    key = os.environ.get("PICTORY_API_KEY")
    if not key:
        print(
            "ERROR: PICTORY_API_KEY is not set. Get a key at https://app.pictory.ai/api-access "
            "and export it, e.g.  export PICTORY_API_KEY=pictai_...",
            file=sys.stderr,
        )
        sys.exit(2)
    return key


def _request(method, path, body=None, query=None):
    url = _base_url() + path
    if query:
        url += "?" + \
            urllib.parse.urlencode(
                {k: v for k, v in query.items() if v is not None})
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        # Pictory uses the raw key in Authorization -- no "Bearer" prefix.
        # Cloudflare bot protection rejects urllib's default UA (403, error 1010).
        headers={
            "Authorization": _api_key(),
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")
        print(f"HTTP {e.code} on {method} {url}\n{detail}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Network error on {method} {url}: {e.reason}", file=sys.stderr)
        sys.exit(1)


def _load_payload(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"ERROR: cannot read payload {path}: {e}", file=sys.stderr)
        sys.exit(2)


def cmd_render(args):
    payload = _load_payload(args.payload)
    resp = _request("POST", "/v2/video/storyboard/render", body=payload)
    job_id = (resp.get("data") or {}).get("jobId")
    if not job_id:
        print(json.dumps(resp, indent=2), file=sys.stderr)
        print("ERROR: no jobId in response", file=sys.stderr)
        sys.exit(1)
    print(job_id)
    return job_id


def cmd_poll(args, job_id=None):
    job_id = job_id or args.job_id
    started = time.time()
    deadline = started + args.timeout
    while time.time() < deadline:
        resp = _request("GET", f"/v1/jobs/{job_id}")
        data = resp.get("data") or {}
        status = data.get("status")
        if status == "completed":
            print(json.dumps(data, indent=2))
            video_url = data.get("videoURL")
            if video_url:
                print(f"\nVIDEO_URL: {video_url}", file=sys.stderr)
            return
        if status == "failed" or resp.get("success") is False:
            print(json.dumps(data, indent=2), file=sys.stderr)
            print(
                f"JOB FAILED: {data.get('error_code')} - {data.get('error_message')}",
                file=sys.stderr,
            )
            sys.exit(3)
        # Heartbeat on every poll so the user always sees the system is still working.
        elapsed = int(time.time() - started)
        progress = data.get("renderProgress")
        detail = f" {progress}%" if progress not in (None, "") else ""
        detail += f" {data.get('renderProgressMessage')}" if data.get(
            "renderProgressMessage") else ""
        print(
            f"[{time.strftime('%H:%M:%S')}] still working — status: {status}{detail} "
            f"(elapsed {elapsed // 60}m{elapsed % 60:02d}s, next check in {args.interval}s)",
            file=sys.stderr,
        )
        time.sleep(args.interval)
    print(
        f"TIMEOUT: job {job_id} not finished after {args.timeout}s", file=sys.stderr)
    sys.exit(4)


def cmd_render_and_wait(args):
    job_id = cmd_render(args)
    cmd_poll(args, job_id=job_id)


def cmd_search(args):
    resp = _request(
        "GET",
        "/v1/media/search",
        query={"keyword": args.keyword,
               "category": args.category, "language": "en"},
    )
    results = (resp.get("data") or {}).get("searchResults") or []
    out = [
        {
            "assetId": r.get("assetId"),
            "mediaType": r.get("mediaType"),
            "duration": r.get("duration"),
            "description": r.get("mediaDescription"),
            "previewJpg": (r.get("preview") or {}).get("jpg"),
            "library": r.get("searchLibrary"),
        }
        for r in results[: args.max]
    ]
    print(json.dumps(out, indent=2))


def cmd_voices(args):
    resp = _request("GET", "/v1/voiceovers/tracks")
    tracks = resp if isinstance(resp, list) else (
        resp.get("data") or resp.get("tracks") or [])
    out = []
    for t in tracks:
        if args.language and not (t.get("language") or "").lower().startswith(args.language.lower()):
            continue
        if args.service and (t.get("service") or "").lower() != args.service.lower():
            continue
        out.append(
            {
                "id": t.get("id"),
                "name": t.get("name"),
                "gender": t.get("gender"),
                "language": t.get("language"),
                "accent": t.get("accent"),
                "engine": t.get("engine"),
                "service": t.get("service"),
            }
        )
    print(json.dumps(out, indent=2))


def cmd_music(args):
    body = {"page": 1, "pageSize": 20, "sort": "featured"}
    if args.query:
        body["query"] = args.query
    if args.mood:
        body["mood"] = [args.mood]
    if args.purpose:
        body["purpose"] = [args.purpose]
    resp = _request("POST", "/v1/music/search", body=body)
    data = resp.get("data") or resp
    items = data.get("items") or data.get(
        "searchResults") or data.get("tracks") or []
    out = [
        {
            "id": t.get("id"),
            "title": t.get("title"),
            "audioUrl": t.get("audioUrl"),
            "duration": t.get("duration"),
            "moods": t.get("moods"),
            "purposes": t.get("purposes"),
        }
        for t in items[: args.max]
    ]
    print(json.dumps(out, indent=2))


def cmd_music_options(_args):
    for label, path in [
        ("moods", "/v1/music/moods"),
        ("genres", "/v1/music/genres"),
        ("purposes", "/v1/music/purposes"),
    ]:
        resp = _request("GET", path)
        print(f"## {label}")
        # These endpoints return a bare list; render/search-style endpoints wrap in {data}.
        print(json.dumps(resp.get("data", resp) if isinstance(resp, dict) else resp, indent=2))


# --- payload layout lint -----------------------------------------------------
# Empirical renderer geometry, verified frame-by-frame against rendered videos:
# text is measured at fontSize*4/3 px on a reference canvas 1280x720 (16:9) or
# 720x1280 (9:16). Derived constants per aspect ratio, all in percent of frame:
#   chars/line ~ width% * WRAP / fontSize      (heuristic wrap budget, fallback only)
#   line height ~ fontSize / LINE              (vertical pitch per wrapped line)
#   cap height ~ fontSize / CAP                (digit/uppercase glyph height;
#                                               also the top -> optical-center offset)
# When the actual TTF is resolvable (Pictory CDN or Google Fonts, cached locally),
# line breaks are computed with real glyph metrics via Pillow instead.
_LINT_CONSTANTS = {"16:9": (1750, 4.5, 7.2), "9:16": (980, 8.0, 12.8)}
_SHAPE_ASPECTS = {"rectangle": 1.0, "circle": 1.0, "pill": 3.2, "line": 300 / 16}
_REF_WIDTH = {"16:9": 1280, "9:16": 720}
_TEXT_PADDING_EM = 0.25  # renderer pads the text span 0.25em per side
_FONT_CACHE_DIR = os.path.join(os.path.expanduser("~"), ".cache", "pictory-skill-fonts")
# Weight suffixes that appear inside Pictory family names ("Poppins Extrabold",
# "Barlow Black") -> the TTF weight-name candidates for that family's file.
_WEIGHT_SUFFIXES = {"extrabold": ["ExtraBold", "Black"], "black": ["Black", "ExtraBold"],
                    "thin": ["Thin", "Light"]}


def _pct(value):
    return float(str(value).rstrip("%"))


def _font_url_candidates(family, bold):
    """URL candidates for a family, derived by convention — no hard-coded font list.

    1. Pictory's public font CDN: /static/fonts/<Family_With_Underscores>/
       <FamilyNoSpaces>-<Weight>.ttf
    2. Google Fonts repo (the renderer's source for most catalog families):
       raw.githubusercontent.com/google/fonts/main/ofl/<familylower>/<FamilyNoSpaces>-<Weight>.ttf
       (plus the variable-font [wght] file some families ship instead).
    """
    base_family, weights = family, []
    last = family.split(" ")[-1].lower()
    if last in _WEIGHT_SUFFIXES:
        base_family = family[: -len(family.split(" ")[-1])].strip()
        weights = list(_WEIGHT_SUFFIXES[last])
    weights += ["Bold"] if bold else []
    weights += ["Regular"]

    compact = base_family.replace(" ", "")
    urls = []
    for weight in weights:
        urls.append("https://pictory-static.pictorycontent.com/static/fonts/"
                    f"{base_family.replace(' ', '_')}/{compact}-{weight}.ttf")
        urls.append("https://raw.githubusercontent.com/google/fonts/main/ofl/"
                    f"{base_family.replace(' ', '').lower()}/{compact}-{weight}.ttf")
    urls.append("https://raw.githubusercontent.com/google/fonts/main/ofl/"
                f"{base_family.replace(' ', '').lower()}/{compact}[wght].ttf")
    return urls


def _resolve_font(family, bold):
    """Download-and-cache the TTF for a family; None if unresolvable (offline/unknown)."""
    os.makedirs(_FONT_CACHE_DIR, exist_ok=True)
    key = f"{family.replace(' ', '_')}{'-b' if bold else ''}.ttf"
    cached = os.path.join(_FONT_CACHE_DIR, key)
    if os.path.exists(cached):
        return cached if os.path.getsize(cached) > 0 else None  # empty file = known miss
    for url in _font_url_candidates(family, bold):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "pictory-skill-lint"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = resp.read()
            with open(cached, "wb") as f:
                f.write(data)
            return cached
        except Exception:
            continue
    open(cached, "wb").close()  # cache the miss so we don't retry every run
    return None


def _measure_lines(text, style, font_px, box_px, ref_height):
    """Real-metrics greedy word wrap mirroring the renderer's splitTextIntoLines.

    Returns (line_count, pitch_pct, 'exact') with the actual TTF, or
    (None, None, 'approx') when the font can't be resolved or Pillow is missing.
    pitch_pct is the frame-height % between consecutive line tops: the renderer's
    line box is (ascent + descent + 0.2em padding) — calibrated against measured
    frames (Poppins fontSize 44 on 16:9: predicted 13.1%, measured 13.2%).
    """
    family = style.get("fontFamily", "Plus Jakarta Sans")
    bold = "bold" in (style.get("decorations") or [])
    if (style.get("case") or "").replace("case-", "") == "uppercase":
        text = text.upper()
    try:
        from PIL import ImageFont
        path = _resolve_font(family, bold)
        if not path:
            raise RuntimeError("font unresolved")
        font = ImageFont.truetype(path, size=max(1, round(font_px)))
        ascent, descent = font.getmetrics()
        pitch_pct = (ascent + descent + 0.2 * font_px) / ref_height * 100
        avail = box_px - 2 * _TEXT_PADDING_EM * font_px
        lines, current = 1, ""
        for word in text.split():
            trial = f"{current} {word}".strip()
            if font.getlength(trial) <= avail or not current:
                current = trial
            else:
                lines += 1
                current = word
        return lines, pitch_pct, "exact"
    except Exception:
        return None, None, "approx"


def cmd_lint(args):
    payload = _load_payload(args.payload)
    ar = payload.get("aspectRatio", "16:9")
    if ar not in _LINT_CONSTANTS:
        print(f"lint: aspect ratio {ar} not supported (16:9 and 9:16 only)", file=sys.stderr)
        sys.exit(2)
    wrap_c, line_c, cap_c = _LINT_CONSTANTS[ar]
    frame_ar = 16 / 9 if ar == "16:9" else 9 / 16
    ref_w = _REF_WIDTH[ar]
    problems, approx_fonts = [], set()

    for si, scene in enumerate(payload.get("scenes", []), 1):
        elements = scene.get("elements") or []
        shapes = [e for e in elements if e.get("type") == "shape"
                  and e.get("name") in _SHAPE_ASPECTS and "top" in e and "left" in e]
        # occupied rects for overlap detection: (desc, left, top, right, bottom, paired_shape_or_None)
        rects = []

        def _shape_h(el, w):
            if el["name"] == "rectangle" and not el.get("borderRadius"):
                return w  # plain sharp rectangle renders percent-square (frame-measured)
            return w * frame_ar / _SHAPE_ASPECTS[el["name"]]

        for el in elements:
            etype = el.get("type")
            if etype == "shape" and el.get("name") in _SHAPE_ASPECTS and "top" in el:
                w = _pct(el["width"])
                h = _shape_h(el, w)
                rects.append((f"{el['name']}", _pct(el["left"]), _pct(el["top"]),
                              _pct(el["left"]) + w, _pct(el["top"]) + h, None))
            elif etype in ("image", "video") and "top" in el and "left" in el:
                w = _pct(el.get("width", "30%"))
                h = w * frame_ar / 1.7778  # media box assumed 16:9 (approx)
                rects.append((f"{etype}~", _pct(el["left"]), _pct(el["top"]),
                              _pct(el["left"]) + w, _pct(el["top"]) + h, None))

        for el in elements:
            if el.get("type") != "text" or "top" not in el:
                continue
            style = el.get("style") or {}
            font = style.get("fontSize", 20)
            text, width = el.get("text", ""), _pct(el.get("width", "90%"))
            top = _pct(el["top"])
            font_px = font * 4 / 3
            ref_h = ref_w / frame_ar
            lines, pitch, mode = _measure_lines(text, style, font_px, width / 100 * ref_w, ref_h)
            if lines is None:
                lines = max(1, -(-len(text) // (width / 100 * wrap_c / font)))
                approx_fonts.add(style.get("fontFamily", "?"))
            line_h, cap_h = font / line_c, font / cap_c
            pitch = pitch if pitch is not None else line_h
            marker = "" if mode == "exact" else " (approx)"

            if lines > 2:
                problems.append(f"S{si} '{text[:30]}': wraps to {lines} lines{marker} — shorten or shrink")

            # text-on-shape pair: same left/width as a shape in this scene
            pair = next((s for s in shapes if s.get("left") == el.get("left")
                         and s.get("width") == el.get("width")), None)
            # occupied block: line-1 glyphs start ~capH/2 below top; last line adds a
            # descender/box allowance of ~capH/2 (frame-calibrated)
            block_h = 2 * cap_h + (lines - 1) * pitch
            rects.append((f"'{text[:18]}'{'x' + str(lines) if lines > 1 else ''}",
                          _pct(el["left"]), top, _pct(el["left"]) + width, top + block_h, pair))
            if not pair:
                continue
            label = f"S{si} '{text[:20]}' on {pair['name']}"
            s_top, s_w = _pct(pair["top"]), _pct(pair["width"])
            s_h = _shape_h(pair, s_w)
            s_center = s_top + s_h / 2
            if lines > 1:
                problems.append(f"{label}: label wraps to {lines} lines{marker} — on-shape labels must be single-line")
            if style.get("backgroundColor") != "rgba(0,0,0,0)":
                problems.append(f"{label}: missing transparent backgroundColor rgba(0,0,0,0)")
            want_top = s_center - cap_h - (lines - 1) / 2 * pitch
            slack = 2.5 if pair["name"] == "pill" else 1.0
            if abs(top - want_top) > slack:
                problems.append(f"{label}: top {top:.0f}% off-center — use {want_top:.0f}% "
                                f"(shape center {s_center:.1f}%)")
            min_h = 2.2 * cap_h + (lines - 1) * pitch
            if s_h < min_h:
                want_w = min_h * _SHAPE_ASPECTS[pair["name"]] / frame_ar
                problems.append(f"{label}: shape too small for fontSize {font} "
                                f"(height {s_h:.1f}% < {min_h:.1f}%) — widen shape to ~{want_w:.0f}%")

        # pairwise overlap within the scene, skipping label<->its own shape pairs
        def _is_own_shape(text_rect, other_rect):
            pair = text_rect[5]
            return (pair is not None
                    and abs(other_rect[1] - _pct(pair["left"])) < 0.01
                    and abs(other_rect[2] - _pct(pair["top"])) < 0.01)

        for i in range(len(rects)):
            for j in range(i + 1, len(rects)):
                a, b = rects[i], rects[j]
                if _is_own_shape(a, b) or _is_own_shape(b, a):
                    continue
                ox = min(a[3], b[3]) - max(a[1], b[1])
                oy = min(a[4], b[4]) - max(a[2], b[2])
                if ox > 1.0 and oy > 1.0:  # >1% bite in both axes
                    approx = " (approx)" if "~" in a[0] or "~" in b[0] else ""
                    problems.append(f"S{si} overlap: {a[0]} and {b[0]} intersect "
                                    f"{ox:.0f}%x{oy:.0f}%{approx}")

    if approx_fonts:
        print(f"note: heuristic metrics for unresolved fonts: {', '.join(sorted(approx_fonts))}",
              file=sys.stderr)
    if problems:
        print("\n".join(problems))
        sys.exit(1)
    print(f"lint OK: {sum(len(s.get('elements') or []) for s in payload.get('scenes', []))} elements, "
          f"no wrap/centering/sizing/overlap issues ({ar})")


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("render", help="submit a render job")
    p.add_argument("payload")
    p.set_defaults(func=cmd_render)

    p = sub.add_parser("poll", help="poll a job until done")
    p.add_argument("job_id")
    p.add_argument("--interval", type=int, default=30)
    p.add_argument("--timeout", type=int, default=1800)
    p.set_defaults(func=cmd_poll)

    p = sub.add_parser("render-and-wait", help="submit then poll")
    p.add_argument("payload")
    p.add_argument("--interval", type=int, default=30)
    p.add_argument("--timeout", type=int, default=1800)
    p.set_defaults(func=cmd_render_and_wait)

    p = sub.add_parser("search", help="stock visual search")
    p.add_argument("keyword")
    p.add_argument("--category")
    p.add_argument("--max", type=int, default=10)
    p.set_defaults(func=cmd_search)

    p = sub.add_parser("voices", help="list AI voices")
    p.add_argument("--language")
    p.add_argument("--service")
    p.set_defaults(func=cmd_voices)

    p = sub.add_parser("music", help="search background music")
    p.add_argument("--query")
    p.add_argument("--mood")
    p.add_argument("--purpose")
    p.add_argument("--max", type=int, default=10)
    p.set_defaults(func=cmd_music)

    p = sub.add_parser(
        "music-options", help="list music moods/genres/purposes")
    p.set_defaults(func=cmd_music_options)

    p = sub.add_parser("lint", help="check payload text wrap/centering/shape sizing")
    p.add_argument("payload")
    p.set_defaults(func=cmd_lint)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
