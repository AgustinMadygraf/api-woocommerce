"""
Path: src/entities/wc_variable_product.py
"""

from typing import Any, Dict

class WCVariableProduct:
    "Entidad que representa un producto variable de WooCommerce"
    def __init__(self, data: Dict[str, Any]):
        self.data = data

    @classmethod
    def from_api_response(cls, api_data: Dict[str, Any]):
        "Crea una instancia de WCVariableProduct desde la respuesta de la API"
        return cls(api_data)

    def to_dict(self):
        "Convierte la entidad a un diccionario"
        return self.data
