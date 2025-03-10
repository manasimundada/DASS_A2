import unittest
import sys
import os
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Add the src directory to path for importing modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from order import OrderManager

class TestOrderManager(unittest.TestCase):
    def setUp(self):
        self.order_manager = OrderManager()
        self.test_data = {
            "menu": {"burger": 150.00, "pizza": 300.00, "coke": 50.00},
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
                    "order_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                },
                {
                    "id": 1002,
                    "customer": "test2",
                    "type": "Takeaway",
                    "items": ["pizza"],
                    "total_price": 300.00,
                    "status": "Completed",
                    "delivery_agent": "-"
                }
            ],
            "delivery_agents": ["bob"],
            "next_order_id": 1003
        }

    @patch('order.read_json')
    @patch('order.write_json')
    @patch('builtins.input')
    @patch('random.randint')
    @patch('datetime.datetime')
    @patch('order.DeliveryManager.assign_delivery_agent')
    @patch('order.RestaurantManager.view_menu')
    @patch('rich.console.Console.print')
    def test_place_order_delivery(self, mock_print, mock_view_menu, mock_assign_agent, mock_datetime, 
                                mock_randint, mock_input, mock_write_json, mock_read_json):
        mock_read_json.return_value = self.test_data
        mock_datetime.now.return_value = datetime(2023, 1, 1, 12, 0)
        mock_randint.return_value = 20
        mock_input.side_effect = ["John Doe", "delivery", "burger, coke"]
        
        self.order_manager.place_order()
        
        mock_assign_agent.assert_called_once()
        mock_read_json.assert_called_once()
        mock_write_json.assert_called_once()
        
        # Verify the new order
        updated_data = mock_write_json.call_args[0][0]
        self.assertEqual(updated_data["next_order_id"], 1004)
        new_order = updated_data["orders"][-1]
        self.assertEqual(new_order["id"], 1003)
        self.assertEqual(new_order["customer"], "John Doe")
        self.assertEqual(new_order["type"], "Delivery")
        self.assertEqual(new_order["items"], ["burger", "coke"])
        self.assertEqual(new_order["total_price"], 200.00)
        self.assertEqual(new_order["status"], "Pending")
        self.assertEqual(new_order["expected_delivery_time"], 20)

    @patch('order.read_json')
    @patch('order.write_json')
    @patch('builtins.input')
    @patch('order.RestaurantManager.view_menu')
    @patch('rich.console.Console.print')
    def test_place_order_takeaway(self, mock_print, mock_view_menu, mock_input, mock_write_json, mock_read_json):
        mock_read_json.return_value = self.test_data
        mock_input.side_effect = ["Jane Doe", "takeaway", "pizza"]
        
        self.order_manager.place_order()
        
        mock_read_json.assert_called_once()
        mock_write_json.assert_called_once()
        
        # Verify the new order
        updated_data = mock_write_json.call_args[0][0]
        self.assertEqual(updated_data["next_order_id"], 1004)
        new_order = updated_data["orders"][-1]
        self.assertEqual(new_order["id"], 1003)
        self.assertEqual(new_order["customer"], "Jane Doe")
        self.assertEqual(new_order["type"], "Takeaway")
        self.assertEqual(new_order["items"], ["pizza"])
        self.assertEqual(new_order["total_price"], 300.00)
        self.assertEqual(new_order["status"], "Completed")
        self.assertEqual(new_order["delivery_agent"], "-")

    @patch('order.read_json')
    @patch('builtins.input')
    @patch('order.RestaurantManager.view_menu')
    @patch('rich.console.Console.print')
    def test_place_order_invalid_item(self, mock_print, mock_view_menu, mock_input, mock_read_json):
        mock_read_json.return_value = self.test_data
        mock_input.side_effect = ["John Doe", "delivery", "invalid_item"]
        
        self.order_manager.place_order()
        
        mock_read_json.assert_called_once()
        mock_print.assert_called_with("[bold red]Item 'invalid_item' is not available in the menu.[/bold red]")

    @patch('order.read_json')
    @patch('builtins.input')
    @patch('rich.console.Console.print')
    @patch('order.datetime')
    def test_track_order_delivery_pending(self, mock_datetime, mock_print, mock_input, mock_read_json):
        mock_read_json.return_value = self.test_data
        order_time = datetime.now() - timedelta(minutes=10)  # Order placed 10 minutes ago
        self.test_data["orders"][0]["order_time"] = order_time.strftime("%Y-%m-%d %H:%M:%S")
        mock_datetime.now.return_value = datetime.now()
        mock_datetime.strptime.return_value = order_time
        mock_input.return_value = "1001"  # First order in test data
        
        self.order_manager.track_order()
        
        mock_read_json.assert_called_once()
        # Should print the remaining time (30 - 10 = 20 minutes)
        mock_print.assert_any_call("[bold blue]Estimated time left for delivery: 20 mins[/bold blue]")

    @patch('order.read_json')
    @patch('builtins.input')
    @patch('rich.console.Console.print')
    def test_track_order_takeaway(self, mock_print, mock_input, mock_read_json):
        mock_read_json.return_value = self.test_data
        mock_input.return_value = "1002"  # Second order in test data (takeaway)
        
        self.order_manager.track_order()
        
        mock_read_json.assert_called_once()
        # Should not print estimated time for takeaway
        for call in mock_print.call_args_list:
            self.assertNotIn("Estimated time left for delivery", str(call))

    @patch('order.read_json')
    @patch('builtins.input')
    @patch('rich.console.Console.print')
    def test_track_order_not_found(self, mock_print, mock_input, mock_read_json):
        mock_read_json.return_value = self.test_data
        mock_input.return_value = "9999"  # Non-existent order
        
        self.order_manager.track_order()
        
        mock_read_json.assert_called_once()
        mock_print.assert_called_with("[bold red]Order not found![/bold red]")

    @patch('order.read_json')
    @patch('builtins.input')
    @patch('rich.console.Console.print')
    def test_track_order_invalid_id(self, mock_print, mock_input, mock_read_json):
        mock_read_json.return_value = self.test_data
        mock_input.return_value = "abc"  # Invalid order ID format
        
        self.order_manager.track_order()
        
        mock_read_json.assert_called_once()
        mock_print.assert_called_with("[bold red]Invalid Order ID. Please enter a number.[/bold red]")

if __name__ == '__main__':
    unittest.main()
