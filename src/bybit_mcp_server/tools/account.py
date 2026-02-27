"""Account tools (read-only, requires API key)."""

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

from bybit_mcp_server.client import format_result, get_session

READ_ONLY = ToolAnnotations(readOnlyHint=True, openWorldHint=True)


def register_account_tools(mcp: FastMCP) -> None:
    @mcp.tool(annotations=READ_ONLY)
    async def get_wallet_balance(accountType: str, coin: str | None = None) -> str:
        """Get wallet balance and account risk information.

        Args:
            accountType: Account type - UNIFIED, CONTRACT, SPOT, OPTION, FUND
            coin: Coin name (e.g. BTC). If omitted, returns all coins with balance.
        """
        session = get_session()
        params: dict = {"accountType": accountType}
        if coin:
            params["coin"] = coin
        result = session.get_wallet_balance(**params)
        return format_result(result)

    @mcp.tool(annotations=READ_ONLY)
    async def get_fee_rate(
        category: str | None = None,
        symbol: str | None = None,
        baseCoin: str | None = None,
    ) -> str:
        """Get trading fee rate.

        Args:
            category: Product type - spot, linear, inverse, option
            symbol: Symbol name
            baseCoin: Base coin
        """
        session = get_session()
        params: dict = {}
        for key, val in [("category", category), ("symbol", symbol), ("baseCoin", baseCoin)]:
            if val is not None:
                params[key] = val
        result = session.get_fee_rates(**params)
        return format_result(result)

    @mcp.tool(annotations=READ_ONLY)
    async def get_account_info() -> str:
        """Get account margin mode and configuration info."""
        session = get_session()
        result = session.get_account_info()
        return format_result(result)
