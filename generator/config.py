import os

from dotenv import load_dotenv

load_dotenv()


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(
            f"Missing required environment variable: {name}. "
            "Set it in your .env file (see .env.example)."
        )
    return value


ANTHROPIC_API_KEY = _require_env("ANTHROPIC_API_KEY")
RECRAFT_API_KEY = _require_env("RECRAFT_API_KEY")
IDEOGRAM_API_KEY = _require_env("IDEOGRAM_API_KEY")
