"""
Tests for TextIndexer.
"""
import unittest

from text_indexer import TextIndexer

class TestTextIndexer(unittest.TestCase):
    """
    Unit tests for TextIndexer.
    """
    def test_example_1(self):
        """
        Tests suggestion on one word and fail if more than one specified.
        """
        text_indexer = TextIndexer(1)

        text_indexer.add_text(1, 'Python is great! Python is funny! Python is great!')
        text_indexer.add_text(2, 'Python is slow!')

        self.assertRaises(ValueError, text_indexer.suggest, 'python', 'is')

        self.assertEqual(["is"], text_indexer.suggest('python'))

    def test_example_2(self):
        """
        Test with more than one text.
        """
        text_indexer = TextIndexer(2)

        text_indexer.add_text(1, 'Python is slow!')
        text_indexer.add_text(2, 'Python is great! Python is funny! Python is great!')

        self.assertEqual(["great"], text_indexer.suggest('python', 'is'))

    def test_example_3(self):
        """
        Test with multiple matches.
        """
        text_indexer = TextIndexer(1)
        text_indexer.add_text(1, "start one. start two.")

        self.assertEqual(["one", "two"], text_indexer.suggest('start'))

if __name__ == '__main__':
    unittest.main()
