"""Bybit MCP Server implementation."""

import json
import os

from mcp.server.fastmcp import FastMCP
from pybit.unified_trading import HTTP

mcp = FastMCP("bybit-mcp-server")


def _get_session() -> HTTP:
    """Create a pybit HTTP session from environment variables."""
    testnet = os.getenv("BYBIT_TESTNET", "true").lower() == "true"
    api_key = os.getenv("BYBIT_API_KEY", "")
    api_secret = os.getenv("BYBIT_API_SECRET", "")

    return HTTP(
        testnet=testnet,
        api_key=api_key or None,
        api_secret=api_secret or None,
    )


@mcp.tool()
async def get_tickers(category: str, symbol: str | None = None) -> str:
    """Get latest price ticker for a symbol.

    Args:
        category: Product type - spot, linear, inverse, option
        symbol: Trading pair (e.g. BTCUSDT). If omitted, returns all tickers for the category.
    """
    session = _get_session()
    params: dict = {"category": category}
    if symbol:
        params["symbol"] = symbol
    result = session.get_tickers(**params)
    return json.dumps(result["result"], indent=2)


@mcp.tool()
async def get_server_time() -> str:
    """Get the current Bybit server time."""
    session = _get_session()
    result = session.get_server_time()
    return json.dumps(result["result"], indent=2)


def main():
    """Run the MCP server."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
