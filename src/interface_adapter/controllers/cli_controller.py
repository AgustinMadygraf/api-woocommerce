"""
Path: src/interface_adapter/controllers/cli_controller.py
"""

from src.infrastructure.cli.as400_ui import AS400UI
from src.infrastructure.cli.commands.wc_commands import VariableProductsCommand, ProductVariationsCommand
from src.interface_adapter.gateways.wc_gateway import WCGateway

class CLIController:
    "Controlador para orquestar la interacción entre la CLI, casos de uso y presentadores."
    def __init__(self, api_client: WCGateway, ui: AS400UI):
        self.api_client = api_client
        self.ui = ui
        self.variable_products_cmd = VariableProductsCommand(api_client, ui)
        self.product_variations_cmd = ProductVariationsCommand(api_client, ui)

    def show_variable_products(self):
        "Muestra productos variables desde la API de WooCommerce"
        return self.variable_products_cmd.execute()

    def show_product_variations(self, product_id: str, page: int = 1, per_page: int = 20):
        "Muestra variaciones de un producto desde la API de WooCommerce"
        return self.product_variations_cmd.execute(product_id, page, per_page)
