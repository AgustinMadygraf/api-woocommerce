"""
Path: src/infrastructure/cli/as400_ui.py
"""

from colorama import Fore

class AS400UI:
    "Funciones de presentación con estilo AS400 IBM."
    def print_header(self, title):
        "Imprime el encabezado con estilo AS400"
        print(Fore.GREEN + "=" * 78)
        print(Fore.GREEN + f"{title.center(78)}")
        print(Fore.GREEN + "=" * 78)

    def print_menu(self):
        "Imprime el menú con estilo AS400"
        print(Fore.GREEN + "1. Ver productos variables".ljust(50) + "F1=Ayuda")
        print(Fore.GREEN + "2. Ver variaciones de producto".ljust(50) + "F3=Salir")
        print(Fore.GREEN + "0. Salir".ljust(50))
        print(Fore.GREEN + "=" * 78)

    def print_rows_area(self, rows):
        "Imprime un área de filas con estilo AS400"
        for row in rows:
            self.print_row(row)
            print(Fore.GREEN + "-" * 78)

    def print_row(self, data: dict):
        "Imprime una fila con estilo AS400"
        for k, v in data.items():
            key = str(k)[:20].ljust(20)
            val = str(v)[:55].ljust(55)
            print(Fore.GREEN + f"{key}{val}")

    def print_message_area(self, message):
        "Imprime un área de mensajes con estilo AS400"
        print(Fore.GREEN + "=" * 78)
        if message:
            print(Fore.YELLOW + f"{message[:76].ljust(76)}")
        else:
            print(Fore.GREEN + " " * 78)
        print(Fore.GREEN + "=" * 78)

    def print_variations_table(self, rows):
        "Imprime una tabla de variaciones con estilo AS400"
        print(Fore.GREEN + "=" * 78)
        print(Fore.GREEN + "ID".ljust(10) + "Cantidad".ljust(12) + "Estado".ljust(10) + "Manijas".ljust(15) + "Impresión".ljust(25))
        print(Fore.GREEN + "-" * 78)
        for row in rows:
            print(
                str(row.get("ID", "")).ljust(10) +
                str(row.get("Cantidad", "")).ljust(12) +
                str(row.get("Estado", "")).ljust(10) +
                str(row.get("Manijas", "")).ljust(15) +
                str(row.get("Impresion", "")).ljust(25)
            )
            print(Fore.GREEN + "-" * 78)
        print(Fore.GREEN + "=" * 78)
