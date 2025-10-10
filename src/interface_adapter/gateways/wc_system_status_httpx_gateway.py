"""
Gateway de interface adapter para obtener el estado del sistema WooCommerce usando httpx.
No depende directamente de infraestructura, solo recibe una función externa.
"""

from src.domain.entities.wc_system_status import WCSystemStatus

class WCSystemStatusHttpxGateway:
    def __init__(self, httpx_get_status_func):
        self._get_status_func = httpx_get_status_func

    async def get_system_status(self, wc_url: str, ck: str, cs: str, auth: str = "basic"):
        resp = await self._get_status_func(wc_url, ck, cs, auth)
        if resp.status_code >= 400:
            return resp
        data = resp.json()
        return WCSystemStatus.from_api_response(data)
