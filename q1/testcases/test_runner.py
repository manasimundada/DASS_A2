import unittest
import sys
import os

# Add the src directory to path for importing modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Import all test modules
from test_utils import TestUtils
from test_restaurant import TestRestaurantManager
from test_delivery import TestDeliveryManager
from test_order import TestOrderManager

def run_tests():
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add tests from each test class
    test_suite.addTest(unittest.makeSuite(TestUtils))
    test_suite.addTest(unittest.makeSuite(TestRestaurantManager))
    test_suite.addTest(unittest.makeSuite(TestDeliveryManager))
    test_suite.addTest(unittest.makeSuite(TestOrderManager))
    
    # Run the test suite
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Return exit code based on test success/failure
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    sys.exit(run_tests())
