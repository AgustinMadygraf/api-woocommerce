"""
Path: src/infrastructure/cli/cli_app.py
"""

import os
import requests
from colorama import init, Fore

init(autoreset=True)

class AS400WooCommerceCLI:
    "CLI para consumir la API de WooCommerce con estética tipo AS400 IBM."
    def __init__(self, api_base: str):
        self.api_base = api_base
        self.last_message = ""

    def print_as400_header(self, title):
        "Imprime el encabezado (área superior)"
        print(Fore.GREEN + "=" * 78)
        print(Fore.GREEN + f"{title.center(78)}")
        print(Fore.GREEN + "=" * 78)

    def print_as400_menu(self):
        "Imprime el menú (área lateral/izquierda)"
        print(Fore.GREEN + "1. Ver productos variables".ljust(50) + "F1=Ayuda")
        print(Fore.GREEN + "2. Ver variaciones de producto".ljust(50) + "F3=Salir")
        print(Fore.GREEN + "0. Salir".ljust(50))
        print(Fore.GREEN + "=" * 78)

    def print_as400_rows_area(self, rows):
        "Imprime el área de trabajo (listado de datos)"
        for row in rows:
            self.print_as400_row(row)
            print(Fore.GREEN + "-" * 78)

    def print_as400_row(self, data: dict):
        "Imprime una fila de datos estilo AS400"
        for k, v in data.items():
            key = str(k)[:20].ljust(20)
            val = str(v)[:55].ljust(55)
            print(Fore.GREEN + f"{key}{val}")

    def print_as400_message_area(self):
        "Imprime el área de mensajes (pie de pantalla)"
        print(Fore.GREEN + "=" * 78)
        if self.last_message:
            print(Fore.YELLOW + f"{self.last_message[:76].ljust(76)}")
        else:
            print(Fore.GREEN + " " * 78)
        print(Fore.GREEN + "=" * 78)

    def main_menu(self):
        "Muestra la pantalla principal con áreas funcionales"
        self.clear_screen()
        self.print_as400_header("WOOCOMMERCE API - AS400 IBM STYLE")
        self.print_as400_menu()
        self.print_as400_message_area()
        return input(Fore.GREEN + "Seleccione opción: ").strip()

    def show_variable_products(self):
        "Muestra productos variables obtenidos desde la API"
        self.clear_screen()
        self.print_as400_header("PRODUCTOS VARIABLES")
        try:
            resp = requests.get(f"{self.api_base}/products?product_type=variable", timeout=10)
            if resp.status_code != 200:
                self.last_message = f"Error: {resp.status_code} - {resp.text}"
                self.print_as400_message_area()
                input(Fore.GREEN + "Presione ENTER para continuar...")
                return
            products = resp.json()
            rows = []
            for prod in products:
                rows.append({
                    "ID": prod.get("id"),
                    "Nombre": prod.get("name"),
                    "SKU": prod.get("sku"),
                    "Precio": prod.get("price"),
                    "Estado": prod.get("status"),
                    "Tipo": prod.get("type"),
                })
            self.print_as400_rows_area(rows)
            self.last_message = f"Mostrando {len(products)} productos variables."
        except requests.RequestException as e:
            self.last_message = f"Error de conexión: {str(e)}"
        except ValueError as e:
            self.last_message = f"Error al procesar datos: {str(e)}"
        self.print_as400_message_area()
        input(Fore.GREEN + "Presione ENTER para continuar...")

    def show_product_variations(self):
        "Muestra variaciones de un producto variable dado su ID"
        self.clear_screen()
        self.print_as400_header("VARIACIONES DE PRODUCTO")
        product_id = input(Fore.GREEN + "Ingrese el ID del producto variable: ").strip()
        try:
            resp = requests.get(f"{self.api_base}/products/{product_id}/variations", timeout=10)
            if resp.status_code != 200:
                self.last_message = f"Error: {resp.status_code} - {resp.text}"
                self.print_as400_message_area()
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
            self.print_as400_rows_area(rows)
            self.last_message = f"Mostrando {len(variations)} variaciones."
        except requests.RequestException as e:
            self.last_message = f"Error de conexión: {str(e)}"
        except ValueError as e:
            self.last_message = f"Error al procesar datos: {str(e)}"
        self.print_as400_message_area()
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
                    self.print_as400_message_area()
                    break
                else:
                    self.last_message = "Opción inválida. Intente nuevamente."
        except KeyboardInterrupt:
            self.last_message = "Interrupción detectada. Saliendo del sistema."
            self.clear_screen()
            self.print_as400_message_area()
