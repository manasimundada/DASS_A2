from rich.console import Console
from rich.table import Table
from utils import read_json, write_json

console = Console()

class RestaurantManager:
    def view_menu(self):
        data = read_json()
        table = Table(title="Food Menu")
        table.add_column("Item", justify="center", style="cyan")
        table.add_column("Price (₹)", justify="center", style="green")
        for item, price in data["menu"].items():
            table.add_row(item.capitalize(), f"{price:.2f}")
        console.print(table)

    def edit_menu(self):
        while True:
            console.print("\n[bold magenta]=== Edit Menu ===[/bold magenta]")
            console.print("[yellow]1.[/yellow] Add Item")
            console.print("[yellow]2.[/yellow] Remove Item")
            console.print("[yellow]3.[/yellow] View Menu")
            console.print("[yellow]4.[/yellow] Back to Manager Menu")

            choice = input("\nSelect an option: ").strip()
            data = read_json()
            
            if choice == "1":
                new_item = input("Enter the name of the new item: ").strip().lower()
                new_price = input("Enter the price of the new item: ").strip()
                try:
                    new_price = float(new_price)
                    if new_item and new_item not in data["menu"]:
                        data["menu"][new_item] = new_price
                        write_json(data)
                        console.print(f"[bold green]{new_item.capitalize()} added to the menu with price ₹{new_price:.2f}.[/bold green]")
                    else:
                        console.print("[bold red]Invalid item or item already exists.[/bold red]")
                except ValueError:
                    console.print("[bold red]Invalid price. Please enter a valid number.[/bold red]")
            elif choice == "2":
                remove_item = input("Enter the name of the item to remove: ").strip().lower()
                if remove_item in data["menu"]:
                    del data["menu"][remove_item]
                    write_json(data)
                    console.print(f"[bold green]{remove_item.capitalize()} removed from the menu.[/bold green]")
                else:
                    console.print("[bold red]Item not found in the menu.[/bold red]")
            elif choice == "3":
                self.view_menu()
            elif choice == "4":
                break
            else:
                console.print("[bold red]Invalid option. Please try again.[/bold red]")

    def view_orders(self):
        data = read_json()
        if not data["orders"]:
            console.print("[bold red]No orders available.[/bold red]")
            return

        table = Table(title="All Orders")
        headers = data["orders"][0].keys()
        for header in headers:
            table.add_column(header, justify="center", style="cyan")

        for order in data["orders"]:
            table.add_row(*map(str, order.values()))

        console.print(table)
