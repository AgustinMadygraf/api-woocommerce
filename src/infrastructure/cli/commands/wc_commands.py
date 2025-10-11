"""
Path: src/infrastructure/cli/commands/wc_commands.py
"""

from src.interface_adapter.gateways.wc_gateway import WCGateway
from src.use_cases.get_wc_variable_products import GetWCVariableProductsUseCase
from src.interface_adapter.presenters.wc_variable_products_presenter import WCVariableProductsPresenter
from src.interface_adapter.presenters.wc_product_variations_presenter import WCProductVariationsPresenter
from src.infrastructure.cli.as400_ui import AS400UI

class VariableProductsCommand:
    "Comando para mostrar productos variables"

    def __init__(self, api_client: WCGateway, ui: AS400UI):
        self.api_client = api_client
        self.ui = ui

    def execute(self) -> str:
        "Ejecuta el comando y retorna un mensaje de resultado"
        self.ui.print_header("PRODUCTOS VARIABLES")
        try:
            use_case = GetWCVariableProductsUseCase(lambda: [prod for prod, _ in [self.api_client.get_variable_products()]][0])
            products = use_case.execute()
            variation_counts = {}
            for prod in products:
                variation_counts[prod.id] = self.api_client.get_product_variation_count(prod.id)
            rows = WCVariableProductsPresenter.present(products, variation_counts)
            self.ui.print_variable_products_table(rows)
            return f"Mostrando {len(products)} productos variables."
        except (ConnectionError, ValueError, KeyError, TypeError) as e:
            return self._handle_error(e)

    def _handle_error(self, e):
        if isinstance(e, ConnectionError):
            return str(e)
        elif isinstance(e, ValueError):
            return f"Error de valor: {str(e)}"
        elif isinstance(e, KeyError):
            return f"Error de clave: {str(e)}"
        elif isinstance(e, TypeError):
            return f"Error de tipo: {str(e)}"
        else:
            return f"Error inesperado: {str(e)}"

class ProductVariationsCommand:
    "Comando para mostrar variaciones de un producto"
    def __init__(self, api_client: WCGateway, ui: AS400UI):
        self.api_client = api_client
        self.ui = ui

    def execute(self, product_id: str, page: int = 1, per_page: int = 20) -> tuple:
        "Ejecuta el comando y retorna un mensaje de resultado y total de páginas"
        self.ui.print_header("VARIACIONES DE PRODUCTO")
        try:
            variations, status_code, total = self.api_client.get_product_variations(product_id, page=page, per_page=per_page)
            if status_code != 200:
                return f"Error: {status_code} - No se pudieron obtener las variaciones", 1
            rows = WCProductVariationsPresenter.present(variations) if status_code == 200 else []
            if rows:
                self.ui.print_variations_table(rows)
            total_pages = (total // per_page) + (1 if total % per_page else 0)
            return f"Mostrando {len(variations)} variaciones.", total_pages
        except (ConnectionError, ValueError, KeyError, TypeError) as e:
            return self._handle_error(e), 1

    def _handle_error(self, e):
        if isinstance(e, ConnectionError):
            return str(e)
        elif isinstance(e, ValueError):
            return f"Error de valor: {str(e)}"
        elif isinstance(e, KeyError):
            return f"Error de clave: {str(e)}"
        elif isinstance(e, TypeError):
            return f"Error de tipo: {str(e)}"
        else:
            return f"Error inesperado: {str(e)}"
