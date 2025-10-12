"""
Formatter para formateo de datos con estilo AS400 IBM.
"""
from colorama import Fore

class AS400Formatter:
    "Encapsula la lógica de formateo para la UI AS400"
    MAX_COLS = 80
    MAX_ROWS = 24

    @staticmethod
    def format_header(title: str) -> str:
        "Formatea el encabezado con estilo AS400"
        return (Fore.GREEN + "=" * AS400Formatter.MAX_COLS + "\n" +
                Fore.GREEN + f"{title[:AS400Formatter.MAX_COLS].center(AS400Formatter.MAX_COLS)}" + "\n" +
                Fore.GREEN + "=" * AS400Formatter.MAX_COLS)

    @staticmethod
    def format_menu() -> str:
        "Formatea el menú con estilo AS400"
        menu = [
            "  0. Estado del sistema",
            "  1. Listar productos variables",
            "  2. Listar variaciones de producto",
            "  q. Salir (o F3)"
        ]
        menu_str = Fore.YELLOW + "\n".join(menu)
        return menu_str.center(AS400Formatter.MAX_COLS)

    @staticmethod
    def format_row(data: dict) -> str:
        "Formatea una fila con estilo AS400"
        return "\n".join([
            Fore.GREEN + f"{str(k)[:20].ljust(20)}{str(v)[:AS400Formatter.MAX_COLS - 20].ljust(AS400Formatter.MAX_COLS - 20)}"
            for k, v in data.items()
        ])

    @staticmethod
    def format_message_area(message: str) -> str:
        "Formatea el área de mensajes con estilo AS400"
        return (Fore.GREEN + "=" * AS400Formatter.MAX_COLS + "\n" +
                (Fore.YELLOW + f"{message[:AS400Formatter.MAX_COLS - 4].ljust(AS400Formatter.MAX_COLS - 4)}" if message else Fore.GREEN + " " * AS400Formatter.MAX_COLS) + "\n" +
                Fore.GREEN + "=" * AS400Formatter.MAX_COLS)
