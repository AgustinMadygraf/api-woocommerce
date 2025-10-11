"""
Path: src/interface_adapter/gateways/wc_gateway.py

Gateway abstracto para acceso a datos de WooCommerce.
Permite desacoplar la infraestructura y facilitar la inyección de caché/mock.
"""

from src.interface_adapter.gateways.product_gateway import ProductGateway
from src.interface_adapter.gateways.variation_gateway import VariationGateway

class WCGateway(ProductGateway, VariationGateway):
    "Gateway compuesto para acceso a datos de WooCommerce"
    pass # pylint: disable=unnecessary-pass
