from __future__ import annotations

from typing import TYPE_CHECKING
from hashlib import sha256
import hmac

if TYPE_CHECKING:
    from aiohttp.web import Request

__slots__ = "verify_signature"

async def verify_signature(request: Request, signing_key: str):
    try:
        t, v1, *_ = request.headers["Stripe-Signature"].split(",")
        if not (t.startswith("t=") or v1.startswith("v1=")):
            return False

        t = t.split("=")[1]
        v1 = v1.split("=")[1]

    except:
        return False
    
    payload = await request.text()

    signed_payload = f"{t}.{payload}"

    signature = hmac.new(signed_payload.encode(), signing_key.encode(), digestmod=sha256).hexdigest()

    return hmac.compare_digest(signature, v1)
