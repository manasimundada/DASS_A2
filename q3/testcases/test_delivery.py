import pytest
import sys
import os
from unittest.mock import patch, MagicMock

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.dollmarket import Delivery

class TestDelivery:
    """Tests for Delivery class functionality"""
    
    def test_delivery_creation(self):
        """Test creating a delivery with correct attributes"""
        # Create mock order
        mock_order = MagicMock()
        
        # Create delivery
        delivery = Delivery(mock_order)
        
        # Verify delivery attributes
        assert delivery.order == mock_order
        assert delivery.status == "Processing"
        assert 2 <= delivery.estimated_days <= 7
        assert hasattr(delivery, "delivery_id")
        
    def test_update_status(self):
        """Test updating delivery status"""
        # Create mock order
        mock_order = MagicMock()
        
        # Create delivery
        delivery = Delivery(mock_order)
        
        # Update status
        with patch('builtins.print'):
            delivery.update_status("Shipped")
        
        # Verify status was updated
        assert delivery.status == "Shipped"
        
        # Update again
        with patch('builtins.print'):
            delivery.update_status("Delivered")
        
        # Verify status was updated again
        assert delivery.status == "Delivered"
