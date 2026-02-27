"""Tests for market tools."""

import json

import pytest
from mcp.server.fastmcp import FastMCP

from bybit_mcp_server.tools.market import register_market_tools


@pytest.fixture
def mcp_app(patch_session):
    app = FastMCP("test")
    register_market_tools(app)
    return app


class TestGetServerTime:
    @pytest.mark.asyncio
    async def test_returns_time(self, mcp_app, patch_session):
        result = await mcp_app.call_tool("get_server_time", {})
        data = json.loads(result[0][0].text)
        assert "timeSecond" in data


class TestGetTickers:
    @pytest.mark.asyncio
    async def test_with_symbol(self, mcp_app, patch_session):
        result = await mcp_app.call_tool("get_tickers", {"category": "spot", "symbol": "BTCUSDT"})
        data = json.loads(result[0][0].text)
        assert data["category"] == "spot"
        patch_session.get_tickers.assert_called_once_with(category="spot", symbol="BTCUSDT")

    @pytest.mark.asyncio
    async def test_without_symbol(self, mcp_app, patch_session):
        await mcp_app.call_tool("get_tickers", {"category": "spot"})
        patch_session.get_tickers.assert_called_once_with(category="spot")


class TestGetKline:
    @pytest.mark.asyncio
    async def test_required_params(self, mcp_app, patch_session):
        await mcp_app.call_tool("get_kline", {"category": "linear", "symbol": "BTCUSDT", "interval": "1"})
        patch_session.get_kline.assert_called_once_with(category="linear", symbol="BTCUSDT", interval="1")

    @pytest.mark.asyncio
    async def test_optional_params(self, mcp_app, patch_session):
        await mcp_app.call_tool("get_kline", {
            "category": "linear", "symbol": "BTCUSDT", "interval": "1",
            "start": 1000, "end": 2000, "limit": 100,
        })
        patch_session.get_kline.assert_called_once_with(
            category="linear", symbol="BTCUSDT", interval="1",
            start=1000, end=2000, limit=100,
        )


class TestGetInstrumentsInfo:
    @pytest.mark.asyncio
    async def test_basic(self, mcp_app, patch_session):
        await mcp_app.call_tool("get_instruments_info", {"category": "spot"})
        patch_session.get_instruments_info.assert_called_once_with(category="spot")


class TestGetOrderbook:
    @pytest.mark.asyncio
    async def test_basic(self, mcp_app, patch_session):
        await mcp_app.call_tool("get_orderbook", {"category": "spot", "symbol": "BTCUSDT"})
        patch_session.get_orderbook.assert_called_once_with(category="spot", symbol="BTCUSDT")


class TestGetFundingRateHistory:
    @pytest.mark.asyncio
    async def test_basic(self, mcp_app, patch_session):
        await mcp_app.call_tool("get_funding_rate_history", {"category": "linear", "symbol": "BTCUSDT"})
        patch_session.get_funding_rate_history.assert_called_once_with(category="linear", symbol="BTCUSDT")


class TestGetPublicTrades:
    @pytest.mark.asyncio
    async def test_basic(self, mcp_app, patch_session):
        await mcp_app.call_tool("get_public_trades", {"category": "spot", "symbol": "BTCUSDT"})
        patch_session.get_public_trade_history.assert_called_once_with(category="spot", symbol="BTCUSDT")


class TestGetOpenInterest:
    @pytest.mark.asyncio
    async def test_basic(self, mcp_app, patch_session):
        await mcp_app.call_tool("get_open_interest", {
            "category": "linear", "symbol": "BTCUSDT", "intervalTime": "1h",
        })
        patch_session.get_open_interest.assert_called_once_with(
            category="linear", symbol="BTCUSDT", intervalTime="1h",
        )
