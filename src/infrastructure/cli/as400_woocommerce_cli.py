"""
Path: src/infrastructure/cli/as400_woocommerce_cli.py
"""

import os
from colorama import init, Fore
import keyboard  # Agrega esta importación
import msvcrt  # Agrega esta importación arriba

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
        "Muestra el menú principal y captura la opción del usuario o teclas F1/F3"
        self.clear_screen()
        self.ui.print_header("WOOCOMMERCE API - AS400 IBM STYLE")
        self.ui.print_menu()
        self.ui.print_message_area(self.last_message)
        self.last_message = ""

        print("Seleccione opción (o presione F1 para ayuda, F3 para salir):")
        while True:
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                if event.name == 'f1':
                    return 'F1'
                elif event.name == 'f3':
                    return '0'
                elif event.name.isdigit():
                    return event.name

    def show_variable_products(self):
        "Muestra productos variables desde la API de WooCommerce"
        self.clear_screen()
        print(Fore.YELLOW + "Cargando productos variables... Por favor espere.")
        # Bloquea teclado durante la carga
        keyboard.block_key('enter')
        keyboard.block_key('1')
        keyboard.block_key('2')
        keyboard.block_key('f1')
        keyboard.block_key('f3')
        self.flush_keyboard_events()
        self.flush_stdin()
        self.last_message = self.variable_products_cmd.execute()
        keyboard.unblock_key('enter')
        keyboard.unblock_key('1')
        keyboard.unblock_key('2')
        keyboard.unblock_key('f1')
        keyboard.unblock_key('f3')
        input(Fore.GREEN + "Presione ENTER para continuar...")

    def show_product_variations(self):
        "Muestra variaciones de un producto variable"
        self.clear_screen()
        self.flush_keyboard_events()
        self.flush_stdin()
        product_id = input(Fore.GREEN + "Ingrese el ID del producto variable: ").strip()
        print(Fore.YELLOW + "Cargando variaciones... Por favor espere.")
        # Bloquea teclado durante la carga
        keyboard.block_key('enter')
        keyboard.block_key('1')
        keyboard.block_key('2')
        keyboard.block_key('f1')
        keyboard.block_key('f3')
        self.last_message = self.product_variations_cmd.execute(product_id)
        keyboard.unblock_key('enter')
        keyboard.unblock_key('1')
        keyboard.unblock_key('2')
        keyboard.unblock_key('f1')
        keyboard.unblock_key('f3')
        self.flush_stdin()
        input(Fore.GREEN + "Presione ENTER para continuar...")

    def clear_screen(self):
        "Limpia la pantalla para simular área de trabajo AS400"
        os.system('cls' if os.name == 'nt' else 'clear')

    def flush_keyboard_events(self):
        "Vacía el buffer de eventos del teclado para evitar entradas fantasma"
        try:
            while keyboard.peek():
                keyboard.read_event(suppress=True)
        except AttributeError:
            # Si peek no existe, simplemente pasa
            pass
        keyboard.clear_all_hotkeys()

    def flush_stdin(self):
        "Vacía el buffer de stdin para evitar entradas fantasma en input()"
        while msvcrt.kbhit():
            msvcrt.getch()

    def run(self):
        "Ejecuta el loop principal del CLI"
        try:
            while True:
                opt = self.main_menu()
                if opt == "1":
                    self.show_variable_products()
                elif opt == "2":
                    self.show_product_variations()
                elif opt == "F1":
                    self.clear_screen()
                    self.ui.print_header("AYUDA")
                    print("F1: Ayuda\nF3/0: Salir\n1: Ver productos variables\n2: Ver variaciones de producto")
                    input("Presione ENTER para continuar...")
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
