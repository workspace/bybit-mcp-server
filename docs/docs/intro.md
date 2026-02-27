---
sidebar_position: 1
slug: /
---

# Bybit MCP Server

A **Model Context Protocol** server that connects AI assistants to the [Bybit](https://bybit.com) cryptocurrency exchange via the V5 API.

## Features

- **Market Data** — Real-time tickers, orderbook, klines, funding rates
- **Account Info** — Wallet balance, fee rates, account settings
- **Trading** — Place, amend, and cancel orders with safety confirmation
- **Position Management** — View positions, set leverage, TP/SL
- **Asset Management** — Internal transfers, coin balances

## Safety First

Write operations (trading, transfers) include multiple safety layers:

1. **Testnet by default** — No real funds at risk until explicitly configured
2. **Permission modes** — `read`, `trade`, `full` control what tools are available
3. **Confirmation flow** — Dangerous operations require explicit user approval

## Quick Install

```bash
# Using uvx (recommended)
uvx bybit-mcp

# Or install from PyPI
pip install bybit-mcp
```

See [Getting Started](./getting-started) for full setup instructions.
