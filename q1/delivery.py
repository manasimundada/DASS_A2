from rich.console import Console
from utils import read_json, write_json

console = Console()

class DeliveryManager:
    def __init__(self):
        self.logged_in_agents = set()

    def signup_login(self):
        data = read_json()
        agent_name = input("Enter your name (Delivery Agent): ").strip().lower()
        if agent_name not in data["delivery_agents"]:
            data["delivery_agents"].append(agent_name)
            write_json(data)
        self.logged_in_agents.add(agent_name)
        console.print(f"[bold green]Welcome, {agent_name.capitalize()}! You are now logged in.[/bold green]")
        return agent_name

    def update_order_status(self, agent_name):
        data = read_json()
        orders = data["orders"]
        if not orders:
            console.print("[bold red]No orders available for delivery.[/bold red]")
            return

        try:
            order_id = int(input("Enter Order ID to update: ").strip())
        except ValueError:
            console.print("[bold red]Invalid Order ID. Please enter a number.[/bold red]")
            return

        for order in orders:
            if order["id"] == order_id:
                if order["type"] == "Takeaway":
                    console.print("[bold yellow]This is a takeaway order and is already completed.[/bold yellow]")
                    return

                if order["delivery_agent"] != agent_name:
                    console.print(f"[bold red]This order is assigned to {order['delivery_agent'].capitalize()}.[/bold red]")
                    return

                if order["status"] == "Delivered":
                    console.print(f"[bold yellow]Order {order_id} has already been delivered and cannot be updated.[/bold yellow]")
                    return

                console.print(f"[bold blue]Current status: {order['status']}[/bold blue]")

                while True:
                    new_status = input("Enter new status (Picked Up / Out for Delivery / Delivered): ").strip().lower()

                    if order["status"] == "Pending" and new_status != "picked up":
                        console.print("[bold red]You must pick up this order first.[/bold red]")
                        continue

                    if order["status"] == "Picked Up" and new_status != "out for delivery":
                        console.print("[bold red]This order must be marked as 'Out for Delivery' before it can be delivered.[/bold red]")
                        continue

                    if order["status"] == "Out for Delivery" and new_status != "delivered":
                        console.print("[bold red]This order is already out for delivery and must be marked as 'Delivered' next.[/bold red]")
                        continue

                    order["status"] = new_status.capitalize()
                    console.print(f"[bold green]Order {order_id} status updated to '{order['status']}' by {agent_name.capitalize()}.[/bold green]")
                    write_json(data)  # Save changes after updating status
                    return

        console.print("[bold red]Order not found![/bold red]")

    def assign_delivery_agent(self, order):
        data = read_json()
        for agent in data["delivery_agents"]:
            if agent not in self.logged_in_agents:
                continue
            if not any(o["delivery_agent"] == agent and o["status"] != "Delivered" for o in data["orders"]):
                order["delivery_agent"] = agent
                return
        order["delivery_agent"] = "bob"
