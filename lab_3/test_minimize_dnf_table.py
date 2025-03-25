import unittest
from minimize_dnf_table import PerfectDNF_Optimizer


class TestPerfectDNF_Optimizer(unittest.TestCase):
    def test_parse_expression(self):
        test_cases = [
            ("False", []),
            ("(a ∧ b) ∨ (c ∧ d)", [{'a', 'b'}, {'c', 'd'}]),
            ("(a ∧ ¬b) ∨ (¬c ∧ d)", [{'a', '¬b'}, {'¬c', 'd'}])
        ]

        for expr, expected in test_cases:
            with self.subTest(expr=expr):
                result = PerfectDNF_Optimizer._parse_expression(expr)
                self.assertEqual(len(result), len(expected))
                for item in result:
                    self.assertIn(item, expected)

    def test_check_merge_condition(self):
        test_cases = [
            ({'a', 'b'}, {'a', '¬b'}, True),
            ({'a', 'b'}, {'c', 'd'}, False),
            ({'a'}, {'¬a'}, True),
            ({'a', 'b', 'c'}, {'a', 'b', '¬c'}, True)
        ]

        for t1, t2, expected in test_cases:
            with self.subTest(t1=t1, t2=t2):
                result = PerfectDNF_Optimizer._check_merge_condition(t1, t2)
                self.assertEqual(result, expected)


    def test_prime_implicants_extraction(self):
        optimizer = PerfectDNF_Optimizer("(a ∧ b) ∨ (a ∧ ¬b)")
        optimizer._extract_prime_implicants()
        self.assertEqual(len(optimizer.essential_primes), 1)
        self.assertIn(frozenset({'a'}), optimizer.essential_primes)

    def test_coverage_matrix(self):
        optimizer = PerfectDNF_Optimizer("(a ∧ b) ∨ (a ∧ ¬b)")
        optimizer._extract_prime_implicants()
        matrix = optimizer._construct_coverage_matrix()
        self.assertEqual(len(matrix), 1)
        self.assertIn(frozenset({'a'}), matrix.keys())

    def test_full_optimization(self):
        test_cases = [
            ("(a ∧ b) ∨ (a ∧ ¬b)", "a"),
            ("(a ∧ b ∧ c) ∨ (a ∧ b ∧ ¬c)", "a ∧ b"),
            ("(a ∧ b) ∨ (c ∧ d)", "(c ∧ d) ∨ (a ∧ b)"),
        ]

        for input_expr, expected in test_cases:
            with self.subTest(input=input_expr):
                optimizer = PerfectDNF_Optimizer(input_expr)
                result = optimizer.optimize()
                self.assertEqual(result, expected)




if __name__ == '__main__':
    unittest.main()