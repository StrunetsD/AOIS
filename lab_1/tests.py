import unittest
from run import *


class TestMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.method = Methods()

    def test_get_positive_binary(self):
        self.assertEqual(self.method.get_positive_binary(11), "00000000000000000000000000001011")
        self.assertEqual(self.method.get_positive_binary(25), "00000000000000000000000000011001")

    def test_get_negative_binary(self):
        self.assertEqual(self.method.get_negative_binary(-11), "10000000000000000000000000001011")
        self.assertEqual(self.method.get_negative_binary(-25), "10000000000000000000000000011001")

    def test_convert_to_decimal(self):
        self.assertEqual(self.method.convert_to_decimal("00001011"), 11)
        self.assertEqual(self.method.convert_to_decimal("11110101"), -11)

    def test_convert_to_binary(self):
        self.assertEqual(self.method.convert_to_binary(11), "00000000000000000000000000001011")
        self.assertEqual(self.method.convert_to_binary(-11), "10000000000000000000000000001011")

    def test_direct_sum_of_binary_numbers(self):
        self.assertEqual(self.method.direct_sum_of_binary_numbers(11, 25), "00000000000000000000000000100100")
        self.assertEqual(self.method.direct_sum_of_binary_numbers(11, -25), "10000000000000000000000000100100")

    def test_convert_to_reverse_binary(self):
        self.assertEqual(self.method.convert_to_reverse_binary(11), "00000000000000000000000000001011")
        self.assertEqual(self.method.convert_to_reverse_binary(-11), "11111111111111111111111111110100")

    def test_convert_to_additional_binary(self):
        self.assertEqual(self.method.convert_to_additional_binary(11), "00000000000000000000000000001011")
        self.assertEqual(self.method.convert_to_additional_binary(-11), "11111111111111111111111111110101")

    def test_sum_of_additional_binary(self):
        self.assertEqual(self.method.sum_of_additional_binary(11, 25), "00000000000000000000000000100100")
        self.assertEqual(self.method.sum_of_additional_binary(11, -25), "11111111111111111111111111110010")

    def test_multi_of_binary_numbers(self):
        self.assertEqual(self.method.multi_of_binary_numbers(11, 25), 275)
        self.assertEqual(self.method.multi_of_binary_numbers(-11, 25), -275)

    def test_float_to_binary_fraction(self):
        self.assertEqual(self.method.float_to_binary_fraction(0.5), "1")
        self.assertEqual(self.method.float_to_binary_fraction(0.25), "01")

    def test_float_to_binary(self):
        self.assertEqual(self.method.convert_float_to_binary(11.5), "01000001001110000000000000000000")
        self.assertEqual(self.method.convert_float_to_binary(-11.5), "11000001001110000000000000000000")

    def test_div_of_binary_numbers(self):
        self.assertEqual(self.method.div_of_binary_numbers("00001011", "00011001"), "00111110111000010100011110101110")
        self.assertEqual(self.method.div_of_binary_numbers("11110101", "00011001"), "10111110111000010100011110101110")



if __name__ == '__main__':
    unittest.main()
