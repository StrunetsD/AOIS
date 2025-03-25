from formula import Formula


class ConjunctiveNormalFormReducer:
    def __init__(self, initial_expression):
        self.input_expression = initial_expression
        self.disjunctive_clauses = self._process_input(initial_expression)
        self.reduction_steps = []

    @staticmethod
    def _process_input(logical_expression):
        if logical_expression == "True":
            return []
        clause_list = logical_expression.split(" ∧ ")
        processed_clauses = []
        for clause in clause_list:
            clause = clause.strip("()")
            variables = clause.split(" ∨ ")
            processed_clauses.append(set(variables))
        return processed_clauses

    @staticmethod
    def _check_merge_possibility(set1, set2):
        difference = set1.symmetric_difference(set2)
        if len(difference) != 2:
            return False
        item1, item2 = difference
        if item1 == f'¬{item2}' or item2 == f'¬{item1}':
            return True
        return False

    def _combine_clauses(self, set1, set2):
        combined = set1.intersection(set2)
        return combined

    def simplify(self):
        current_clauses = self.disjunctive_clauses.copy()
        iteration = 0

        while True:
            new_clause_set = []
            processed_indices = set()
            self.reduction_steps.append(
                {"iteration": iteration, "clauses": current_clauses.copy(), "combinations": []})

            for i in range(len(current_clauses)):
                for j in range(i + 1, len(current_clauses)):
                    first_clause = current_clauses[i]
                    second_clause = current_clauses[j]
                    if self._check_merge_possibility(first_clause, second_clause):
                        combined_clause = self._combine_clauses(first_clause, second_clause)
                        new_clause_set.append(combined_clause)
                        processed_indices.update((i, j))
                        self.reduction_steps[-1]["combinations"].append(
                            (first_clause, second_clause, combined_clause))

            for idx, clause in enumerate(current_clauses):
                if idx not in processed_indices:
                    new_clause_set.append(clause)

            if len(new_clause_set) == len(current_clauses):
                break

            current_clauses = []
            unique_clauses = []
            for clause in new_clause_set:
                if clause not in unique_clauses:
                    current_clauses.append(clause)
                    unique_clauses.append(clause)
            iteration += 1

        self.optimized_form = current_clauses
        return self._format_output(current_clauses)

    def _format_output(self, clause_collection):
        if not clause_collection:
            return "True"
        output_expression = []
        for clause in clause_collection:
            if not clause:
                return "False"
            output_expression.append(f'({" ∨ ".join(sorted(clause))})')
        return " ∧ ".join(output_expression)

    def display_reduction_process(self):
        print("Процесс минимизации:")
        for step in self.reduction_steps:
            print(f"\nИтерация {step['iteration']}:")
            print("Текущие дизъюнкты:")
            for clause in step['clauses']:
                print(f"  ({' ∨ '.join(sorted(clause))})")
            if step['combinations']:
                print("Объединенные пары:")
                for c1, c2, merged in step['combinations']:
                    print(
                        f"  ({' ∨ '.join(sorted(c1))})  и  ({' ∨ '.join(sorted(c2))}) → ({' ∨ '.join(sorted(merged))})")


def main():
    input_expression = ('!a→(!(b∨c)∨d)')
    formula_processor = Formula(input_expression)
    cnf_expression = formula_processor.get_cnf_for_minimization()
    print("\nИсходная СКНФ:", cnf_expression)

    reducer = ConjunctiveNormalFormReducer(cnf_expression)
    minimized_result = reducer.simplify()
    print("\nМинимизированная СКНФ:", minimized_result)


if __name__ == "__main__":
    main()