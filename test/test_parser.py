"""Tests for manual input parsing."""

import unittest

from src.emulator import parse_line


class TestParser(unittest.TestCase):
    """Test cases for manual command line string parsing."""

    def test_simple_command(self):
        """chec spaces only"""
        self.assertEqual(parse_line("ls -l /tmp"), ["ls", "-l", "/tmp"])

    def test_double_quotes_preservation(self):
        self.assertEqual(parse_line('cd "my folder name"'), ["cd", "my folder name"])

    def test_single_quotes(self):
        self.assertEqual(parse_line("cd 'another folder'"), ["cd", "another folder"])

    def test_multiple_spaces(self):
        self.assertEqual(parse_line("ls    -a    /home"), ["ls", "-a", "/home"])

    def test_unclosed_double_quote(self):
        with self.assertRaises(ValueError) as context:
            parse_line('cd "unclosed folder')

        self.assertEqual(str(context.exception), "No closing quotation")

    def test_unclosed_single_quote(self):
        with self.assertRaises(ValueError) as context:
            parse_line("cd 'unclosed folder")

        self.assertEqual(str(context.exception), "No closing quotation")


if __name__ == "__main__":
    unittest.main()
