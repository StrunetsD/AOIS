import unittest
from minimize_dnf_calculative import DNFMinimizer


class TestDNFMinimizer(unittest.TestCase):
    def test_parse_expression(self):
        test_cases = [
            ("False", []),
            ("True", [set()]),
            ("(a ∧ b) ∨ (c ∧ d)", [{'a', 'b'}, {'c', 'd'}]),
            ("(a ∧ ¬b) ∨ (¬c ∧ d)", [{'a', '¬b'}, {'¬c', 'd'}])
        ]

        for expr, expected in test_cases:
            with self.subTest(expr=expr):
                result = DNFMinimizer.parse_expression(expr)
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
                result = DNFMinimizer.can_combine(t1, t2)
                self.assertEqual(result, expected)

    def test_combine_terms(self):
        test_cases = [
            ({'a', 'b'}, {'a', '¬b'}, {'a'}),
            ({'a', 'b', 'c'}, {'a', 'b', '¬c'}, {'a', 'b'})
        ]

        for t1, t2, expected in test_cases:
            with self.subTest(t1=t1, t2=t2):
                result = DNFMinimizer.combine_terms(t1, t2)
                self.assertEqual(result, expected)

    def test_remove_redundant_terms(self):
        test_cases = [
            ([{'a'}, {'a', 'b'}], [{'a'}]),
            ([{'a', 'b'}, {'a', 'c'}], [{'a', 'b'}, {'a', 'c'}]),
            ([{'a'}, {'a'}], [{'a'}])
        ]

        for input_terms, expected in test_cases:
            with self.subTest(input=input_terms):
                result = DNFMinimizer.remove_redundant_terms(input_terms)
                self.assertEqual(result, expected)

    def test_minimize_expression(self):
        test_cases = [
            ("(a ∧ b) ∨ (a ∧ ¬b)", "(a)"),
            ("(a ∧ b ∧ c) ∨ (a ∧ b ∧ ¬c)", "(a ∧ b)"),
            ("(a ∧ b) ∨ (c ∧ d)", "(a ∧ b) ∨ (c ∧ d)"),
            ("(a ∧ b) ∨ (a ∧ c) ∨ (b ∧ c)", "(a ∧ b) ∨ (a ∧ c) ∨ (b ∧ c)")
        ]

        for input_expr, expected in test_cases:
            with self.subTest(input=input_expr):
                minimizer = DNFMinimizer(input_expr)
                result = minimizer.minimize_expression()
                self.assertEqual(result, expected)

    def test_format_expression(self):
        test_cases = [
            ([{'a', 'b'}, {'c', 'd'}], "(a ∧ b) ∨ (c ∧ d)"),
            ([{'a'}], "(a)"),
            ([set()], "True"),
            ([], "False")
        ]

        for terms, expected in test_cases:
            with self.subTest(terms=terms):
                result = DNFMinimizer.format_expression(terms)
                self.assertEqual(result, expected)

    def test_edge_cases(self):
        test_cases = [
            ("True", "True"),
        ]

        for input_expr, expected in test_cases:
            with self.subTest(input=input_expr):
                minimizer = DNFMinimizer(input_expr)
                result = minimizer.minimize_expression()
                self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()