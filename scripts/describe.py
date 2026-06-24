"""Describe a local image file via an OpenAI-compatible vision model.

Configuration via environment variables (see .env.example):

    VISION_BASE_URL  — OpenAI-compatible API base URL (default: https://openrouter.ai/api/v1)
    VISION_API_KEY   — API key (required)
    VISION_MODEL     — Vision-capable model name (default: nvidia/nemotron-nano-12b-v2-vl:free)
    VISION_MAX_TOKENS— Max output tokens (default: 1024)

Supports any provider with an /chat/completions endpoint that accepts
image_url content blocks (OpenRouter, OpenAI, Ollama, vLLM, etc.).
"""
import base64
import json
import os
import sys
from pathlib import Path

import httpx

# ── Load .env from script directory (optional) ────────────────────────────
try:
    from dotenv import load_dotenv
    _env_path = Path(__file__).resolve().parent / ".env"
    if _env_path.exists():
        load_dotenv(_env_path)
except ImportError:
    pass

VISION_BASE_URL = os.getenv("VISION_BASE_URL", "https://openrouter.ai/api/v1")
VISION_API_KEY = os.getenv("VISION_API_KEY", "")
VISION_MODEL = os.getenv("VISION_MODEL", "nvidia/nemotron-nano-12b-v2-vl:free")
VISION_MAX_TOKENS = int(os.getenv("VISION_MAX_TOKENS", "1024"))

# Auth header format: "Bearer" for OpenAI/OpenRouter, "x-api-key" for DeepSeek, etc.
VISION_AUTH_HEADER = os.getenv("VISION_AUTH_HEADER", "Bearer")

# Extra JSON fields to merge into the request body (for provider-specific params)
_VISION_EXTRA_BODY = os.getenv("VISION_EXTRA_BODY", "")

MIME_MAP = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".webp": "image/webp",
    ".bmp": "image/bmp",
    ".tiff": "image/tiff",
    ".tif": "image/tiff",
}

DEFAULT_PROMPT = (
    "Describe this image in detail. "
    "Include all visible text, labels, numbers, chart elements, and key visual features."
)


def describe(path: str, question: str = DEFAULT_PROMPT) -> str:
    """Send image to vision model and return text description."""
    ext = Path(path).suffix.lower()
    mime = MIME_MAP.get(ext, "image/png")

    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()

    body = {
        "model": VISION_MODEL,
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": question},
                {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}},
            ],
        }],
        "max_tokens": VISION_MAX_TOKENS,
        "stream": False,
    }

    # Merge provider-specific extra params
    if _VISION_EXTRA_BODY:
        try:
            body.update(json.loads(_VISION_EXTRA_BODY))
        except json.JSONDecodeError:
            pass

    # Build auth header: "Bearer <key>" or "x-api-key: <key>" or custom
    if VISION_AUTH_HEADER.lower() in ("none", "no", "skip"):
        auth_value = VISION_API_KEY
    else:
        auth_value = f"{VISION_AUTH_HEADER} {VISION_API_KEY}".strip()

    headers = {
        "Authorization": auth_value,
        "Content-Type": "application/json",
    }

    resp = httpx.post(
        f"{VISION_BASE_URL.rstrip('/')}/chat/completions",
        headers=headers,
        json=body,
        timeout=120.0,
    )
    resp.raise_for_status()
    data = resp.json()

    # Parse response — handles minor format variations across providers
    choices = data.get("choices", [])
    if not choices:
        raise ValueError(f"No choices in response: {json.dumps(data, indent=2)[:300]}")
    choice = choices[0]
    # Standard path: choices[0].message.content
    if "message" in choice and "content" in choice["message"]:
        return choice["message"]["content"]
    # Fallback: choices[0].text (some simpler APIs)
    if "text" in choice:
        return choice["text"]
    raise ValueError(f"Unexpected response structure: {json.dumps(choice, indent=2)[:300]}")


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(
            "Usage: python describe.py <image_path> [question]\n"
            "\n"
            "Describe a local image file using a vision model.\n"
            "\n"
            "Environment variables:\n"
            "  VISION_API_KEY      API key (required)\n"
            "  VISION_BASE_URL     API base URL (default: OpenRouter)\n"
            "  VISION_MODEL        Model name\n"
            "  VISION_MAX_TOKENS   Max output tokens (default: 1024)\n"
            "  VISION_AUTH_HEADER  Auth prefix (default: Bearer)\n"
            "  VISION_EXTRA_BODY   JSON object merged into request body\n"
            "\n"
            "Examples:\n"
            "  python describe.py photo.jpg\n"
            "  python describe.py chart.png \"Top 3 values?\"\n"
        )
        sys.exit(0)

    if not VISION_API_KEY:
        print("Error: VISION_API_KEY environment variable is required.", file=sys.stderr)
        sys.exit(1)

    path = sys.argv[1]
    question = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_PROMPT

    try:
        result = describe(path, question)
        print(result)
    except httpx.HTTPStatusError as e:
        print(f"API error ({e.response.status_code}): {e.response.text[:500]}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(f"File not found: {path}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
