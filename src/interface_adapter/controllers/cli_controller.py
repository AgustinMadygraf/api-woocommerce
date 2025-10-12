"""
Path: src/interface_adapter/controllers/cli_controller.py
"""

from src.infrastructure.cli.as400_ui import AS400UI
from src.infrastructure.cli.commands.wc_commands import VariableProductsCommand, ProductVariationsCommand
from src.interface_adapter.gateways.wc_gateway import WCGateway

class CLIController:
    "Controlador para orquestar la interacción entre la CLI, casos de uso y presentadores."
    def __init__(self, api_client: WCGateway, ui: AS400UI, local_gateway=None):
        self.api_client = api_client
        self.ui = ui
        self.variable_products_cmd = VariableProductsCommand(api_client, ui)
        self.product_variations_cmd = ProductVariationsCommand(api_client, ui)
        self.local_gateway = local_gateway

    def show_variable_products(self):
        "Muestra productos variables desde la API de WooCommerce"
        return self.variable_products_cmd.execute()

    def show_product_variations(self, product_id: str, page: int = 1, per_page: int = 20):
        "Muestra variaciones de un producto desde la API de WooCommerce"
        return self.product_variations_cmd.execute(product_id, page, per_page)

    def show_local_system_status(self):
        "Muestra el estado del sistema local"
        from src.use_cases.get_local_system_status_use_case import GetLocalSystemStatusUseCase
        from src.interface_adapter.presenters.local_system_status_presenter import LocalSystemStatusPresenter
        if not self.local_gateway:
            return "LocalStore gateway no configurado."
        use_case = GetLocalSystemStatusUseCase(self.local_gateway)
        status = use_case.execute()
        if status:
            data = LocalSystemStatusPresenter.present(status)
            self.ui.print_header("ESTADO DEL SISTEMA LOCAL")
            self.ui.print_dict(data)
            return "Estado del sistema local mostrado."
        return "No se pudo obtener el estado del sistema local."

    def show_local_variable_products(self):
        "Muestra productos variables del almacenamiento local"
        from src.use_cases.get_local_variable_products import GetLocalVariableProductsUseCase
        from src.interface_adapter.presenters.local_variable_products_presenter import LocalVariableProductsPresenter
        if not self.local_gateway:
            return "LocalStore gateway no configurado."
        use_case = GetLocalVariableProductsUseCase(self.local_gateway)
        products = use_case.execute()
        rows = LocalVariableProductsPresenter.present(products)
        self.ui.print_header("PRODUCTOS VARIABLES (LOCAL)")
        self.ui.print_variable_products_table(rows)
        return f"Mostrando {len(products)} productos variables locales."

    def show_local_product_variations(self, product_id: int, page: int = 1, per_page: int = 20):
        "Muestra variaciones de producto variable local"
        from src.use_cases.get_local_variations import GetLocalVariationsUseCase
        from src.interface_adapter.presenters.local_variations_presenter import LocalVariationsPresenter
        if not self.local_gateway:
            return "LocalStore gateway no configurado."
        use_case = GetLocalVariationsUseCase(self.local_gateway)
        variations = use_case.execute(product_id, page, per_page)
        rows = LocalVariationsPresenter.present(variations)
        self.ui.print_header("VARIACIONES DE PRODUCTO (LOCAL)")
        self.ui.print_variations_table(rows)
        return f"Mostrando {len(variations)} variaciones locales."
