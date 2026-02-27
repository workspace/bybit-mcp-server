---
sidebar_position: 4
---

# Position Tools

Tools for position management.

## Read-only

### get_positions

Query real-time position data.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `category` | string | Yes | `linear`, `inverse`, `option` |
| `symbol` | string | No | Trading pair |
| `baseCoin` | string | No | Base coin |
| `settleCoin` | string | No | Settle coin |
| `limit` | int | No | Max 200, default 20 |
| `cursor` | string | No | Pagination cursor |

**Example prompt:** "Show my open positions"

---

### get_closed_pnl

Query closed profit and loss records.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `category` | string | Yes | `linear`, `inverse` |
| `symbol` | string | No | Trading pair |
| `startTime` | int | No | Start timestamp (ms) |
| `endTime` | int | No | End timestamp (ms) |
| `limit` | int | No | Max 100, default 50 |
| `cursor` | string | No | Pagination cursor |

---

## Write (requires `trade` mode)

### set_leverage

Set leverage for a symbol. **HIGH risk — requires confirmation.**

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

Set take profit, stop loss, or trailing stop for a position. **MEDIUM risk.**

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `category` | string | Yes | `linear`, `inverse` |
| `symbol` | string | Yes | Trading pair |
| `takeProfit` | string | No | TP price |
| `stopLoss` | string | No | SL price |
| `trailingStop` | string | No | Trailing stop distance |
| `tpTriggerBy` | string | No | `LastPrice`, `MarkPrice`, `IndexPrice` |
| `slTriggerBy` | string | No | SL trigger price type |
| `tpSize` | string | No | TP order quantity |
| `slSize` | string | No | SL order quantity |
| `positionIdx` | int | No | 0: one-way, 1: hedge buy, 2: hedge sell |

---

### set_auto_add_margin

Turn on/off auto-add-margin for isolated margin position. **MEDIUM risk.**

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `category` | string | Yes | `linear` |
| `symbol` | string | Yes | Trading pair |
| `autoAddMargin` | int | Yes | `0` = off, `1` = on |
| `positionIdx` | int | No | 0: one-way, 1: hedge buy, 2: hedge sell |
