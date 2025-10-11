"""
Path: src/interface_adapter/gateways/wc_gateway.py

Gateway abstracto para acceso a datos de WooCommerce.
Permite desacoplar la infraestructura y facilitar la inyección de caché/mock.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple

class WCGateway(ABC):
    "Gateway abstracto para acceso a datos de WooCommerce"
    @abstractmethod
    def get_variable_products(self) -> Tuple[List[Dict], int]:
        "Obtiene productos variables y devuelve (productos, código_estado)"
        pass # pylint: disable=unnecessary-pass

    @abstractmethod
    def get_product_variation_count(self, product_id: int) -> Optional[str]:
        "Obtiene el número total de variaciones de un producto"
        pass # pylint: disable=unnecessary-pass

    @abstractmethod
    def get_product_variations(self, product_id: int, page: int = 1, per_page: int = 20) -> Tuple[List[Dict], int, int]:
        "Obtiene variaciones de un producto y devuelve (variaciones, código_estado, total_variaciones)"
        pass # pylint: disable=unnecessary-pass
