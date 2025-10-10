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
                        f"{self.api_base}/products/{prod.get('id')}/variations?per_page=1",
                        timeout=10
                    )
                    if var_resp.status_code == 200:
                        total_variaciones = var_resp.headers.get("X-WP-Total", "?")
                    else:
                        total_variaciones = "?"
                except requests.RequestException:
                    total_variaciones = "?"
                rows.append({
                    "ID": prod.get("id"),
                    "Nombre": prod.get("name"),
                    "Estado": prod.get("status"),
                    "Tipo": prod.get("type"),
                    "Variaciones": total_variaciones,
                    "Stock": prod.get("stock_quantity") if prod.get("stock_quantity") is not None else "Por variación",
                })
            # Imprimir tabla con formato alineado
            print(Fore.GREEN + "=" * 90)
            print(Fore.GREEN + "ID".ljust(7) + 
                  "Estado".ljust(10) + 
                  "Tipo".ljust(10) + 
                  "Variaciones".ljust(12) + 
                  "Stock".ljust(10) + 
                  "Nombre".ljust(40))
            print(Fore.GREEN + "-" * 90)
            for row in rows:
                print(
                    str(row.get("ID", "")).ljust(7) +
                    str(row.get("Estado", "")).ljust(10) +
                    str(row.get("Tipo", "")).ljust(10) +
                    str(row.get("Variaciones", "")).ljust(12) +
                    str(row.get("Stock", "")).ljust(10) +
                    str(row.get("Nombre", "")).ljust(40)
                )
            print(Fore.GREEN + "=" * 90)
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
            per_page = 50  # Puedes ajustar este valor (máximo 100)
            page = 1
            total = None

            while True:
                resp = requests.get(
                    f"{self.api_base}/products/{product_id}/variations?per_page={per_page}&page={page}",
                    timeout=20
                )

                if resp.status_code != 200:
                    self.last_message = f"Error: {resp.status_code} - {resp.text}"
                    self.ui.print_message_area(self.last_message)
                    input(Fore.GREEN + "Presione ENTER para continuar...")
                    return

                variations = resp.json()
                if not variations:
                    break

                all_variations.extend(variations)

                # Leer el total de variaciones del header
                if total is None:
                    total_str = resp.headers.get("X-WP-Total")
                    total = int(total_str) if total_str and total_str.isdigit() else None

                # Si ya tenemos todas las variaciones, salimos
                if total is not None and len(all_variations) >= total:
                    break

                page += 1

            rows = []
            for var in all_variations:
                cantidad = ""
                manijas = ""
                impresion = ""
                con_sin_manijas = ""
                for attr in var.get("attributes", []):
                    if attr.get("name", "").lower() == "cantidad":
                        cantidad = attr.get("option", "")
                    elif attr.get("name", "").lower() == "impresión":
                        impresion = attr.get("option", "")
                    elif attr.get("name", "").lower() == "con o sin manijas":
                        manijas = attr.get("option", "")
                        if manijas.strip().lower() == "con manijas":
                            con_sin_manijas = "Con manijas"
                        elif manijas.strip().lower() == "sin manijas":
                            con_sin_manijas = "Sin manijas"
                        else:
                            con_sin_manijas = manijas  # Por si hay otros valores
                precio_final_raw = var.get("price")
                try:
                    precio_final = "{:,.2f}".format(float(precio_final_raw)) if precio_final_raw else ""
                except (ValueError, TypeError):
                    precio_final = precio_final_raw or ""
                rows.append({
                    "ID": var.get("id"),
                    "Precio": precio_final,
                    "Cantidad": cantidad,
                    "Estado": var.get("status"),
                    "Manijas": manijas,
                    "Impresion": impresion,
                    "Precio Final": precio_final,
                    "Con/Sin Manijas": con_sin_manijas,
                })
            # Ordenar por cantidad ascendente
            rows.sort(key=lambda x: int(x["Cantidad"]) if str(x["Cantidad"]).isdigit() else 0)
            # Luego ordenar por impresión descendente (mantiene el orden de cantidad dentro de cada impresión)
            rows.sort(key=lambda x: str(x["Impresion"]).lower(), reverse=True)
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
