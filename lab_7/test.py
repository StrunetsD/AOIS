import unittest
from main import *
class TestDiagonalMatrix(unittest.TestCase):

    def setUp(self):
        self.dm = DiagonalMatrix(rows=16, cols=16)
        self.dm.set_word([1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1], 0, 0)
        self.dm.set_word([1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0], 1, 1)
        self.dm.set_word([0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1], 2, 2)

    def test_set_word(self):
        self.assertEqual(self.dm.matrix[0], [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(self.dm.matrix[1], [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(self.dm.matrix[2], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    def test_get_column(self):
        self.assertEqual(self.dm.get_column(0), [1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1])
        self.assertEqual(self.dm.get_column(1), [0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0])
        self.assertEqual(self.dm.get_column(2), [1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1])

    def test_F1_operation(self):
        result = self.dm.F1_operation(0, 1)
        expected = [0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0]
        self.assertEqual(result, expected)

    def test_F14_operation(self):
        result = self.dm.F14_operation(0, 1)
        expected = [1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1]
        self.assertEqual(result, expected)

    def test_F3_operation(self):
        result = self.dm.F3_operation(0, 1)
        expected = [1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1]
        self.assertEqual(result, expected)

    def test_F12_operation(self):
        result = self.dm.F12_operation(0, 1)
        expected = [0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0]
        self.assertEqual(result, expected)

    def test_sum_fields_by_indexs(self):
        self.dm.sum_fields_by_indexs([0, 1, 2])
        expected_row_0 = [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        expected_row_1 =  [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        expected_row_2 = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.assertEqual(self.dm.matrix[0], expected_row_0)
        self.assertEqual(self.dm.matrix[1], expected_row_1)
        self.assertEqual(self.dm.matrix[2], expected_row_2)

if __name__ == '__main__':
    unittest.main()