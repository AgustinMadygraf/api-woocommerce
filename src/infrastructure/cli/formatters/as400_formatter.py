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
        return (Fore.GREEN + "=" * AS400Formatter.MAX_COLS + "\n" +
                Fore.GREEN + f"{title[:AS400Formatter.MAX_COLS].center(AS400Formatter.MAX_COLS)}" + "\n" +
                Fore.GREEN + "=" * AS400Formatter.MAX_COLS)

    @staticmethod
    def format_menu() -> str:
        menu_lines = [
            "1. Ver productos variables".ljust(50) + "F1=Ayuda",
            "2. Ver variaciones de producto".ljust(50) + "F3=Salir",
            "0. Salir".ljust(50),
            "=" * AS400Formatter.MAX_COLS
        ]
        return "\n".join([Fore.GREEN + line[:AS400Formatter.MAX_COLS] for line in menu_lines])

    @staticmethod
    def format_row(data: dict) -> str:
        return "\n".join([
            Fore.GREEN + f"{str(k)[:20].ljust(20)}{str(v)[:AS400Formatter.MAX_COLS - 20].ljust(AS400Formatter.MAX_COLS - 20)}"
            for k, v in data.items()
        ])

    @staticmethod
    def format_message_area(message: str) -> str:
        return (Fore.GREEN + "=" * AS400Formatter.MAX_COLS + "\n" +
                (Fore.YELLOW + f"{message[:AS400Formatter.MAX_COLS - 4].ljust(AS400Formatter.MAX_COLS - 4)}" if message else Fore.GREEN + " " * AS400Formatter.MAX_COLS) + "\n" +
                Fore.GREEN + "=" * AS400Formatter.MAX_COLS)

    # Métodos para formatear tablas pueden agregarse aquí
