"""
Path: src/entities/wc_variable_product.py
"""

from typing import Any, Dict

class WCVariableProduct:
    "Entidad que representa un producto variable de WooCommerce"
    def __init__(self, id: int, name: str, data: Dict[str, Any]):
        self.id = id
        self.name = name
        self.data = data
        self.status = data.get("status", "")
        self.type = data.get("type", "")
        self.stock_quantity = data.get("stock_quantity", None)

    @classmethod
    def from_api_response(cls, data: dict):
        "Crea una instancia de WCVariableProduct desde la respuesta de la API"
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            data=data
        )

    def to_dict(self):
        "Convierte la entidad a un diccionario"
        return self.data
