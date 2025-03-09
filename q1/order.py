from rich.console import Console
from rich.table import Table

console = Console()

class OrderManager:
    def __init__(self):
        self.orders = []
        self.order_id = 1001  # Starting order ID

    def place_order(self):
        customer_name = input("Enter your name: ").strip()
        
        while True:
            order_type = input("Enter order type (Delivery/Takeaway): ").strip().lower()
            if order_type in ["delivery", "takeaway"]:
                break
            else:
                console.print("[bold red]Invalid option. Choose 'Delivery' or 'Takeaway'.[/bold red]")

        items = input("Enter items (comma-separated): ").split(",")

        order = {
            "id": self.order_id,
            "customer": customer_name,
            "type": order_type.capitalize(),
            "items": [item.strip() for item in items],
            "status": "Completed" if order_type == "takeaway" else "Pending",
            "delivery_agent": "-" if order_type == "takeaway" else "Not Assigned"
        }

        self.orders.append(order)
        console.print(f"[bold green]Order placed successfully! Your Order ID is {self.order_id}[/bold green]")
        self.order_id += 1

    def track_order(self):
        order_id = input("Enter your Order ID: ").strip()
        try:
            order_id = int(order_id)
        except ValueError:
            console.print("[bold red]Invalid Order ID. Please enter a number.[/bold red]")
            return

        for order in self.orders:
            if order["id"] == order_id:
                table = Table(title="Order Details")
                for key in order.keys():
                    table.add_column(key, justify="center", style="cyan")
                table.add_row(*map(str, order.values()))
                console.print(table)
                return

        console.print("[bold red]Order not found![/bold red]")
