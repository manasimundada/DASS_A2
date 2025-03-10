import pytest
import sys
import os

# Add parent directory to path to import dollmarket module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Define test markers for easier test selection
def pytest_configure(config):
    """Set up pytest configuration"""
    config.addinivalue_line("markers", "user: tests for user functionality")
    config.addinivalue_line("markers", "product: tests for product functionality")
    config.addinivalue_line("markers", "cart: tests for cart operations")
    config.addinivalue_line("markers", "order: tests for order processing")
    config.addinivalue_line("markers", "delivery: tests for delivery functionality")
    config.addinivalue_line("markers", "discount: tests for discount and coupon functionality")
    config.addinivalue_line("markers", "integration: tests for end-to-end workflows")
    config.addinivalue_line("markers", "edge: tests for edge cases")
