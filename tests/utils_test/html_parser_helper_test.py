import unittest

class TestOne(unittest.TestCase):
    def test_add(self):
        self.assertEqual(13, 13)
        self.assertEqual(6, 6)

if __name__ == '__main__':
    unittest.main()