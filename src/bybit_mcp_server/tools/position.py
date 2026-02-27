"""Position tools."""

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

from bybit_mcp_server.client import format_result, get_session
from bybit_mcp_server.decorators import register_impl, require_confirmation, require_mode

READ_ONLY = ToolAnnotations(readOnlyHint=True, openWorldHint=True)
WRITE_DESTRUCTIVE = ToolAnnotations(readOnlyHint=False, destructiveHint=True, openWorldHint=True)


def register_position_tools(mcp: FastMCP) -> None:
    @mcp.tool(annotations=READ_ONLY)
    async def get_positions(
        category: str,
        symbol: str | None = None,
        baseCoin: str | None = None,
        settleCoin: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> str:
        """Query real-time position data.

        Args:
            category: Product type - linear, inverse, option
            symbol: Symbol name
            baseCoin: Base coin
            settleCoin: Settle coin
            limit: Limit per page (max 200, default 20)
            cursor: Pagination cursor
        """
        session = get_session()
        params: dict = {"category": category}
        for key, val in [
            ("symbol", symbol),
            ("baseCoin", baseCoin),
            ("settleCoin", settleCoin),
            ("limit", limit),
            ("cursor", cursor),
        ]:
            if val is not None:
                params[key] = val
        result = session.get_positions(**params)
        return format_result(result)

    @mcp.tool(annotations=READ_ONLY)
    async def get_closed_pnl(
        category: str,
        symbol: str | None = None,
        startTime: int | None = None,
        endTime: int | None = None,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> str:
        """Query closed profit and loss records.

        Args:
            category: Product type - linear, inverse
            symbol: Symbol name
            startTime: Start timestamp in milliseconds
            endTime: End timestamp in milliseconds
            limit: Limit per page (max 100, default 50)
            cursor: Pagination cursor
        """
        session = get_session()
        params: dict = {"category": category}
        for key, val in [
            ("symbol", symbol),
            ("startTime", startTime),
            ("endTime", endTime),
            ("limit", limit),
            ("cursor", cursor),
        ]:
            if val is not None:
                params[key] = val
        result = session.get_closed_pnl(**params)
        return format_result(result)

    # --- Write position tools ---

    async def _set_leverage_impl(**kwargs: object) -> str:
        session = get_session()
        result = session.set_leverage(**kwargs)
        return format_result(result)

    register_impl("set_leverage", _set_leverage_impl)

    @mcp.tool(annotations=WRITE_DESTRUCTIVE)
    @require_mode("trade")
    @require_confirmation
    async def set_leverage(
        category: str,
        symbol: str,
        buyLeverage: str,
        sellLeverage: str,
    ) -> str:
        """Set leverage for a position (HIGH risk - requires confirmation).

        Args:
            category: Product type - linear, inverse
            symbol: Symbol name
            buyLeverage: Buy leverage (0 to max for risk limit)
            sellLeverage: Sell leverage (0 to max for risk limit)
        """
        return await _set_leverage_impl(
            category=category,
            symbol=symbol,
            buyLeverage=buyLeverage,
            sellLeverage=sellLeverage,
        )

    @mcp.tool(annotations=WRITE_DESTRUCTIVE)
    @require_mode("trade")
    async def set_trading_stop(
        category: str,
        symbol: str,
        takeProfit: str | None = None,
        stopLoss: str | None = None,
        trailingStop: str | None = None,
        tpTriggerBy: str | None = None,
        slTriggerBy: str | None = None,
        tpSize: str | None = None,
        slSize: str | None = None,
        positionIdx: int | None = None,
    ) -> str:
        """Set take profit, stop loss, or trailing stop for a position (MEDIUM risk).

        Args:
            category: Product type - linear, inverse
            symbol: Symbol name
            takeProfit: Take profit price
            stopLoss: Stop loss price
            trailingStop: Trailing stop distance
            tpTriggerBy: TP trigger price type - LastPrice, MarkPrice, IndexPrice
            slTriggerBy: SL trigger price type
            tpSize: TP order quantity
            slSize: SL order quantity
            positionIdx: Position index (0: one-way, 1: hedge buy, 2: hedge sell)
        """
        session = get_session()
        params: dict = {"category": category, "symbol": symbol}
        for key, val in [
            ("takeProfit", takeProfit),
            ("stopLoss", stopLoss),
            ("trailingStop", trailingStop),
            ("tpTriggerBy", tpTriggerBy),
            ("slTriggerBy", slTriggerBy),
            ("tpSize", tpSize),
            ("slSize", slSize),
            ("positionIdx", positionIdx),
        ]:
            if val is not None:
                params[key] = val
        result = session.set_trading_stop(**params)
        return format_result(result)

    @mcp.tool(annotations=WRITE_DESTRUCTIVE)
    @require_mode("trade")
    async def set_auto_add_margin(
        category: str,
        symbol: str,
        autoAddMargin: int,
        positionIdx: int | None = None,
    ) -> str:
        """Turn on/off auto-add-margin for isolated margin position (MEDIUM risk).

        Args:
            category: Product type - linear
            symbol: Symbol name
            autoAddMargin: 0 to turn off, 1 to turn on
            positionIdx: Position index (0: one-way, 1: hedge buy, 2: hedge sell)
        """
        session = get_session()
        params: dict = {"category": category, "symbol": symbol, "autoAddMargin": autoAddMargin}
        if positionIdx is not None:
            params["positionIdx"] = positionIdx
        result = session.set_auto_add_margin(**params)
        return format_result(result)
