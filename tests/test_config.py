"""Tests for config module."""



from bybit_mcp_server.config import (
    MODE_PERMISSIONS,
    Mode,
    get_api_key,
    get_api_secret,
    get_mode,
    get_recv_window,
    get_testnet,
)


class TestGetMode:
    def test_default_is_read(self, monkeypatch):
        monkeypatch.delenv("BYBIT_MODE", raising=False)
        assert get_mode() == Mode.READ

    def test_read_mode(self, monkeypatch):
        monkeypatch.setenv("BYBIT_MODE", "read")
        assert get_mode() == Mode.READ

    def test_trade_mode(self, monkeypatch):
        monkeypatch.setenv("BYBIT_MODE", "trade")
        assert get_mode() == Mode.TRADE

    def test_full_mode(self, monkeypatch):
        monkeypatch.setenv("BYBIT_MODE", "full")
        assert get_mode() == Mode.FULL

    def test_invalid_falls_back_to_read(self, monkeypatch):
        monkeypatch.setenv("BYBIT_MODE", "invalid")
        assert get_mode() == Mode.READ

    def test_case_insensitive(self, monkeypatch):
        monkeypatch.setenv("BYBIT_MODE", "TRADE")
        assert get_mode() == Mode.TRADE


class TestGetTestnet:
    def test_default_is_true(self, monkeypatch):
        monkeypatch.delenv("BYBIT_TESTNET", raising=False)
        assert get_testnet() is True

    def test_true(self, monkeypatch):
        monkeypatch.setenv("BYBIT_TESTNET", "true")
        assert get_testnet() is True

    def test_false(self, monkeypatch):
        monkeypatch.setenv("BYBIT_TESTNET", "false")
        assert get_testnet() is False


class TestGetApiKey:
    def test_returns_none_when_empty(self, monkeypatch):
        monkeypatch.setenv("BYBIT_API_KEY", "")
        assert get_api_key() is None

    def test_returns_key(self, monkeypatch):
        monkeypatch.setenv("BYBIT_API_KEY", "test-key")
        assert get_api_key() == "test-key"


class TestGetApiSecret:
    def test_returns_none_when_empty(self, monkeypatch):
        monkeypatch.setenv("BYBIT_API_SECRET", "")
        assert get_api_secret() is None

    def test_returns_secret(self, monkeypatch):
        monkeypatch.setenv("BYBIT_API_SECRET", "test-secret")
        assert get_api_secret() == "test-secret"


class TestGetRecvWindow:
    def test_returns_none_when_empty(self, monkeypatch):
        monkeypatch.delenv("BYBIT_RECV_WINDOW", raising=False)
        assert get_recv_window() is None

    def test_returns_int(self, monkeypatch):
        monkeypatch.setenv("BYBIT_RECV_WINDOW", "5000")
        assert get_recv_window() == 5000


class TestModePermissions:
    def test_read_only_allows_read(self):
        assert MODE_PERMISSIONS[Mode.READ] == {"read"}

    def test_trade_allows_read_and_trade(self):
        assert MODE_PERMISSIONS[Mode.TRADE] == {"read", "trade"}

    def test_full_allows_all(self):
        assert MODE_PERMISSIONS[Mode.FULL] == {"read", "trade", "full"}
