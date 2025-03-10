import json
import os

DEFAULT_DATA = {
    "menu": {
        "burger": 150.00,
        "pizza": 300.00,
        "pasta": 250.00,
        "salad": 120.00,
        "coke": 50.00,
        "water": 20.00,
        "fries": 100.00,
        "chicken wings": 200.00,
        "ice cream": 80.00,
        "coffee": 60.00
    },
    "orders": [],
    "delivery_agents": ["bob"],
    "next_order_id": 1001
}

JSON_FILE = "data.json"

def read_json():
    """Read data from JSON file, create with default data if doesn't exist"""
    try:
        if not os.path.exists(JSON_FILE):
            write_json(DEFAULT_DATA)
            return DEFAULT_DATA
        with open(JSON_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error reading JSON: {e}")
        return DEFAULT_DATA

def write_json(data):
    """Write data to JSON file"""
    try:
        with open(JSON_FILE, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error writing JSON: {e}")
