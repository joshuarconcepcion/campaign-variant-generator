from anthropic import Anthropic

from .config import ANTHROPIC_API_KEY
from .models import CampaignBrief, HeadlineSet, HeadlineVariant

_MODEL = "claude-opus-5"

_client = Anthropic(api_key=ANTHROPIC_API_KEY)


def generate_headlines(brief: CampaignBrief, n: int) -> HeadlineSet:
    prompt = (
        f"Generate {n} distinct headline variants for this ad campaign.\n\n"
        f"Product: {brief.product}\n"
        f"Key message: {brief.key_message}\n"
        f"Target audience: {brief.target_audience}\n"
        f"Tone: {brief.tone}\n"
        f"Style guide: {brief.style_guide}\n\n"
        "Give each variant a genuinely distinct angle or tone — don't just "
        "reword the same idea. For each, explain in one sentence why it "
        "would resonate with the target audience."
    )

    response = _client.messages.create(
        model=_MODEL,
        max_tokens=4096,
        output_config={
            "effort": "medium",
            "format": {
                "type": "json_schema",
                "schema": HeadlineSet.model_json_schema(),
            },
        },
        messages=[{"role": "user", "content": prompt}],
    )

    text_block = next(block for block in response.content if block.type == "text")
    return HeadlineSet.model_validate_json(text_block.text)


def derive_visual_prompt(headline: HeadlineVariant, brief: CampaignBrief) -> str:
    prompt = (
        "Turn this headline into a concise, vivid prompt for an AI image "
        "generation model. Describe the subject, scene, lighting, and "
        "composition in a couple of sentences. Reflect the brand's style "
        "guide. Do not describe any text or lettering appearing in the "
        "image. Return only the image prompt — no preamble, no quotes.\n\n"
        f"Headline: {headline.headline}\n"
        f"Tone: {headline.tone}\n"
        f"Product: {brief.product}\n"
        f"Style guide: {brief.style_guide}"
    )

    response = _client.messages.create(
        model=_MODEL,
        max_tokens=512,
        output_config={"effort": "low"},
        messages=[{"role": "user", "content": prompt}],
    )

    text_block = next(block for block in response.content if block.type == "text")
    return text_block.text.strip()
