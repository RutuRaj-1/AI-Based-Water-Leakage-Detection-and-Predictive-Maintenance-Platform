"""
Security helpers.

If `API_KEY` is configured, mutating endpoints require a matching
`X-API-Key` header. When unset (default for local dev) the API is open.
"""

from __future__ import annotations

import hmac

from fastapi import Header, HTTPException, status

from app.core.config import settings


async def require_api_key(x_api_key: str | None = Header(default=None)) -> None:
    if not settings.api_key:
        return
    if not x_api_key or not hmac.compare_digest(x_api_key, settings.api_key):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or missing X-API-Key")

