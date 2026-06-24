---
name: read-image
description: |
  Read and describe local image files (PNG, JPG, GIF, WebP, BMP) using a vision model.
  Use this skill whenever the user wants to view, read, describe, analyze, or extract text from an image file.
  Also use when the user references an image by path and wants to know what's in it.
  Trigger on phrases like: "read this image", "what's in this picture", "describe this image",
  "analyze this chart", "check this screenshot", "what does this image show", or any mention of an image file.
---

# Read Image

Use the bundled `scripts/describe.py` script to send a local image to a vision model
via any OpenAI-compatible `/chat/completions` endpoint (Zhipu GLM-4V-Flash by default, also supports OpenAI, OpenRouter, etc.).

## Setup (required on first use)

Set these environment variables before using the skill:

```
VISION_API_KEY=your-api-key       # required
VISION_BASE_URL=...               # optional, defaults to Zhipu (GLM-4V-Flash)
VISION_MODEL=...                  # optional, defaults to GLM-4V-Flash
```

See [README.md](README.md) for detailed setup instructions and provider examples.

## Usage

Run the bundled script with `python` (or `python3`) and an absolute image path:

```bash
python "{skill_dir}/scripts/describe.py" "/absolute/path/to/image.png"
```

With a specific question:
```bash
python "{skill_dir}/scripts/describe.py" "/absolute/path/to/image.png" "What does the red line represent?"
```

> **Note:** `{skill_dir}` is the directory containing this SKILL.md file.
> Use `python` or `python3` — whichever is available. The script requires the `httpx` package.

## Supported formats

PNG, JPG/JPEG, GIF, WebP, BMP, TIFF.

## Output

The script prints the model's text description to stdout. Relay it directly to the user.
