"""
Path: src/infrastructure/cli/as400_woocommerce_cli.py
"""

import os
import msvcrt
from colorama import init, Fore
import keyboard

from src.infrastructure.cli.as400_ui import AS400UI
from src.infrastructure.cli.services.wc_api_client import WCApiClient
from src.interface_adapter.gateways.wc_gateway import WCGateway
from src.interface_adapter.controllers.cli_controller import CLIController


init(autoreset=True)

class AS400WooCommerceCLI:
    "CLI para consumir la API de WooCommerce con estética tipo AS400 IBM."
    def __init__(self, api_base: str):
        self.api_base = api_base
        self.last_message = ""
        self.ui = AS400UI()
        self.api_client: WCGateway = WCApiClient(api_base)
        self.controller = CLIController(self.api_client, self.ui)

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
        import time
        import threading
        self.clear_screen()
        keyboard.block_key('enter')
        keyboard.block_key('0')
        keyboard.block_key('1')
        keyboard.block_key('2')
        keyboard.block_key('f1')
        keyboard.block_key('f3')
        keyboard.block_key('q')
        self.flush_keyboard_events()
        self.flush_stdin()

        loading_done = threading.Event()
        result_holder = {}

        def loading_animation():
            loading_base = "Cargarndo"
            max_len = 80
            i = 1
            while not loading_done.is_set():
                dots = "." * (i % (max_len - len(loading_base)))
                line = (loading_base + dots)[:max_len]
                print(Fore.YELLOW + line, end='\r', flush=True)
                time.sleep(0.1)
                i += 1
            print(" " * max_len, end='\r')  # Limpiar línea

        def fetch_products():
            result_holder['msg'] = self.controller.show_variable_products()
            loading_done.set()

        t1 = threading.Thread(target=loading_animation)
        t2 = threading.Thread(target=fetch_products)
        t1.start()
        t2.start()
        t2.join()
        t1.join()

        self.last_message = result_holder.get('msg', '')
        self.ui.print_message_area(self.last_message)
        keyboard.unblock_key('enter')
        keyboard.unblock_key('0')
        keyboard.unblock_key('1')
        keyboard.unblock_key('2')
        keyboard.unblock_key('f1')
        keyboard.unblock_key('f3')
        keyboard.unblock_key('q')
        input(Fore.GREEN + "Presione ENTER para continuar...")

    def show_product_variations(self):
        "Muestra variaciones de un producto variable con paginación"
        self.clear_screen()
        self.flush_keyboard_events()
        self.flush_stdin()
        product_id = input(Fore.GREEN + "Ingrese el ID del producto variable: ").strip()
        per_page = 20
        page = 1
        while True:
            self.clear_screen()
            print(Fore.YELLOW + f"Cargando variaciones... Página {page} (F7=Anterior, F8=Siguiente, F3=Salir)")
            keyboard.block_key('enter')
            keyboard.block_key('f1')
            keyboard.block_key('f3')
            keyboard.block_key('f7')
            keyboard.block_key('f8')
            self.flush_keyboard_events()
            self.flush_stdin()
            result = self.controller.show_product_variations(product_id, page, per_page)
            keyboard.unblock_key('enter')
            keyboard.unblock_key('f1')
            keyboard.unblock_key('f3')
            keyboard.unblock_key('f7')
            keyboard.unblock_key('f8')
            if isinstance(result, tuple):
                _, total_pages = result
            else:
                _, total_pages = result, 1
            print(Fore.GREEN + f"Página {page}/{total_pages}  [F7=Anterior] [F8=Siguiente] [F3=Salir]")
            input_msg = Fore.GREEN + "Presione ENTER para continuar, F7/F8 para navegar, F3/q para salir..."
            print(input_msg)
            while True:
                event = keyboard.read_event()
                if event.event_type == keyboard.KEY_DOWN:
                    if event.name == 'f3':
                        return
                    elif event.name == 'f7' and page > 1:
                        page -= 1
                        break
                    elif event.name == 'f8' and page < total_pages:
                        page += 1
                        break
                    elif event.name == 'enter':
                        return

    def clear_screen(self):
        "Limpia la pantalla para simular área de trabajo AS400"
        os.system('cls' if os.name == 'nt' else 'clear')

    def flush_keyboard_events(self):
        "Vacía el buffer de eventos del teclado para evitar entradas fantasma"
        try:
            while keyboard.peek():
                keyboard.read_event(suppress=True)
        except AttributeError:
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
                    print("F1: Ayuda\nF3/q: Salir\n1: Ver productos variables\n2: Ver variaciones de producto")
                    input("Presione ENTER para continuar...")
                elif opt == "q":
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
