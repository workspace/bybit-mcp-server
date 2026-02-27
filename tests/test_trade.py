"""Tests for trade tools."""

import json

import pytest
from mcp.server.fastmcp import FastMCP

from bybit_mcp_server.decorators import _pending_confirmations
from bybit_mcp_server.tools.trade import register_trade_tools


@pytest.fixture
def mcp_app(patch_session):
    app = FastMCP("test")
    register_trade_tools(app)
    return app


@pytest.fixture(autouse=True)
def clear_pending():
    _pending_confirmations.clear()
    yield
    _pending_confirmations.clear()


class TestGetOpenOrders:
    @pytest.mark.asyncio
    async def test_basic(self, mcp_app, patch_session):
        result = await mcp_app.call_tool("get_open_orders", {"category": "spot"})
        data = json.loads(result[0][0].text)
        assert "list" in data


class TestGetOrderHistory:
    @pytest.mark.asyncio
    async def test_basic(self, mcp_app, patch_session):
        await mcp_app.call_tool("get_order_history", {"category": "spot"})
        patch_session.get_order_history.assert_called_once_with(category="spot")


class TestGetTradeHistory:
    @pytest.mark.asyncio
    async def test_basic(self, mcp_app, patch_session):
        await mcp_app.call_tool("get_trade_history", {"category": "spot"})
        patch_session.get_executions.assert_called_once_with(category="spot")


class TestPlaceOrder:
    @pytest.mark.asyncio
    async def test_requires_trade_mode(self, mcp_app, patch_session, monkeypatch):
        monkeypatch.setenv("BYBIT_MODE", "read")
        result = await mcp_app.call_tool("place_order", {
            "category": "linear", "symbol": "BTCUSDT", "side": "Buy",
            "orderType": "Market", "qty": "0.001",
        })
        data = json.loads(result[0][0].text)
        assert "error" in data
        assert "Permission denied" in data["error"]

    @pytest.mark.asyncio
    async def test_returns_confirmation(self, mcp_app, patch_session, monkeypatch):
        monkeypatch.setenv("BYBIT_MODE", "trade")
        result = await mcp_app.call_tool("place_order", {
            "category": "linear", "symbol": "BTCUSDT", "side": "Buy",
            "orderType": "Market", "qty": "0.001",
        })
        data = json.loads(result[0][0].text)
        assert data["status"] == "confirmation_required"
        assert "confirmation_id" in data


class TestCancelOrder:
    @pytest.mark.asyncio
    async def test_executes_directly(self, mcp_app, patch_session, monkeypatch):
        monkeypatch.setenv("BYBIT_MODE", "trade")
        result = await mcp_app.call_tool("cancel_order", {
            "category": "spot", "symbol": "BTCUSDT", "orderId": "1234",
        })
        data = json.loads(result[0][0].text)
        assert data["orderId"] == "1234"

    @pytest.mark.asyncio
    async def test_requires_trade_mode(self, mcp_app, patch_session, monkeypatch):
        monkeypatch.setenv("BYBIT_MODE", "read")
        result = await mcp_app.call_tool("cancel_order", {
            "category": "spot", "symbol": "BTCUSDT", "orderId": "1234",
        })
        data = json.loads(result[0][0].text)
        assert "error" in data


class TestCancelAllOrders:
    @pytest.mark.asyncio
    async def test_returns_confirmation(self, mcp_app, patch_session, monkeypatch):
        monkeypatch.setenv("BYBIT_MODE", "trade")
        result = await mcp_app.call_tool("cancel_all_orders", {"category": "spot"})
        data = json.loads(result[0][0].text)
        assert data["status"] == "confirmation_required"
