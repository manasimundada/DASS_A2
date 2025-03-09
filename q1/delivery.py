from rich.console import Console
from data_storage import read_data, write_data

console = Console()

class DeliveryManager:
    def __init__(self):
        # No need to store state as we'll read from file each time
        pass

    def update_order_status(self):
        # Read fresh data
        data = read_data()
        orders = data["orders"]
        
        if not orders:
            console.print("[bold red]No orders available for delivery.[/bold red]")
            return

        agent_name = input("Enter your name (Delivery Agent): ").strip().capitalize()

        try:
            order_id = int(input("Enter Order ID to update: ").strip())
        except ValueError:
            console.print("[bold red]Invalid Order ID. Please enter a number.[/bold red]")
            return

        for i, order in enumerate(orders):
            if order["id"] == order_id:
                if order["type"] == "Takeaway":
                    console.print("[bold yellow]This is a takeaway order and is already completed.[/bold yellow]")
                    return

                # Prevent another agent from updating an already assigned order
                if order["delivery_agent"] != "Not Assigned" and order["delivery_agent"] != agent_name:
                    console.print(f"[bold red]This order is already being handled by {order['delivery_agent']}.[/bold red]")
                    return

                # Prevent modification of a delivered order
                if order["status"] == "Delivered":
                    console.print(f"[bold yellow]Order {order_id} has already been delivered and cannot be updated.[/bold yellow]")
                    return

                console.print(f"[bold blue]Current status: {order['status']}[/bold blue]")

                while True:
                    new_status = input("Enter new status (Picked Up / Out for Delivery / Delivered): ").strip().lower()

                    # **Strictly enforce status progression**
                    if order["status"] == "Pending":
                        if new_status != "picked up":
                            console.print("[bold red]You must pick up this order first.[/bold red]")
                            continue

                    elif order["status"] == "Picked Up":
                        if new_status != "out for delivery":
                            console.print("[bold red]This order must be marked as 'Out for Delivery' before it can be delivered.[/bold red]")
                            continue

                    elif order["status"] == "Out for Delivery":
                        if new_status != "delivered":
                            console.print("[bold red]This order is already out for delivery and must be marked as 'Delivered' next.[/bold red]")
                            continue

                    # **Valid Status Change**
                    order["status"] = new_status.capitalize()
                    order["delivery_agent"] = agent_name  # Auto-assign delivery agent
                    
                    # Update the order in the data and write back to file
                    data["orders"][i] = order
                    write_data(data)
                    
                    console.print(f"[bold green]Order {order_id} status updated to '{order['status']}' by {agent_name}.[/bold green]")
                    return

        console.print("[bold red]Order not found![/bold red]")
