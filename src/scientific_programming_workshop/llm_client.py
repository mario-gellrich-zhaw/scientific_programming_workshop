"""OpenAI client helpers (API key loading and client creation)."""

from __future__ import annotations

import os
from typing import Optional

from dotenv import load_dotenv
from openai import OpenAI


def get_openai_api_key() -> Optional[str]:
    """Load and return the OPENAI_API_KEY (if present)."""
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key and api_key.strip():
        return api_key
    return None


def get_openai_client() -> OpenAI:
    """Create an OpenAI client.

    Raises:
        ValueError: if OPENAI_API_KEY isn't set.
    """
    api_key = get_openai_api_key()
    if not api_key:
        raise ValueError(
            "Please set OPENAI_API_KEY in a .env file (or as an environment variable)."
        )
    return OpenAI(api_key=api_key)
