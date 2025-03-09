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

<!-- ## **5. Non-Functional Requirements**
- **Scalability:** System should support a large number of orders and users.
- **Performance:** Orders and updates should reflect in real-time.
- **Security:** Secure transactions with encrypted payments.
- **Availability:** 99.9% uptime with cloud-based infrastructure.
- **Data Persistence:** Maintain order status even after app restarts. -->
