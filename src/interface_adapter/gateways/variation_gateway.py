"""
Gateway abstracto para operaciones de variaciones de productos de WooCommerce.
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Tuple

class VariationGateway(ABC):
    "Gateway para variaciones de productos"
    @abstractmethod
    def get_product_variations(self, product_id: int, page: int = 1, per_page: int = 20) -> Tuple[List[Dict], int, int]:
        "Obtiene variaciones de un producto y devuelve (variaciones, código_estado, total_variaciones)"
        pass # pylint: disable=unnecessary-pass
