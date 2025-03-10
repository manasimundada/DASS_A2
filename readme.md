# **Q1 Software Specification Document**
## **1. System Overview**
The online food delivery system aims to streamline food ordering, preparation, and delivery for a new food company. It will support **Home Delivery and Takeaway orders**, with real-time tracking and an efficient order management system.

The system will consist of:
- A **Customer Interface** for placing orders and tracking them.
- A **Delivery Management System** to allocate orders to delivery agents.
- A **Restaurant Manager Dashboard** to monitor order status and kitchen operations.
- A **Persistent Application Instance** ensuring real-time updates across all sessions.

---

## **2. Key Functional Requirements**
### **2.1 User Roles**
1. **Customer**
   - Browse menu & place orders.
   - Select either **Home Delivery** or **Takeaway**.
   - Track order status and estimated delivery time.
   - Make online payments or opt for cash-on-delivery.
   - Manage multiple concurrent orders.
   - Provide feedback/rating after order completion.

2. **Delivery Agent**
   - Receive assigned orders for delivery.
   - Get optimized delivery routes.
   - Update real-time status (picked up, en route, delivered).
   - Mark order as completed.

3. **Restaurant Manager**
   - Monitor all incoming orders.
   - Update order preparation status.
   - View delivery agent assignments.
   - Manage restaurant menu and availability.

4. **Admin (System Manager)**
   - Oversee all system activities.
   - Manage users, restaurants, and delivery agents.
   - Access analytics and reports.

---

## **3. System Features & Functionalities**
### **3.1 Ordering System**
- Customers can select items from the menu.
- Option to customize orders (e.g., extra toppings, special requests).
- Multiple orders can be placed simultaneously.
- Customers can choose between **Home Delivery** and **Takeaway**.
- Automatic price calculation, including taxes and delivery fees.

### **3.2 Real-Time Order Tracking**
- Customers get estimated time of preparation and delivery.
- Live status updates (e.g., Order Received → Preparing → Out for Delivery → Delivered).
- Push notifications for major status changes.

### **3.3 Delivery Management**
- Auto-assign delivery agents based on proximity and availability.
- Delivery agents receive optimized route recommendations.
- Delivery progress is updated in real-time.

### **3.4 Persistent Application Instance**
- Shared session across multiple terminals.
- Order status updates in real-time, even if multiple devices are used.
- Database-driven system ensuring no data loss between sessions.

### **3.5 Payment & Checkout**
- Integration with UPI, Credit/Debit Cards, and Wallets.
- Cash-on-Delivery option.
- Refund and cancellation policies.

### **3.6 Restaurant Manager Dashboard**
- View & manage new, ongoing, and completed orders.
- Assign orders manually if required.
- Modify restaurant details and menu items.

### **3.7 User Feedback & Ratings**
- Customers can rate food, delivery, and overall experience.
- Restaurants can view feedback and respond.

---

## **4. Use Cases**
### **4.1 Customer Use Cases**
| Use Case ID | Use Case Name | Description |
|-------------|-------------|-------------|
| UC-1 | Browse Menu | Customers can view available food items and prices. |
| UC-2 | Place Order | Customers can select items and confirm an order. |
| UC-3 | Choose Order Type | Customers choose between **Home Delivery** and **Takeaway**. |
| UC-4 | Make Payment | Customers complete payment via various options. |
| UC-5 | Track Order | Customers track real-time order status and estimated time. |
| UC-6 | Rate & Review | Customers give feedback on food and delivery service. |

### **4.2 Delivery Agent Use Cases**
| Use Case ID | Use Case Name | Description |
|-------------|-------------|-------------|
| UC-7 | Receive Order Assignment | Delivery agents are notified of new orders. |
| UC-8 | Update Order Status | Delivery agents mark orders as picked up and delivered. |
| UC-9 | View Delivery Route | Delivery agents receive navigation assistance. |

### **4.3 Restaurant Manager Use Cases**
| Use Case ID | Use Case Name | Description |
|-------------|-------------|-------------|
| UC-10 | View Orders | The restaurant manager views all incoming orders. |
| UC-11 | Update Order Status | Mark orders as **Preparing, Ready for Pickup, or Completed**. |
| UC-12 | Assign Delivery Agents | Manually assign orders if necessary. |

### **4.4 Admin Use Cases**
| Use Case ID | Use Case Name | Description |
|-------------|-------------|-------------|
| UC-13 | Manage Users | Admins can add, remove, or modify user accounts. |
| UC-14 | Manage Restaurants | Admins can onboard new restaurants and update details. |
| UC-15 | Generate Reports | Admins access analytics and performance metrics. |

---

## **5. Test Cases and Implementation Notes**

### **5.1 Overview of Test Coverage**
The test suite covers all major components of the online food delivery system: Restaurant management, Order processing, and Delivery management. Tests ensure that the system meets all requirements specified by the company.

### **5.2 Test Cases Implementation**

#### **Restaurant Manager Tests**
- **Test View Menu**: Verifies that menu items are correctly displayed to users
- **Test Edit Menu**: Multiple test cases for adding, removing, and modifying menu items
  - Adding new items with valid prices
  - Adding items that already exist (should fail)
  - Removing existing items
  - Removing non-existent items (should fail)
- **Test View Orders**: Ensures orders are displayed correctly, including handling empty order lists

#### **Order Manager Tests**
- **Test Place Order**: 
  - Placing delivery orders with valid items
  - Placing takeaway orders
  - Handling invalid item errors
- **Test Track Order**: 
  - Tracking delivery orders with correct time estimation
  - Tracking takeaway orders
  - Handling non-existent orders
  - Validating order ID input

#### **Delivery Manager Tests**
- **Test Agent Login/Signup**: 
  - Login with existing agents
  - Creating new agent accounts
- **Test Order Status Updates**:
  - Valid status updates through the delivery workflow
  - Invalid status updates (out of sequence)
  - Handling invalid order IDs
  - Preventing agents from updating orders assigned to others
- **Test Agent Assignment**: Automatic assignment of delivery agents to orders

### **5.3 Testing Methodology**
- **Unit Testing**: Testing individual components in isolation
- **Mock Objects**: Utilizing mock objects to simulate external dependencies
- **Test Data**: Creating standardized test data for consistent testing

### **5.4 How to Run Tests**

#### **Running Tests**
1. Run all tests using the test runner:
   ```
   python testcases/test_runner.py
   ```

2. To run individual test modules:
   ```
   python -m unittest testcases/test_restaurant.py
   python -m unittest testcases/test_order.py
   python -m unittest testcases/test_delivery.py
   ```

### **5.5 Implementation Notes**

#### **Persistent Application Instance**
- The system uses file-based persistence with JSON data storage
- All application instances read from and write to the same JSON file
- This ensures data consistency across multiple terminals

#### **Home Delivery and Takeaway Support**
- Orders can be placed as either delivery or takeaway
- Different workflows implemented for each type
- Takeaway orders are marked completed immediately
- Delivery orders are assigned to agents with status tracking

#### **Order Time Tracking**
- Delivery orders include expected delivery time
- Real-time calculation of remaining delivery time
- Progress tracking through various status updates

#### **Multiple Concurrent Orders**
- System supports multiple orders in different states
- Orders are identified by unique IDs
- Can be placed and tracked independently

#### **Restaurant Manager Perspective**
- Complete view of all orders in the system
- Ability to modify menu items and pricing
- Order monitoring across all statuses

# **Q2: Gobblet Jr. Board Game**
### **Overview**
Gobblet Jr. is a 3x3 board game based on the tic-tac-toe concept. Players use three sizes of pieces to cover smaller ones.

### **Implementation Details**
- **Pygame-based UI**
- **Supports move validation, piece stacking, and win detection**
- **Interactive drag-and-drop gameplay**
- **Turn-based mechanics**

### **Linting & Code Improvements**
1. **Initial Lint Report (Score: 6.93/10)** - Issues included:
   - Trailing whitespaces
   - Long lines exceeding 100 characters
   - Missing docstrings
   - Too many nested blocks

2. **Iteration 2 (Score: 7.39/10)** - Fixes:
   - Removed unnecessary else-after-return
   - Reduced argument count in functions
   - Fixed variable naming issues

3. **Iteration 3 (Score: 7.64/10)** - Fixes:
   - Added missing docstrings
   - Reduced nested blocks
   - Improved readability

4. **Final Iteration (Score: 7.82/10)** - Fixes:
   - Removed unused variables
   - Optimized function complexity
   - Improved PEP8 compliance

### **How to Run Gobblet Jr.**
```bash
python gobbletfinal.py
```

### **How to Run Pylint Analysis**
```bash
pylint gobbletfinal.py
```

---

# Q3: Dollmart E-Marketing System

## Overview
This implementation of the Dollmart e-marketing system provides a command-line interface (CLI) for customers to browse products, place orders, and manage their shopping experience. The system follows object-oriented design principles and is represented visually using a UML class diagram.

## System Features
- **User Management**: Registration and login for customers
- **Customer Types**: Support for both regular customers and retailers with different pricing
- **Shopping Cart**: Add, remove, and view items in cart
- **Order Processing**: Place orders and track status
- **Discount System**: Loyalty points and discount coupons
- **Delivery Tracking**: Order delivery status updates

## UML Class Diagram
The UML diagram (located in `uml/diagram.mmd`) represents the class structure of the system:
- **User**: Base class with authentication functionality
- **Customer**: Extends User with shopping capabilities and retailer status
- **Product**: Represents items with regular and retailer pricing
- **Order**: Handles order creation and processing
- **Delivery**: Manages delivery status and timeframes
- **DiscountCoupon**: Implements the coupon discount functionality

## Implementation Details
The main system is implemented in `src/dollmarket.py` and includes:
- Class implementations for all entities in the UML diagram
- A CLI menu system for user interaction
- Sample data for demonstration purposes
- Authentication and authorization
- Shopping cart functionality
- Order placement and processing
- Discount and loyalty system

## Testing
The system has comprehensive test coverage using PyTest. Tests are organized by functionality:

### Test Organization
- **test_user.py**: Tests user creation and authentication
- **test_product.py**: Tests product creation and inventory management
- **test_order.py**: Tests order processing and discounts
- **test_delivery.py**: Tests delivery status management
- **test_cart.py**: Tests shopping cart operations
- **test_integration.py**: Tests end-to-end workflows
- **test_edge_cases.py**: Tests handling of boundary conditions

### Test Coverage
1. **User Management**:
   - User and customer creation
   - Regular vs. retailer customer differences
   - Loyalty points calculation

2. **Product Management**:
   - Product creation and attributes
   - Stock updates and inventory checks
   - Different pricing for retailers

3. **Shopping Cart**:
   - Adding items to cart
   - Updating quantities
   - Removing items
   - Viewing cart contents

4. **Order Processing**:
   - Creating orders from cart
   - Order confirmation
   - Applying customer discounts
   - Using discount coupons

5. **Delivery**:
   - Creating deliveries for orders
   - Updating delivery status

6. **Edge Cases**:
   - Empty cart orders
   - Out-of-stock products
   - Multiple discount applications
   - Minimum order requirements for discounts

7. **Integration Tests**:
   - Complete shopping workflow
   - Retailer discount workflow
   - Coupon application workflow

