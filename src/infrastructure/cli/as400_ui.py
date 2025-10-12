"""
Path: src/infrastructure/cli/as400_ui.py
"""

from colorama import Fore

from src.infrastructure.cli.formatters.rich_formatter import RichFormatter
from src.infrastructure.cli.formatters.as400_formatter import AS400Formatter

class AS400UI:
    "Funciones de presentación con estilo AS400 IBM."
    MAX_COLS = 80
    MAX_ROWS = 24

    def print_header(self, title):
        "Imprime el encabezado con estilo Rich"
        RichFormatter.print_header(title)

    def print_menu(self):
        "Imprime el menú con estilo Rich"
        menu_items = [
            "  0. Estado del sistema (API WooCommerce)",
            "  1. Estado del sistema (Almacenamiento Local)",
            "  2. Listar productos variables (Almacenamiento Local)",
            "  3. Listar variaciones de producto (Almacenamiento Local)",
            "  4. Listar productos variables (API WooCommerce)",
            "  5. Listar variaciones de producto (API WooCommerce)",
            "  q. Salir (o F3)"
        ]
        RichFormatter.print_menu(menu_items)

    def print_rows_area(self, rows):
        "Imprime un área de filas con estilo AS400, limitado a 24 filas"
        max_data_rows = self.MAX_ROWS - 2
        for row in rows[:max_data_rows]:
            self.print_row(row)
            print(Fore.GREEN + "-" * self.MAX_COLS)
        if len(rows) > max_data_rows:
            print(Fore.YELLOW + "[Más abajo...]".ljust(self.MAX_COLS))

    def print_row(self, data: dict):
        "Imprime una fila con estilo AS400 usando el formatter"
        print(AS400Formatter.format_row(data))

    def print_message_area(self, message, msg_type="info"):
        "Imprime un área de mensajes con estilo Rich"
        RichFormatter.print_message(message, msg_type)

    def print_variations_table(self, rows):
        "Imprime una tabla de variaciones con Rich"
        headers = ["ID", "Cantidad", "Estado", "Manijas", "Precio Final", "Impresion"]
        RichFormatter.print_table(headers, rows)

    def print_variable_products_table(self, rows):
        "Imprime una tabla de productos variables con Rich"
        headers = ["ID", "Nombre", "Estado", "Tipo", "Variaciones", "Stock"]
        RichFormatter.print_table(headers, rows)
