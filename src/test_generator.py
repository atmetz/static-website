import unittest

from generator import extract_title

class TestHTMLGenerator(unittest.TestCase):

    def test_extract_title(self):

        self.assertEqual(
            extract_title("# Hello "),
            'Hello',
        )

    def test_extract_title_multiline(self):

        self.assertEqual(
            extract_title("Text before\n# Hello\nMore"),
            'Hello',
        )

    def test_extract_not_title(self):

        with self.assertRaises(Exception):
            extract_title("## Not a title")

    def test_extract_title_again(self):

        self.assertEqual(
            extract_title("# Spaced"),
            'Spaced',
        )

    def test_extract_title_blank(self):

        with self.assertRaises(Exception):
            extract_title("")