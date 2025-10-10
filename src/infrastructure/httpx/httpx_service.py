"""
Path: src/infrastructure/httpx/httpx_service.py
"""

import httpx
from src.shared.logger import get_logger

logger = get_logger("httpx-service")

async def get_wc_system_status(wc_url: str, ck: str, cs: str, auth: str = "basic") -> httpx.Response:
    "Obtiene el estado del sistema WooCommerce usando httpx"
    timeout = httpx.Timeout(connect=10.0, read=20.0, write=10.0, pool=5.0)
    async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
        resp = None
        if auth == "basic":
            resp = await client.get(wc_url, auth=(ck, cs))
            if resp.status_code == 401 and "Consumer" in resp.text:
                logger.warning("Basic Auth falló; probando auth por querystring…")
                resp = await client.get(
                    wc_url,
                    params={"consumer_key": ck, "consumer_secret": cs},
                )
        else:
            resp = await client.get(
                wc_url,
                params={"consumer_key": ck, "consumer_secret": cs},
            )
    return resp
