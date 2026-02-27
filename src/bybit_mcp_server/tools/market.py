"""Market data tools (read-only)."""

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

from bybit_mcp_server.client import format_result, get_session

READ_ONLY = ToolAnnotations(readOnlyHint=True, openWorldHint=True)


def register_market_tools(mcp: FastMCP) -> None:
    @mcp.tool(annotations=READ_ONLY)
    async def get_server_time() -> str:
        """Get the current Bybit server time."""
        session = get_session()
        result = session.get_server_time()
        return format_result(result)

    @mcp.tool(annotations=READ_ONLY)
    async def get_tickers(category: str, symbol: str | None = None) -> str:
        """Get latest price ticker for a symbol.

        Args:
            category: Product type - spot, linear, inverse, option
            symbol: Trading pair (e.g. BTCUSDT). If omitted, returns all tickers for the category.
        """
        session = get_session()
        params: dict = {"category": category}
        if symbol:
            params["symbol"] = symbol
        result = session.get_tickers(**params)
        return format_result(result)

    @mcp.tool(annotations=READ_ONLY)
    async def get_kline(
        category: str,
        symbol: str,
        interval: str,
        start: int | None = None,
        end: int | None = None,
        limit: int | None = None,
    ) -> str:
        """Query kline/candlestick data.

        Args:
            category: Product type - spot, linear, inverse
            symbol: Symbol name (e.g. BTCUSDT)
            interval: Kline interval - 1,3,5,15,30,60,120,240,360,720,D,M,W
            start: Start timestamp in milliseconds
            end: End timestamp in milliseconds
            limit: Limit for data size per page (max 200, default 200)
        """
        session = get_session()
        params: dict = {"category": category, "symbol": symbol, "interval": interval}
        if start is not None:
            params["start"] = start
        if end is not None:
            params["end"] = end
        if limit is not None:
            params["limit"] = limit
        result = session.get_kline(**params)
        return format_result(result)

    @mcp.tool(annotations=READ_ONLY)
    async def get_instruments_info(
        category: str,
        symbol: str | None = None,
        status: str | None = None,
        baseCoin: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> str:
        """Query instrument specifications and trading rules.

        Args:
            category: Product type - spot, linear, inverse, option
            symbol: Symbol name
            status: Symbol status filter - Trading, Settling, etc.
            baseCoin: Base coin
            limit: Limit for data size per page
            cursor: Pagination cursor
        """
        session = get_session()
        params: dict = {"category": category}
        for key, val in [
            ("symbol", symbol),
            ("status", status),
            ("baseCoin", baseCoin),
            ("limit", limit),
            ("cursor", cursor),
        ]:
            if val is not None:
                params[key] = val
        result = session.get_instruments_info(**params)
        return format_result(result)

    @mcp.tool(annotations=READ_ONLY)
    async def get_orderbook(category: str, symbol: str, limit: int | None = None) -> str:
        """Query order book depth data.

        Args:
            category: Product type - spot, linear, inverse, option
            symbol: Symbol name (e.g. BTCUSDT)
            limit: Depth limit (spot: 1-200, default 1; derivatives: 1-500, default 25)
        """
        session = get_session()
        params: dict = {"category": category, "symbol": symbol}
        if limit is not None:
            params["limit"] = limit
        result = session.get_orderbook(**params)
        return format_result(result)

    @mcp.tool(annotations=READ_ONLY)
    async def get_funding_rate_history(
        category: str,
        symbol: str,
        startTime: int | None = None,
        endTime: int | None = None,
        limit: int | None = None,
    ) -> str:
        """Query historical funding rate.

        Args:
            category: Product type - linear, inverse
            symbol: Symbol name (e.g. BTCUSDT)
            startTime: Start timestamp in milliseconds
            endTime: End timestamp in milliseconds
            limit: Limit for data size per page (max 200, default 200)
        """
        session = get_session()
        params: dict = {"category": category, "symbol": symbol}
        for key, val in [("startTime", startTime), ("endTime", endTime), ("limit", limit)]:
            if val is not None:
                params[key] = val
        result = session.get_funding_rate_history(**params)
        return format_result(result)

    @mcp.tool(annotations=READ_ONLY)
    async def get_public_trades(
        category: str,
        symbol: str,
        baseCoin: str | None = None,
        optionType: str | None = None,
        limit: int | None = None,
    ) -> str:
        """Query recent public trading data.

        Args:
            category: Product type - spot, linear, inverse, option
            symbol: Symbol name (e.g. BTCUSDT)
            baseCoin: Base coin (for option only)
            optionType: Option type - Call, Put (for option only)
            limit: Limit for data size (spot: 1-60 default 60; others: 1-1000 default 500)
        """
        session = get_session()
        params: dict = {"category": category, "symbol": symbol}
        for key, val in [("baseCoin", baseCoin), ("optionType", optionType), ("limit", limit)]:
            if val is not None:
                params[key] = val
        result = session.get_public_trade_history(**params)
        return format_result(result)

    @mcp.tool(annotations=READ_ONLY)
    async def get_open_interest(
        category: str,
        symbol: str,
        intervalTime: str,
        startTime: int | None = None,
        endTime: int | None = None,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> str:
        """Get open interest for each symbol.

        Args:
            category: Product type - linear, inverse
            symbol: Symbol name (e.g. BTCUSDT)
            intervalTime: Interval - 5min, 15min, 30min, 1h, 4h, 1d
            startTime: Start timestamp in milliseconds
            endTime: End timestamp in milliseconds
            limit: Limit for data size per page (max 200, default 50)
            cursor: Pagination cursor
        """
        session = get_session()
        params: dict = {"category": category, "symbol": symbol, "intervalTime": intervalTime}
        for key, val in [
            ("startTime", startTime),
            ("endTime", endTime),
            ("limit", limit),
            ("cursor", cursor),
        ]:
            if val is not None:
                params[key] = val
        result = session.get_open_interest(**params)
        return format_result(result)
