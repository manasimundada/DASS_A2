import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add the src directory to path for importing modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from restaurant import RestaurantManager

class TestRestaurantManager(unittest.TestCase):
    def setUp(self):
        self.restaurant_manager = RestaurantManager()
        self.test_data = {
            "menu": {
                "burger": 150.00,
                "pizza": 300.00
            },
            "orders": [
                {
                    "id": 1001,
                    "customer": "test",
                    "type": "Delivery",
                    "items": ["burger"],
                    "total_price": 150.00,
                    "status": "Pending",
                    "delivery_agent": "bob"
                }
            ],
            "delivery_agents": ["bob"],
            "next_order_id": 1002
        }

    @patch('restaurant.read_json')
    @patch('rich.console.Console.print')
    def test_view_menu(self, mock_print, mock_read_json):
        mock_read_json.return_value = self.test_data
        self.restaurant_manager.view_menu()
        mock_read_json.assert_called_once()
        # Verify that console.print was called
        self.assertTrue(mock_print.called)

    @patch('restaurant.read_json')
    @patch('restaurant.write_json')
    @patch('builtins.input')
    @patch('rich.console.Console.print')
    def test_edit_menu_add_item(self, mock_print, mock_input, mock_write_json, mock_read_json):
        mock_read_json.return_value = self.test_data
        mock_input.side_effect = ["1", "salad", "120", "4"]
        self.restaurant_manager.edit_menu()
        mock_read_json.assert_called()
        updated_data = mock_write_json.call_args[0][0]
        self.assertIn("salad", updated_data["menu"])
        self.assertEqual(updated_data["menu"]["salad"], 120.0)

    @patch('restaurant.read_json')
    @patch('restaurant.write_json')
    @patch('builtins.input')
    @patch('rich.console.Console.print')
    def test_edit_menu_add_existing_item(self, mock_print, mock_input, mock_write_json, mock_read_json):
        mock_read_json.return_value = self.test_data
        mock_input.side_effect = ["1", "burger", "160", "4"]
        self.restaurant_manager.edit_menu()
        # Should show an error because burger already exists
        self.assertTrue(mock_print.called)
        # write_json should not be called because no changes were made
        mock_write_json.assert_not_called()

    @patch('restaurant.read_json')
    @patch('restaurant.write_json')
    @patch('builtins.input')
    @patch('rich.console.Console.print')
    def test_edit_menu_remove_item(self, mock_print, mock_input, mock_write_json, mock_read_json):
        mock_read_json.return_value = self.test_data
        mock_input.side_effect = ["2", "burger", "4"]
        self.restaurant_manager.edit_menu()
        updated_data = mock_write_json.call_args[0][0]
        self.assertNotIn("burger", updated_data["menu"])

    @patch('restaurant.read_json')
    @patch('restaurant.write_json')
    @patch('builtins.input')
    @patch('rich.console.Console.print')
    def test_edit_menu_remove_nonexistent_item(self, mock_print, mock_input, mock_write_json, mock_read_json):
        mock_read_json.return_value = self.test_data
        mock_input.side_effect = ["2", "nonexistent", "4"]
        self.restaurant_manager.edit_menu()
        # Should show an error because the item doesn't exist
        self.assertTrue(mock_print.called)
        # write_json should not be called because no changes were made
        mock_write_json.assert_not_called()

    @patch('restaurant.read_json')
    @patch('rich.console.Console.print')
    def test_view_orders(self, mock_print, mock_read_json):
        mock_read_json.return_value = self.test_data
        self.restaurant_manager.view_orders()
        mock_read_json.assert_called_once()
        self.assertTrue(mock_print.called)

    @patch('restaurant.read_json')
    @patch('rich.console.Console.print')
    def test_view_orders_empty(self, mock_print, mock_read_json):
        empty_data = self.test_data.copy()
        empty_data["orders"] = []
        mock_read_json.return_value = empty_data
        self.restaurant_manager.view_orders()
        mock_read_json.assert_called_once()
        # Should print a message about no orders
        mock_print.assert_called_with("[bold red]No orders available.[/bold red]")

if __name__ == '__main__':
    unittest.main()
