import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add the src directory to path for importing modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from delivery import DeliveryManager

class TestDeliveryManager(unittest.TestCase):
    def setUp(self):
        self.delivery_manager = DeliveryManager()
        self.test_data = {
            "menu": {"burger": 150.00},
            "orders": [
                {
                    "id": 1001,
                    "customer": "test",
                    "type": "Delivery",
                    "items": ["burger"],
                    "total_price": 150.00,
                    "status": "Pending",
                    "delivery_agent": "bob",
                    "expected_delivery_time": 30,
                    "order_time": "2023-01-01 12:00:00"
                },
                {
                    "id": 1002,
                    "customer": "test2",
                    "type": "Takeaway",
                    "items": ["burger"],
                    "total_price": 150.00,
                    "status": "Completed",
                    "delivery_agent": "-"
                },
                {
                    "id": 1003,
                    "customer": "test3",
                    "type": "Delivery",
                    "items": ["burger"],
                    "total_price": 150.00,
                    "status": "Picked Up",
                    "delivery_agent": "alice",
                    "expected_delivery_time": 30,
                    "order_time": "2023-01-01 12:00:00"
                },
                {
                    "id": 1004,
                    "customer": "test4",
                    "type": "Delivery",
                    "items": ["burger"],
                    "total_price": 150.00,
                    "status": "Delivered",
                    "delivery_agent": "bob",
                    "expected_delivery_time": 30,
                    "order_time": "2023-01-01 12:00:00"
                }
            ],
            "delivery_agents": ["bob", "alice"],
            "next_order_id": 1005
        }

    @patch('delivery.read_json')
    @patch('delivery.write_json')
    @patch('builtins.input')
    @patch('rich.console.Console.print')
    def test_signup_login_existing_agent(self, mock_print, mock_input, mock_write_json, mock_read_json):
        mock_read_json.return_value = self.test_data
        mock_input.return_value = "bob"
        agent_name = self.delivery_manager.signup_login()
        mock_read_json.assert_called_once()
        # Should not call write_json because agent already exists
        mock_write_json.assert_not_called()
        self.assertEqual(agent_name, "bob")
        self.assertIn("bob", self.delivery_manager.logged_in_agents)

    @patch('delivery.read_json')
    @patch('delivery.write_json')
    @patch('builtins.input')
    @patch('rich.console.Console.print')
    def test_signup_login_new_agent(self, mock_print, mock_input, mock_write_json, mock_read_json):
        mock_read_json.return_value = self.test_data
        mock_input.return_value = "charlie"
        agent_name = self.delivery_manager.signup_login()
        mock_read_json.assert_called_once()
        # Should call write_json because it's a new agent
        mock_write_json.assert_called_once()
        # Verify the agent was added to delivery_agents
        updated_data = mock_write_json.call_args[0][0]
        self.assertIn("charlie", updated_data["delivery_agents"])
        self.assertEqual(agent_name, "charlie")
        self.assertIn("charlie", self.delivery_manager.logged_in_agents)

    @patch('delivery.read_json')
    @patch('delivery.write_json')
    @patch('builtins.input')
    @patch('rich.console.Console.print')
    def test_update_order_status_valid(self, mock_print, mock_input, mock_write_json, mock_read_json):
        mock_read_json.return_value = self.test_data
        mock_input.side_effect = ["1001", "picked up"]
        self.delivery_manager.update_order_status("bob")
        mock_read_json.assert_called_once()
        # Should update the order status
        updated_data = mock_write_json.call_args[0][0]
        found_order = next(order for order in updated_data["orders"] if order["id"] == 1001)
        # Match the case used in the application (first letter of each word capitalized)
        self.assertEqual(found_order["status"], "Picked Up")

    @patch('delivery.read_json')
    @patch('builtins.input')
    @patch('rich.console.Console.print')
    def test_update_order_status_no_orders(self, mock_print, mock_input, mock_read_json):
        empty_data = self.test_data.copy()
        empty_data["orders"] = []
        mock_read_json.return_value = empty_data
        self.delivery_manager.update_order_status("bob")
        mock_print.assert_called_with("[bold red]No orders available for delivery.[/bold red]")

    @patch('delivery.read_json')
    @patch('builtins.input')
    @patch('rich.console.Console.print')
    def test_update_order_status_invalid_id(self, mock_print, mock_input, mock_read_json):
        mock_read_json.return_value = self.test_data
        mock_input.return_value = "abc"
        self.delivery_manager.update_order_status("bob")
        mock_print.assert_called_with("[bold red]Invalid Order ID. Please enter a number.[/bold red]")

    @patch('delivery.read_json')
    @patch('builtins.input')
    @patch('rich.console.Console.print')
    def test_update_order_status_not_found(self, mock_print, mock_input, mock_read_json):
        mock_read_json.return_value = self.test_data
        mock_input.return_value = "9999"  # Non-existent order ID
        self.delivery_manager.update_order_status("bob")
        mock_print.assert_called_with("[bold red]Order not found![/bold red]")

    @patch('delivery.read_json')
    @patch('builtins.input')
    @patch('rich.console.Console.print')
    def test_update_order_status_wrong_agent(self, mock_print, mock_input, mock_read_json):
        mock_read_json.return_value = self.test_data
        mock_input.return_value = "1001"  # Order assigned to bob
        self.delivery_manager.update_order_status("alice")
        mock_print.assert_called_with("[bold red]This order is assigned to Bob.[/bold red]")

    @patch('delivery.read_json')
    @patch('builtins.input')
    @patch('rich.console.Console.print')
    def test_update_order_status_takeaway(self, mock_print, mock_input, mock_read_json):
        mock_read_json.return_value = self.test_data
        mock_input.return_value = "1002"  # Takeaway order
        self.delivery_manager.update_order_status("bob")
        mock_print.assert_called_with("[bold yellow]This is a takeaway order and is already completed.[/bold yellow]")

    @patch('delivery.read_json')
    @patch('builtins.input')
    @patch('rich.console.Console.print')
    def test_update_order_status_already_delivered(self, mock_print, mock_input, mock_read_json):
        mock_read_json.return_value = self.test_data
        mock_input.return_value = "1004"  # Already delivered order
        self.delivery_manager.update_order_status("bob")
        mock_print.assert_called_with("[bold yellow]Order 1004 has already been delivered and cannot be updated.[/bold yellow]")

    def test_assign_delivery_agent_logged_in(self):
        # Simulate logged in agent
        test_order = {"delivery_agent": "Not Assigned"}
        self.delivery_manager.logged_in_agents.add("bob")
        self.delivery_manager.assign_delivery_agent(test_order)
        self.assertEqual(test_order["delivery_agent"], "bob")

    def test_assign_delivery_agent_default(self):
        # No logged in agents
        test_order = {"delivery_agent": "Not Assigned"}
        self.delivery_manager.assign_delivery_agent(test_order)
        self.assertEqual(test_order["delivery_agent"], "bob")  # Default to "bob"

if __name__ == '__main__':
    unittest.main()
