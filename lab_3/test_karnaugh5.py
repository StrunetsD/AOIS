import unittest
from formula import Formula
from karnaugh_template import KNF_Optimizer
from karnaugh_5 import KarnaughMapProcessor, BooleanExpressionMinimizer

class TestKarnaughMinimizer5Vars(unittest.TestCase):
    def test_all_true_expression(self):
        # Истинно для всех наборов: a∨¬a → True
        expr = "a∨¬a"
        formula = Formula(expr)
        table, headers, _ = formula.create_table_of_truth()
        processor = KarnaughMapProcessor(headers[:-1], table, is_conjunctive_form=False)
        result = processor.compute_minimized_form(expr)
        self.assertEqual(str(result), "")

    def test_all_false_expression(self):
        expr = "a∧¬a"
        formula = Formula(expr)
        table, headers, _ = formula.create_table_of_truth()
        processor = KarnaughMapProcessor(headers[:-1], table, is_conjunctive_form=True)
        result = processor.compute_minimized_form(expr)
        self.assertEqual(str(result), "")

    def test_simple_conjunction(self):
        expr = "a∧b∧c∧d∧e"
        formula = Formula(expr)
        table, headers, _ = formula.create_table_of_truth()
        processor = KarnaughMapProcessor(headers[:-1], table, is_conjunctive_form=False)
        result = processor.compute_minimized_form(expr)
        self.assertIn("(a ∧ b ∧ c ∧ d ∧ e)", str(result))

    def test_invalid_variable_count(self):
        expr = "a∧b"
        formula = Formula(expr)
        table, headers, _ = formula.create_table_of_truth()
        processor = KarnaughMapProcessor(headers[:-1], table, is_conjunctive_form=False)
        self.assertFalse(processor.valid_processing)

    def test_empty_truth_table(self):
        processor = KarnaughMapProcessor(['a', 'b', 'c', 'd', 'e'], [], is_conjunctive_form=True)
        self.assertFalse(processor.valid_processing)


if __name__ == '__main__':
    unittest.main()
