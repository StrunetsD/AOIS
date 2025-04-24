from formula import Formula

class BooleanExpressionMinimizer:
    def __init__(self, is_conjunctive_form):
        self.is_conjunctive = is_conjunctive_form
        self.expression_components = []

    def append_component(self, variable_set):
        self.expression_components.append(variable_set)

    def __str__(self):
        outer_operator = ' ∧ ' if self.is_conjunctive else ' ∨ '
        inner_operator = ' ∨ ' if self.is_conjunctive else ' ∧ '
        formatted_components = []
        for component in self.expression_components:
            variable_list = []
            for var in component:
                var_name, var_state = var
                if var_state:
                    variable_list.append(f"{var_name}")
                else:
                    variable_list.append(f"¬{var_name}")
            formatted_components.append(f"({inner_operator.join(variable_list)})")
        return outer_operator.join(formatted_components)


class KarnaughMapProcessor:
    def __init__(self, variables, truth_table_rows, is_conjunctive_form):
        self.is_conjunctive = is_conjunctive_form
        self.valid_processing = True
        self._map_data = []
        self.variables = variables
        self.truth_table_rows = truth_table_rows

        if not truth_table_rows:
            self.valid_processing = False
            return

        variable_count = len(variables)
        if variable_count == 2:
            self._initialize_2var_map()
        elif variable_count == 3:
            self._initialize_3var_map()
        elif variable_count == 4:
            self._initialize_4var_map()
        else:
            self.valid_processing = False

        self.display_map()

    @staticmethod
    def _calculate_position_index(primary, secondary):
        if primary == 0:
            return secondary
        else:
            return 3 if secondary == 0 else 2

    def _initialize_2var_map(self):
        self._map_data = [[{'vars': [], 'result': None, 'processed': False} for _ in range(2)] for _ in range(2)]
        for row in self.truth_table_rows:
            y = row[0]
            x = row[1]
            cell_value = row[2]
            current_cell = self._map_data[y][x]
            current_cell['vars'].extend([
                (self.variables[0], row[0]),
                (self.variables[1], row[1])
            ])
            current_cell['result'] = int(cell_value)


    def _initialize_3var_map(self):
        self._map_data = [[{'vars': [], 'result': None, 'processed': False} for _ in range(4)] for _ in range(2)]
        for row in self.truth_table_rows:
            row_index = row[0]
            col_index = self._calculate_position_index(row[1], row[2])
            cell_value = row[3]
            current_cell = self._map_data[row_index][col_index]
            current_cell['vars'].extend([(self.variables[0], row[0]),
                                          (self.variables[1], row[1]),
                                          (self.variables[2], row[2])])
            current_cell['result'] = int(cell_value)

    def _initialize_4var_map(self):
        self._map_data = [[{'vars': [], 'result': None, 'processed': False} for _ in range(4)] for _ in range(4)]
        for row in self.truth_table_rows:
            row_index = self._calculate_position_index(row[0], row[1])
            col_index = self._calculate_position_index(row[2], row[3])
            cell_value = row[4]
            current_cell = self._map_data[row_index][col_index]
            current_cell['vars'].extend([(self.variables[0], row[0]),
                                         (self.variables[1], row[1]),
                                         (self.variables[2], row[2]),
                                         (self.variables[3], row[3])])
            current_cell['result'] = int(cell_value)

    def _validate_region(self, start_col, start_row, region_width, region_height):
        has_unprocessed = False
        for dy in range(region_height):
            for dx in range(region_width):
                y = (start_row + dy) % len(self._map_data)
                x = (start_col + dx) % len(self._map_data[0])
                cell = self._map_data[y][x]
                if cell['result'] == self.is_conjunctive:
                    return False
                if not cell['processed']:
                    has_unprocessed = True
        return has_unprocessed

    def _mark_region(self, start_col, start_row, region_width, region_height):
        for dy in range(region_height):
            for dx in range(region_width):
                y = (start_row + dy) % len(self._map_data)
                x = (start_col + dx) % len(self._map_data[0])
                self._map_data[y][x]['processed'] = True

    def _extract_common_vars(self, start_col, start_row, region_width, region_height):
        shared_variables = []
        reference_cell = self._map_data[start_row][start_col]
        for var_index in range(len(reference_cell['vars'])):
            var_name, var_value = reference_cell['vars'][var_index]
            is_consistent = True
            for dy in range(region_height):
                if not is_consistent:
                    break
                for dx in range(region_width):
                    y = (start_row + dy) % len(self._map_data)
                    x = (start_col + dx) % len(self._map_data[0])
                    current_var = self._map_data[y][x]['vars'][var_index]
                    if current_var != (var_name, var_value):
                        is_consistent = False
                        break
            if is_consistent:
                if self.is_conjunctive:
                    shared_variables.append((var_name, not var_value))
                else:
                    shared_variables.append((var_name, var_value))
        return shared_variables

    def display_map(self):
        for row in self._map_data:
            print([cell['result'] for cell in row])

    def compute_minimized_form(self):
        if not self.valid_processing:
            return BooleanExpressionMinimizer(self.is_conjunctive)

        possible_regions = [
            (4, 4), (2, 4), (4, 2),
            (2, 2), (1, 4), (4, 1),
            (1, 2), (2, 1), (1, 1)
        ]

        identified_regions = []
        for region in possible_regions:
            width, height = region
            if width > len(self._map_data[0]) or height > len(self._map_data):
                continue

            for y in range(len(self._map_data)):
                for x in range(len(self._map_data[0])):
                    if self._validate_region(x, y, width, height):
                        identified_regions.append((x, y, width, height))
                        self._mark_region(x, y, width, height)

        result = BooleanExpressionMinimizer(self.is_conjunctive)
        for region in identified_regions:
            x, y, w, h = region
            common_vars = self._extract_common_vars(x, y, w, h)
            if common_vars:
                result.append_component(common_vars)

        return result


class TruthTableData:
    def __init__(self, variable_list, table_content):
        self.variable_names = variable_list
        self.data_rows = table_content

# self.operators = {
#             "!": {"priority": 4, "unary": True},
#             "&": {"priority": 3, "unary": False},
#             "|": {"priority": 2, "unary": False},
#             "->": {"priority": 1, "unary": False},
#             "~": {"priority": 0, "unary": False},
#         }
# self.expression = formula.replace('∨', '|').replace(
#             '∧', '&').replace('→', '->').replace('↔', '~')
def main():
    input_expr = "(a→b)∧!C"
    formula = Formula(input_expr)
    truth_table, headers, results = formula.create_table_of_truth()
    variables = headers[:-1]

    dnf_processor = KarnaughMapProcessor(
        variables=variables,
        truth_table_rows=truth_table,
        is_conjunctive_form=False
    )
    print("Упрощенная ДНФ:", dnf_processor.compute_minimized_form())
    print("==============================")
    cnf_processor = KarnaughMapProcessor(
        variables=variables,
        truth_table_rows=truth_table,
        is_conjunctive_form=True
    )
    print("Упрощенная КНФ:", cnf_processor.compute_minimized_form())


if __name__ == "__main__":
    main()