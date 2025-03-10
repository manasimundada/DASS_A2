import uuid
import random
import sys
from getpass import getpass
from tabulate import tabulate

# ========== CLASS DEFINITIONS ==========

class User:
    def __init__(self, name, email, password):
        self.user_id = str(uuid.uuid4())
        self.name = name
        self.email = email
        self.password = password

class Customer(User):
    def __init__(self, name, email, password, address, is_retailer=False):
        super().__init__(name, email, password)
        self.address = address
        self.is_retailer = is_retailer
        self.discount = 0.1 if is_retailer else 0.05  
        self.orders = []
        self.coupons = []
        self.loyalty_points = 0
        self.cart = []  # Initialize empty cart
    
    def place_order(self, order):
        """
        Finalizes placing the order after we've adjusted all discounts in place_order() function.
        Adds the order to the customer's order list and awards loyalty points.
        """
        self.orders.append(order)
        self.earn_loyalty_points(order.total_price)
        print(f"\nOrder {order.order_id} placed successfully.\n")

    def view_orders(self):
        if not self.orders:
            print("\nNo orders found.\n")
        else:
            table = [[o.order_id, o.status, f"${o.total_price:.2f}"] for o in self.orders]
            print("\nYour Orders:\n" + tabulate(table, headers=["Order ID", "Status", "Total Price"], tablefmt="grid"))

    def earn_loyalty_points(self, total_spent):
        """
        1 point per $10 spent.
        """
        points_earned = int(total_spent // 10)
        self.loyalty_points += points_earned

        print(f"You earned {points_earned} points! Total points: {self.loyalty_points}")
        threshold = 50  # Points needed for the next discount coupon
        if self.loyalty_points >= threshold:
            self.generate_discount_coupon()
        else:
            needed = threshold - self.loyalty_points
            print(f"You need {needed} more points to earn a 5% discount coupon on orders over $100.")

    def generate_discount_coupon(self):
        discount_percentage = 5
        min_order_amount = 100
        new_coupon = DiscountCoupon(self, discount_percentage, min_order_amount)
        self.coupons.append(new_coupon)
        self.loyalty_points -= 50
        print(f"Congratulations! You received a {discount_percentage}% discount coupon for orders over ${min_order_amount}.")

    def add_to_cart(self, product, quantity):
        """Add a product to the customer's cart"""
        price = product.get_price(self.is_retailer)
        
        # Check if product already exists in cart
        for item in self.cart:
            if item['product'].product_id == product.product_id:
                item['quantity'] += quantity
                print(f"\nUpdated quantity of {product.name} in cart to {item['quantity']}.\n")
                return
        
        # Add new item to cart
        self.cart.append({"product": product, "quantity": quantity, "price": price})
        print(f"\nAdded {quantity} x {product.name} to your cart.\n")
    
    def remove_from_cart(self, product_index):
        """Remove a product from the cart by index"""
        if 0 <= product_index < len(self.cart):
            removed_item = self.cart.pop(product_index)
            print(f"\nRemoved {removed_item['product'].name} from your cart.\n")
        else:
            print("\nInvalid item index.\n")
    
    def clear_cart(self):
        """Empty the entire cart"""
        self.cart = []
        print("\nYour cart has been cleared.\n")
    
    def view_cart(self):
        """Display the contents of the customer's cart"""
        if not self.cart:
            print("\nYour cart is empty.\n")
            return
        
        table = [[i, item['product'].name, item['quantity'], 
                 f"${item['price']:.2f}", 
                 f"${item['price'] * item['quantity']:.2f}"] 
                for i, item in enumerate(self.cart)]
        
        print("\nYour Cart:\n" + tabulate(table, 
              headers=["#", "Product", "Quantity", "Price", "Total"], 
              tablefmt="grid"))
        
        cart_total = sum(item['price'] * item['quantity'] for item in self.cart)
        print(f"\nCart Total: ${cart_total:.2f}\n")

class Product:
    def __init__(self, name, category, price, retailer_price, stock):
        self.product_id = str(uuid.uuid4())
        self.name = name
        self.category = category
        self.price = price               # Non-retailer price
        self.retailer_price = retailer_price
        self.stock = stock

    def update_stock(self, quantity):
        if self.stock >= quantity:
            self.stock -= quantity
            return True
        else:
            print(f"\nInsufficient stock for {self.name}.\n")
            return False

    def get_price(self, is_retailer):
        """
        Returns the correct price depending on whether the customer is a retailer.
        """
        return self.retailer_price if is_retailer else self.price

    def __str__(self):
        return f"{self.name} - {self.category} - ${self.price} (${self.retailer_price} for retailers) - Stock: {self.stock}"

class Order:
    def __init__(self, customer, items):
        self.order_id = str(uuid.uuid4())
        self.customer = customer
        self.items = items
        # Subtotal is the sum of all items' line prices
        self.sub_total = sum(item['price'] * item['quantity'] for item in items)
        self.total_price = self.sub_total  # We'll apply discounts externally
        self.status = "Pending"

    def confirm_order(self):
        self.status = "Confirmed"
        self.delivery = Delivery(self)
        print(f"\nOrder {self.order_id} confirmed.")
        print(f"Delivery {self.delivery.delivery_id} created (estimated {self.delivery.estimated_days} days).")

class DiscountCoupon:
    def __init__(self, customer, discount_percentage, min_order_amount):
        self.coupon_id = str(uuid.uuid4())
        self.customer = customer
        self.discount_percentage = discount_percentage
        self.min_order_amount = min_order_amount

    def apply_discount(self, order):
        """
        Applies a coupon discount to the order if it meets the minimum order amount.
        """
        if order.total_price >= self.min_order_amount:
            discount_amount = (self.discount_percentage / 100) * order.total_price
            order.total_price -= discount_amount
            print(f"Coupon applied! You saved ${discount_amount:.2f}. New total: ${order.total_price:.2f}")
            return True
        print(f"Coupon requires a minimum order of ${self.min_order_amount}. Not applied.")
        return False

class Delivery:
    def __init__(self, order):
        self.delivery_id = str(uuid.uuid4())
        self.order = order
        self.status = "Processing"
        self.estimated_days = random.randint(2, 7)

    def update_status(self, new_status):
        self.status = new_status
        print(f"Delivery {self.delivery_id} status updated to {self.status}")

# ========== SAMPLE DATA ==========
products = [
    Product("Laptop", "Electronics", 1000, 900, 5),
    Product("Rice", "Grocery", 50, 45, 100),
    Product("Shampoo", "Personal Care", 10, 9, 50),
]

customers = []
current_customer = None

# ========== HELPER FUNCTIONS ==========

def is_valid_email(email: str) -> bool:
    return "@" in email and "." in email

def print_header(title):
    print("\n" + "=" * 50)
    print(f"  {title}".upper())
    print("=" * 50 + "\n")

def view_products():
    table = [
        [p.name, p.category, f"${p.price:.2f}", f"${p.retailer_price:.2f}", p.stock]
        for p in products
    ]
    print("\nAvailable Products:\n" + tabulate(
        table,
        headers=["Name", "Category", "Price", "Retailer Price", "Stock"],
        tablefmt="grid"
    ))

def view_coupons():
    print_header("Your Coupons")
    if not current_customer or not current_customer.coupons:
        print("No coupons available.")
    else:
        for coupon in current_customer.coupons:
            print(f"Coupon ID: {coupon.coupon_id} - {coupon.discount_percentage}% off on orders over ${coupon.min_order_amount}")

def add_to_cart_menu():
    print_header("Add to Cart")
    view_products()
    
    product_name = input("\nEnter product name to add to cart (or 'cancel'): ").strip().lower()
    if product_name == 'cancel':
        return
    
    product = next((p for p in products if p.name.lower() == product_name), None)
    if not product:
        print("\nProduct not found.\n")
        return
    
    try:
        quantity = int(input(f"Enter quantity for {product.name}: "))
        if quantity <= 0:
            print("\nQuantity must be positive.\n")
            return
            
        if quantity <= product.stock:
            current_customer.add_to_cart(product, quantity)
        else:
            print(f"\nInsufficient stock. Only {product.stock} available.\n")
    except ValueError:
        print("\nInvalid quantity. Please enter a number.\n")

def manage_cart_menu():
    print_header("Manage Cart")
    current_customer.view_cart()
    
    if not current_customer.cart:
        return
    
    print("\n1. Remove item\n2. Clear cart\n3. Return to main menu")
    choice = input("\nChoose an option: ")
    
    if choice == "1":
        try:
            index = int(input("Enter the # of item to remove: "))
            current_customer.remove_from_cart(index)
        except ValueError:
            print("\nInvalid input. Please enter a number.\n")
    
    elif choice == "2":
        confirm = input("Are you sure you want to clear your cart? (yes/no): ").lower()
        if confirm == "yes":
            current_customer.clear_cart()
    
    elif choice != "3":
        print("\nInvalid choice.\n")

def place_order():
    print_header("Place Order")
    
    # First check if cart is empty
    if not current_customer.cart:
        print("\nYour cart is empty. Add some items first.\n")
        return
    
    # Display cart contents
    current_customer.view_cart()
    
    # Confirm order placement
    confirm = input("\nProceed with order? (yes/no): ").lower()
    if confirm != "yes":
        print("\nOrder canceled.\n")
        return
    
    # Create order items from cart
    order_items = []
    for item in current_customer.cart:
        product = item['product']
        quantity = item['quantity']
        
        # Verify stock availability (may have changed since adding to cart)
        if product.update_stock(quantity):
            price = item['price']
            order_items.append({"product": product, "quantity": quantity, "price": price})
        else:
            print(f"\nOrder canceled due to insufficient stock of {product.name}.\n")
            return
    
    # Create the order with a sub_total
    order = Order(current_customer, order_items)

    # Show the user the subtotal before any discounts
    print(f"\nSubtotal (before any discounts): ${order.sub_total:.2f}")
    
    # Initialize discount tracking
    original_total = order.total_price
    
    # Apply discounts as before
    if current_customer.loyalty_points >= 50 and not current_customer.is_retailer:
        loyalty_discount_amount = order.total_price * current_customer.discount
        order.total_price -= loyalty_discount_amount
        print(f"Loyalty discount applied: You saved ${loyalty_discount_amount:.2f}")
    
    # Check for coupons
    if current_customer.coupons:
        print("\nYou have discount coupons available.")
        use_coupon = input("Would you like to apply a coupon? (yes/no): ").strip().lower()
        if use_coupon == "yes":
            applied = False
            for coupon in current_customer.coupons:
                if coupon.apply_discount(order):
                    current_customer.coupons.remove(coupon)
                    applied = True
                    break
            if not applied:
                print("No valid coupons could be applied.")

    # Finalize the order
    current_customer.place_order(order)
    
    # Clear the cart after successful order
    current_customer.cart = []

    # Show final total after all discounts
    if original_total != order.total_price:
        print(f"Original subtotal: ${original_total:.2f}")
        print(f"Final total after discounts: ${order.total_price:.2f}")
        print(f"You saved: ${original_total - order.total_price:.2f}")
    else:
        print(f"Final total (no discounts applied): ${order.total_price:.2f}")

def admin_menu():
    while True:
        print_header("Welcome Admin")
        print("1. Add Product\n2. Delete Product\n3. Update Product Price\n4. Update Product Stock\n5. Logout")
        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            name = input("Enter product name: ")
            category = input("Enter product category: ")
            try:
                price = float(input("Enter product price: "))
                retailer_price = float(input("Enter retailer price: "))
                stock = int(input("Enter initial stock: "))
                products.append(Product(name, category, price, retailer_price, stock))
                print(f"\nProduct '{name}' added successfully.\n")
            except ValueError:
                print("\nInvalid price or stock.\n")
        
        elif choice == "2":
            name = input("Enter product name to delete: ").lower()
            for p in products:
                if p.name.lower() == name:
                    products.remove(p)
                    print(f"\n'{p.name}' deleted.\n")
                    break
            else:
                print("\nProduct not found.\n")

        elif choice == "3":
            name = input("Enter product name to update price: ").lower()
            for p in products:
                if p.name.lower() == name:
                    try:
                        new_price = float(input("Enter new price: "))
                        p.price = new_price
                        print(f"\nPrice updated to ${new_price:.2f} for '{p.name}'.\n")
                    except ValueError:
                        print("\nInvalid price.\n")
                    break
            else:
                print("\nProduct not found.\n")

        elif choice == "4":
            name = input("Enter product name to update stock: ").lower()
            for p in products:
                if p.name.lower() == name:
                    try:
                        new_stock = int(input("Enter new stock: "))
                        p.stock = new_stock
                        print(f"\nStock updated to {new_stock} for '{p.name}'.\n")
                    except ValueError:
                        print("\nInvalid stock.\n")
                    break
            else:
                print("\nProduct not found.\n")

        elif choice == "5":
            print("\nAdmin logged out.\n")
            return
        else:
            print("\nInvalid choice. Try again.\n")

# ========== MAIN CLI MENU ==========

def main():
    global current_customer
    while True:
        if current_customer:
            print_header(f"Welcome, {current_customer.name}")
            print("1. View Products\n2. Add to Cart\n3. View/Edit Cart\n4. Place Order\n5. View Orders\n6. View Coupons\n7. Logout")
            choice = input("\nChoose an option: ")
            
            if choice == "1":
                view_products()
            elif choice == "2":
                add_to_cart_menu()
            elif choice == "3":
                manage_cart_menu()
            elif choice == "4":
                place_order()
            elif choice == "5":
                current_customer.view_orders()
            elif choice == "6":
                view_coupons()
            elif choice == "7":
                print("\nLogged out successfully.\n")
                current_customer = None
            else:
                print("\nInvalid choice. Try again.\n")

        else:
            print_header("DOLLMART E-MARKETPLACE")
            print("1. Register\n2. Login\n3. Exit")
            choice = input("\nChoose an option: ")
            
            if choice == "1":
                register_customer()
            elif choice == "2":
                login_customer()
            elif choice == "3":
                print("\nExiting the system. Have a great day.\n")
                sys.exit()
            else:
                print("\nInvalid choice. Try again.\n")

def register_customer():
    print_header("Register New Customer")
    name = input("Enter name: ")
    
    email = input("Enter email: ")
    while not is_valid_email(email):
        print("Invalid email format. Please try again.")
        email = input("Enter email again: ")

    password = getpass("Enter password (hidden): ")
    address = input("Enter address: ")
    is_retailer = input("Are you a retailer? (yes/no): ").strip().lower()
    while is_retailer not in ["yes", "no"]:
        print("Please answer yes or no.")
        is_retailer = input("Are you a retailer? (yes/no): ").strip().lower()

    is_retailer = (is_retailer == "yes")
    new_customer = Customer(name, email, password, address, is_retailer)
    customers.append(new_customer)
    print("\nRegistration successful. You can now log in.\n")

def login_customer():
    print_header("Login")
    email = input("Enter email: ")
    password = getpass("Enter password (hidden): ")

    global current_customer
    if email == "admin@dollmarket.com" and password == "admin":
        print("\nWelcome Admin.\n")
        admin_menu()
        return

    current_customer = next((c for c in customers if c.email == email and c.password == password), None)
    
    if current_customer:
        print(f"\nWelcome back, {current_customer.name}.\n")
    else:
        print("\nInvalid credentials. Try again.\n")

if __name__ == "__main__":
    main()
