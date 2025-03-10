from rich.console import Console
from rich.table import Table
import random
from datetime import datetime, timedelta
from delivery import DeliveryManager
from restaurant import RestaurantManager
from utils import read_json, write_json

console = Console()

class OrderManager:
    def __init__(self):
        self.delivery_manager = DeliveryManager()
        self.restaurant_manager = RestaurantManager()

    def place_order(self):
        data = read_json()
        customer_name = input("Enter your name: ").strip()
        
        while True:
            order_type = input("Enter order type (Delivery/Takeaway): ").strip().lower()
            if order_type in ["delivery", "takeaway"]:
                break
            else:
                console.print("[bold red]Invalid option. Choose 'Delivery' or 'Takeaway'.[/bold red]")

        self.restaurant_manager.view_menu()
        items = input("Enter items (comma-separated): ").split(",")
        items = [item.strip().lower() for item in items]

        total_price = 0
        for item in items:
            if item not in data["menu"]:
                console.print(f"[bold red]Item '{item}' is not available in the menu.[/bold red]")
                return
            total_price += data["menu"][item]

        order = {
            "id": data["next_order_id"],
            "customer": customer_name,
            "type": order_type.capitalize(),
            "items": items,
            "total_price": total_price,
            "status": "Completed" if order_type == "takeaway" else "Pending",
            "delivery_agent": "-" if order_type == "takeaway" else "Not Assigned"
        }

        if order_type == "delivery":
            order["expected_delivery_time"] = random.randint(10, 45)
            order["order_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.delivery_manager.assign_delivery_agent(order)

        data["orders"].append(order)
        data["next_order_id"] += 1
        write_json(data)
        console.print(f"[bold green]Order placed successfully! Your Order ID is {data['next_order_id'] - 1}[/bold green]")
        console.print(f"[bold blue]Total Price: ₹{total_price:.2f}[/bold blue]")
        if order_type == "delivery":
            console.print(f"[bold blue]Estimated time left for delivery: {order['expected_delivery_time']} mins[/bold blue]")

    def track_order(self):
        data = read_json()
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
                if order["type"] == "Delivery":
                    if order["status"] != "Delivered":
                        order_time = datetime.strptime(order["order_time"], "%Y-%m-%d %H:%M:%S")
                        elapsed_minutes = int((datetime.now() - order_time).total_seconds() // 60)
                        time_left = order["expected_delivery_time"] - elapsed_minutes
                        if time_left < 0:
                            time_left = 0
                        console.print(f"[bold blue]Estimated time left for delivery: {time_left} mins[/bold blue]")
                return

        console.print("[bold red]Order not found![/bold red]")
