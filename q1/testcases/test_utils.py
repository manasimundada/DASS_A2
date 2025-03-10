import unittest
import sys
import os
import json
from unittest.mock import patch, mock_open

# Add the src directory to path for importing modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from utils import read_json, write_json, DEFAULT_DATA

class TestUtils(unittest.TestCase):
    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({"test": "data"}))
    def test_read_json_existing_file(self, mock_file, mock_exists):
        mock_exists.return_value = True
        data = read_json()
        mock_exists.assert_called_once()
        mock_file.assert_called_once()
        self.assertEqual(data, {"test": "data"})

    @patch('os.path.exists')
    @patch('utils.write_json')
    def test_read_json_non_existing_file(self, mock_write, mock_exists):
        mock_exists.return_value = False
        data = read_json()
        mock_exists.assert_called_once()
        mock_write.assert_called_once_with(DEFAULT_DATA)
        self.assertEqual(data, DEFAULT_DATA)

    @patch('builtins.open', new_callable=mock_open)
    def test_write_json(self, mock_file):
        test_data = {"test": "data"}
        write_json(test_data)
        mock_file.assert_called_once()
        # Instead of asserting the write was called once, check that it was called at least once
        # and that the written data contains our expected content
        self.assertTrue(mock_file().write.called)
        written_data = ''.join(call[0][0] for call in mock_file().write.call_args_list)
        self.assertIn('"test": "data"', written_data)

    @patch('builtins.open')
    def test_write_json_exception(self, mock_file):
        mock_file.side_effect = Exception("Test exception")
        with patch('builtins.print') as mock_print:
            write_json({"test": "data"})
            mock_print.assert_called_once()
            self.assertIn("Error writing JSON", mock_print.call_args[0][0])

    @patch('os.path.exists')
    @patch('builtins.open')
    def test_read_json_exception(self, mock_file, mock_exists):
        mock_exists.return_value = True
        mock_file.side_effect = Exception("Test exception")
        with patch('builtins.print') as mock_print:
            data = read_json()
            mock_print.assert_called_once()
            self.assertIn("Error reading JSON", mock_print.call_args[0][0])
            self.assertEqual(data, DEFAULT_DATA)

if __name__ == '__main__':
    unittest.main()
