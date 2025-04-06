from formula import *

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
                variable_list.append(f"{var_name}" if var_state else f"¬{var_name}")
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
            print("Ошибка: пустая таблица истинности.")
            return

        variable_count = len(variables)
        print(f"Количество переменных: {variable_count}")

        if variable_count == 5:
            self._initialize_5var_map()
        else:
            self.valid_processing = False
            print("Ошибка: неподдерживаемое количество переменных.")

        self.display_map()

    @staticmethod
    def _calculate_position_index(primary, secondary):
        gray_code = {
            (0, 0): 0,
            (0, 1): 1,
            (1, 1): 2,
            (1, 0): 3
        }
        return gray_code.get((primary, secondary), 0)

    def _initialize_5var_map(self):
        print("Инициализация карты для 5 переменных.")
        gray_code_3bit = [
            (0, 0, 0),
            (0, 0, 1),
            (0, 1, 1),
            (0, 1, 0),
            (1, 1, 0),
            (1, 1, 1),
            (1, 0, 1),
            (1, 0, 0)
        ]
        self._map_data = [[{'vars': [], 'result': None, 'processed': False} for _ in range(4)] for _ in range(8)]
        for row in self.truth_table_rows:
            a, b, c, d, e = row[:5]
            try:
                row_index = gray_code_3bit.index((a, b, c))
            except ValueError:
                print(f"Ошибка: комбинация ({a}, {b}, {c}) не найдена.")
                continue
            col_index = self._calculate_position_index(d, e)
            cell_value = row[5]
            current_cell = self._map_data[row_index][col_index]
            current_cell['vars'].extend([
                (self.variables[0], a),
                (self.variables[1], b),
                (self.variables[2], c),
                (self.variables[3], d),
                (self.variables[4], e)
            ])
            current_cell['result'] = int(cell_value)
            print(f"Ячейка [{row_index}][{col_index}]: {current_cell}")

    def _validate_region(self, start_col, start_row, region_width, region_height):
        target_value = 0 if self.is_conjunctive else 1
        for dy in range(region_height):
            for dx in range(region_width):
                y = (start_row + dy) % len(self._map_data)
                x = (start_col + dx) % len(self._map_data[0])
                cell = self._map_data[y][x]
                if cell['result'] != target_value:
                    return False
        return True

    def _mark_region(self, start_col, start_row, region_width, region_height):
        for dy in range(region_height):
            for dx in range(region_width):
                y = (start_row + dy) % len(self._map_data)
                x = (start_col + dx) % len(self._map_data[0])
                self._map_data[y][x]['processed'] = True

    def _extract_common_vars(self, start_col, start_row, region_width, region_height):
        shared_vars = []
        var_values = [set() for _ in range(len(self.variables))]

        for dy in range(region_height):
            for dx in range(region_width):
                y = (start_row + dy) % len(self._map_data)
                x = (start_col + dx) % len(self._map_data[0])
                for i, (name, val) in enumerate(self._map_data[y][x]['vars']):
                    var_values[i].add(val)

        for i, vals in enumerate(var_values):
            if len(vals) == 1:
                var_name = self.variables[i]
                var_val = vals.pop()
                if self.is_conjunctive:
                    shared_vars.append((var_name, not var_val))
                else:
                    shared_vars.append((var_name, var_val))
        return shared_vars

    def display_map(self):
        print("\nКарта Карно:")
        for i, row in enumerate(self._map_data):
            print(f"{i:2}:", end=" ")
            for cell in row:
                print(cell['result'] if cell['result'] is not None else 'X', end=" ")
            print()

    def compute_minimized_form(self):
        if not self.valid_processing:
            print("Ошибка: недопустимая обработка.")
            return BooleanExpressionMinimizer(self.is_conjunctive)

        if self.is_conjunctive:
            return self._compute_knf_karnaugh()
        else:
            return self._compute_dnf_karnaugh()

    def _compute_knf_karnaugh(self):
        zero_cells = []
        for y in range(len(self._map_data)):
            for x in range(len(self._map_data[0])):
                if self._map_data[y][x]['result'] == 0:
                    zero_cells.append((x, y))

        if not zero_cells:
            print("Нет нулевых ячеек для минимизации КНФ.")
            return BooleanExpressionMinimizer(True)

        possible_regions = self._get_possible_regions_order()
        regions = self._find_maximal_regions(zero_cells, possible_regions)

        result = BooleanExpressionMinimizer(True)
        for region in regions:
            common_vars = self._get_common_vars_for_region(region, is_knf=True)
            if common_vars:
                result.append_component(common_vars)

        return result

    def _compute_dnf_karnaugh(self):
        one_cells = []
        for y in range(len(self._map_data)):
            for x in range(len(self._map_data[0])):
                if self._map_data[y][x]['result'] == 1:
                    one_cells.append((x, y))

        if not one_cells:
            print("Нет единичных ячеек для минимизации ДНФ.")
            return BooleanExpressionMinimizer(False)

        possible_regions = self._get_possible_regions_order()
        regions = self._find_maximal_regions(one_cells, possible_regions)

        result = BooleanExpressionMinimizer(False)
        for region in regions:
            common_vars = self._get_common_vars_for_region(region, is_knf=False)
            if common_vars:
                result.append_component(common_vars)

        return result

    def _get_possible_regions_order(self):
        rows = len(self._map_data)
        cols = len(self._map_data[0]) if rows > 0 else 0

        regions = []
        max_size = max(rows, cols)

        for h in [8, 4, 2, 1]:
            for w in [8, 4, 2, 1]:
                if h <= rows and w <= cols:
                    regions.append((w, h))

        regions = list(set(regions))
        regions.sort(key=lambda x: -(x[0] * x[1]))

        return regions

    def _find_maximal_regions(self, target_cells, possible_regions):
        covered = set()
        regions = []

        for w, h in possible_regions:
            for y in range(len(self._map_data)):
                for x in range(len(self._map_data[0])):
                    valid = True
                    cells_in_region = set()

                    for dy in range(h):
                        for dx in range(w):
                            ny = (y + dy) % len(self._map_data)
                            nx = (x + dx) % len(self._map_data[0])
                            if (nx, ny) not in target_cells:
                                valid = False
                                break
                            cells_in_region.add((nx, ny))
                        if not valid:
                            break

                    if valid:
                        new_cells = cells_in_region - covered
                        if new_cells:
                            regions.append((x, y, w, h))
                            covered.update(cells_in_region)

        return regions

    def _get_common_vars_for_region(self, region, is_knf):
        x, y, w, h = region
        num_vars = len(self.variables)
        var_values = [set() for _ in range(num_vars)]

        for dy in range(h):
            for dx in range(w):
                ny = (y + dy) % len(self._map_data)
                nx = (x + dx) % len(self._map_data[0])
                cell_vars = self._map_data[ny][nx]['vars']

                for i, (var_name, var_val) in enumerate(cell_vars):
                    var_values[i].add(var_val)

        result = []
        for i, values in enumerate(var_values):
            var_name = self.variables[i]
            if len(values) == 1:
                val = values.pop()
                result.append((var_name, not val if is_knf else val))

        return result


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
    input_expr = "a∧b∧c∧d∨e"
    print(f"Входное выражение: {input_expr}")
    formula = Formula(input_expr)
    truth_table, headers, results = formula.create_table_of_truth()
    print("Таблица истинности:")
    print(headers)
    for row in truth_table:
        print(row)

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