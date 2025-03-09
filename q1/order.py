from rich.console import Console
from rich.table import Table
from data_storage import read_data, write_data

console = Console()

class OrderManager:
    def __init__(self):
        # No need to store state in memory as we'll read from file each time
        pass

    def place_order(self):
        # Read current data
        data = read_data()
        
        customer_name = input("Enter your name: ").strip()
        
        while True:
            order_type = input("Enter order type (Delivery/Takeaway): ").strip().lower()
            if order_type in ["delivery", "takeaway"]:
                break
            else:
                console.print("[bold red]Invalid option. Choose 'Delivery' or 'Takeaway'.[/bold red]")

        items = input("Enter items (comma-separated): ").split(",")

        # Create new order with ID from file
        order = {
            "id": data["next_order_id"],
            "customer": customer_name,
            "type": order_type.capitalize(),
            "items": [item.strip() for item in items],
            "status": "Completed" if order_type == "takeaway" else "Pending",
            "delivery_agent": "-" if order_type == "takeaway" else "Not Assigned"
        }

        # Update data and write back to file
        data["orders"].append(order)
        data["next_order_id"] += 1
        write_data(data)
        
        console.print(f"[bold green]Order placed successfully! Your Order ID is {order['id']}[/bold green]")

    def track_order(self):
        # Read fresh data for each operation
        data = read_data()
        
        order_id = input("Enter your Order ID: ").strip()
        try:
            order_id = int(order_id)
        except ValueError:
            console.print("[bold red]Invalid Order ID. Please enter a number.[/bold red]")
            return

        for order in data["orders"]:
            if order["id"] == order_id:
                table = Table(title="Order Details")
                for key in order.keys():
                    table.add_column(key, justify="center", style="cyan")
                table.add_row(*map(str, order.values()))
                console.print(table)
                return

        console.print("[bold red]Order not found![/bold red]")
