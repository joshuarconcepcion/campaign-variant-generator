import base64
from pathlib import Path

import httpx

_CAMPAIGNS_DIR = Path(__file__).resolve().parent.parent / "campaigns"


def get_campaign_dir(campaign_id: str) -> Path:
    campaign_dir = _CAMPAIGNS_DIR / campaign_id
    campaign_dir.mkdir(parents=True, exist_ok=True)
    return campaign_dir

# Downloads file in pieces and writes each piece to disk as it arrives
def save_image_from_url(url: str, save_path: Path) -> Path:
    save_path.parent.mkdir(parents=True, exist_ok=True)
    with httpx.stream("GET", url, timeout=60.0) as response:
        response.raise_for_status()
        with open(save_path, "wb") as f:
            for chunk in response.iter_bytes(): 
                f.write(chunk)
    return save_path


def save_image_from_b64(b64: str, save_path: Path) -> Path:
    save_path.parent.mkdir(parents=True, exist_ok=True)
    save_path.write_bytes(base64.b64decode(b64))
    return save_path
