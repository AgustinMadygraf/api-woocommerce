"""
Entidad para variación de producto WooCommerce.
"""

from typing import Any, Dict

class WCProductVariation:
    "Entidad que representa una variación de producto de WooCommerce"
    def __init__(self, data: Dict[str, Any]):
        self.data = data

    @classmethod
    def from_api_response(cls, api_data: Dict[str, Any]):
        "Crea una instancia de WCProductVariation desde la respuesta de la API"
        return cls(api_data)

    def to_dict(self):
        "Convierte la entidad a un diccionario"
        return self.data
