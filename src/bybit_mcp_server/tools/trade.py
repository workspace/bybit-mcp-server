"""Trade tools (requires 'trade' permission mode for write operations)."""

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

from bybit_mcp_server.client import format_result, get_session
from bybit_mcp_server.decorators import register_impl, require_confirmation, require_mode

READ_ONLY = ToolAnnotations(readOnlyHint=True, openWorldHint=True)
WRITE_DESTRUCTIVE = ToolAnnotations(readOnlyHint=False, destructiveHint=True, openWorldHint=True)


def register_trade_tools(mcp: FastMCP) -> None:
    # --- Read-only trade queries ---

    @mcp.tool(annotations=READ_ONLY)
    async def get_open_orders(
        category: str,
        symbol: str | None = None,
        baseCoin: str | None = None,
        orderId: str | None = None,
        orderLinkId: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> str:
        """Query unfilled or partially filled orders.

        Args:
            category: Product type - spot, linear, inverse, option
            symbol: Symbol name
            baseCoin: Base coin (for linear/inverse only)
            orderId: Order ID
            orderLinkId: User custom order ID
            limit: Limit per page (max 50, default 20)
            cursor: Pagination cursor
        """
        session = get_session()
        params: dict = {"category": category}
        for key, val in [
            ("symbol", symbol),
            ("baseCoin", baseCoin),
            ("orderId", orderId),
            ("orderLinkId", orderLinkId),
            ("limit", limit),
            ("cursor", cursor),
        ]:
            if val is not None:
                params[key] = val
        result = session.get_open_orders(**params)
        return format_result(result)

    @mcp.tool(annotations=READ_ONLY)
    async def get_order_history(
        category: str,
        symbol: str | None = None,
        orderId: str | None = None,
        orderLinkId: str | None = None,
        orderStatus: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> str:
        """Query order history.

        Args:
            category: Product type - spot, linear, inverse, option
            symbol: Symbol name
            orderId: Order ID
            orderLinkId: User custom order ID
            orderStatus: Order status - New, PartiallyFilled, Filled, Cancelled, etc.
            limit: Limit per page (max 50, default 20)
            cursor: Pagination cursor
        """
        session = get_session()
        params: dict = {"category": category}
        for key, val in [
            ("symbol", symbol),
            ("orderId", orderId),
            ("orderLinkId", orderLinkId),
            ("orderStatus", orderStatus),
            ("limit", limit),
            ("cursor", cursor),
        ]:
            if val is not None:
                params[key] = val
        result = session.get_order_history(**params)
        return format_result(result)

    @mcp.tool(annotations=READ_ONLY)
    async def get_trade_history(
        category: str,
        symbol: str | None = None,
        orderId: str | None = None,
        startTime: int | None = None,
        endTime: int | None = None,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> str:
        """Query trade execution history.

        Args:
            category: Product type - spot, linear, inverse, option
            symbol: Symbol name
            orderId: Order ID
            startTime: Start timestamp in milliseconds
            endTime: End timestamp in milliseconds
            limit: Limit per page (max 100, default 50)
            cursor: Pagination cursor
        """
        session = get_session()
        params: dict = {"category": category}
        for key, val in [
            ("symbol", symbol),
            ("orderId", orderId),
            ("startTime", startTime),
            ("endTime", endTime),
            ("limit", limit),
            ("cursor", cursor),
        ]:
            if val is not None:
                params[key] = val
        result = session.get_executions(**params)
        return format_result(result)

    # --- Write trade tools (require 'trade' mode) ---

    async def _place_order_impl(**kwargs: object) -> str:
        session = get_session()
        result = session.place_order(**kwargs)
        return format_result(result)

    register_impl("place_order", _place_order_impl)

    @mcp.tool(annotations=WRITE_DESTRUCTIVE)
    @require_mode("trade")
    @require_confirmation
    async def place_order(
        category: str,
        symbol: str,
        side: str,
        orderType: str,
        qty: str,
        price: str | None = None,
        timeInForce: str | None = None,
        orderLinkId: str | None = None,
        reduceOnly: bool | None = None,
        takeProfit: str | None = None,
        stopLoss: str | None = None,
    ) -> str:
        """Place an order (HIGH risk - requires confirmation).

        Args:
            category: Product type - spot, linear, inverse, option
            symbol: Symbol name (e.g. BTCUSDT)
            side: Buy or Sell
            orderType: Market or Limit
            qty: Order quantity (as string)
            price: Order price (required for Limit orders)
            timeInForce: Time in force - GTC, IOC, FOK, PostOnly
            orderLinkId: User custom order ID
            reduceOnly: Reduce only (true means close position)
            takeProfit: Take profit price
            stopLoss: Stop loss price
        """
        params: dict = {"category": category, "symbol": symbol, "side": side, "orderType": orderType, "qty": qty}
        for key, val in [
            ("price", price),
            ("timeInForce", timeInForce),
            ("orderLinkId", orderLinkId),
            ("reduceOnly", reduceOnly),
            ("takeProfit", takeProfit),
            ("stopLoss", stopLoss),
        ]:
            if val is not None:
                params[key] = val
        return await _place_order_impl(**params)

    async def _amend_order_impl(**kwargs: object) -> str:
        session = get_session()
        result = session.amend_order(**kwargs)
        return format_result(result)

    register_impl("amend_order", _amend_order_impl)

    @mcp.tool(annotations=WRITE_DESTRUCTIVE)
    @require_mode("trade")
    @require_confirmation
    async def amend_order(
        category: str,
        symbol: str,
        orderId: str | None = None,
        orderLinkId: str | None = None,
        qty: str | None = None,
        price: str | None = None,
        triggerPrice: str | None = None,
        takeProfit: str | None = None,
        stopLoss: str | None = None,
    ) -> str:
        """Amend an existing order (HIGH risk - requires confirmation).

        Args:
            category: Product type - spot, linear, inverse, option
            symbol: Symbol name
            orderId: Order ID (either orderId or orderLinkId required)
            orderLinkId: User custom order ID
            qty: New order quantity
            price: New order price
            triggerPrice: New trigger price
            takeProfit: New take profit price
            stopLoss: New stop loss price
        """
        params: dict = {"category": category, "symbol": symbol}
        for key, val in [
            ("orderId", orderId),
            ("orderLinkId", orderLinkId),
            ("qty", qty),
            ("price", price),
            ("triggerPrice", triggerPrice),
            ("takeProfit", takeProfit),
            ("stopLoss", stopLoss),
        ]:
            if val is not None:
                params[key] = val
        return await _amend_order_impl(**params)

    @mcp.tool(annotations=WRITE_DESTRUCTIVE)
    @require_mode("trade")
    async def cancel_order(
        category: str,
        symbol: str,
        orderId: str | None = None,
        orderLinkId: str | None = None,
    ) -> str:
        """Cancel an existing order (MEDIUM risk - no confirmation required).

        Args:
            category: Product type - spot, linear, inverse, option
            symbol: Symbol name
            orderId: Order ID (either orderId or orderLinkId required)
            orderLinkId: User custom order ID
        """
        session = get_session()
        params: dict = {"category": category, "symbol": symbol}
        if orderId:
            params["orderId"] = orderId
        if orderLinkId:
            params["orderLinkId"] = orderLinkId
        result = session.cancel_order(**params)
        return format_result(result)

    async def _cancel_all_orders_impl(**kwargs: object) -> str:
        session = get_session()
        result = session.cancel_all_orders(**kwargs)
        return format_result(result)

    register_impl("cancel_all_orders", _cancel_all_orders_impl)

    @mcp.tool(annotations=WRITE_DESTRUCTIVE)
    @require_mode("trade")
    @require_confirmation
    async def cancel_all_orders(
        category: str,
        symbol: str | None = None,
        baseCoin: str | None = None,
        settleCoin: str | None = None,
    ) -> str:
        """Cancel all open orders (HIGH risk - requires confirmation).

        Args:
            category: Product type - spot, linear, inverse, option
            symbol: Symbol name
            baseCoin: Base coin
            settleCoin: Settle coin
        """
        params: dict = {"category": category}
        for key, val in [("symbol", symbol), ("baseCoin", baseCoin), ("settleCoin", settleCoin)]:
            if val is not None:
                params[key] = val
        return await _cancel_all_orders_impl(**params)
