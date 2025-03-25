import unittest
from minimize_cnf_calculative import ConjunctiveNormalFormReducer
from unittest.mock import patch

class TestConjunctiveNormalFormReducer(unittest.TestCase):

    def test_complex_cases(self):
        test_cases = [
            ("(a ∨ b ∨ c) ∧ (a ∨ b ∨ ¬c)", "(a ∨ b)"),
            ("(a ∨ b ∨ c) ∧ (a ∨ ¬b ∨ c)", "(a ∨ c)"),
            ("(b ∨ a) ∧ (d ∨ c)", "(a ∨ b) ∧ (c ∨ d)"),
            ("(a ∨ b) ∧ (a ∨ b)", "(a ∨ b) ∧ (a ∨ b)"),
            ("(a) ∧ (a ∨ b ∨ c)", "(a) ∧ (a ∨ b ∨ c)"),
            ("(a ∨ b) ∧ (¬a ∨ ¬b)", "(a ∨ b) ∧ (¬a ∨ ¬b)"),
        ]

        for input_expr, expected in test_cases:
            with self.subTest(input_expr=input_expr):
                reducer = ConjunctiveNormalFormReducer(input_expr)
                self.assertEqual(reducer.simplify(), expected)

    def test_empty_clause_handling(self):
        reducer = ConjunctiveNormalFormReducer("() ∧ (a ∨ b)")
        self.assertEqual(reducer.simplify(), "() ∧ (a ∨ b)")

    def test_no_modification_needed(self):
        input_expr = "(a ∨ b) ∧ (c ∨ d)"
        reducer = ConjunctiveNormalFormReducer(input_expr)
        self.assertEqual(reducer.simplify(), input_expr)

    def test_parallel_processing(self):
        input_expr = "(a ∨ b ∨ c) ∧ (a ∨ b ∨ ¬c) ∧ (d ∨ e) ∧ (d ∨ ¬e)"
        expected = "(a ∨ b) ∧ (d)"
        reducer = ConjunctiveNormalFormReducer(input_expr)
        self.assertEqual(reducer.simplify(), expected)

    def test_initialization(self):
        reducer = ConjunctiveNormalFormReducer("(a ∨ b) ∧ (¬c ∨ d)")
        self.assertEqual(reducer.input_expression, "(a ∨ b) ∧ (¬c ∨ d)")
        self.assertEqual(len(reducer.disjunctive_clauses), 2)

    def test_merge_possibility_check(self):
        test_cases = [
            ({"a", "b"}, {"a", "¬b"}, True),
            ({"a", "b"}, {"a", "c"}, False),
            ({"a"}, {"¬a"}, True),
            ({"a", "¬a"}, {"b"}, False)
        ]

        for set1, set2, expected in test_cases:
            with self.subTest(set1=set1, set2=set2):
                result = ConjunctiveNormalFormReducer._check_merge_possibility(set1, set2)
                self.assertEqual(result, expected)

    def test_clause_combination(self):
        reducer = ConjunctiveNormalFormReducer("")
        self.assertEqual(
            reducer._combine_clauses({"a", "b"}, {"a", "¬b"}),
            {"a"}
        )

    def test_simplification_process(self):
        test_cases = [
            ("(a ∨ b) ∧ (a ∨ ¬b)", "(a)"),
            ("(a ∨ b ∨ c) ∧ (a ∨ ¬b ∨ c)", "(a ∨ c)"),
            ("(a ∨ b) ∧ (c ∨ d)", "(a ∨ b) ∧ (c ∨ d)"),
            ("True", "True"),
            ("(a) ∧ (¬a)", "False")
        ]

        for input_expr, expected in test_cases:
            with self.subTest(input=input_expr):
                reducer = ConjunctiveNormalFormReducer(input_expr)
                result = reducer.simplify()
                self.assertEqual(result, expected)

    def test_absorption(self):
        reducer = ConjunctiveNormalFormReducer("(a) ∧ (a ∨ b)")
        result = reducer.simplify()
        self.assertEqual(result, "(a) ∧ (a ∨ b)")

    def test_process_input_special_cases(self):
        self.assertEqual(ConjunctiveNormalFormReducer._process_input("True"), [])
        self.assertEqual(ConjunctiveNormalFormReducer._process_input(""), [{''}])

    def test_output_formatting(self):
        reducer = ConjunctiveNormalFormReducer("(a ∨ b) ∧ (¬c ∨ d)")
        test_clauses = [{"a", "b"}, {"¬c", "d"}]
        self.assertEqual(
            reducer._format_output(test_clauses),
            "(a ∨ b) ∧ (d ∨ ¬c)"
        )

        self.assertEqual(reducer._format_output([]), "True")
        self.assertEqual(reducer._format_output([set()]), "False")

    def test_error_handling(self):
        with self.assertRaises(AttributeError):
            ConjunctiveNormalFormReducer(123)


if __name__ == '__main__':
    unittest.main()