import json
import os
from pathlib import Path

# Define path to the data file
DATA_FILE = Path(__file__).parent / 'food_delivery_data.json'

# Initial data structure
INITIAL_DATA = {
    "orders": [],
    "next_order_id": 1001
}

def initialize_data():
    """Create the data file if it doesn't exist"""
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump(INITIAL_DATA, f, indent=4)

def read_data():
    """Read data from the JSON file"""
    initialize_data()
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        # If file is corrupted, reinitialize it
        with open(DATA_FILE, 'w') as f:
            json.dump(INITIAL_DATA, f, indent=4)
        return INITIAL_DATA

def write_data(data):
    """Write data to the JSON file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)
