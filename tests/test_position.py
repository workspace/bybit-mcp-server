"""Tests for position tools."""

import json

import pytest
from mcp.server.fastmcp import FastMCP

from bybit_mcp_server.decorators import _pending_confirmations
from bybit_mcp_server.tools.position import register_position_tools


@pytest.fixture
def mcp_app(patch_session):
    app = FastMCP("test")
    register_position_tools(app)
    return app


@pytest.fixture(autouse=True)
def clear_pending():
    _pending_confirmations.clear()
    yield
    _pending_confirmations.clear()


class TestGetPositions:
    @pytest.mark.asyncio
    async def test_basic(self, mcp_app, patch_session):
        result = await mcp_app.call_tool("get_positions", {"category": "linear"})
        data = json.loads(result[0][0].text)
        assert "list" in data


class TestGetClosedPnl:
    @pytest.mark.asyncio
    async def test_basic(self, mcp_app, patch_session):
        await mcp_app.call_tool("get_closed_pnl", {"category": "linear"})
        patch_session.get_closed_pnl.assert_called_once_with(category="linear")


class TestSetLeverage:
    @pytest.mark.asyncio
    async def test_returns_confirmation(self, mcp_app, patch_session, monkeypatch):
        monkeypatch.setenv("BYBIT_MODE", "trade")
        result = await mcp_app.call_tool("set_leverage", {
            "category": "linear", "symbol": "BTCUSDT",
            "buyLeverage": "10", "sellLeverage": "10",
        })
        data = json.loads(result[0][0].text)
        assert data["status"] == "confirmation_required"

    @pytest.mark.asyncio
    async def test_requires_trade_mode(self, mcp_app, patch_session, monkeypatch):
        monkeypatch.setenv("BYBIT_MODE", "read")
        result = await mcp_app.call_tool("set_leverage", {
            "category": "linear", "symbol": "BTCUSDT",
            "buyLeverage": "10", "sellLeverage": "10",
        })
        data = json.loads(result[0][0].text)
        assert "error" in data


class TestSetTradingStop:
    @pytest.mark.asyncio
    async def test_executes_directly(self, mcp_app, patch_session, monkeypatch):
        monkeypatch.setenv("BYBIT_MODE", "trade")
        await mcp_app.call_tool("set_trading_stop", {
            "category": "linear", "symbol": "BTCUSDT", "takeProfit": "50000",
        })
        patch_session.set_trading_stop.assert_called_once_with(
            category="linear", symbol="BTCUSDT", takeProfit="50000",
        )


class TestSetAutoAddMargin:
    @pytest.mark.asyncio
    async def test_executes_directly(self, mcp_app, patch_session, monkeypatch):
        monkeypatch.setenv("BYBIT_MODE", "trade")
        await mcp_app.call_tool("set_auto_add_margin", {
            "category": "linear", "symbol": "BTCUSDT", "autoAddMargin": 1,
        })
        patch_session.set_auto_add_margin.assert_called_once_with(
            category="linear", symbol="BTCUSDT", autoAddMargin=1,
        )
