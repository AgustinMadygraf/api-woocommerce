"""
Path: src/infrastructure/cli/as400_woocommerce_cli.py
"""

import os
import requests
from colorama import init, Fore
from src.infrastructure.cli.as400_ui import (
    print_as400_header,
    print_as400_menu,
    print_as400_rows_area,
    print_as400_message_area,
)

init(autoreset=True)

class AS400WooCommerceCLI:
    "CLI para consumir la API de WooCommerce con estética tipo AS400 IBM."
    def __init__(self, api_base: str):
        self.api_base = api_base
        self.last_message = ""

    def main_menu(self):
        "Muestra el menú principal y captura la opción del usuario"
        self.clear_screen()
        print_as400_header("WOOCOMMERCE API - AS400 IBM STYLE")
        print_as400_menu()
        print_as400_message_area(self.last_message)
        return input(Fore.GREEN + "Seleccione opción: ").strip()

    def show_variable_products(self):
        "Muestra productos variables desde la API de WooCommerce"
        self.clear_screen()
        print_as400_header("PRODUCTOS VARIABLES")
        try:
            resp = requests.get(f"{self.api_base}/products?product_type=variable", timeout=10)
            if resp.status_code != 200:
                self.last_message = f"Error: {resp.status_code} - {resp.text}"
                print_as400_message_area(self.last_message)
                input(Fore.GREEN + "Presione ENTER para continuar...")
                return
            products = resp.json()
            rows = []
            for prod in products:
                rows.append({
                    "ID": prod.get("id"),
                    "Nombre": prod.get("name"),
                    "SKU": prod.get("sku"),
                    # "Precio": prod.get("price"),  # Eliminar este campo para productos variables
                    "Estado": prod.get("status"),
                    "Tipo": prod.get("type"),
                })
            print_as400_rows_area(rows)
            self.last_message = f"Mostrando {len(products)} productos variables."
        except requests.RequestException as e:
            self.last_message = f"Error de conexión: {str(e)}"
        except ValueError as e:
            self.last_message = f"Error al procesar datos: {str(e)}"
        print_as400_message_area(self.last_message)
        input(Fore.GREEN + "Presione ENTER para continuar...")

    def show_product_variations(self):
        "Muestra variaciones de un producto variable desde la API de WooCommerce"
        self.clear_screen()
        print_as400_header("VARIACIONES DE PRODUCTO")
        product_id = input(Fore.GREEN + "Ingrese el ID del producto variable: ").strip()
        try:
            resp = requests.get(f"{self.api_base}/products/{product_id}/variations", timeout=10)
            if resp.status_code != 200:
                self.last_message = f"Error: {resp.status_code} - {resp.text}"
                print_as400_message_area(self.last_message)
                input(Fore.GREEN + "Presione ENTER para continuar...")
                return
            variations = resp.json()
            rows = []
            for var in variations:
                rows.append({
                    "ID": var.get("id"),
                    "SKU": var.get("sku"),
                    "Precio": var.get("price"),
                    "Estado": var.get("status"),
                    "Atributos": str(var.get("attributes")),
                })
            print_as400_rows_area(rows)
            self.last_message = f"Mostrando {len(variations)} variaciones."
        except requests.RequestException as e:
            self.last_message = f"Error de conexión: {str(e)}"
        except ValueError as e:
            self.last_message = f"Error al procesar datos: {str(e)}"
        print_as400_message_area(self.last_message)
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
                    print_as400_message_area(self.last_message)
                    break
                else:
                    self.last_message = "Opción inválida. Intente nuevamente."
        except KeyboardInterrupt:
            self.last_message = "Interrupción detectada. Saliendo del sistema."
            self.clear_screen()
            print_as400_message_area(self.last_message)
