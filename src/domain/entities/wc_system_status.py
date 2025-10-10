"""
Entidad de dominio para el estado del sistema WooCommerce
"""

from typing import Optional

class WCSystemStatus:
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
        env = data.get("environment", {})
        return cls(
            home_url=env.get("home_url", "N/A"),
            version=env.get("version", "N/A"),
            environment=env,
            raw_data=data,
        )