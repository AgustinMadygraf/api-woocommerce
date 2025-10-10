"""
Path: src/entities/wc_system_status.py
"""

from typing import Optional

class WCSystemStatus:
    "Entidad que representa el estado del sistema WooCommerce"
    def __init__(
        self,
        home_url: str,
        version: str,
        environment: Optional[dict] = None,
        raw_data: Optional[dict] = None,
    ):
        self.home_url = home_url
        self.version = version
        self.environment = environment or {}
        self.raw_data = raw_data or {}

    @classmethod
    def from_api_response(cls, data: dict):
        "Crea una instancia de WCSystemStatus a partir de la respuesta de la API"
        env = data.get("environment", {})
        return cls(
            home_url=env.get("home_url", "N/A"),
            version=env.get("version", "N/A"),
            environment=env,
            raw_data=data,
        )
