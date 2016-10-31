
import unittest
from lazy import LazyOperation, lazy_add, lazy_mul, lazy

# testing the LazyOperation class
class TestLazyOperation(unittest.TestCase):
    ## test eval
    def test_LazyOperation_invalid_func(self):
        with self.assertRaises(TypeError):
            LazyOperation(5).eval()
    def test_LazyOperation_empty_func(self):
        with self.assertRaises(TypeError):
            LazyOperation().eval()
    def test_LazyOperation_constructor(self):
        self.assertIsInstance(lazy_add(1,2), LazyOperation)
    def test_eval(self):
        self.assertEqual(lazy_add(lazy_mul(10,20), 5).eval(), 205)
    

if __name__ == '__main__':
    unittest.main()