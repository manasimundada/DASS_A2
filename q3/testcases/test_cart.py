import pytest
import sys
import os
from unittest.mock import patch

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.dollmarket import Customer, Product

@pytest.fixture
def customer():
    """Fixture to create a customer for cart tests"""
    return Customer("Test Customer", "customer@example.com", "password123", "123 Test St", False)

@pytest.fixture
def products():
    """Fixture to create sample products for cart tests"""
    return [
        Product("Laptop", "Electronics", 1000, 900, 5),
        Product("Headphones", "Electronics", 100, 90, 20),
        Product("Book", "Books", 15, 12, 50)
    ]

class TestCart:
    """Tests for cart functionality in Customer class"""
    
    def test_add_to_cart(self, customer, products):
        """Test adding an item to cart"""
        laptop = products[0]
        
        # Add item to cart
        with patch('builtins.print'):  # Suppress print output
            customer.add_to_cart(laptop, 2)
        
        # Verify cart contents
        assert len(customer.cart) == 1
        assert customer.cart[0]['product'] == laptop
        assert customer.cart[0]['quantity'] == 2
        assert customer.cart[0]['price'] == 1000  # Regular customer price
        
    def test_add_existing_product_to_cart(self, customer, products):
        """Test adding more of an existing product to cart"""
        laptop = products[0]
        
        # Add laptop to cart
        with patch('builtins.print'):
            customer.add_to_cart(laptop, 1)
            
            # Add more of the same product
            customer.add_to_cart(laptop, 2)
        
        # Verify cart was updated correctly
        assert len(customer.cart) == 1  # Still just one unique product
        assert customer.cart[0]['quantity'] == 3  # 1 + 2 = 3
        
    def test_add_multiple_products_to_cart(self, customer, products):
        """Test adding multiple different products to cart"""
        laptop = products[0]
        headphones = products[1]
        
        # Add different products
        with patch('builtins.print'):
            customer.add_to_cart(laptop, 1)
            customer.add_to_cart(headphones, 2)
        
        # Verify cart contents
        assert len(customer.cart) == 2
        
        # First item is laptop
        assert customer.cart[0]['product'] == laptop
        assert customer.cart[0]['quantity'] == 1
        
        # Second item is headphones
        assert customer.cart[1]['product'] == headphones
        assert customer.cart[1]['quantity'] == 2
        
    def test_remove_from_cart(self, customer, products):
        """Test removing an item from cart"""
        laptop = products[0]
        headphones = products[1]
        
        # Add items to cart
        with patch('builtins.print'):
            customer.add_to_cart(laptop, 1)
            customer.add_to_cart(headphones, 2)
            
            # Remove first item
            customer.remove_from_cart(0)
        
        # Verify laptop was removed
        assert len(customer.cart) == 1
        assert customer.cart[0]['product'] == headphones
        
    def test_remove_invalid_index(self, customer, products):
        """Test removing an item with invalid index"""
        laptop = products[0]
        
        # Add item to cart
        with patch('builtins.print'):
            customer.add_to_cart(laptop, 1)
            
            # Try removing with invalid index
            customer.remove_from_cart(5)  # Invalid index
        
        # Verify cart is unchanged
        assert len(customer.cart) == 1
        assert customer.cart[0]['product'] == laptop
        
    def test_clear_cart(self, customer, products):
        """Test clearing the entire cart"""
        # Add multiple items
        with patch('builtins.print'):
            customer.add_to_cart(products[0], 1)
            customer.add_to_cart(products[1], 2)
            
            # Clear cart
            customer.clear_cart()
        
        # Verify cart is empty
        assert len(customer.cart) == 0
        
    def test_view_cart_empty(self, customer):
        """Test viewing an empty cart"""
        with patch('builtins.print') as mock_print:
            customer.view_cart()
            
            # Verify empty cart message was printed
            mock_print.assert_any_call("\nYour cart is empty.\n")
            
    def test_view_cart_with_items(self, customer, products):
        """Test viewing cart with items"""
        with patch('builtins.print'):
            # Add items to cart
            customer.add_to_cart(products[0], 1)  # Laptop
            customer.add_to_cart(products[1], 2)  # Headphones
            
        with patch('builtins.print') as mock_print:
            # View cart
            customer.view_cart()
            
            # Check that some output was generated (we can't easily check the exact tabulate output)
            assert mock_print.call_count > 1
