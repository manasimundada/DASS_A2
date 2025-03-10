#!/bin/bash

# Navigate to the project directory
cd "$(dirname "$0")"

# Run all tests with verbose output
python -m pytest -v testcases/
