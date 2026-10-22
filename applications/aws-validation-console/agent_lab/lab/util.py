"""Canonical evidence, clocks, identifiers, and bounded error descriptions."""
from __future__ import annotations
import hashlib
import json
import re
import uuid
from datetime import datetime, timezone
from typing import Any


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def iso(value: datetime | None = None) -> str:
    return (value or utcnow()).astimezone(timezone.utc).isoformat().replace('+00:00', 'Z')


def dt(value: str | datetime) -> datetime:
    out = datetime.fromisoformat(value.replace('Z', '+00:00')) if isinstance(value, str) else value
    if out.tzinfo is None:
        raise ValueError('Timezone-aware timestamps required')
    return out.astimezone(timezone.utc)


def normal(value: Any) -> Any:
    if isinstance(value, datetime):
        return iso(value)
    if isinstance(value, dict):
        return {k: normal(v) for k, v in value.items() if k != 'ResponseMetadata'}
    if isinstance(value, (list, tuple)):
        return [normal(v) for v in value]
    return value


def canonical(value: Any) -> str:
    return json.dumps(normal(value), sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def uid(prefix: str) -> str:
    return prefix + '-' + uuid.uuid4().hex[:20]


def error_code(exc: Exception) -> str:
    response = getattr(exc, 'response', {})
    code = response.get('Error', {}).get('Code', type(exc).__name__) if isinstance(response, dict) else type(exc).__name__
    return re.sub(r'[^A-Za-z0-9_.-]', '', str(code))[:100]


class Blocked(ValueError):
    """Known failed prerequisite; not a successful or empty observation."""


class UnknownRemoteState(RuntimeError):
    """A remote operation may have happened; reconcile rather than duplicate it."""
