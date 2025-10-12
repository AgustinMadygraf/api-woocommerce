"""
Formatter para formateo de datos con estilo avanzado usando Rich.
"""
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

class RichFormatter:
    "Encapsula la lógica de formateo para la UI usando Rich"
    console = Console()
    MAX_COLS = 80
    MAX_ROWS = 24

    @staticmethod
    def print_header(title: str):
        RichFormatter.console.print(Panel(Text(title, style="bold white"), style="green", width=RichFormatter.MAX_COLS))

    @staticmethod
    def print_menu(menu_items):
        table = Table(show_header=False, box=None, width=RichFormatter.MAX_COLS)
        for item in menu_items:
            table.add_row(Text(item, style="yellow"))
        RichFormatter.console.print(table)

    @staticmethod
    def print_message(message: str, msg_type: str = "info"):
        styles = {
            "error": "bold red",
            "warning": "bold yellow",
            "success": "bold green",
            "info": "bold blue"
        }
        icon = {
            "error": "❌",
            "warning": "⚠️",
            "success": "✅",
            "info": "ℹ️"
        }
        style = styles.get(msg_type, "bold blue")
        ic = icon.get(msg_type, "ℹ️")
        RichFormatter.console.print(Panel(f"{ic} {message}", style=style, width=RichFormatter.MAX_COLS))

    @staticmethod
    def print_table(headers, rows):
        table = Table(show_header=True, header_style="bold magenta", width=RichFormatter.MAX_COLS)
        for h in headers:
            table.add_column(h)
        for row in rows:
            table.add_row(*[str(row.get(h, "")) for h in headers])
        RichFormatter.console.print(table)

    @staticmethod
    def print_panel(content, style="white"):
        RichFormatter.console.print(Panel(content, style=style, width=RichFormatter.MAX_COLS))
