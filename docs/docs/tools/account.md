---
sidebar_position: 3
---

# Account & Position Tools

Tools for account information and position management.

## Account (Read-only)

### get_wallet_balance

Get unified account wallet balance.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `accountType` | string | Yes | `UNIFIED` (default), `SPOT`, `CONTRACT` |
| `coin` | string | No | Specific coin (e.g. `BTC`) |

---

### get_fee_rate

Get current trading fee rate.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `category` | string | Yes | `spot`, `linear`, `inverse`, `option` |
| `symbol` | string | No | Specific symbol |

---

### get_account_info

Get account configuration info. No parameters required.

---

## Position

### get_positions

Get current open positions (read-only).

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `category` | string | Yes | `linear`, `inverse`, `option` |
| `symbol` | string | No | Trading pair |

---

### set_leverage

Set leverage for a symbol. Requires `trade` mode.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `category` | string | Yes | `linear`, `inverse` |
| `symbol` | string | Yes | Trading pair |
| `buyLeverage` | string | Yes | Buy side leverage |
| `sellLeverage` | string | Yes | Sell side leverage |

:::warning
Changing leverage affects margin requirements for existing positions.
:::

---

### set_trading_stop

Set take profit / stop loss for a position. Requires `trade` mode.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `category` | string | Yes | `linear`, `inverse` |
| `symbol` | string | Yes | Trading pair |
| `takeProfit` | string | No | TP price |
| `stopLoss` | string | No | SL price |
| `positionIdx` | int | No | Position index (0=one-way, 1=buy, 2=sell) |

---

### get_closed_pnl

Get closed profit and loss records (read-only).

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `category` | string | Yes | `linear`, `inverse` |
| `symbol` | string | No | Trading pair |
| `limit` | int | No | Number of records |
