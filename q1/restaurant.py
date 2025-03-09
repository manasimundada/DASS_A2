from rich.console import Console
from rich.table import Table
from data_storage import read_data

console = Console()

class RestaurantManager:
    def __init__(self):
        self.menu = ["Burger", "Pizza", "Pasta", "Salad"]

    def view_orders(self):
        # Read fresh data
        data = read_data()
        orders = data["orders"]
        
        if not orders:
            console.print("[bold red]No orders available.[/bold red]")
            return

        table = Table(title="All Orders")
        headers = orders[0].keys() if orders else []
        
        if headers:
            for header in headers:
                table.add_column(header, justify="center", style="cyan")

            for order in orders:
                table.add_row(*map(str, order.values()))

            console.print(table)
