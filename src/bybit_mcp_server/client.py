"""Pybit HTTP session factory."""

import json

from pybit.unified_trading import HTTP

from bybit_mcp_server.config import get_api_key, get_api_secret, get_recv_window, get_testnet


def get_session() -> HTTP:
    """Create a new pybit HTTP session from environment config."""
    kwargs: dict = {
        "testnet": get_testnet(),
        "api_key": get_api_key(),
        "api_secret": get_api_secret(),
    }
    recv_window = get_recv_window()
    if recv_window is not None:
        kwargs["recv_window"] = recv_window
    return HTTP(**kwargs)


def format_result(result: dict) -> str:
    """Extract the 'result' key from pybit response and format as JSON string."""
    return json.dumps(result["result"], indent=2)
