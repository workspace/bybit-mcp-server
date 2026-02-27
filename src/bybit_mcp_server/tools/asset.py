"""Asset tools."""

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

from bybit_mcp_server.client import format_result, get_session
from bybit_mcp_server.decorators import register_impl, require_confirmation, require_mode

READ_ONLY = ToolAnnotations(readOnlyHint=True, openWorldHint=True)
WRITE_DESTRUCTIVE = ToolAnnotations(readOnlyHint=False, destructiveHint=True, openWorldHint=True)


def register_asset_tools(mcp: FastMCP) -> None:
    @mcp.tool(annotations=READ_ONLY)
    async def get_coin_balance(
        accountType: str,
        coin: str | None = None,
        memberId: str | None = None,
        withTransferSafeAmount: int | None = None,
    ) -> str:
        """Query coin balance of a specific account type.

        Args:
            accountType: Account type - UNIFIED, CONTRACT, SPOT, OPTION, FUND
            coin: Coin name
            memberId: UID (required when querying sub UID balance)
            withTransferSafeAmount: Query transfer safe amount (0 or 1)
        """
        session = get_session()
        params: dict = {"accountType": accountType}
        for key, val in [
            ("coin", coin),
            ("memberId", memberId),
            ("withTransferSafeAmount", withTransferSafeAmount),
        ]:
            if val is not None:
                params[key] = val
        result = session.get_coin_balance(**params)
        return format_result(result)

    @mcp.tool(annotations=READ_ONLY)
    async def get_coin_info(coin: str | None = None) -> str:
        """Query coin information including chain info, deposit/withdraw status.

        Args:
            coin: Coin name. If omitted, returns all coins.
        """
        session = get_session()
        params: dict = {}
        if coin:
            params["coin"] = coin
        result = session.get_coin_info(**params)
        return format_result(result)

    @mcp.tool(annotations=READ_ONLY)
    async def get_transfer_history(
        transferId: str | None = None,
        coin: str | None = None,
        status: str | None = None,
        startTime: int | None = None,
        endTime: int | None = None,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> str:
        """Query internal transfer records.

        Args:
            transferId: UUID of transfer
            coin: Coin name
            status: Transfer status - SUCCESS, PENDING, FAILED
            startTime: Start timestamp in milliseconds
            endTime: End timestamp in milliseconds
            limit: Limit per page (max 50, default 20)
            cursor: Pagination cursor
        """
        session = get_session()
        params: dict = {}
        for key, val in [
            ("transferId", transferId),
            ("coin", coin),
            ("status", status),
            ("startTime", startTime),
            ("endTime", endTime),
            ("limit", limit),
            ("cursor", cursor),
        ]:
            if val is not None:
                params[key] = val
        result = session.get_internal_transfer_records(**params)
        return format_result(result)

    # --- Write asset tools ---

    async def _internal_transfer_impl(**kwargs: object) -> str:
        session = get_session()
        result = session.create_internal_transfer(**kwargs)
        return format_result(result)

    register_impl("internal_transfer", _internal_transfer_impl)

    @mcp.tool(annotations=WRITE_DESTRUCTIVE)
    @require_mode("full")
    @require_confirmation
    async def internal_transfer(
        transferId: str,
        coin: str,
        amount: str,
        fromAccountType: str,
        toAccountType: str,
    ) -> str:
        """Transfer funds between account types under same UID (HIGH risk, requires 'full' mode).

        Args:
            transferId: UUID (generate a UUID before calling)
            coin: Coin name (e.g. USDT)
            amount: Transfer amount (as string)
            fromAccountType: Source account type - UNIFIED, CONTRACT, SPOT, OPTION, FUND
            toAccountType: Destination account type
        """
        return await _internal_transfer_impl(
            transferId=transferId,
            coin=coin,
            amount=amount,
            fromAccountType=fromAccountType,
            toAccountType=toAccountType,
        )
