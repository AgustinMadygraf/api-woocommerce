"""
Path: src/interface_adapter/gateways/wc_system_status_httpx_gateway.py
"""

from src.entities.wc_system_status import WCSystemStatus
from src.infrastructure.httpx.httpx_service import WCSystemStatusGatewayError

class WCSystemStatusHttpxGateway:
    "Implementación del gateway usando httpx"
    def __init__(self, httpx_get_status_func):
        self._get_status_func = httpx_get_status_func

    async def get_system_status(self, wc_url: str, ck: str, cs: str, auth: str = "basic"):
        "Obtiene el estado del sistema WooCommerce usando httpx"
        try:
            data = await self._get_status_func(wc_url, ck, cs, auth)
            return WCSystemStatus.from_api_response(data)
        except WCSystemStatusGatewayError as e:
            raise e
