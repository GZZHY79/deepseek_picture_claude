# read-image — Vision Skill for Claude Code

A Claude Code skill that lets Claude read and describe local image files. Works with any OpenAI-compatible vision API. Defaults to Zhipu GLM-4V-Flash (free), also supports OpenAI, OpenRouter, vLLM, etc.

- ⚡ **Lightweight** — one Python script, one dependency (`httpx`), nothing else
- 🔌 **Easy install** — marketplace (two commands) or manual (one copy)

## Why?

Claude Code's built-in `Read` tool refuses to send images to non-Anthropic API endpoints. If you use Claude Code with DeepSeek or any third-party LLM provider, reading images is broken — you just get `[Unsupported Image]`.

This skill bypasses the limitation by reading the image file directly and calling a vision model API, returning the text description to Claude.

## How it works

```
User: "What's in this chart?"  →  Skill triggers  →  Python script reads image
                                                       ↓
User sees text description     ←  Claude relays it  ←  Vision API returns text
```

## Installation & Configuration

Configuration is **required** — the skill won't work without an API key.

### Step 1: Install

**Marketplace (recommended):**
```bash
claude plugin marketplace add https://github.com/GZZHY79/deepseek_picture_claude
claude plugin install read-image
```

**Manual:**
```bash
mkdir -p ~/.claude/skills/
cp -r read-image ~/.claude/skills/
pip install httpx
```

### Step 2: Configure API key ⚠️ required

Add to `~/.claude/settings.json` (or project `.claude/settings.json`):

```json
{
  "env": {
    "VISION_API_KEY": "your-real-key-here",
    "VISION_BASE_URL": "https://open.bigmodel.cn/api/paas/v4",
    "VISION_MODEL": "GLM-4V-Flash"
  }
}
```

Be careful about the "{}" position
Get a free key at [open.bigmodel.cn/apikey/platform](https://open.bigmodel.cn/apikey/platform).

### Other providers

<details>
<summary>OpenRouter (free)</summary>

Get a key at [openrouter.ai/keys](https://openrouter.ai/keys):
```json
{
  "env": {
    "VISION_API_KEY": "sk-or-v1-...",
    "VISION_BASE_URL": "https://openrouter.ai/api/v1",
    "VISION_MODEL": "nvidia/nemotron-nano-12b-v2-vl:free"
  }
}
```
</details>

<details>
<summary>OpenAI</summary>

```json
{
  "env": {
    "VISION_API_KEY": "sk-...",
    "VISION_BASE_URL": "https://api.openai.com/v1",
    "VISION_MODEL": "gpt-4o-mini"
  }
}
```
</details>


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
| `VISION_BASE_URL` | `https://open.bigmodel.cn/api/paas/v4` | OpenAI-compatible base URL |
| `VISION_MODEL` | `GLM-4V-Flash` | Vision model name |

## Supported image formats

PNG, JPG/JPEG, GIF, WebP, BMP, TIFF.

## Troubleshooting

**`claude plugin marketplace add` hangs or times out:**
```bash
CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS=600000 claude plugin marketplace add https://github.com/GZZHY79/deepseek_picture_claude
```

**`VISION_API_KEY environment variable is required`:**
Make sure you completed [Step 2](#step-2-configure-api-key-%EF%B8%8F-required) — add the `env` block to your `settings.json`.

## License

MIT

---

Issues and suggestions welcome — [open an issue](https://github.com/GZZHY79/deepseek_picture_claude/issues)，I will check as soon as possible.
