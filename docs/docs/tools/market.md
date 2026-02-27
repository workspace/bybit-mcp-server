---
sidebar_position: 1
---

# Market Data Tools

Read-only tools for fetching market data. Available in all permission modes.

## get_tickers

Get latest price ticker for a symbol.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `category` | string | Yes | `spot`, `linear`, `inverse`, `option` |
| `symbol` | string | No | Trading pair (e.g. `BTCUSDT`) |

**Example prompt:** "What's the current price of ETH?"

---

## get_kline

Query historical candlestick data.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `category` | string | Yes | `spot`, `linear`, `inverse`, `option` |
| `symbol` | string | Yes | Trading pair |
| `interval` | string | Yes | `1`, `3`, `5`, `15`, `30`, `60`, `120`, `240`, `360`, `720`, `D`, `W`, `M` |
| `limit` | int | No | Number of records (max 1000, default 200) |

---

## get_orderbook

Get current orderbook depth.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `category` | string | Yes | `spot`, `linear`, `inverse`, `option` |
| `symbol` | string | Yes | Trading pair |
| `limit` | int | No | Depth level (1, 50, 200) |

---

## get_instruments_info

Get trading instrument specifications.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `category` | string | Yes | `spot`, `linear`, `inverse`, `option` |
| `symbol` | string | No | Specific symbol to query |

---

## get_server_time

Get the current Bybit server time. No parameters required.

---

## get_funding_rate_history

Get funding rate history for perpetual contracts.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `category` | string | Yes | `linear`, `inverse` |
| `symbol` | string | Yes | Trading pair |
| `limit` | int | No | Number of records (max 200) |

---

## get_public_trades

Get recent public trading history.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `category` | string | Yes | `spot`, `linear`, `inverse`, `option` |
| `symbol` | string | Yes | Trading pair |
| `limit` | int | No | Number of records (max 1000) |

---

## get_open_interest

Get open interest data.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `category` | string | Yes | `linear`, `inverse` |
| `symbol` | string | Yes | Trading pair |
| `intervalTime` | string | Yes | `5min`, `15min`, `30min`, `1h`, `4h`, `1d` |
