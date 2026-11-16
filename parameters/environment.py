"""Load project settings from .env, preserving process environment overrides."""

import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv(Path(__file__).resolve().parents[1] / ".env")


_REQUIRED = object()


def setting(name: str, convert=str, *, default=_REQUIRED):
    value = os.environ.get(name)
    if value is None:
        if default is not _REQUIRED:
            return default
        raise ValueError(f"Missing setting {name}. Copy .env.example to .env.")
    try:
        return convert(value)
    except ValueError as error:
        raise ValueError(f"Invalid value for {name}: {value!r}") from error
