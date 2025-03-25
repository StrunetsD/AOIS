import unittest
from karnaugh_template import BooleanExpressionMinimizer, KarnaughMapProcessor, TruthTableData, Formula


class TestBooleanExpressionMinimizer(unittest.TestCase):
    def test_initialization(self):
        minimizer = BooleanExpressionMinimizer(True)
        self.assertEqual(len(minimizer.expression_components), 0)

    def test_add_component(self):
        minimizer = BooleanExpressionMinimizer(False)
        minimizer.append_component([('a', True), ('b', False)])
        self.assertEqual(len(minimizer.expression_components), 1)

    def test_string_conversion(self):
        minimizer = BooleanExpressionMinimizer(True)
        minimizer.append_component([('a', True), ('b', False)])
        self.assertEqual(str(minimizer), "(a ∨ ¬b)")


class TestKarnaughMapProcessor(unittest.TestCase):
    def setUp(self):
        self.sample_data_2var = TruthTableData(
            ['a', 'b'],
            [
                [0, 0, 1],
                [0, 1, 0],
                [1, 0, 1],
                [1, 1, 1]
            ]
        )

    def test_2var_map_initialization(self):
        processor = KarnaughMapProcessor(self.sample_data_2var.variable_names, self.sample_data_2var.data_rows, False)
        self.assertEqual(len(processor._map_data), 2)
        self.assertEqual(len(processor._map_data[0]), 2)

    def test_minimization_logic(self):
        processor = KarnaughMapProcessor(self.sample_data_2var.variable_names, self.sample_data_2var.data_rows, False)
        result = processor.compute_minimized_form()
        self.assertIn('a', str(result))


class TestTruthTableData(unittest.TestCase):
    def test_data_initialization(self):
        data = TruthTableData(['a', 'b'], [[0, 0, 1], [1, 1, 0]])
        self.assertEqual(len(data.data_rows), 2)


class TestIntegration(unittest.TestCase):
    def test_full_workflow(self):
        expr = "a ∨ (a ∧ b)"
        formula = Formula(expr)
        truth_table, headers, results = formula.create_table_of_truth()
        table_data = TruthTableData(headers[:-1], truth_table)

        processor = KarnaughMapProcessor(table_data.variable_names, table_data.data_rows, False)
        minimized = processor.compute_minimized_form()
        self.assertEqual(str(minimized).strip(), "(a)")


class TestEdgeCases(unittest.TestCase):
    def test_empty_expression(self):
        processor = KarnaughMapProcessor([], [], True)
        result = processor.compute_minimized_form()
        self.assertEqual(str(result), '')

    def test_tautology(self):
        data = TruthTableData(['a'], [[0, 1], [1, 1]])
        processor = KarnaughMapProcessor(data.variable_names, data.data_rows, False)
        result = processor.compute_minimized_form()
        self.assertIn('', str(result))


if __name__ == '__main__':
    unittest.main()