"""
Path: src/infrastructure/cli/as400_ui.py
"""

from colorama import Fore

class AS400UI:
    "Funciones de presentación con estilo AS400 IBM."
    MAX_COLS = 80
    MAX_ROWS = 24

    def print_header(self, title):
        "Imprime el encabezado con estilo AS400"
        print(Fore.GREEN + "=" * self.MAX_COLS)
        print(Fore.GREEN + f"{title[:self.MAX_COLS].center(self.MAX_COLS)}")
        print(Fore.GREEN + "=" * self.MAX_COLS)

    def print_menu(self):
        "Imprime el menú con estilo AS400"
        menu_lines = [
            "1. Ver productos variables".ljust(50) + "F1=Ayuda",
            "2. Ver variaciones de producto".ljust(50) + "F3=Salir",
            "0. Salir".ljust(50),
            "=" * self.MAX_COLS
        ]
        for line in menu_lines:
            print(Fore.GREEN + line[:self.MAX_COLS])

    def print_rows_area(self, rows):
        "Imprime un área de filas con estilo AS400, limitado a 24 filas"
        max_data_rows = self.MAX_ROWS - 2
        for row in rows[:max_data_rows]:
            self.print_row(row)
            print(Fore.GREEN + "-" * self.MAX_COLS)
        if len(rows) > max_data_rows:
            print(Fore.YELLOW + "[Más abajo...]".ljust(self.MAX_COLS))

    def print_row(self, data: dict):
        "Imprime una fila con estilo AS400"
        for k, v in data.items():
            key = str(k)[:20].ljust(20)
            val = str(v)[:self.MAX_COLS - 20].ljust(self.MAX_COLS - 20)
            print(Fore.GREEN + f"{key}{val[:self.MAX_COLS - 20]}")

    def print_message_area(self, message):
        "Imprime un área de mensajes con estilo AS400"
        print(Fore.GREEN + "=" * self.MAX_COLS)
        if message:
            print(Fore.YELLOW + f"{message[:self.MAX_COLS - 4].ljust(self.MAX_COLS - 4)}")
        else:
            print(Fore.GREEN + " " * self.MAX_COLS)
        print(Fore.GREEN + "=" * self.MAX_COLS)

    def print_variations_table(self, rows):
        "Imprime una tabla de variaciones con estilo AS400, limitado a 24 filas"
        header = (
            "ID".ljust(8) +
            "Cantidad".ljust(10) +
            "Estado".ljust(10) +
            "Manijas".ljust(15) +
            "Precio Final".rjust(13) + "   " +
            "Impresión".ljust(18)
        )
        print(Fore.GREEN + "=" * self.MAX_COLS)
        print(Fore.GREEN + header[:self.MAX_COLS])
        print(Fore.GREEN + "-" * self.MAX_COLS)
        max_data_rows = self.MAX_ROWS - 4  # Encabezado y separadores
        for row in rows[:max_data_rows]:
            line = (
                str(row.get("ID", ""))[:8].ljust(8) +
                str(row.get("Cantidad", ""))[:10].ljust(10) +
                str(row.get("Estado", ""))[:10].ljust(10) +
                str(row.get("Manijas", ""))[:15].ljust(15) +
                str(row.get("Precio Final", ""))[:13].rjust(13) + "   " +
                str(row.get("Impresion", ""))[:18].ljust(18)
            )
            print(line[:self.MAX_COLS])
            print(Fore.GREEN + "-" * self.MAX_COLS)
        if len(rows) > max_data_rows:
            print(Fore.YELLOW + "[Más abajo...]".ljust(self.MAX_COLS))
        print(Fore.GREEN + "=" * self.MAX_COLS)

    def print_variable_products_table(self, rows):
        "Imprime una tabla de productos variables con el orden solicitado, limitado a 24 filas"
        header = (
            "ID".ljust(6) +
            "Nombre".ljust(37) +
            "Estado".ljust(10) +
            "Tipo".ljust(10) +
            "Variaciones".ljust(12) +
            "Stock".ljust(10)
        )
        print(Fore.GREEN + "=" * self.MAX_COLS)
        print(Fore.GREEN + header[:self.MAX_COLS])
        print(Fore.GREEN + "-" * self.MAX_COLS)
        max_data_rows = self.MAX_ROWS - 4  # Encabezado y separadores
        for row in rows[:max_data_rows]:
            line = (
                str(row.get("ID", ""))[:6].ljust(6) +
                str(row.get("Nombre", ""))[:37].ljust(37) +
                str(row.get("Estado", ""))[:10].ljust(10) +
                str(row.get("Tipo", ""))[:10].ljust(10) +
                str(row.get("Variaciones", ""))[:12].ljust(12) +
                str(row.get("Stock", ""))[:10].ljust(10)
            )
            print(line[:self.MAX_COLS])
            print(Fore.GREEN + "-" * self.MAX_COLS)
        if len(rows) > max_data_rows:
            print(Fore.YELLOW + "[Más abajo...]".ljust(self.MAX_COLS))
        print(Fore.GREEN + "=" * self.MAX_COLS)
