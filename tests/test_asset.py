"""Tests for asset tools."""

import json

import pytest
from mcp.server.fastmcp import FastMCP

from bybit_mcp_server.decorators import _pending_confirmations
from bybit_mcp_server.tools.asset import register_asset_tools


@pytest.fixture
def mcp_app(patch_session):
    app = FastMCP("test")
    register_asset_tools(app)
    return app


@pytest.fixture(autouse=True)
def clear_pending():
    _pending_confirmations.clear()
    yield
    _pending_confirmations.clear()


class TestGetCoinBalance:
    @pytest.mark.asyncio
    async def test_basic(self, mcp_app, patch_session):
        result = await mcp_app.call_tool("get_coin_balance", {"accountType": "UNIFIED"})
        data = json.loads(result[0][0].text)
        assert "accountType" in data


class TestGetCoinInfo:
    @pytest.mark.asyncio
    async def test_basic(self, mcp_app, patch_session):
        await mcp_app.call_tool("get_coin_info", {})
        patch_session.get_coin_info.assert_called_once_with()

    @pytest.mark.asyncio
    async def test_with_coin(self, mcp_app, patch_session):
        await mcp_app.call_tool("get_coin_info", {"coin": "BTC"})
        patch_session.get_coin_info.assert_called_once_with(coin="BTC")


class TestGetTransferHistory:
    @pytest.mark.asyncio
    async def test_basic(self, mcp_app, patch_session):
        await mcp_app.call_tool("get_transfer_history", {})
        patch_session.get_internal_transfer_records.assert_called_once_with()


class TestInternalTransfer:
    @pytest.mark.asyncio
    async def test_requires_full_mode(self, mcp_app, patch_session, monkeypatch):
        monkeypatch.setenv("BYBIT_MODE", "trade")
        result = await mcp_app.call_tool("internal_transfer", {
            "transferId": "uuid-1", "coin": "USDT", "amount": "100",
            "fromAccountType": "UNIFIED", "toAccountType": "FUND",
        })
        data = json.loads(result[0][0].text)
        assert "error" in data
        assert "Permission denied" in data["error"]

    @pytest.mark.asyncio
    async def test_returns_confirmation_in_full_mode(self, mcp_app, patch_session, monkeypatch):
        monkeypatch.setenv("BYBIT_MODE", "full")
        result = await mcp_app.call_tool("internal_transfer", {
            "transferId": "uuid-1", "coin": "USDT", "amount": "100",
            "fromAccountType": "UNIFIED", "toAccountType": "FUND",
        })
        data = json.loads(result[0][0].text)
        assert data["status"] == "confirmation_required"
