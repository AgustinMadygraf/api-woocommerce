"""
Path: src/infrastructure/cli/as400_ui.py
"""

from colorama import Fore

def print_as400_header(title):
    "Imprime el encabezado con estilo AS400"
    print(Fore.GREEN + "=" * 78)
    print(Fore.GREEN + f"{title.center(78)}")
    print(Fore.GREEN + "=" * 78)

def print_as400_menu():
    "Imprime el menú con estilo AS400"
    print(Fore.GREEN + "1. Ver productos variables".ljust(50) + "F1=Ayuda")
    print(Fore.GREEN + "2. Ver variaciones de producto".ljust(50) + "F3=Salir")
    print(Fore.GREEN + "0. Salir".ljust(50))
    print(Fore.GREEN + "=" * 78)

def print_as400_rows_area(rows):
    "Imprime un área de filas con estilo AS400"
    for row in rows:
        print_as400_row(row)
        print(Fore.GREEN + "-" * 78)

def print_as400_row(data: dict):
    "Imprime una fila con estilo AS400"
    for k, v in data.items():
        key = str(k)[:20].ljust(20)
        val = str(v)[:55].ljust(55)
        print(Fore.GREEN + f"{key}{val}")

def print_as400_message_area(message):
    "Imprime un área de mensajes con estilo AS400"
    print(Fore.GREEN + "=" * 78)
    if message:
        print(Fore.YELLOW + f"{message[:76].ljust(76)}")
    else:
        print(Fore.GREEN + " " * 78)
    print(Fore.GREEN + "=" * 78)
