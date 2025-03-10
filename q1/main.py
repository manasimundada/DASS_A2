from rich.console import Console
from order import OrderManager
from delivery import DeliveryManager
from restaurant import RestaurantManager

console = Console()

def main():
    order_manager = OrderManager()
    delivery_manager = DeliveryManager()
    restaurant_manager = RestaurantManager()

    while True:
        console.print("\n[bold cyan]=== Online Food Delivery System ===[/bold cyan]")
        console.print("[bold white]Who are you?[/bold white]")
        console.print("[yellow]1.[/yellow] Customer")
        console.print("[yellow]2.[/yellow] Company Manager")
        console.print("[yellow]3.[/yellow] Delivery Agent")
        console.print("[yellow]4.[/yellow] Exit")

        role = input("\nSelect your role: ").strip().lower()

        if role == "1":  # Customer
            while True:
                console.print("\n[bold magenta]=== Customer Menu ===[/bold magenta]")
                console.print("[yellow]1.[/yellow] View Menu")
                console.print("[yellow]2.[/yellow] Place Order")
                console.print("[yellow]3.[/yellow] Track Order")
                console.print("[yellow]4.[/yellow] Back to Main Menu")

                choice = input("\nSelect an option: ").strip().lower()
                if choice == "1":
                    restaurant_manager.view_menu()
                elif choice == "2":
                    order_manager.place_order()
                elif choice == "3":
                    order_manager.track_order()
                elif choice == "4":
                    break
                else:
                    console.print("[bold red]Invalid option. Please try again.[/bold red]")

        elif role == "2":  # Restaurant Manager
            while True:
                console.print("\n[bold magenta]=== Restaurant Manager Menu ===[/bold magenta]")
                console.print("[yellow]1.[/yellow] Edit Menu")
                console.print("[yellow]2.[/yellow] View Orders")
                console.print("[yellow]3.[/yellow] Back to Main Menu")

                choice = input("\nSelect an option: ").strip().lower()
                if choice == "1":
                    restaurant_manager.edit_menu()
                elif choice == "2":
                    restaurant_manager.view_orders()  # Remove orders parameter
                elif choice == "3":
                    break
                else:
                    console.print("[bold red]Invalid option. Please try again.[/bold red]")

        elif role == "3":  # Delivery Agent
            agent_name = None
            while True:
                console.print("\n[bold magenta]=== Delivery Agent Menu ===[/bold magenta]")
                console.print("[yellow]1.[/yellow] Login/Signup")
                console.print("[yellow]2.[/yellow] Update Order Status")
                console.print("[yellow]3.[/yellow] Back to Main Menu")

                choice = input("\nSelect an option: ").strip().lower()
                if choice == "1":
                    agent_name = delivery_manager.signup_login()
                elif choice == "2":
                    if agent_name:
                        delivery_manager.update_order_status(agent_name)  # Remove orders parameter
                    else:
                        console.print("[bold red]You must login/signup first.[/bold red]")
                elif choice == "3":
                    break
                else:
                    console.print("[bold red]Invalid option. Please try again.[/bold red]")

        elif role == "4":
            console.print("[bold green]Exiting application...[/bold green]")
            break
        else:
            console.print("[bold red]Invalid selection. Please enter a valid option.[/bold red]")

if __name__ == "__main__":
    main()
