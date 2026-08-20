import asyncio
import random

import httpx

from .models import ImageResult

_RECRAFT_URL = "https://external.api.recraft.ai/v1/images/generations"
_IDEOGRAM_URL = "https://api.ideogram.ai/v1/ideogram-v3/generate"

_MAX_RETRIES = 3
_TIMEOUT = 60.0

# Wrapper for .post(). Retries up to 3 times after delays
async def _post_with_retry(
    client: httpx.AsyncClient, url: str, **kwargs
) -> httpx.Response:
    response = None
    for attempt in range(_MAX_RETRIES + 1): # original request + 3 retries
        response = await client.post(url, **kwargs)
        if response.status_code != 429 or attempt == _MAX_RETRIES:
            return response
        retry_after = response.headers.get("retry-after")
        delay = float(retry_after) if retry_after else (2**attempt) + random.random()
        await asyncio.sleep(delay)
    return response

# API call and returns ImageResult object with url to created image or error message if something went wrong
async def generate_image_recraft(prompt: str, api_key: str) -> ImageResult:
    async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
        try:
            response = await _post_with_retry( # pauses gen function until response returns
                client,
                _RECRAFT_URL,
                headers={"Authorization": f"Bearer {api_key}"},
                json={
                    "prompt": prompt,
                    "model": "recraftv4_1_pro",
                    "size": "2048x2048",
                    "n": 1,
                },
            )
            response.raise_for_status() # gets status code. if error, jumps to except
            url = response.json()["data"][0]["url"] # gets url from result json
            return ImageResult(
                provider="recraft", prompt=prompt, source_url=url, success=True
            )
        except (httpx.HTTPError, KeyError, IndexError) as exc:
            return ImageResult(
                provider="recraft",
                prompt=prompt,
                source_url="",
                success=False,
                error=str(exc),
            )


async def generate_image_ideogram(prompt: str, api_key: str) -> ImageResult:
    async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
        try:
            response = await _post_with_retry(
                client,
                _IDEOGRAM_URL,
                headers={"Api-Key": api_key},
                json={
                    "prompt": prompt,
                },
            )
            response.raise_for_status()
            url = response.json()["data"][0]["url"]
            return ImageResult(
                provider="ideogram", prompt=prompt, source_url=url, success=True
            )
        except (httpx.HTTPError, KeyError, IndexError) as exc:
            return ImageResult(
                provider="ideogram",
                prompt=prompt,
                source_url="",
                success=False,
                error=str(exc),
            )

# Takes list of prompts from result of derive_visual_prompt() and provider (recraft/ideogram)
# and returns list[ImageResult] -- one result per prompt
async def generate_images_concurrent(
    prompts: list[str], provider: str
) -> list[ImageResult]:
    from .config import IDEOGRAM_API_KEY, RECRAFT_API_KEY

    # Tuple unpacking based on provider
    if provider == "recraft":
        api_key, fn = RECRAFT_API_KEY, generate_image_recraft
    elif provider == "ideogram":
        api_key, fn = IDEOGRAM_API_KEY, generate_image_ideogram
    else:
        raise ValueError(f"Unknown provider: {provider}")

    # For each prompt in list, calls fn(prompt, api_key) (doesn't run it immediately because fn is async)
    # *() unpacks generator expression because .gather expects each coroutine as separate arg
    # .gather() schedules all coroutines to run concurrently and returns a list of results in same order as coroutines passed in
    return await asyncio.gather(*(fn(prompt, api_key) for prompt in prompts))
