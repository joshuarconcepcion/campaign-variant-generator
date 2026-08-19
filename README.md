# Campaign Variant Generator

AI-powered creative production pipeline: a campaign brief and brand style
guide go in, and the pipeline generates copy variants (Claude), matching
images (Recraft + Ideogram), and a browsable gallery of the results.

Portfolio project for AI Creative Technologist roles — optimized for
demo-ability and visual output.

## Status

**Phase 1 — core generation tools.** The `generator/` package (copy
generation, image generation, file persistence) is implemented and runnable
standalone via `examples/run_demo.py`. No frontend or API server yet.

## Stack

Python, FastAPI (later phases), Pydantic, Anthropic API, Recraft API,
Ideogram API, httpx + asyncio, Jinja2 (later phases), SQLite (later phases),
Docker (later phases).

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# fill in ANTHROPIC_API_KEY, RECRAFT_API_KEY, IDEOGRAM_API_KEY
```

## Run the Phase 1 demo

```bash
python -m examples.run_demo
```

This generates four headline variants for a sample campaign brief, derives
an image prompt per headline, generates matching images via Recraft, and
saves them to `campaigns/demo-run/`.

## Package layout

```
generator/
├── config.py       # loads and validates required API keys from .env
├── models.py        # CampaignBrief, HeadlineVariant, HeadlineSet, ImageResult
├── copy_tools.py     # Claude-based headline generation + visual prompt derivation
├── image_tools.py    # async Recraft/Ideogram image generation with 429 retry/backoff
└── file_tools.py     # save generated images, manage per-campaign directories
```

`config.py` fails loudly (raises `RuntimeError`) at import time if any of
`ANTHROPIC_API_KEY`, `RECRAFT_API_KEY`, or `IDEOGRAM_API_KEY` is missing.

## Note on third-party API shapes

The Recraft and Ideogram request/response shapes in `image_tools.py` reflect
each provider's documented image-generation endpoint at time of writing.
Verify against current provider docs before relying on them in production —
third-party APIs change independently of this repo.

## Roadmap

- **Phase 2** — HTML gallery assembly (Jinja2), SQLite campaign/run persistence
- **Phase 3** — FastAPI backend wrapping the pipeline
- **Phase 4** — web frontend (Next.js or plain HTML/JS), Docker packaging
