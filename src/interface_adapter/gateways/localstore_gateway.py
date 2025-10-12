"""
Gateway para acceso a datos de almacenamiento local (LocalStore)
"""
from src.interface_adapter.gateways.product_gateway import ProductGateway
from src.interface_adapter.gateways.variation_gateway import VariationGateway
from src.infrastructure.cli.services.localstore_api_client import LocalStoreApiClient
from typing import Dict, List, Tuple, Optional

class LocalStoreGateway(ProductGateway, VariationGateway):
    "Gateway compuesto para acceso a datos de LocalStore"
    def __init__(self, api_base: str):
        self.client = LocalStoreApiClient(api_base)

    def get_system_status(self) -> Tuple[Optional[Dict], int]:
        return self.client.get_system_status()

    def get_variable_products(self) -> Tuple[List[Dict], int]:
        return self.client.get_variable_products()

    def get_product_variation_count(self, product_id: int) -> str:
        variations, status = self.client.get_product_variations(product_id)
        return str(len(variations)) if status == 200 else "0"

    def get_product_variations(self, product_id: int, page: int = 1, per_page: int = 20) -> Tuple[List[Dict], int, int]:
        variations, status = self.client.get_product_variations(product_id, page, per_page)
        total_variations = len(variations) if status == 200 else 0
        return variations, status, total_variations
