from rich.console import Console
from rich.table import Table

console = Console()

class RestaurantManager:
    def __init__(self):
        self.menu = ["Burger", "Pizza", "Pasta", "Salad"]

    def view_orders(self, orders):
        if not orders:
            console.print("[bold red]No orders available.[/bold red]")
            return

        table = Table(title="All Orders")
        headers = orders[0].keys()
        for header in headers:
            table.add_column(header, justify="center", style="cyan")

        for order in orders:
            table.add_row(*map(str, order.values()))

        console.print(table)
