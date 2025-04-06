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
        return (item1 == f'¬{item2}') or (item2 == f'¬{item1}')

    def _combine_clauses(self, set1, set2):
        return set1.intersection(set2)

    def simplify(self):
        current_clauses = self.disjunctive_clauses.copy()
        iteration = 0
        changed = True

        while changed:
            changed = False
            print(f"\nИтерация {iteration}: Текущие дизъюнкты: {current_clauses}")
            new_clauses = []
            used = set()

            for i in range(len(current_clauses)):
                for j in range(i + 1, len(current_clauses)):
                    clause1 = current_clauses[i]
                    clause2 = current_clauses[j]
                    if self._check_merge_possibility(clause1, clause2):
                        merged = self._combine_clauses(clause1, clause2)
                        if merged not in new_clauses:
                            new_clauses.append(merged)
                            used.add(i)
                            used.add(j)
                            changed = True

            for idx, clause in enumerate(current_clauses):
                if idx not in used and clause not in new_clauses:
                    new_clauses.append(clause)

            if changed:
                current_clauses = new_clauses
                iteration += 1
            else:
                break

        self.disjunctive_clauses = current_clauses
        return self._format_output(current_clauses)

    def _format_output(self, clause_collection):
        if not clause_collection:
            return "True"
        output = []
        for clause in clause_collection:
            if not clause:
                return "False"
            output.append(f"({' ∨ '.join(sorted(clause))})")
        return " ∧ ".join(output)

def main():
    input_expression = '!(a→(b∧!c))'
    formula_processor = Formula(input_expression)
    cnf_expression = formula_processor.get_cnf_for_minimization()
    print("\nИсходная СКНФ:", cnf_expression)

    reducer = ConjunctiveNormalFormReducer(cnf_expression)
    minimized_result = reducer.simplify()
    print("\nМинимизированная СКНФ:", minimized_result)

if __name__ == "__main__":
    main()