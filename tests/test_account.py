"""Tests for account tools."""

import json

import pytest
from mcp.server.fastmcp import FastMCP

from bybit_mcp_server.tools.account import register_account_tools


@pytest.fixture
def mcp_app(patch_session):
    app = FastMCP("test")
    register_account_tools(app)
    return app


class TestGetWalletBalance:
    @pytest.mark.asyncio
    async def test_basic(self, mcp_app, patch_session):
        result = await mcp_app.call_tool("get_wallet_balance", {"accountType": "UNIFIED"})
        data = json.loads(result[0][0].text)
        assert "list" in data
        patch_session.get_wallet_balance.assert_called_once_with(accountType="UNIFIED")

    @pytest.mark.asyncio
    async def test_with_coin(self, mcp_app, patch_session):
        await mcp_app.call_tool("get_wallet_balance", {"accountType": "UNIFIED", "coin": "BTC"})
        patch_session.get_wallet_balance.assert_called_once_with(accountType="UNIFIED", coin="BTC")


class TestGetFeeRate:
    @pytest.mark.asyncio
    async def test_basic(self, mcp_app, patch_session):
        await mcp_app.call_tool("get_fee_rate", {"category": "spot"})
        patch_session.get_fee_rates.assert_called_once_with(category="spot")


class TestGetAccountInfo:
    @pytest.mark.asyncio
    async def test_basic(self, mcp_app, patch_session):
        result = await mcp_app.call_tool("get_account_info", {})
        data = json.loads(result[0][0].text)
        assert "marginMode" in data
