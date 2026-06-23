# read-image — Vision Skill for Claude Code

A Claude Code skill that lets Claude read and describe local image files. Works with any OpenAI-compatible vision API (OpenRouter, OpenAI, Ollama, vLLM, etc.).

## Why?

Claude Code's built-in `Read` tool refuses to send images to non-Anthropic API endpoints. If you use Claude Code with DeepSeek, Ollama, or any third-party LLM provider, reading images is broken — you just get `[Unsupported Image]`.

This skill bypasses the limitation by reading the image file directly and calling a vision model API, returning the text description to Claude.

## How it works

```
User: "What's in this chart?"  →  Skill triggers  →  Python script reads image
                                                       ↓
User sees text description     ←  Claude relays it  ←  Vision API returns text
```

## Installation

### Option A: Install from Marketplace (recommended)

```bash
# Add the marketplace
claude marketplace add <github-user>/read-image

# Enable the plugin
claude plugins install read-image@read-image
```

Or in `settings.json`:
```json
{
  "extraKnownMarketplaces": {
    "read-image": {
      "source": { "source": "github", "repo": "<github-user>/read-image" }
    }
  },
  "enabledPlugins": {
    "read-image@read-image": true
  }
}
```

### Option B: Manual install

```bash
# 1. Copy the skill into your user skills directory
cp -r read-image ~/.claude/skills/

# 2. Install dependencies
pip install httpx python-dotenv

# 3. Configure (see below)
```

## Configuration

Create a `.env` file in the skill's `scripts/` directory. The script auto-loads it on each run.

**Quick start — copy the template:**
```bash
cp .env.example scripts/.env
# then edit scripts/.env with your keys
```

**`.env` file format:**
```env
VISION_API_KEY=sk-or-v1-your-key-here
VISION_MODEL=nvidia/nemotron-nano-12b-v2-vl:free
# VISION_BASE_URL defaults to https://openrouter.ai/api/v1
```

> **Where is `scripts/` after marketplace install?**
> Run `claude plugins list` to find the plugin cache path, then put `.env` in its `scripts/` folder.
>
> **Manual install?** Just put `.env` next to `describe.py`.

### Provider examples

**OpenRouter (free, no credit card):**
```env
VISION_API_KEY=sk-or-v1-...      # https://openrouter.ai/keys
VISION_MODEL=nvidia/nemotron-nano-12b-v2-vl:free
```

**OpenAI:**
```env
VISION_API_KEY=sk-...
VISION_BASE_URL=https://api.openai.com/v1
VISION_MODEL=gpt-4o-mini
```

**Ollama (local):**
```env
VISION_BASE_URL=http://localhost:11434/v1
VISION_MODEL=llava:latest
VISION_API_KEY=ollama             # ignored, but required
```

## Usage

Once installed and configured, just ask Claude:

> "Read this image: /path/to/screenshot.png"
>
> "What does this chart show? ~/Downloads/results.png"
>
> "Analyze this diagram: /tmp/architecture.jpg"

## Configuration reference

| Variable | Default | Description |
|----------|---------|-------------|
| `VISION_API_KEY` | *(required)* | API key for your vision provider |
| `VISION_BASE_URL` | `https://openrouter.ai/api/v1` | OpenAI-compatible base URL |
| `VISION_MODEL` | `nvidia/nemotron-nano-12b-v2-vl:free` | Vision model name |
| `VISION_MAX_TOKENS` | `1024` | Max output tokens |
| `VISION_AUTH_HEADER` | `Bearer` | Auth header prefix (`x-api-key` for DeepSeek) |
| `VISION_EXTRA_BODY` | *(none)* | JSON object merged into request body |

## Supported image formats

PNG, JPG/JPEG, GIF, WebP, BMP, TIFF.

## License

MIT
