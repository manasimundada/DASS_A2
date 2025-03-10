import pytest
import sys
import os
from unittest.mock import patch

# Add parent directory to path to import dollmarket module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.dollmarket import User, Customer

class TestUser:
    """Tests for User class functionality"""
    
    def test_user_creation(self):
        """Test that a User object is created with correct attributes"""
        user = User("Test User", "test@example.com", "password123")
        
        assert user.name == "Test User"
        assert user.email == "test@example.com"
        assert user.password == "password123"
        assert hasattr(user, "user_id")
        assert isinstance(user.user_id, str)
        
    def test_customer_creation_regular(self):
        """Test that a regular Customer is created with correct attributes"""
        customer = Customer("Test Customer", "customer@example.com", "password123", "123 Test St", False)
        
        assert customer.name == "Test Customer"
        assert customer.email == "customer@example.com"
        assert customer.address == "123 Test St"
        assert customer.is_retailer is False
        assert customer.discount == 0.05  # Regular customer discount
        assert customer.orders == []
        assert customer.coupons == []
        assert customer.loyalty_points == 0
        assert customer.cart == []
        
    def test_customer_creation_retailer(self):
        """Test that a retailer Customer is created with correct attributes"""
        retailer = Customer("Test Retailer", "retailer@example.com", "password123", "456 Business St", True)
        
        assert retailer.name == "Test Retailer"
        assert retailer.is_retailer is True
        assert retailer.discount == 0.1  # Retailer discount
        
    def test_earn_loyalty_points(self):
        """Test that loyalty points are earned correctly based on spent amount"""
        customer = Customer("Test Customer", "customer@example.com", "password123", "123 Test St", False)
        
        # Initial points should be 0
        assert customer.loyalty_points == 0
        
        # Test earning points with $100 spent (should get 10 points)
        with patch('builtins.print'):  # Suppress print output for testing
            customer.earn_loyalty_points(100)
            assert customer.loyalty_points == 10
            
            # Test earning more points
            customer.earn_loyalty_points(250)  # Should earn 25 more points
            assert customer.loyalty_points == 35
            
            # Test with amount less than $10 (shouldn't earn points)
            customer.earn_loyalty_points(5)
            assert customer.loyalty_points == 35  # Points remain unchanged
    
    def test_generate_discount_coupon(self):
        """Test generating a discount coupon with sufficient loyalty points"""
        customer = Customer("Test Customer", "customer@example.com", "password123", "123 Test St", False)
        
        # Give customer enough points to generate a coupon
        customer.loyalty_points = 50
        
        # Generate coupon
        with patch('builtins.print'):  # Suppress print output
            customer.generate_discount_coupon()
        
        # Verify coupon was created and points were deducted
        assert len(customer.coupons) == 1
        assert customer.loyalty_points == 0
        
        # Verify coupon properties
        coupon = customer.coupons[0]
        assert coupon.customer == customer
        assert coupon.discount_percentage == 5
        assert coupon.min_order_amount == 100
