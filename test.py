import unittest
import expression


class TestStringMethods(unittest.TestCase):

    def test_single_numbers(self):
        for i in range(0, 1000):
            self.assertEqual(expression.parse(str(i)).evaluate(), i)

    def test_isupper(self):
        self.assertEqual(expression.parse('4+2').evaluate(), 6)
        self.assertRaises(Exception, expression.parse, '42/0')


if __name__ == '__main__':
    unittest.main()
