---
sidebar_position: 3
---

# Account Tools

Read-only tools for account information. Available in all permission modes.

## get_wallet_balance

Get unified account wallet balance.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `accountType` | string | Yes | `UNIFIED` (default), `SPOT`, `CONTRACT` |
| `coin` | string | No | Specific coin (e.g. `BTC`) |

**Example prompt:** "What's my account balance?"

---

## get_fee_rate

Get current trading fee rate.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `category` | string | Yes | `spot`, `linear`, `inverse`, `option` |
| `symbol` | string | No | Specific symbol |

---

## get_account_info

Get account configuration info (margin mode, account level, etc.). No parameters required.
