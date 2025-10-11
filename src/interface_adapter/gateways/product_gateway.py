"""
Gateway abstracto para operaciones de productos variables de WooCommerce.
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Tuple

class ProductGateway(ABC):
    "Gateway para productos variables"
    @abstractmethod
    def get_variable_products(self) -> Tuple[List[Dict], int]:
        "Obtiene productos variables y devuelve (productos, código_estado)"
        pass # pylint: disable=unnecessary-pass

    @abstractmethod
    def get_product_variation_count(self, product_id: int) -> str:
        "Obtiene el número total de variaciones de un producto"
        pass # pylint: disable=unnecessary-pass
