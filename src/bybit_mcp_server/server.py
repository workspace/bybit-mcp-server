"""Bybit MCP Server implementation."""

import json

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

from bybit_mcp_server.decorators import execute_confirmed, get_impl, require_mode
from bybit_mcp_server.tools.account import register_account_tools
from bybit_mcp_server.tools.asset import register_asset_tools
from bybit_mcp_server.tools.market import register_market_tools
from bybit_mcp_server.tools.position import register_position_tools
from bybit_mcp_server.tools.trade import register_trade_tools

mcp = FastMCP("bybit-mcp-server")

# Register all tool modules
register_market_tools(mcp)
register_account_tools(mcp)
register_trade_tools(mcp)
register_position_tools(mcp)
register_asset_tools(mcp)

# Cross-cutting confirmation tool
WRITE_DESTRUCTIVE = ToolAnnotations(readOnlyHint=False, destructiveHint=True, openWorldHint=True)


@mcp.tool(annotations=WRITE_DESTRUCTIVE)
@require_mode("trade")
async def confirm_order(confirmation_id: str) -> str:
    """Execute a previously prepared HIGH-risk operation after review.

    When a HIGH-risk tool (place_order, amend_order, cancel_all_orders, set_leverage,
    internal_transfer) is called, it returns a confirmation summary instead of executing.
    Call this tool with the confirmation_id to actually execute the operation.

    Args:
        confirmation_id: The confirmation_id returned by the HIGH-risk tool.
    """
    pending = execute_confirmed(confirmation_id)
    if pending is None:
        return json.dumps(
            {"error": "Confirmation not found or expired. Please retry the original operation."},
            indent=2,
        )

    impl = get_impl(pending["tool"])
    if impl is None:
        return json.dumps(
            {"error": f"No implementation found for tool: {pending['tool']}"},
            indent=2,
        )

    return await impl(**pending["kwargs"])


def main():
    """Run the MCP server."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
