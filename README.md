# pictory-claude-skills

Claude Code skills for creating videos with the [Pictory API](https://docs.pictory.ai).

## Skills

### `pictory-text-to-video`

Turns a text brief ("make a 60-second video about X") into a rendered video:

1. Plans the story arc and writes per-scene narration paced for voice-over.
2. Designs each scene — palettes, typography, text/shape/media overlay elements,
   color overlays, stock or AI-generated backgrounds, music, and transitions.
3. Builds the request body for `POST /v2/video/storyboard/render`, submits it, and
   polls the job until the video URL is ready.

## Prerequisites

- [Claude Code](https://claude.com/claude-code) installed (`npm install -g @anthropic-ai/claude-code`)
- Python 3.8+ (the bundled API helper script uses only the standard library)
- A Pictory account with API access

## Installing the skill

Clone this repository, then copy (or symlink) the skill directory into a Claude Code
skills folder. Claude Code discovers skills from two places:

**Option A — globally, available in every project:**

```bash
git clone <this-repo-url>
cd pictory-claude-skills
mkdir -p ~/.claude/skills
cp -r pictory-text-to-video ~/.claude/skills/
```

**Option B — for a single project only:**

```bash
mkdir -p /path/to/your/project/.claude/skills
cp -r pictory-text-to-video /path/to/your/project/.claude/skills/
```

Tip: use a symlink instead of `cp -r` if you want `git pull` on this repo to update the
installed skill automatically:

```bash
ln -s "$(pwd)/pictory-text-to-video" ~/.claude/skills/pictory-text-to-video
```

**Verify the install:** start Claude Code and run `/pictory-text-to-video` — the skill
should be listed and invocable. Skills are picked up on session start, so restart Claude
Code if it was already running.

## Adding your API key

### 1. Get a key

From the official guide at [docs.pictory.ai](https://docs.pictory.ai/):

1. **Create a Pictory account** — sign up for free at [app.pictory.ai](https://app.pictory.ai).
2. **Buy an API subscription** — click your profile picture in the top-right corner,
   select [API Subscription](https://app.pictory.ai/api-access), choose a plan based on
   how many videos you plan to create per month, and complete the purchase to activate
   API access.
3. **Copy your API key** — once the subscription is active, your API key is displayed on
   the same [API Subscription](https://app.pictory.ai/api-access) page. Click **Copy**
   and save it securely.

Keys start with `pictai_`. Treat the key like a password — anyone who has it can create
videos on your account; if it is ever exposed, regenerate it from the same page.

### 2. Make the key available to Claude Code

The skill reads the key from the `PICTORY_API_KEY` environment variable. Pick one:

**Shell profile (recommended for personal machines)** — add to `~/.zshrc` or
`~/.bashrc`, then open a new terminal:

```bash
export PICTORY_API_KEY=pictai_your_key_here
```

**Current session only** — export it in the terminal before launching Claude Code:

```bash
export PICTORY_API_KEY=pictai_your_key_here
claude
```

**Per project via Claude Code settings** — put it in the project's
`.claude/settings.local.json` (git-ignored by default) so it applies only to that
project:

```json
{
  "env": {
    "PICTORY_API_KEY": "pictai_your_key_here"
  }
}
```

> ⚠️ Never commit an API key. Use `settings.local.json` (not `settings.json`) for
> project-level keys, and keep keys out of shared dotfiles.

If the key is missing at runtime, the skill stops and asks you for it before making any
API call.

### 3. Optional: choose the API environment

| Environment variable | Required | Description |
|---|---|---|
| `PICTORY_API_KEY` | yes | Raw API key (`pictai_…`) from https://app.pictory.ai/api-access |
| `PICTORY_API_BASE_URL` | no | API base URL. Defaults to the Pictory dev environment; set to `https://api.pictory.ai/pictoryapis` for production |

### 4. Verify the setup

```bash
# should print "set"
echo ${PICTORY_API_KEY:+set}

# should list AI voices from the API (proves key + connectivity)
python3 ~/.claude/skills/pictory-text-to-video/scripts/pictory_api.py voices --language en
```

## Usage

In Claude Code, just ask:

> Create a 45-second vertical video about the benefits of morning workouts,
> energetic voice, upbeat music.

The skill gathers any missing choices (aspect ratio, voice-over, music, whether
AI-generated visuals are okay), shows a scene plan, renders with progress updates every
30 seconds, and returns the video URL. You can also invoke it explicitly with
`/pictory-text-to-video`.
