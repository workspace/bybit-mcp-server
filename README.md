# bybit-mcp-server

A [Model Context Protocol](https://modelcontextprotocol.io/) server for the [Bybit](https://bybit.com) V5 API.

Connect AI assistants (Claude, Cursor, etc.) to Bybit for market data, trading, and account management.

## Quick Start

```bash
uvx bybit-mcp-server
```

## MCP Client Configuration

### Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "bybit": {
      "command": "uvx",
      "args": ["bybit-mcp-server"],
      "env": {
        "BYBIT_API_KEY": "your-api-key",
        "BYBIT_API_SECRET": "your-api-secret",
        "BYBIT_TESTNET": "true"
      }
    }
  }
}
```

### Cursor

Add to `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "bybit": {
      "command": "uvx",
      "args": ["bybit-mcp-server"],
      "env": {
        "BYBIT_API_KEY": "your-api-key",
        "BYBIT_API_SECRET": "your-api-secret",
        "BYBIT_TESTNET": "true"
      }
    }
  }
}
```

## Available Tools

| Category | Tools | Permission |
|----------|-------|------------|
| **Market** | `get_tickers`, `get_kline`, `get_orderbook`, `get_instruments_info`, `get_server_time`, `get_funding_rate_history`, `get_public_trades`, `get_open_interest` | `read` |
| **Account** | `get_wallet_balance`, `get_fee_rate`, `get_account_info` | `read` |
| **Trade** | `place_order`, `amend_order`, `cancel_order`, `cancel_all_orders`, `get_open_orders`, `get_order_history` | `trade` |
| **Position** | `get_positions`, `set_leverage`, `set_trading_stop`, `get_closed_pnl` | `read` / `trade` |
| **Asset** | `get_coin_balance`, `get_coin_info`, `internal_transfer` | `read` / `full` |

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `BYBIT_API_KEY` | — | API key from Bybit |
| `BYBIT_API_SECRET` | — | API secret from Bybit |
| `BYBIT_TESTNET` | `true` | Use testnet (`true`) or mainnet (`false`) |
| `BYBIT_MODE` | `read` | Permission mode: `read`, `trade`, or `full` |

## Development

```bash
git clone https://github.com/workspace/bybit-mcp-server.git
cd bybit-mcp-server
uv sync --all-groups
uv run bybit-mcp-server
```

## Documentation

Full docs at [workspace.github.io/bybit-mcp-server](https://workspace.github.io/bybit-mcp-server)

## License

MIT
