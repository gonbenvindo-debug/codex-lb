from __future__ import annotations

import hashlib
import json
from typing import Any

from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response

REVALIDATE_CACHE_CONTROL = "private, max-age=0, must-revalidate"


def conditional_json_response(
    request: Request,
    payload: Any,
    *,
    cache_control: str = REVALIDATE_CACHE_CONTROL,
) -> JSONResponse | Response:
    encoded_payload = jsonable_encoder(payload, by_alias=True)
    canonical_json = json.dumps(
        encoded_payload,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    etag = f'W/"{hashlib.sha256(canonical_json).hexdigest()}"'
    headers = {
        "Cache-Control": cache_control,
        "ETag": etag,
    }
    if _etag_matches(request.headers.get("if-none-match"), etag):
        return Response(status_code=304, headers=headers)
    return JSONResponse(content=encoded_payload, headers=headers)


def _etag_matches(if_none_match_header: str | None, etag: str) -> bool:
    if not if_none_match_header:
        return False
    expected_strong = etag[2:] if etag.startswith("W/") else etag
    candidates = [candidate.strip() for candidate in if_none_match_header.split(",") if candidate.strip()]
    for candidate in candidates:
        if candidate == "*":
            return True
        if candidate == etag:
            return True
        if candidate == expected_strong:
            return True
        if candidate.startswith("W/") and candidate[2:] == expected_strong:
            return True
    return False
