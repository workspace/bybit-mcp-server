---
sidebar_position: 2
---

# Trade Tools

Tools for order management. Requires `trade` or `full` permission mode.

:::warning
Trade tools interact with real orders. Always test on **testnet** first.
:::

## place_order

Create a new order.

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
| `takeProfit` | string | No | Take profit price |
| `stopLoss` | string | No | Stop loss price |

**Safety:** This tool uses the confirmation flow. The server returns an order summary first, requiring explicit confirmation before execution.

---

## amend_order

Modify an existing order.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `category` | string | Yes | Product type |
| `symbol` | string | Yes | Trading pair |
| `orderId` | string | No | Order ID (either this or orderLinkId) |
| `qty` | string | No | New quantity |
| `price` | string | No | New price |

---

## cancel_order

Cancel a single order.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `category` | string | Yes | Product type |
| `symbol` | string | Yes | Trading pair |
| `orderId` | string | No | Order ID (either this or orderLinkId) |

---

## cancel_all_orders

Cancel all open orders for a category.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `category` | string | Yes | Product type |
| `symbol` | string | No | Specific symbol (cancels all if omitted) |

---

## get_open_orders

Get current open/unfilled orders (read-only).

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `category` | string | Yes | Product type |
| `symbol` | string | No | Trading pair |

---

## get_order_history

Get past order history (read-only).

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `category` | string | Yes | Product type |
| `symbol` | string | No | Trading pair |
| `limit` | int | No | Number of records |
