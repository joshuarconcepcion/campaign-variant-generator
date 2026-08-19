from typing import Literal

from pydantic import BaseModel

# Single generated headline (returned by generate_headlines)
class HeadlineVariant(BaseModel):
    headline: str
    tone: str
    reasoning: str

# List of HeadlineVariant (thin wrapper)
# Used instead of list[HeadlineVariant] because Pydantic needs model with JSON object shape
class HeadlineSet(BaseModel):
    variants: list[HeadlineVariant]

# Normalized result of one image generation attempt
class ImageResult(BaseModel):
    provider: Literal["recraft", "ideogram"] # rejects typos
    prompt: str
    source_url: str # holds provider's returned URL
    local_path: str | None = None # based on whether file has been downloaded to disk
    success: bool
    error: str | None = None

# Input for pipeline, five fields represent creative brief
class CampaignBrief(BaseModel):
    product: str
    key_message: str
    target_audience: str
    tone: str
    style_guide: str
