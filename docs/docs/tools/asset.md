---
sidebar_position: 5
---

# Asset Tools

Tools for asset management. Internal transfers require `full` permission mode.

## Read-only

### get_coin_balance

Query coin balance of a specific account type.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `accountType` | string | Yes | `UNIFIED`, `CONTRACT`, `SPOT`, `OPTION`, `FUND` |
| `coin` | string | No | Coin name (e.g. `USDT`) |
| `memberId` | string | No | UID (for sub-account queries) |
| `withTransferSafeAmount` | int | No | `0` or `1` |

---

### get_coin_info

Query coin information including chain info, deposit/withdraw status.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `coin` | string | No | Coin name. Returns all coins if omitted. |

---

### get_transfer_history

Query internal transfer records.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `transferId` | string | No | UUID of transfer |
| `coin` | string | No | Coin name |
| `status` | string | No | `SUCCESS`, `PENDING`, `FAILED` |
| `startTime` | int | No | Start timestamp (ms) |
| `endTime` | int | No | End timestamp (ms) |
| `limit` | int | No | Max 50, default 20 |
| `cursor` | string | No | Pagination cursor |

---

## Write (requires `full` mode)

### internal_transfer

Transfer funds between account types under the same UID. **HIGH risk — requires confirmation and `full` mode.**

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `transferId` | string | Yes | UUID (generate before calling) |
| `coin` | string | Yes | Coin name (e.g. `USDT`) |
| `amount` | string | Yes | Transfer amount |
| `fromAccountType` | string | Yes | Source: `UNIFIED`, `CONTRACT`, `SPOT`, `OPTION`, `FUND` |
| `toAccountType` | string | Yes | Destination account type |

:::warning
This tool requires `BYBIT_MODE=full`. It is not available in `read` or `trade` modes.
:::
