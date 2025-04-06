from formula import *
import itertools # Needed for combinations

class BooleanExpressionMinimizer:
    # ... (keep this class as is) ...
    def __init__(self, is_conjunctive_form):
        self.is_conjunctive = is_conjunctive_form
        self.expression_components = []

    def append_component(self, variable_set):
        # Sort variables within component for consistent output
        sorted_component = sorted(variable_set, key=lambda x: x[0])
        # Avoid adding duplicate components
        if sorted_component not in self.expression_components:
            self.expression_components.append(sorted_component)
             # Sort components themselves (optional, for consistent order)
            self.expression_components.sort(key=lambda comp: "".join(v[0] for v in comp))


    def __str__(self):
        outer_operator = ' ∧ ' if self.is_conjunctive else ' ∨ '
        inner_operator = ' ∨ ' if self.is_conjunctive else ' ∧ '
        formatted_components = []
        if not self.expression_components:
             # Handle cases where the function is always True (empty DNF) or always False (empty CNF)
             if self.is_conjunctive:
                 return "1" # KNF is trivially True if no zeros
             else:
                 return "0" # DNF is trivially False if no ones

        for component in self.expression_components:
            variable_list = []
            # Ensure consistent order for variables within a term
            sorted_vars = sorted(component, key=lambda x: x[0])
            for var in sorted_vars:
                var_name, var_state = var
                # For KNF (is_conjunctive=True): var_state=True means ¬var_name, var_state=False means var_name
                # For DNF (is_conjunctive=False): var_state=True means var_name, var_state=False means ¬var_name
                if self.is_conjunctive:
                     variable_list.append(f"¬{var_name}" if var_state else f"{var_name}")
                else:
                     variable_list.append(f"{var_name}" if var_state else f"¬{var_name}")

            # Handle single variable terms without parentheses
            if len(variable_list) == 1:
                 formatted_components.append(variable_list[0])
            else:
                 formatted_components.append(f"({inner_operator.join(variable_list)})")

        # Sort the final terms alphabetically based on the first variable in each term
        # formatted_components.sort() # Optional: Sort final terms if desired

        return outer_operator.join(formatted_components)


class KarnaughMapProcessor:
    def __init__(self, variables, truth_table_rows, is_conjunctive_form):
        self.is_conjunctive = is_conjunctive_form
        self.valid_processing = True
        self._map_data = []
        self._map_coords_to_vars = {} # Store variable assignments per coordinate
        self.variables = variables
        self.truth_table_rows = truth_table_rows
        self.num_vars = len(variables)
        self.target_value = 0 if self.is_conjunctive else 1

        if not truth_table_rows:
            self.valid_processing = False
            print("Ошибка: пустая таблица истинности.")
            return

        print(f"Количество переменных: {self.num_vars}")

        if self.num_vars == 5:
            self.rows, self.cols = 8, 4 # A,B,C rows; D,E cols
            self._initialize_5var_map()
        elif self.num_vars == 4:
             self.rows, self.cols = 4, 4 # A,B rows; C,D cols
             self._initialize_4var_map()
        elif self.num_vars == 3:
             self.rows, self.cols = 2, 4 # A rows; B, C cols
             self._initialize_3var_map()
        elif self.num_vars == 2:
             self.rows, self.cols = 2, 2 # A rows; B cols
             self._initialize_2var_map()
        else:
            self.valid_processing = False
            print("Ошибка: неподдерживаемое количество переменных (поддерживается 2-5).")
            return

        self.display_map()

    @staticmethod
    def _gray_code(n):
        """Generates Gray code for n bits."""
        if n == 0: return [()]
        if n == 1: return [(0,), (1,)]
        lower_gray = KarnaughMapProcessor._gray_code(n - 1)
        return [(0,) + code for code in lower_gray] + [(1,) + code for code in reversed(lower_gray)]

    @staticmethod
    def _get_gray_indices(bits):
        """Map bit tuple to its index in the Gray sequence."""
        gray_seq = KarnaughMapProcessor._gray_code(len(bits))
        try:
            return gray_seq.index(bits)
        except ValueError:
            print(f"Warning: Bit combination {bits} not found in Gray sequence.")
            return -1 # Should not happen if truth table is complete

    def _initialize_map(self, row_vars_count, col_vars_count):
        """Generic map initializer."""
        self._map_data = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self._map_coords_to_vars = {}

        for row_data in self.truth_table_rows:
            inputs = tuple(row_data[:self.num_vars])
            output = int(row_data[self.num_vars])

            row_bits = inputs[:row_vars_count]
            col_bits = inputs[row_vars_count:]

            row_idx = self._get_gray_indices(row_bits)
            col_idx = self._get_gray_indices(col_bits)

            if row_idx != -1 and col_idx != -1:
                if self._map_data[row_idx][col_idx] is not None:
                     print(f"Warning: Overwriting map cell [{row_idx}][{col_idx}]")
                self._map_data[row_idx][col_idx] = output
                # Store variable mapping for easier lookup later
                var_assignment = list(zip(self.variables, inputs))
                self._map_coords_to_vars[(row_idx, col_idx)] = var_assignment
            else:
                 print(f"Error processing row: {row_data} - invalid Gray indices.")

         # Check for any None cells - indicates incomplete truth table mapping
        for r in range(self.rows):
            for c in range(self.cols):
                if self._map_data[r][c] is None:
                    print(f"Warning: Map cell [{r}][{c}] was not initialized. Assigning default value (e.g., 0).")
                    self._map_data[r][c] = 0 # Or handle as error / don't care

    # --- Specific Initializers ---
    def _initialize_5var_map(self):
        print("Инициализация карты для 5 переменных (A,B,C | D,E).")
        self._initialize_map(3, 2)

    def _initialize_4var_map(self):
        print("Инициализация карты для 4 переменных (A,B | C,D).")
        self._initialize_map(2, 2)

    def _initialize_3var_map(self):
        print("Инициализация карты для 3 переменных (A | B,C).")
        self._initialize_map(1, 2)

    def _initialize_2var_map(self):
        print("Инициализация карты для 2 переменных (A | B).")
        self._initialize_map(1, 1)
    # --- End Initializers ---


    def display_map(self):
        if not self.valid_processing or not self._map_data:
            return
        print("\nКарта Карно:")
        # Simple display, add headers later if needed
        for r in range(self.rows):
            print(f"{r:2}:", end=" ")
            for c in range(self.cols):
                val = self._map_data[r][c]
                print(val if val is not None else 'X', end=" ")
            print()

    def _get_coords_in_region(self, r, c, h, w):
        """Get all (row, col) tuples within a region, handling wrap-around."""
        coords = set()
        for dr in range(h):
            for dc in range(w):
                curr_r = (r + dr) % self.rows
                curr_c = (c + dc) % self.cols
                coords.add((curr_r, curr_c))
        return coords

    def _is_valid_region(self, coords):
        """Check if all cells in coords have the target value."""
        if not coords: return False
        for r_idx, c_idx in coords:
            if self._map_data[r_idx][c_idx] != self.target_value:
                return False
        return True

    def _get_region_variables(self, coords):
        """Find constant variables within the region."""
        if not coords: return []

        var_values = {var: set() for var in self.variables}

        first_coord = next(iter(coords)) # Get one coordinate to initialize
        if first_coord not in self._map_coords_to_vars:
             print(f"Error: Variable assignment not found for coord {first_coord}")
             # Fallback: Try to find variables based on gray codes? Might be complex.
             # For now, return empty - indicating an issue.
             return []

        # Populate variable values seen in the region
        for r_idx, c_idx in coords:
            coord_key = (r_idx, c_idx)
            if coord_key in self._map_coords_to_vars:
                assignments = self._map_coords_to_vars[coord_key]
                for var, val in assignments:
                    var_values[var].add(val)
            else:
                # This should ideally not happen if _initialize_map worked fully
                print(f"Warning: Missing variable assignment for coordinate ({r_idx}, {c_idx}) in region.")
                # If we hit this, the common variable detection might be incorrect
                # We could try to reconstruct from gray code indices but that adds complexity

        # Determine common variables based on collected values
        common_vars = []
        for var, seen_vals in var_values.items():
            if len(seen_vals) == 1:
                val = seen_vals.pop()
                # KNF logic: val=0 -> var, val=1 -> ¬var (represented by (var, True) in result)
                # DNF logic: val=0 -> ¬var, val=1 -> var (represented by (var, True) in result)
                # Store the variable name and its *required state* in the term
                if self.is_conjunctive:
                    common_vars.append((var, bool(val))) # KNF: True means it was 1, needs negation
                else:
                    common_vars.append((var, bool(val))) # DNF: True means it was 1, needs direct var

        return common_vars

    def find_prime_implicants(self):
        """Find all maximal blocks (prime implicants) of the target value."""
        prime_implicants = {} # Store as { frozenset(coords): term_vars }
        target_coords = set()
        for r in range(self.rows):
            for c in range(self.cols):
                if self._map_data[r][c] == self.target_value:
                    target_coords.add((r, c))

        processed_coords = set() # Track coords included in *some* PI

        # Iterate through all target cells as potential starting points
        for r_start in range(self.rows):
            for c_start in range(self.cols):
                if (r_start, c_start) not in target_coords:
                    continue

                # Try expanding rectangles of power-of-2 dimensions
                # Max height/width are map dimensions, restricted to powers of 2
                possible_heights = [2**i for i in range(self.rows.bit_length()) if 2**i <= self.rows]
                possible_widths = [2**i for i in range(self.cols.bit_length()) if 2**i <= self.cols]

                for h in reversed(possible_heights): # Try larger first
                     for w in reversed(possible_widths):
                        coords = self._get_coords_in_region(r_start, c_start, h, w)

                        # Check if the formed rectangle is within the target cells
                        if coords.issubset(target_coords):
                             # Now check if this region is maximal (not contained in a larger valid PI)
                             is_maximal = True
                             # Check expansion vertically
                             if h * 2 <= self.rows and h*2 in possible_heights:
                                 larger_coords_v = self._get_coords_in_region(r_start, c_start, h * 2, w)
                                 if larger_coords_v.issubset(target_coords):
                                     is_maximal = False
                             # Check expansion horizontally
                             if is_maximal and w * 2 <= self.cols and w*2 in possible_widths:
                                 larger_coords_h = self._get_coords_in_region(r_start, c_start, h, w * 2)
                                 if larger_coords_h.issubset(target_coords):
                                     is_maximal = False

                             if is_maximal:
                                 frozen_coords = frozenset(coords)
                                 if frozen_coords not in prime_implicants:
                                      term_vars = self._get_region_variables(coords)
                                      if term_vars is not None: # Avoid adding if error occurred
                                          prime_implicants[frozen_coords] = term_vars
                                      else:
                                           print(f"Error getting vars for PI at {coords}, skipping.")
                                 # Mark these coordinates as potentially covered
                                 processed_coords.update(coords)

        # Final check: ensure all original target coords were covered by some PI attempt
        if target_coords and not prime_implicants:
             # Handle single cell case if necessary (size 1x1 implicants)
             for coord in target_coords:
                  frozen_coord = frozenset([coord])
                  if frozen_coord not in prime_implicants:
                       term_vars = self._get_region_variables(frozen_coord)
                       if term_vars is not None:
                           prime_implicants[frozen_coord] = term_vars

        # Further refinement: Remove non-maximal PIs (if any slipped through)
        # A PI is non-maximal if its coords are a proper subset of another PI's coords
        final_pis = {}
        pi_coords_list = list(prime_implicants.keys())
        for i, coords1 in enumerate(pi_coords_list):
            is_maximal = True
            for j, coords2 in enumerate(pi_coords_list):
                if i == j: continue
                if coords1.issubset(coords2) and coords1 != coords2:
                    is_maximal = False
                    break
            if is_maximal:
                final_pis[coords1] = prime_implicants[coords1]


        print(f"\nНайденные простые импликанты ({'Макстермы' if self.is_conjunctive else 'Минтермы'}):")
        for coords, variables in final_pis.items():
            # Sort variables for display
            sorted_vars_for_print = sorted(variables, key=lambda x: x[0])
            var_strings = []
            for name, state in sorted_vars_for_print:
                # KNF term: state=True means ¬name, state=False means name
                # DNF term: state=True means name, state=False means ¬name
                if self.is_conjunctive:
                     var_strings.append(f"¬{name}" if state else f"{name}")
                else:
                     var_strings.append(f"{name}" if state else f"¬{name}")

            op = " ∨ " if self.is_conjunctive else " ∧ "
            term_str = op.join(var_strings) if len(var_strings)>1 else (var_strings[0] if var_strings else "")

            # Handle potential empty term_str if variables couldn't be determined
            if term_str:
                print(f"- Покрытие {coords}: ({term_str})")
            else:
                 print(f"- Покрытие {coords}: [Ошибка определения переменных]")


        return final_pis # Return map { frozenset(coords): list(vars) }


    def select_minimal_cover(self, prime_implicants):
        """Selects a minimal set of prime implicants to cover all target cells."""
        if not prime_implicants:
            return [] # No PIs means no cover needed or possible

        target_coords = set()
        for r in range(self.rows):
            for c in range(self.cols):
                if self._map_data[r][c] == self.target_value:
                    target_coords.add((r, c))

        if not target_coords:
            print("Нет целевых ячеек для покрытия.")
            return [] # No zeros/ones to cover

        # --- Simple Essential Prime Implicant + Greedy Covering ---
        # 1. Identify Essential PIs
        essential_pis_coords = set()
        covered_by_essentials = set()
        coords_coverage_count = {coord: 0 for coord in target_coords}
        pi_map = {frozenset(coords): term for coords, term in prime_implicants.items()}

        # Map each target coordinate to the PIs that cover it
        coord_to_pis = {coord: [] for coord in target_coords}
        for pi_coords in pi_map:
            for coord in pi_coords:
                if coord in coord_to_pis:
                    coord_to_pis[coord].append(pi_coords)
                    coords_coverage_count[coord]+=1


        # Find coordinates covered by only one PI (these PIs are essential)
        for coord, covering_pis in coord_to_pis.items():
             if len(covering_pis) == 1:
                 essential_pi = covering_pis[0]
                 if essential_pi not in essential_pis_coords:
                      print(f"  - Импликант {essential_pi} существенный (покрывает {coord})")
                      essential_pis_coords.add(essential_pi)
                      covered_by_essentials.update(essential_pi) # Add all coords covered by this essential PI


        # 2. Greedy selection for remaining uncovered coordinates
        selected_cover_coords = set(essential_pis_coords) # Start with essential ones
        remaining_coords = target_coords - covered_by_essentials

        # Filter PIs to only those covering remaining coordinates
        relevant_pis = {}
        for pi_c, pi_v in prime_implicants.items():
            if pi_c not in essential_pis_coords: # Don't reconsider essentials
                 # Check if this PI covers any *remaining* coordinate
                 if any(coord in remaining_coords for coord in pi_c):
                      relevant_pis[pi_c] = pi_v

        print(f"\nОставшиеся для покрытия ячейки: {remaining_coords}")
        print(f"Релевантные (несущественные) импликанты: {list(relevant_pis.keys())}")

        while remaining_coords:
            # Find the PI that covers the most *remaining* coordinates
            best_pi_coords = None
            max_covered_count = -1

            sorted_relevant_pis = sorted(relevant_pis.keys(), key=lambda k: len(k), reverse=True) # Prioritize larger PIs

            for pi_c in sorted_relevant_pis:
                 # Intersection calculates how many remaining coords this PI covers
                 num_covered = len(pi_c.intersection(remaining_coords))
                 if num_covered > max_covered_count:
                      max_covered_count = num_covered
                      best_pi_coords = pi_c

            if best_pi_coords is not None:
                 print(f"  - Выбираем импликант {best_pi_coords} (покрывает {max_covered_count} оставшихся)")
                 selected_cover_coords.add(best_pi_coords)
                 covered_now = best_pi_coords.intersection(remaining_coords)
                 remaining_coords -= covered_now # Update remaining coords
                 # Remove the chosen PI from consideration for the next iteration
                 if best_pi_coords in relevant_pis:
                     del relevant_pis[best_pi_coords]
                 # Remove other PIs that only covered cells now covered by best_pi_coords
                 pis_to_remove = []
                 for pi_check_coords in relevant_pis:
                      if pi_check_coords.intersection(remaining_coords) == set():
                           pis_to_remove.append(pi_check_coords)
                 for pi_rem in pis_to_remove:
                      if pi_rem in relevant_pis:
                           del relevant_pis[pi_rem]


            else:
                 # Should not happen if PIs were generated correctly for all target coords
                 print(f"Ошибка: не удалось найти импликант для покрытия оставшихся ячеек: {remaining_coords}")
                 break # Avoid infinite loop

        # 3. Return the variables associated with the selected PIs
        final_terms = [prime_implicants[pi_c] for pi_c in selected_cover_coords if pi_c in prime_implicants]
        print("\nИтоговое покрытие выбрано:")
        for pi_c in selected_cover_coords:
             if pi_c in prime_implicants:
                 print(f"- {pi_c} -> {prime_implicants[pi_c]}")


        return final_terms


    def compute_minimized_form(self):
        if not self.valid_processing:
            print("Ошибка: недопустимая обработка.")
            return BooleanExpressionMinimizer(self.is_conjunctive) # Return empty

        # 1. Find all Prime Implicants
        prime_implicants = self.find_prime_implicants()

        # Handle edge case: No implicants found (function might be always 0 for DNF, always 1 for KNF)
        if not prime_implicants:
             print("Не найдено простых импликантов.")
             # If target is 1 (DNF) and no PIs, result is '0'
             # If target is 0 (KNF) and no PIs, result is '1'
             result = BooleanExpressionMinimizer(self.is_conjunctive)
             # The __str__ method of BooleanExpressionMinimizer handles this logic
             return result


        # 2. Select Minimal Cover
        minimal_cover_terms = self.select_minimal_cover(prime_implicants)

        # 3. Build the final expression
        result = BooleanExpressionMinimizer(self.is_conjunctive)
        for term_vars in minimal_cover_terms:
            # Correct variable state representation for KNF/DNF handled in BooleanExpressionMinimizer
             if term_vars is not None and term_vars != []: # Ensure valid terms are added
                result.append_component(term_vars) # term_vars is list of (name, state) tuples


        return result


# --- Main Execution ---
def main():
    # Test cases
    # Example 1: (a & b) | c -> Should have DNF: (a&b) | c; KNF should be complex
    # Example 2: a ~ b -> DNF: (a&b)|(!a&!b); KNF: (!a|b)&(a|!b)
    # Example 3: 5 variables - (a&b&c&d) | e (as in your code)

    #test_expression = "a↔b" # Equivalence
    #test_expression = "(a∧b)∨c" # Simple OR/AND
    test_expression = "a∧b∧c∧d∨e" # Your 5-var example
    #test_expression = "a∨b∨c∨d∨e" # All OR
    #test_expression = "a∧b∧c∧d∧e" # All AND
    # test_expression = "(a&!b)|(c&d)" # 4 variable example
    # test_expression = "a^(b^c)" # XOR 3 vars

    print(f"\n--- Обработка выражения: {test_expression} ---")
    formula = Formula(test_expression)
    truth_table, headers, _ = formula.create_table_of_truth() # Ignore results column name

    if not headers:
         print("Ошибка при парсинге формулы или генерации заголовков.")
         return

    print("\nТаблица истинности:")
    print(" ".join(headers))
    for row in truth_table:
        print(" ".join(map(str, row)))

    variables = headers[:-1] # Exclude the result column header

    print("\n--- Минимизация ДНФ ---")
    dnf_processor = KarnaughMapProcessor(
        variables=variables,
        truth_table_rows=truth_table,
        is_conjunctive_form=False # DNF means target value is 1
    )
    if dnf_processor.valid_processing:
        minimized_dnf = dnf_processor.compute_minimized_form()
        print("\nУпрощенная ДНФ:", minimized_dnf)
    else:
        print("Не удалось обработать ДНФ.")


    print("\n--- Минимизация КНФ ---")
    cnf_processor = KarnaughMapProcessor(
        variables=variables,
        truth_table_rows=truth_table,
        is_conjunctive_form=True # KNF means target value is 0
    )
    if cnf_processor.valid_processing:
        minimized_cnf = cnf_processor.compute_minimized_form()
        print("\nУпрощенная КНФ:", minimized_cnf)
    else:
         print("Не удалось обработать КНФ.")


if __name__ == "__main__":
    # Add the Formula class definition here if it's not imported
    # Ensure the Formula class correctly handles operators like ∧, ∨, ¬, →, ↔
    # Make sure formula.create_table_of_truth() returns rows where the last element is the function result (0 or 1)
    # Need formula.py from the original context
    try:
       # This requires your formula.py to be available
       from formula import Formula
       main()
    except ImportError:
       print("="*40)
       print(" ОШИБКА: Не удалось импортировать класс 'Formula' ")
       print(" Пожалуйста, убедитесь, что файл 'formula.py' находится ")
       print(" в той же директории или доступен для импорта. ")
       print("="*40)