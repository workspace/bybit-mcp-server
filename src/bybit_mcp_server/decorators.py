"""Decorators for permission checking and confirmation flow."""

import functools
import json
import time
import uuid
from typing import Any

from bybit_mcp_server.config import MODE_PERMISSIONS, get_mode

# In-memory store for pending confirmations
# Key: confirmation_id, Value: dict with action details and timestamp
_pending_confirmations: dict[str, dict[str, Any]] = {}

# Confirmation expiry in seconds
CONFIRMATION_TTL = 300  # 5 minutes

# Registry of implementation functions for confirmed execution
_impl_registry: dict[str, Any] = {}


def register_impl(tool_name: str, impl_fn: Any) -> None:
    """Register an implementation function for a confirmable tool."""
    _impl_registry[tool_name] = impl_fn


def get_impl(tool_name: str) -> Any:
    """Get the implementation function for a confirmed tool."""
    return _impl_registry.get(tool_name)


def require_mode(permission: str):
    """Decorator that checks if the current BYBIT_MODE allows this permission level.

    Args:
        permission: One of "read", "trade", "full"
    """

    def decorator(fn):
        @functools.wraps(fn)
        async def wrapper(*args, **kwargs):
            mode = get_mode()
            allowed = MODE_PERMISSIONS[mode]
            if permission not in allowed:
                return json.dumps(
                    {
                        "error": f"Permission denied. Tool requires '{permission}' permission, "
                        f"but current BYBIT_MODE is '{mode.value}'. "
                        f"Set BYBIT_MODE={permission} or higher to use this tool."
                    }
                )
            return await fn(*args, **kwargs)

        return wrapper

    return decorator


def require_confirmation(fn):
    """Decorator for HIGH-risk tools. Instead of executing immediately,
    returns a confirmation summary. The user must then call confirm_order
    with the confirmation_id to actually execute.
    """

    @functools.wraps(fn)
    async def wrapper(*args, **kwargs):
        # Filter out None values so only explicit params are stored
        filtered_kwargs = {k: v for k, v in kwargs.items() if v is not None}

        # Generate confirmation ID and store the pending action
        confirmation_id = str(uuid.uuid4())
        _pending_confirmations[confirmation_id] = {
            "tool": fn.__name__,
            "kwargs": filtered_kwargs,
            "timestamp": time.time(),
        }
        # Clean expired confirmations
        _clean_expired()
        # Build a human-readable summary
        summary = {
            "status": "confirmation_required",
            "confirmation_id": confirmation_id,
            "tool": fn.__name__,
            "parameters": filtered_kwargs,
            "message": f"Please review and call confirm_order(confirmation_id='{confirmation_id}') to execute.",
            "expires_in_seconds": CONFIRMATION_TTL,
        }
        return json.dumps(summary, indent=2)

    return wrapper


def execute_confirmed(confirmation_id: str) -> dict[str, Any] | None:
    """Retrieve and remove a pending confirmation. Returns None if not found or expired."""
    _clean_expired()
    return _pending_confirmations.pop(confirmation_id, None)


def _clean_expired() -> None:
    """Remove confirmations older than TTL."""
    now = time.time()
    expired = [k for k, v in _pending_confirmations.items() if now - v["timestamp"] > CONFIRMATION_TTL]
    for k in expired:
        del _pending_confirmations[k]
