---
sidebar_position: 2
---

# Getting Started

## Prerequisites

- Python 3.11+
- A [Bybit](https://bybit.com) account with API keys
- An MCP-compatible client (Claude Desktop, Cursor, etc.)

## 1. Get API Keys

1. Log into Bybit → Account → API Management
2. Create a new API key (System-generated, HMAC)
3. For testing, use **Testnet**: https://testnet.bybit.com

## 2. Configure MCP Client

### Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "bybit": {
      "command": "uvx",
      "args": ["bybit-mcp-server"],
      "env": {
        "BYBIT_API_KEY": "your-api-key",
        "BYBIT_API_SECRET": "your-api-secret",
        "BYBIT_TESTNET": "true",
        "BYBIT_MODE": "read"
      }
    }
  }
}
```

### Cursor

Add to your `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "bybit": {
      "command": "uvx",
      "args": ["bybit-mcp-server"],
      "env": {
        "BYBIT_API_KEY": "your-api-key",
        "BYBIT_API_SECRET": "your-api-secret",
        "BYBIT_TESTNET": "true",
        "BYBIT_MODE": "read"
      }
    }
  }
}
```

## 3. Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `BYBIT_API_KEY` | — | API key from Bybit |
| `BYBIT_API_SECRET` | — | API secret from Bybit |
| `BYBIT_TESTNET` | `true` | Use testnet (`true`) or mainnet (`false`) |
| `BYBIT_MODE` | `read` | Permission mode: `read`, `trade`, or `full` |
| `BYBIT_RECV_WINDOW` | — | Request receive window in ms (e.g. `5000`) |

## 4. Permission Modes

| Mode | Allowed Tools |
|------|---------------|
| `read` | Market data, account info, all read-only queries |
| `trade` | Everything in `read` + orders, cancel, leverage, TP/SL |
| `full` | Everything in `trade` + internal transfers |

HIGH-risk write operations (place_order, amend_order, cancel_all_orders, set_leverage, internal_transfer) use a **confirmation flow** — the server returns a summary first, and the AI must call `confirm_order` to execute.

## 5. Verify

Ask your AI assistant:

> "What's the current BTC price on Bybit?"

If configured correctly, it will use the `get_tickers` tool to fetch the price.
