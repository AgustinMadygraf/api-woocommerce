"""
Path: src/use_cases/get_wc_system_status_use_case.py
"""

from typing import Protocol

class WCSystemStatusGateway(Protocol):
    "Protocolo para el gateway que obtiene el estado del sistema WooCommerce"
    async def get_system_status(self, wc_url: str, ck: str, cs: str, auth: str = "basic"):
        "Obtiene el estado del sistema WooCommerce"
        pass # pylint: disable=unnecessary-pass

class GetWCSystemStatusUseCase:
    "Caso de uso para obtener el estado del sistema WooCommerce"
    def __init__(self, gateway: WCSystemStatusGateway, wc_url: str, ck: str, cs: str):
        self.gateway = gateway
        self.wc_url = wc_url
        self.ck = ck
        self.cs = cs

    async def execute(self, auth: str = "basic"):
        "Ejecuta el caso de uso para obtener el estado del sistema WooCommerce"
        return await self.gateway.get_system_status(self.wc_url, self.ck, self.cs, auth)
