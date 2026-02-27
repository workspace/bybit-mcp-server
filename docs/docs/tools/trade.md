---
sidebar_position: 2
---

# Trade Tools

Tools for order management. Requires `trade` or `full` permission mode for write operations.

:::warning
Trade tools interact with real orders. Always test on **testnet** first.
:::

## Read-only

### get_open_orders

Query unfilled or partially filled orders.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `category` | string | Yes | `spot`, `linear`, `inverse`, `option` |
| `symbol` | string | No | Trading pair |
| `baseCoin` | string | No | Base coin (linear/inverse only) |
| `orderId` | string | No | Order ID |
| `orderLinkId` | string | No | User custom order ID |
| `limit` | int | No | Max 50, default 20 |
| `cursor` | string | No | Pagination cursor |

---

### get_order_history

Query past order history.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `category` | string | Yes | `spot`, `linear`, `inverse`, `option` |
| `symbol` | string | No | Trading pair |
| `orderId` | string | No | Order ID |
| `orderLinkId` | string | No | User custom order ID |
| `orderStatus` | string | No | `New`, `PartiallyFilled`, `Filled`, `Cancelled`, etc. |
| `limit` | int | No | Max 50, default 20 |
| `cursor` | string | No | Pagination cursor |

---

### get_trade_history

Query trade execution history.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `category` | string | Yes | `spot`, `linear`, `inverse`, `option` |
| `symbol` | string | No | Trading pair |
| `orderId` | string | No | Order ID |
| `startTime` | int | No | Start timestamp (ms) |
| `endTime` | int | No | End timestamp (ms) |
| `limit` | int | No | Max 100, default 50 |
| `cursor` | string | No | Pagination cursor |

---

## Write (requires confirmation)

The following tools use the **confirmation flow**: the server returns an order summary with a `confirmation_id` first. The AI must call `confirm_order` with that ID to execute.

### place_order

Create a new order. **HIGH risk — requires confirmation.**

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `category` | string | Yes | `spot`, `linear`, `inverse`, `option` |
| `symbol` | string | Yes | Trading pair (e.g. `BTCUSDT`) |
| `side` | string | Yes | `Buy` or `Sell` |
| `orderType` | string | Yes | `Market` or `Limit` |
| `qty` | string | Yes | Order quantity |
| `price` | string | No | Required for Limit orders |
| `timeInForce` | string | No | `GTC`, `IOC`, `FOK`, `PostOnly` |
| `orderLinkId` | string | No | User custom order ID |
| `reduceOnly` | bool | No | `true` = close position only |
| `takeProfit` | string | No | Take profit price |
| `stopLoss` | string | No | Stop loss price |

**Example prompt:** "Buy 0.01 BTC at market price"

---

### amend_order

Modify an existing order. **HIGH risk — requires confirmation.**

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `category` | string | Yes | Product type |
| `symbol` | string | Yes | Trading pair |
| `orderId` | string | No | Order ID (either this or `orderLinkId`) |
| `orderLinkId` | string | No | User custom order ID |
| `qty` | string | No | New quantity |
| `price` | string | No | New price |
| `triggerPrice` | string | No | New trigger price |
| `takeProfit` | string | No | New take profit price |
| `stopLoss` | string | No | New stop loss price |

---

### cancel_all_orders

Cancel all open orders for a category. **HIGH risk — requires confirmation.**

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `category` | string | Yes | Product type |
| `symbol` | string | No | Specific symbol (cancels all if omitted) |
| `baseCoin` | string | No | Base coin |
| `settleCoin` | string | No | Settle coin |

---

## Write (no confirmation)

### cancel_order

Cancel a single order. **MEDIUM risk — no confirmation required.**

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `category` | string | Yes | Product type |
| `symbol` | string | Yes | Trading pair |
| `orderId` | string | No | Order ID (either this or `orderLinkId`) |
| `orderLinkId` | string | No | User custom order ID |

---

## confirm_order

Execute a previously confirmed order. This is a cross-cutting tool registered at the server level.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `confirmation_id` | string | Yes | UUID returned from a HIGH-risk tool |

Confirmations expire after **5 minutes**.
