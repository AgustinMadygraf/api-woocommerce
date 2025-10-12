"""
Caso de uso para obtener productos variables locales
"""
from src.entities.local_variable_product import LocalVariableProduct
from src.interface_adapter.gateways.localstore_gateway import LocalStoreGateway
from typing import List

class GetLocalVariableProductsUseCase:
    def __init__(self, gateway: LocalStoreGateway):
        self.gateway = gateway

    def execute(self) -> List[LocalVariableProduct]:
        products, status = self.gateway.get_variable_products()
        if status == 200:
            return [LocalVariableProduct(p) for p in products]
        return []
