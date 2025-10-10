"""
Path: src/infrastructure/cli/as400_woocommerce_cli.py
"""

import os
import requests
from colorama import init, Fore
from src.infrastructure.cli.as400_ui import AS400UI

init(autoreset=True)

class AS400WooCommerceCLI:
    "CLI para consumir la API de WooCommerce con estética tipo AS400 IBM."
    def __init__(self, api_base: str):
        self.api_base = api_base
        self.last_message = ""
        self.ui = AS400UI()

    def main_menu(self):
        "Muestra el menú principal y captura la opción del usuario"
        self.clear_screen()
        self.ui.print_header("WOOCOMMERCE API - AS400 IBM STYLE")
        self.ui.print_menu()
        self.ui.print_message_area(self.last_message)
        self.last_message = ""
        return input(Fore.GREEN + "Seleccione opción: ").strip()

    def show_variable_products(self):
        "Muestra productos variables desde la API de WooCommerce, incluyendo cantidad de variaciones"
        self.clear_screen()
        self.ui.print_header("PRODUCTOS VARIABLES")
        try:
            resp = requests.get(f"{self.api_base}/products?product_type=variable", timeout=10)
            if resp.status_code != 200:
                self.last_message = f"Error: {resp.status_code} - {resp.text}"
                self.ui.print_message_area(self.last_message)
                input(Fore.GREEN + "Presione ENTER para continuar...")
                return
            products = resp.json()
            rows = []
            for prod in products:
                try:
                    var_resp = requests.get(
                        f"{self.api_base}/products/{prod.get('id')}/variations",
                        timeout=10
                    )
                    if var_resp.status_code == 200:
                        total_variaciones = len(var_resp.json())
                    else:
                        total_variaciones = "?"
                except requests.RequestException:
                    total_variaciones = "?"
                rows.append({
                    "ID": prod.get("id"),
                    "Nombre": prod.get("name"),
                    "SKU": prod.get("sku"),
                    "Estado": prod.get("status"),
                    "Tipo": prod.get("type"),
                    "Variaciones": total_variaciones,
                })
            # Imprimir tabla con formato alineado
            print(Fore.GREEN + "=" * 78)
            print(Fore.GREEN + "ID".ljust(8) + "Nombre".ljust(40) + "Estado".ljust(10) + "Tipo".ljust(10) + "Variaciones".ljust(10))
            print(Fore.GREEN + "-" * 78)
            for row in rows:
                print(
                    str(row.get("ID", "")).ljust(8) +
                    str(row.get("Nombre", "")).ljust(40) +
                    str(row.get("Estado", "")).ljust(10) +
                    str(row.get("Tipo", "")).ljust(10) +
                    str(row.get("Variaciones", "")).ljust(10)
                )
            print(Fore.GREEN + "=" * 78)
            self.last_message = f"Mostrando {len(products)} productos variables."
        except requests.RequestException as e:
            self.last_message = f"Error de conexión: {str(e)}"
        except ValueError as e:
            self.last_message = f"Error al procesar datos: {str(e)}"
        self.ui.print_message_area(self.last_message)
        input(Fore.GREEN + "Presione ENTER para continuar...")

    def show_product_variations(self):
        "Muestra todas las variaciones de un producto variable desde la API de WooCommerce"
        self.clear_screen()
        self.ui.print_header("VARIACIONES DE PRODUCTO")
        product_id = input(Fore.GREEN + "Ingrese el ID del producto variable: ").strip()
        try:
            all_variations = []

            while True:
                resp = requests.get(
                    f"{self.api_base}/products/{product_id}/variations",
                    timeout=20
                )

                if resp.status_code != 200:
                    self.last_message = f"Error: {resp.status_code} - {resp.text}"
                    self.ui.print_message_area(self.last_message)
                    input(Fore.GREEN + "Presione ENTER para continuar...")
                    return

                variations = resp.json()
                if not variations:  # No more results
                    break

                all_variations.extend(variations)
                break  # Solo una petición, ya que no hay paginación en el backend

            rows = []
            for var in all_variations:
                cantidad = ""
                manijas = ""
                impresion = ""
                for attr in var.get("attributes", []):
                    if attr.get("name", "").lower() == "cantidad":
                        cantidad = attr.get("option", "")
                    elif attr.get("name", "").lower() == "manijas":
                        manijas = attr.get("option", "")
                    elif attr.get("name", "").lower() == "impresión":
                        impresion = attr.get("option", "")
                rows.append({
                    "ID": var.get("id"),
                    "Precio": var.get("price"),
                    "Cantidad": cantidad,
                    "Estado": var.get("status"),
                    "Manijas": manijas,
                    "Impresion": impresion,
                })
            self.ui.print_variations_table(rows)
            self.last_message = f"Mostrando {len(rows)} variaciones."
        except requests.RequestException as e:
            self.last_message = f"Error de conexión: {str(e)}"
        except ValueError as e:
            self.last_message = f"Error al procesar datos: {str(e)}"
        self.ui.print_message_area(self.last_message)
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
