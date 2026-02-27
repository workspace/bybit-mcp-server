"""Test fixtures for bybit-mcp tests."""

from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def mock_session():
    """A mock pybit HTTP session with all methods pre-mocked."""
    session = MagicMock()

    # Market data defaults
    session.get_server_time.return_value = {
        "retCode": 0,
        "retMsg": "OK",
        "result": {"timeSecond": "1700000000", "timeNano": "1700000000000000000"},
    }
    session.get_tickers.return_value = {
        "retCode": 0,
        "retMsg": "OK",
        "result": {"category": "spot", "list": [{"symbol": "BTCUSDT", "lastPrice": "50000"}]},
    }
    session.get_kline.return_value = {
        "retCode": 0,
        "retMsg": "OK",
        "result": {"category": "linear", "symbol": "BTCUSDT", "list": []},
    }
    session.get_instruments_info.return_value = {
        "retCode": 0,
        "retMsg": "OK",
        "result": {"category": "spot", "list": []},
    }
    session.get_orderbook.return_value = {
        "retCode": 0,
        "retMsg": "OK",
        "result": {"s": "BTCUSDT", "b": [], "a": []},
    }
    session.get_funding_rate_history.return_value = {
        "retCode": 0,
        "retMsg": "OK",
        "result": {"category": "linear", "list": []},
    }
    session.get_public_trade_history.return_value = {
        "retCode": 0,
        "retMsg": "OK",
        "result": {"category": "spot", "list": []},
    }
    session.get_open_interest.return_value = {
        "retCode": 0,
        "retMsg": "OK",
        "result": {"category": "linear", "symbol": "BTCUSDT", "list": []},
    }

    # Account defaults
    session.get_wallet_balance.return_value = {
        "retCode": 0,
        "retMsg": "OK",
        "result": {"list": [{"accountType": "UNIFIED", "coin": []}]},
    }
    session.get_fee_rates.return_value = {
        "retCode": 0,
        "retMsg": "OK",
        "result": {"list": []},
    }
    session.get_account_info.return_value = {
        "retCode": 0,
        "retMsg": "OK",
        "result": {"marginMode": "REGULAR_MARGIN", "updatedTime": "1700000000"},
    }

    # Trade defaults
    session.get_open_orders.return_value = {
        "retCode": 0,
        "retMsg": "OK",
        "result": {"category": "spot", "list": []},
    }
    session.get_order_history.return_value = {
        "retCode": 0,
        "retMsg": "OK",
        "result": {"category": "spot", "list": []},
    }
    session.get_executions.return_value = {
        "retCode": 0,
        "retMsg": "OK",
        "result": {"category": "spot", "list": []},
    }
    session.place_order.return_value = {
        "retCode": 0,
        "retMsg": "OK",
        "result": {"orderId": "1234", "orderLinkId": ""},
    }
    session.amend_order.return_value = {
        "retCode": 0,
        "retMsg": "OK",
        "result": {"orderId": "1234", "orderLinkId": ""},
    }
    session.cancel_order.return_value = {
        "retCode": 0,
        "retMsg": "OK",
        "result": {"orderId": "1234", "orderLinkId": ""},
    }
    session.cancel_all_orders.return_value = {
        "retCode": 0,
        "retMsg": "OK",
        "result": {"list": []},
    }

    # Position defaults
    session.get_positions.return_value = {
        "retCode": 0,
        "retMsg": "OK",
        "result": {"category": "linear", "list": []},
    }
    session.get_closed_pnl.return_value = {
        "retCode": 0,
        "retMsg": "OK",
        "result": {"category": "linear", "list": []},
    }
    session.set_leverage.return_value = {
        "retCode": 0,
        "retMsg": "OK",
        "result": {},
    }
    session.set_trading_stop.return_value = {
        "retCode": 0,
        "retMsg": "OK",
        "result": {},
    }
    session.set_auto_add_margin.return_value = {
        "retCode": 0,
        "retMsg": "OK",
        "result": {},
    }

    # Asset defaults
    session.get_coin_balance.return_value = {
        "retCode": 0,
        "retMsg": "OK",
        "result": {"accountType": "UNIFIED", "balance": {}},
    }
    session.get_coin_info.return_value = {
        "retCode": 0,
        "retMsg": "OK",
        "result": {"rows": []},
    }
    session.get_internal_transfer_records.return_value = {
        "retCode": 0,
        "retMsg": "OK",
        "result": {"list": []},
    }
    session.create_internal_transfer.return_value = {
        "retCode": 0,
        "retMsg": "OK",
        "result": {"transferId": "test-uuid"},
    }

    return session


@pytest.fixture
def patch_session(mock_session):
    """Patch get_session in all tool modules to return the mock."""
    targets = [
        "bybit_mcp_server.tools.market.get_session",
        "bybit_mcp_server.tools.account.get_session",
        "bybit_mcp_server.tools.trade.get_session",
        "bybit_mcp_server.tools.position.get_session",
        "bybit_mcp_server.tools.asset.get_session",
    ]
    patches = [patch(t, return_value=mock_session) for t in targets]
    for p in patches:
        p.start()
    yield mock_session
    for p in patches:
        p.stop()
