import unittest
from minimize_cnf_table import KNF_Optimizer


class TestKNFOptimizer(unittest.TestCase):
    def test_parse_knf(self):
        test_cases = [
            ("True", []),
            ("(a ∨ b) ∧ (c ∨ d)", [{'a', 'b'}, {'c', 'd'}]),
            ("(¬a ∨ b) ∧ (c ∨ ¬d)", [{'¬a', 'b'}, {'c', '¬d'}])
        ]

        for expr, expected in test_cases:
            with self.subTest(expr=expr):
                result = KNF_Optimizer._parse_knf(expr)
                self.assertEqual(len(result), len(expected))
                for item in result:
                    self.assertIn(item, expected)

    def test_can_combine(self):
        test_cases = [
            ({'a', 'b'}, {'a', '¬b'}, True),
            ({'a', 'b'}, {'c', 'd'}, False),
            ({'a'}, {'¬a'}, True),
            ({'a', 'b', 'c'}, {'a', 'b', '¬c'}, True)
        ]

        for t1, t2, expected in test_cases:
            with self.subTest(t1=t1, t2=t2):
                result = KNF_Optimizer._can_combine(t1, t2)
                self.assertEqual(result, expected)


    def test_full_optimization(self):
        test_cases = [
            ("(a ∨ b) ∧ (a ∨ ¬b)", "a"),
            ("(a ∨ b ∨ c) ∧ (a ∨ b ∨ ¬c)", "a ∨ b"),
            ("(a ∨ b) ∧ (c ∨ d)", "a ∨ b"),
        ]

        for input_expr, expected in test_cases:
            with self.subTest(input=input_expr):
                optimizer = KNF_Optimizer(input_expr)
                result = optimizer.optimize()
                self.assertEqual(result, expected)

    def test_coverage_matrix(self):
        optimizer = KNF_Optimizer("(a ∨ b) ∧ (c ∨ d)")
        optimizer.optimize()
        matrix = optimizer._build_coverage_matrix()
        self.assertEqual(len(matrix), 2)
        self.assertIn(frozenset({'a', 'b'}), matrix.keys())

    def test_edge_cases(self):
        test_cases = [
            ("(a ∨ ¬a)", "a ∨ ¬a"),
        ]

        for input_expr, expected in test_cases:
            with self.subTest(input=input_expr):
                optimizer = KNF_Optimizer(input_expr)
                result = optimizer.optimize()
                self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()