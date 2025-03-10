import pytest
import sys
import os
from unittest.mock import patch

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.dollmarket import Product

class TestProduct:
    """Tests for Product class functionality"""
    
    def test_product_creation(self):
        """Test that a Product is created with correct attributes"""
        product = Product("Laptop", "Electronics", 1000, 900, 5)
        
        assert product.name == "Laptop"
        assert product.category == "Electronics"
        assert product.price == 1000
        assert product.retailer_price == 900
        assert product.stock == 5
        assert hasattr(product, "product_id")
        
    def test_get_price(self):
        """Test that get_price returns correct price based on retailer status"""
        product = Product("Laptop", "Electronics", 1000, 900, 5)
        
        # Test regular customer price
        assert product.get_price(is_retailer=False) == 1000
        
        # Test retailer price
        assert product.get_price(is_retailer=True) == 900
        
    def test_update_stock_sufficient(self):
        """Test updating stock with sufficient inventory"""
        product = Product("Laptop", "Electronics", 1000, 900, 5)
        
        # Update with valid quantity
        with patch('builtins.print'):  # Suppress print output
            result = product.update_stock(3)
            
            assert result is True
            assert product.stock == 2  # 5 - 3 = 2
            
    def test_update_stock_insufficient(self):
        """Test updating stock with insufficient inventory"""
        product = Product("Laptop", "Electronics", 1000, 900, 5)
        
        # Try to update with quantity exceeding stock
        with patch('builtins.print'):  # Suppress print output
            result = product.update_stock(10)
            
            assert result is False
            assert product.stock == 5  # Stock remains unchanged
            
    def test_update_stock_exact(self):
        """Test updating stock with exact amount of inventory"""
        product = Product("Laptop", "Electronics", 1000, 900, 5)
        
        # Update with quantity equal to stock
        with patch('builtins.print'):  # Suppress print output
            result = product.update_stock(5)
            
            assert result is True
            assert product.stock == 0
