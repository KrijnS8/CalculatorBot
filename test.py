import unittest
import calculate


class TestStringMethods(unittest.TestCase):

    def test_single_numbers(self):
        for i in range(0, 1000):
            self.assertEqual(calculate.calculate(str(i)), i)

    def test_isupper(self):
        self.assertEqual(calculate.calculate('((3+(6x2)+5)x3)'), 60)
        self.assertEqual(calculate.calculate('42'), 42)
        self.assertEqual(calculate.calculate('42+0'), 42)
        self.assertEqual(calculate.calculate('0+42'), 42)
        self.assertEqual(calculate.calculate('0'), 0)
        self.assertRaises(Exception, calculate.calculate, '42/0')
        self.assertEqual(calculate.calculate('42+0'), 42)
        self.assertEqual(calculate.calculate('(3+(6x2)+5)x3'), 60)


if __name__ == '__main__':
    unittest.main()
