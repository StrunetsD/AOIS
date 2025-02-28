import unittest
from run import Formula

class TestFormula(unittest.TestCase):
    def setUp(self):
        self.simple_formula = Formula("a ∧ b")
        self.implication_formula = Formula("a → b")
        self.complex_formula = Formula("(a ∨ b) ∧ ¬c")
        self.unicode_formula = Formula("a∨b→c↔d")

    def test_get_variables(self):
        self.assertEqual(self.simple_formula.get_variables(), ['a', 'b'])
        self.assertEqual(self.complex_formula.get_variables(), ['a', 'b', 'c'])

    def test_tokenize(self):
        self.assertEqual(self.implication_formula.tokenize(), ['a', 'b'])
        self.assertEqual(self.unicode_formula.tokenize(), ['a', '|', 'b', 'c', '~', 'd'])

    def test_postfix_conversion(self):
        postfix = self.implication_formula.to_postfix(self.implication_formula.tokenize())
        self.assertEqual(postfix, ['a', 'b'])

    def test_evaluate_postfix(self):
        tokens = self.simple_formula.tokenize()
        postfix = self.simple_formula.to_postfix(tokens)
        self.assertTrue(self.simple_formula.evaluate_postfix(postfix, {'a': True, 'b': True}))
        self.assertFalse(self.simple_formula.evaluate_postfix(postfix, {'a': True, 'b': False}))

    def test_truth_table(self):
        table, headers, results = self.simple_formula.create_table_of_truth()
        self.assertEqual(headers, ['a', 'b', 'Result'])
        self.assertEqual(len(table), 4)
        self.assertEqual([row[-1] for row in table], [False, False, False, True])

    def test_dnf_cnf(self):
        formula = Formula("a ∨ b")
        self.assertEqual(formula.to_dnf(), "(¬a ∧ b) ∨ (a ∧ ¬b) ∨ (a ∧ b)")
        self.assertEqual(formula.to_cnf(), "(a ∨ b)")

        formula = Formula("a ∧ b")
        self.assertEqual(formula.to_dnf(), "(a ∧ b)")
        self.assertEqual(formula.to_cnf(), "(a ∨ b) ∧ (a ∨ ¬b) ∧ (¬a ∨ b)")

    def test_number_forms(self):
        formula = Formula("a")
        self.assertEqual(formula.get_number_forms(), "(1) v\n(0) ∧")


        formula = Formula("a ∨ b")
        expected = "(1,2,3) v\n(0) ∧"
        self.assertEqual(formula.get_number_forms(), expected)

    def test_index_form(self):
        _, _, results = self.complex_formula.create_table_of_truth()
        result_str = ''.join(str(int(r)) for r in results)
        decimal = Formula.binary_to_decimal_number(result_str)
        self.assertEqual(decimal, 21)

    def test_implication(self):
        _, _, results = self.implication_formula.create_table_of_truth()
        self.assertEqual(results, [False, False, True, True])

    def test_unicode_replacements(self):
        self.assertEqual(self.unicode_formula.expression, "a|b->c~d")

if __name__ == '__main__':
    unittest.main()