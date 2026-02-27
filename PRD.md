# Bybit MCP Server - Product Requirements Document

## 1. Overview

Bybit V5 API를 MCP(Model Context Protocol) 서버로 래핑하여, AI 어시스턴트(Claude, Cursor 등)가 Bybit 거래소와 상호작용할 수 있게 하는 서버.

- **언어**: Python 3.11+
- **패키지 매니저**: uv
- **MCP SDK**: `mcp[cli]` (Python MCP SDK)
- **거래소 SDK**: `pybit` (Bybit 공식 Python SDK)
- **전송 방식**: stdio (로컬), SSE (원격 옵션)

---

## 2. 기존 구현체 분석

| 프로젝트 | 언어 | 도구 수 | 특징 | 한계 |
|----------|------|---------|------|------|
| [sammcj/bybit-mcp](https://www.pulsemcp.com/servers/sammcj-bybit) | TypeScript | 4 | Read-only 시세 조회 | 거래/계좌 기능 없음 |
| [ethancod1ng/bybit-mcp-server](https://github.com/ethancod1ng/bybit-mcp-server) | TypeScript | 11 | Read + Write (주문 3개) | 리스크 관리 없음, 포지션 관리 미지원 |

**우리의 차별점:**
- Python + pybit 공식 SDK 활용 (유지보수 용이)
- Read/Write 권한 분리 아키텍처
- 포지션/마진/펀딩 등 전체 API 커버리지
- 주문 시 confirmation 메커니즘 (안전장치)

---

## 3. 아키텍처

```
┌─────────────┐     stdio/SSE     ┌──────────────┐     HTTPS      ┌──────────┐
│  AI Client  │ ◄──────────────► │  MCP Server  │ ◄────────────► │ Bybit V5 │
│  (Claude)   │                  │  (Python)    │               │   API    │
└─────────────┘                  └──────────────┘               └──────────┘
                                       │
                                       ├── tools/        (MCP 도구 정의)
                                       │   ├── market.py     (Read)
                                       │   ├── trade.py      (Write - 민감)
                                       │   ├── position.py   (Read + Write)
                                       │   ├── account.py    (Read)
                                       │   └── asset.py      (Read + Write)
                                       │
                                       ├── client.py    (pybit 래퍼)
                                       └── server.py    (MCP 서버 엔트리)
```

---

## 4. 환경 설정

### 4.1 인증
```env
BYBIT_API_KEY=xxx
BYBIT_API_SECRET=xxx
BYBIT_TESTNET=true          # 기본값: true (안전)
BYBIT_RECV_WINDOW=5000      # 밀리초
```

### 4.2 권한 모드
```env
BYBIT_MODE=read             # read | trade | full
```

| 모드 | 설명 |
|------|------|
| `read` | 시세, 잔고, 포지션 조회만 가능 |
| `trade` | read + 주문/취소 |
| `full` | trade + 출금, 전송, 포지션 이동 |

---

## 5. MCP 도구(Tools) 정의

### 5.1 Market Data (Read-only) - 8개

| 도구명 | Bybit Endpoint | 설명 |
|--------|---------------|------|
| `get_server_time` | `GET /v5/market/time` | 서버 시간 |
| `get_kline` | `GET /v5/market/kline` | 캔들스틱 (1m~1M) |
| `get_instruments_info` | `GET /v5/market/instruments-info` | 종목 정보 |
| `get_orderbook` | `GET /v5/market/orderbook` | 호가창 |
| `get_tickers` | `GET /v5/market/tickers` | 시세 스냅샷 |
| `get_funding_rate_history` | `GET /v5/market/funding/history` | 펀딩비 이력 |
| `get_public_trades` | `GET /v5/market/recent-trade` | 최근 체결 |
| `get_open_interest` | `GET /v5/market/open-interest` | 미결제약정 |

### 5.2 Account (Read-only) - 3개

| 도구명 | Bybit Endpoint | 설명 |
|--------|---------------|------|
| `get_wallet_balance` | `GET /v5/account/wallet-balance` | 지갑 잔고 (UNIFIED) |
| `get_fee_rate` | `GET /v5/account/fee-rate` | 수수료율 |
| `get_account_info` | `GET /v5/account/info` | 계정 정보 |

### 5.3 Trade (Write - 민감) - 7개

| 도구명 | Bybit Endpoint | 위험도 | 설명 |
|--------|---------------|--------|------|
| `place_order` | `POST /v5/order/create` | **HIGH** | 주문 생성 |
| `amend_order` | `POST /v5/order/amend` | **HIGH** | 주문 수정 |
| `cancel_order` | `POST /v5/order/cancel` | MEDIUM | 주문 취소 |
| `cancel_all_orders` | `POST /v5/order/cancel-all` | **HIGH** | 전체 주문 취소 |
| `get_open_orders` | `GET /v5/order/realtime` | LOW | 미체결 주문 조회 |
| `get_order_history` | `GET /v5/order/history` | LOW | 주문 이력 |
| `get_trade_history` | `GET /v5/order/execution/list` | LOW | 체결 이력 |

### 5.4 Position (Read + Write) - 5개

| 도구명 | Bybit Endpoint | 위험도 | 설명 |
|--------|---------------|--------|------|
| `get_positions` | `GET /v5/position/list` | LOW | 포지션 조회 |
| `set_leverage` | `POST /v5/position/set-leverage` | **HIGH** | 레버리지 설정 |
| `set_trading_stop` | `POST /v5/position/trading-stop` | MEDIUM | TP/SL 설정 |
| `get_closed_pnl` | `GET /v5/position/closed-pnl` | LOW | 종료 손익 |
| `set_auto_add_margin` | `POST /v5/position/set-auto-add-margin` | MEDIUM | 자동 마진 추가 |

### 5.5 Asset (Read + Write) - 4개

| 도구명 | Bybit Endpoint | 위험도 | 설명 |
|--------|---------------|--------|------|
| `get_coin_balance` | `GET /v5/asset/transfer/query-asset-info` | LOW | 코인 잔고 |
| `get_coin_info` | `GET /v5/asset/coin/query-info` | LOW | 코인/체인 정보 |
| `internal_transfer` | `POST /v5/asset/transfer/inter-transfer` | **HIGH** | 계정 간 전송 |
| `get_transfer_history` | `GET /v5/asset/transfer/query-inter-transfer-list` | LOW | 전송 이력 |

---

## 6. 안전 장치 설계

### 6.1 Write 도구 보호 매커니즘

```python
# 모든 HIGH 위험도 도구에 적용
@require_mode("trade")          # 권한 모드 확인
@require_confirmation            # 실행 전 확인 요청
@testnet_default                 # 테스트넷 우선
async def place_order(...):
    ...
```

### 6.2 주문 확인 플로우
1. AI가 `place_order` 호출
2. MCP 서버가 주문 요약 반환 (실제 전송 X)
3. AI가 사용자에게 확인 요청
4. 사용자 확인 후 `confirm_order` 호출 → 실제 주문 전송

### 6.3 제한 사항
- 기본 환경: **testnet** (실서버 전환은 명시적 설정 필요)
- 출금(`withdraw`) 도구: **v1.0에서 제외** (향후 추가 검토)
- 최대 주문 수량 제한: 환경변수로 설정 가능
- Rate limit: pybit 내장 처리 + MCP 레벨 쓰로틀링

---

## 7. 기술 스택

| 항목 | 선택 | 이유 |
|------|------|------|
| 런타임 | Python 3.11+ | pybit 호환, MCP SDK 지원 |
| 패키지 매니저 | **uv** | 빠른 설치, lockfile, 가상환경 자동 관리 |
| MCP SDK | `mcp[cli]` | Anthropic 공식 Python MCP SDK |
| 거래소 SDK | `pybit` | Bybit 공식, V5 API 전체 지원 |
| 타입 검증 | `pydantic` | 요청/응답 스키마 검증 |
| 비동기 | `anyio` / `asyncio` | MCP SDK 표준 |

### 7.1 pybit 활용 전략

pybit가 이미 제공하는 것:
- HMAC/RSA 서명 자동 처리
- 모든 V5 REST API 메서드 (place_order, get_tickers 등)
- WebSocket 연결 관리
- Testnet/Mainnet 전환
- Rate limit 내부 처리

**MCP 서버가 추가로 구현할 것:**
- MCP 도구 스키마 정의 (JSON Schema)
- 입력 검증 및 변환 (Pydantic)
- 권한 모드 체크
- 에러 핸들링 및 사용자 친화적 메시지
- Confirmation 플로우 (write 도구)

---

## 8. 프로젝트 구조

```
bybit-mcp/
├── pyproject.toml          # uv 프로젝트 설정
├── uv.lock                 # 의존성 잠금
├── README.md
├── .env.example
├── src/
│   └── bybit_mcp/
│       ├── __init__.py
│       ├── server.py       # MCP 서버 엔트리포인트
│       ├── client.py       # pybit 세션 래퍼
│       ├── config.py       # 환경변수, 설정
│       ├── types.py        # Pydantic 모델
│       ├── decorators.py   # 권한/확인 데코레이터
│       └── tools/
│           ├── __init__.py
│           ├── market.py   # 시세 도구
│           ├── account.py  # 계정 도구
│           ├── trade.py    # 거래 도구
│           ├── position.py # 포지션 도구
│           └── asset.py    # 자산 도구
└── tests/
    ├── test_market.py
    ├── test_trade.py
    └── conftest.py
```

---

## 9. 설치 및 실행

```bash
# 프로젝트 생성
uv init bybit-mcp
cd bybit-mcp

# 의존성 추가
uv add "mcp[cli]" pybit pydantic

# 실행
uv run mcp run src/bybit_mcp/server.py

# Claude Desktop 설정 (claude_desktop_config.json)
{
  "mcpServers": {
    "bybit": {
      "command": "uv",
      "args": ["--directory", "/path/to/bybit-mcp", "run", "mcp", "run", "src/bybit_mcp/server.py"],
      "env": {
        "BYBIT_API_KEY": "your-key",
        "BYBIT_API_SECRET": "your-secret",
        "BYBIT_TESTNET": "true",
        "BYBIT_MODE": "read"
      }
    }
  }
}
```

---

## 10. 로드맵

### v0.1 - MVP (Phase 1)
- [ ] 프로젝트 셋업 (uv + pyproject.toml)
- [ ] pybit 클라이언트 래퍼
- [ ] Market 도구 8개 (read-only)
- [ ] Account 도구 3개 (read-only)
- [ ] 기본 에러 핸들링

### v0.2 - Trading (Phase 2)
- [ ] Trade 도구 7개
- [ ] Confirmation 플로우
- [ ] 권한 모드 (read/trade)
- [ ] Testnet 안전장치

### v0.3 - Full (Phase 3)
- [ ] Position 도구 5개
- [ ] Asset 도구 4개
- [ ] full 권한 모드
- [ ] Rate limit 관리

### v1.0 - Production
- [ ] 통합 테스트
- [ ] 문서화
- [ ] PyPI 배포 (optional)
- [ ] SSE 전송 지원 (optional)
