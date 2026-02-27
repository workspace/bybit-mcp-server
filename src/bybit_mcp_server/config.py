"""Configuration loaded from environment variables."""

import os
from enum import Enum


class Mode(str, Enum):
    READ = "read"
    TRADE = "trade"
    FULL = "full"


# Permission hierarchy: which modes allow which permission levels
MODE_PERMISSIONS: dict[Mode, set[str]] = {
    Mode.READ: {"read"},
    Mode.TRADE: {"read", "trade"},
    Mode.FULL: {"read", "trade", "full"},
}


def get_mode() -> Mode:
    raw = os.getenv("BYBIT_MODE", "read").lower()
    try:
        return Mode(raw)
    except ValueError:
        return Mode.READ


def get_testnet() -> bool:
    return os.getenv("BYBIT_TESTNET", "true").lower() == "true"


def get_api_key() -> str | None:
    key = os.getenv("BYBIT_API_KEY", "")
    return key or None


def get_api_secret() -> str | None:
    secret = os.getenv("BYBIT_API_SECRET", "")
    return secret or None


def get_recv_window() -> int | None:
    raw = os.getenv("BYBIT_RECV_WINDOW", "")
    return int(raw) if raw else None
