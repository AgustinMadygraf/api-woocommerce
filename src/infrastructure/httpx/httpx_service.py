"""
Path: src/infrastructure/httpx/httpx_service.py
"""

import httpx
from src.shared.logger_fastapi import get_logger

logger = get_logger("httpx-service")

class WCSystemStatusGatewayError(Exception):
    "Excepción para errores en el gateway de estado de sistema WooCommerce"
    def __init__(self, status_code, message, body=None):
        self.status_code = status_code
        self.message = message
        self.body = body
        super().__init__(f"{status_code}: {message}")

async def get_wc_system_status(wc_url: str, ck: str, cs: str, auth: str = "basic") -> dict:
    "Obtiene el estado del sistema WooCommerce usando httpx y devuelve un dict"
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
        if resp.status_code >= 400:
            raise WCSystemStatusGatewayError(
                status_code=resp.status_code,
                message="WooCommerce devolvió un error",
                body=resp.text,
            )
        return resp.json()
