"""Tests for decorators module."""

import json
import time

import pytest

from bybit_mcp_server.decorators import (
    CONFIRMATION_TTL,
    _pending_confirmations,
    execute_confirmed,
    get_impl,
    register_impl,
    require_confirmation,
    require_mode,
)


class TestRequireMode:
    @pytest.mark.asyncio
    async def test_allows_read_in_read_mode(self, monkeypatch):
        monkeypatch.setenv("BYBIT_MODE", "read")

        @require_mode("read")
        async def my_tool():
            return "ok"

        assert await my_tool() == "ok"

    @pytest.mark.asyncio
    async def test_denies_trade_in_read_mode(self, monkeypatch):
        monkeypatch.setenv("BYBIT_MODE", "read")

        @require_mode("trade")
        async def my_tool():
            return "ok"

        result = json.loads(await my_tool())
        assert "error" in result
        assert "Permission denied" in result["error"]

    @pytest.mark.asyncio
    async def test_allows_trade_in_trade_mode(self, monkeypatch):
        monkeypatch.setenv("BYBIT_MODE", "trade")

        @require_mode("trade")
        async def my_tool():
            return "ok"

        assert await my_tool() == "ok"

    @pytest.mark.asyncio
    async def test_allows_full_in_full_mode(self, monkeypatch):
        monkeypatch.setenv("BYBIT_MODE", "full")

        @require_mode("full")
        async def my_tool():
            return "ok"

        assert await my_tool() == "ok"

    @pytest.mark.asyncio
    async def test_denies_full_in_trade_mode(self, monkeypatch):
        monkeypatch.setenv("BYBIT_MODE", "trade")

        @require_mode("full")
        async def my_tool():
            return "ok"

        result = json.loads(await my_tool())
        assert "error" in result


class TestRequireConfirmation:
    @pytest.fixture(autouse=True)
    def clear_pending(self):
        _pending_confirmations.clear()
        yield
        _pending_confirmations.clear()

    @pytest.mark.asyncio
    async def test_returns_confirmation_summary(self):
        @require_confirmation
        async def place_order(category="linear", symbol="BTCUSDT"):
            pass

        result = json.loads(await place_order(category="linear", symbol="BTCUSDT"))
        assert result["status"] == "confirmation_required"
        assert "confirmation_id" in result
        assert result["tool"] == "place_order"
        assert result["parameters"]["category"] == "linear"

    @pytest.mark.asyncio
    async def test_filters_none_values(self):
        @require_confirmation
        async def my_tool(a="x", b=None):
            pass

        result = json.loads(await my_tool(a="x", b=None))
        assert "b" not in result["parameters"]

    @pytest.mark.asyncio
    async def test_stores_pending_confirmation(self):
        @require_confirmation
        async def my_tool(x="1"):
            pass

        result = json.loads(await my_tool(x="1"))
        cid = result["confirmation_id"]
        assert cid in _pending_confirmations
        assert _pending_confirmations[cid]["tool"] == "my_tool"


class TestExecuteConfirmed:
    @pytest.fixture(autouse=True)
    def clear_pending(self):
        _pending_confirmations.clear()
        yield
        _pending_confirmations.clear()

    def test_returns_and_removes_pending(self):
        _pending_confirmations["test-id"] = {
            "tool": "place_order",
            "kwargs": {"symbol": "BTCUSDT"},
            "timestamp": time.time(),
        }
        result = execute_confirmed("test-id")
        assert result is not None
        assert result["tool"] == "place_order"
        assert "test-id" not in _pending_confirmations

    def test_returns_none_for_unknown_id(self):
        assert execute_confirmed("nonexistent") is None

    def test_returns_none_for_expired(self):
        _pending_confirmations["old-id"] = {
            "tool": "place_order",
            "kwargs": {},
            "timestamp": time.time() - CONFIRMATION_TTL - 1,
        }
        assert execute_confirmed("old-id") is None


class TestImplRegistry:
    def test_register_and_get(self):
        async def my_impl(**kwargs):
            pass

        register_impl("test_tool", my_impl)
        assert get_impl("test_tool") is my_impl

    def test_get_unknown_returns_none(self):
        assert get_impl("nonexistent_tool") is None
