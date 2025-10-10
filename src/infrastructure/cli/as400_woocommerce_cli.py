"""
Path: src/infrastructure/cli/as400_woocommerce_cli.py
"""

import os
from colorama import init, Fore

from src.infrastructure.cli.as400_ui import AS400UI
from src.infrastructure.cli.services.wc_api_client import WCApiClient
from src.infrastructure.cli.commands.wc_commands import VariableProductsCommand, ProductVariationsCommand

init(autoreset=True)

class AS400WooCommerceCLI:
    "CLI para consumir la API de WooCommerce con estética tipo AS400 IBM."
    def __init__(self, api_base: str):
        self.api_base = api_base
        self.last_message = ""
        self.ui = AS400UI()
        self.api_client = WCApiClient(api_base)

        # Inicializar comandos
        self.variable_products_cmd = VariableProductsCommand(self.api_client, self.ui)
        self.product_variations_cmd = ProductVariationsCommand(self.api_client, self.ui)

    def main_menu(self):
        "Muestra el menú principal y captura la opción del usuario"
        self.clear_screen()
        self.ui.print_header("WOOCOMMERCE API - AS400 IBM STYLE")
        self.ui.print_menu()
        self.ui.print_message_area(self.last_message)
        self.last_message = ""
        return input(Fore.GREEN + "Seleccione opción: ").strip()

    def show_variable_products(self):
        "Muestra productos variables desde la API de WooCommerce"
        self.clear_screen()
        self.last_message = self.variable_products_cmd.execute()
        input(Fore.GREEN + "Presione ENTER para continuar...")

    def show_product_variations(self):
        "Muestra variaciones de un producto variable"
        self.clear_screen()
        product_id = input(Fore.GREEN + "Ingrese el ID del producto variable: ").strip()
        self.last_message = self.product_variations_cmd.execute(product_id)
        input(Fore.GREEN + "Presione ENTER para continuar...")

    def clear_screen(self):
        "Limpia la pantalla para simular área de trabajo AS400"
        os.system('cls' if os.name == 'nt' else 'clear')

    def run(self):
        "Ejecuta el loop principal del CLI"
        try:
            while True:
                opt = self.main_menu()
                if opt == "1":
                    self.show_variable_products()
                elif opt == "2":
                    self.show_product_variations()
                elif opt == "0":
                    self.last_message = "Gracias por usar el sistema. Hasta luego."
                    self.clear_screen()
                    self.ui.print_message_area(self.last_message)
                    break
                else:
                    self.last_message = "Opción inválida. Intente nuevamente."
        except KeyboardInterrupt:
            self.last_message = "Interrupción detectada. Saliendo del sistema."
            self.clear_screen()
            self.ui.print_message_area(self.last_message)
