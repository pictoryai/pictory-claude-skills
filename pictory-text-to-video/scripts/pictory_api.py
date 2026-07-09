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
#   chars/line ~ width% * WRAP / fontSize      (wrap budget)
#   line height ~ fontSize / LINE              (vertical pitch per wrapped line)
#   cap height ~ fontSize / CAP                (digit/uppercase glyph height;
#                                               also the top -> optical-center offset)
_LINT_CONSTANTS = {"16:9": (1750, 4.5, 7.2), "9:16": (980, 8.0, 12.8)}
_SHAPE_ASPECTS = {"rectangle": 1.0, "circle": 1.0, "pill": 3.2, "line": 300 / 16}


def _pct(value):
    return float(str(value).rstrip("%"))


def cmd_lint(args):
    payload = _load_payload(args.payload)
    ar = payload.get("aspectRatio", "16:9")
    if ar not in _LINT_CONSTANTS:
        print(f"lint: aspect ratio {ar} not supported (16:9 and 9:16 only)", file=sys.stderr)
        sys.exit(2)
    wrap_c, line_c, cap_c = _LINT_CONSTANTS[ar]
    frame_ar = 16 / 9 if ar == "16:9" else 9 / 16
    problems = []

    for si, scene in enumerate(payload.get("scenes", []), 1):
        elements = scene.get("elements") or []
        shapes = [e for e in elements if e.get("type") == "shape"
                  and e.get("name") in _SHAPE_ASPECTS and "top" in e and "left" in e]
        for el in elements:
            if el.get("type") != "text" or "top" not in el:
                continue
            style = el.get("style") or {}
            font = style.get("fontSize", 20)
            text, width = el.get("text", ""), _pct(el.get("width", "90%"))
            top = _pct(el["top"])
            lines = max(1, -(-len(text) // (width / 100 * wrap_c / font)))
            line_h, cap_h = font / line_c, font / cap_c

            if lines > 2:
                problems.append(f"S{si} '{text[:30]}': wraps to {lines} lines "
                                f"(budget {width / 100 * wrap_c / font:.0f} chars/line) — shorten or shrink")

            # text-on-shape pair: same left/width as a shape in this scene
            pair = next((s for s in shapes if s.get("left") == el.get("left")
                         and s.get("width") == el.get("width")), None)
            if not pair:
                continue
            label = f"S{si} '{text[:20]}' on {pair['name']}"
            s_top, s_w = _pct(pair["top"]), _pct(pair["width"])
            s_h = s_w * frame_ar / _SHAPE_ASPECTS[pair["name"]]
            s_center = s_top + s_h / 2
            if lines > 1:
                problems.append(f"{label}: label wraps to {lines} lines — on-shape labels must be single-line")
            if (el.get("style") or {}).get("backgroundColor") != "rgba(0,0,0,0)":
                problems.append(f"{label}: missing transparent backgroundColor rgba(0,0,0,0)")
            want_top = s_center - cap_h - (lines - 1) / 2 * line_h
            if abs(top - want_top) > 1.0:
                problems.append(f"{label}: top {top:.0f}% off-center — use {want_top:.0f}% "
                                f"(shape center {s_center:.1f}%)")
            min_h = 2.2 * cap_h + (lines - 1) * line_h
            if s_h < min_h:
                want_w = min_h * _SHAPE_ASPECTS[pair["name"]] / frame_ar
                problems.append(f"{label}: shape too small for fontSize {font} "
                                f"(height {s_h:.1f}% < {min_h:.1f}%) — widen shape to ~{want_w:.0f}%")

    if problems:
        print("\n".join(problems))
        sys.exit(1)
    print(f"lint OK: {sum(len(s.get('elements') or []) for s in payload.get('scenes', []))} elements, "
          f"no wrap/centering/sizing issues ({ar})")


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
