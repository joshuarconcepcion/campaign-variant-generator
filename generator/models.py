from pydantic import BaseModel


class HeadlineVariant(BaseModel):
    headline: str
    tone: str
    reasoning: str


class HeadlineSet(BaseModel):
    variants: list[HeadlineVariant]


class ImageResult(BaseModel):
    provider: str  # "recraft" | "ideogram"
    prompt: str
    file_path: str
    success: bool
    error: str | None = None


class CampaignBrief(BaseModel):
    product: str
    key_message: str
    target_audience: str
    tone: str
    style_guide: str
