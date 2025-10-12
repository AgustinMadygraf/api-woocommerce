"""
Caso de uso para obtener variaciones de producto local
"""
from src.entities.local_variation import LocalVariation
from src.interface_adapter.gateways.localstore_gateway import LocalStoreGateway
from typing import List

class GetLocalVariationsUseCase:
    def __init__(self, gateway: LocalStoreGateway):
        self.gateway = gateway

    def execute(self, product_id: int, page: int = 1, per_page: int = 20) -> List[LocalVariation]:
        variations, status, _ = self.gateway.get_product_variations(product_id, page, per_page)
        if status == 200:
            return [LocalVariation(v) for v in variations]
        return []
