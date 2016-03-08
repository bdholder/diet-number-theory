'''You should go on a coffee break when running these tests because they could take a few minutes.'''

from dietnt import *
import unittest


class TestFactorInteger(unittest.TestCase):
    def test_factor_integer(self):
        test_cases = ((517858891518965537, {517858891518965537: 1}),
                      (794381603082488147, {271976087: 1, 2920777381: 1}))
        for i, ex in test_cases:
            with self.subTest(i=i, ex=ex):
                self.assertEqual(factor_integer(i), ex)



class TestIsPrime(unittest.TestCase):
    def test_is_prime(self):
        test_cases = ((271976087, True),
                      (2920777381, True),
                      (517858891518965537, True),
                      (794381603082488147, False))
        for i, ex in test_cases:
            with self.subTest(i=i, ex=ex):
                self.assertEqual(is_prime(i), ex)



if __name__ == '__main__':
    unittest.main()
