"""Tests for UI components."""

import unittest
from io import StringIO
from unittest.mock import patch

from src.emulator import print_config_box


class TestUI(unittest.TestCase):
    """Test cases for user interface functions."""

    def test_print_config_box_with_args(self):
        expected = (
            "┌────────────────────────┐\n"
            "│ Emulator configuration │\n"
            "├────────────────────────┤\n"
            "│ VFS path: test.zip     │\n"
            "│ Script path: start.txt │\n"
            "└────────────────────────┘\n"
        )

        with patch("sys.stdout", new_callable=StringIO) as fake_out:
            print_config_box("test.zip", "start.txt")
            self.assertEqual(fake_out.getvalue(), expected)

    def test_print_config_box_none(self):
        expected = (
            "┌────────────────────────┐\n"
            "│ Emulator configuration │\n"
            "├────────────────────────┤\n"
            "│ VFS path: None         │\n"
            "│ Script path: None      │\n"
            "└────────────────────────┘\n"
        )

        with patch("sys.stdout", new_callable=StringIO) as fake_out:
            print_config_box(None, None)
            self.assertEqual(fake_out.getvalue(), expected)

    def test_print_config_box_dynamic_width(self):
        long_path = "very_long_directory_name/archive.zip"
        # Длина строки "VFS path: very_long_directory_name/archive.zip" = 46 символов
        expected = (
            "┌────────────────────────────────────────────────┐\n"
            "│             Emulator configuration             │\n"
            "├────────────────────────────────────────────────┤\n"
            "│ VFS path: very_long_directory_name/archive.zip │\n"
            "│ Script path: None                              │\n"
            "└────────────────────────────────────────────────┘\n"
        )

        with patch("sys.stdout", new_callable=StringIO) as fake_out:
            print_config_box(long_path, None)
            self.assertEqual(fake_out.getvalue(), expected)


if __name__ == "__main__":
    unittest.main()
