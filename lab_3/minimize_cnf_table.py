from formula import Formula

class KNF_Optimizer:
    def __init__(self, knf_input):
        self.initial_knf = knf_input
        self.disjunctive_terms = self._parse_knf(knf_input)
        self.core_terms = []
        self.optimized_form = []
        print(f"Исходная КНФ: {self.initial_knf}")
        print(f"Разобранные термы: {self.disjunctive_terms}")

    @staticmethod
    def _parse_knf(knf_str):
        if knf_str == "True" or not knf_str.strip():
            return []
        term_list = knf_str.split(" ∧ ")
        parsed_terms = []
        for term in term_list:
            term = term.strip("()")
            literals = term.split(" ∨ ")
            parsed_terms.append(frozenset(literals))
        return parsed_terms

    @staticmethod
    def _can_combine(term1, term2):
        difference = term1.symmetric_difference(term2)
        if len(difference) != 2:
            return False
        var1, var2 = difference
        can_combine = var1 == f'¬{var2}' or var2 == f'¬{var1}'
        print(f"Проверка комбинирования: {term1} и {term2} -> {can_combine}")
        return can_combine

    def _combine_terms(self, term1, term2):
        combined = term1.intersection(term2)
        print(f"Комбинирование: {term1} и {term2} -> {combined}")
        return combined

    def _filter_redundancies(self):
        essential_terms = []
        for i in range(len(self.optimized_form)):
            current_term = self.optimized_form[i]
            temp_form = self.optimized_form[:i] + self.optimized_form[i + 1:]
            if all(any(term.issubset(imp) for imp in temp_form) for term in self.disjunctive_terms):
                continue
            essential_terms.append(current_term)
        self.optimized_form = essential_terms
        print(f"Отфильтрованные термы: {self.optimized_form}")

    def _find_core_terms(self):
        current_terms = self.disjunctive_terms.copy()
        self.core_terms = []

        while True:
            new_terms = []
            used_indices = set()

            for i in range(len(current_terms)):
                for j in range(i + 1, len(current_terms)):
                    term1 = current_terms[i]
                    term2 = current_terms[j]
                    if self._can_combine(term1, term2):
                        combined = self._combine_terms(term1, term2)
                        new_terms.append(combined)
                        used_indices.update((i, j))

            if not new_terms:
                break

            current_terms = [term for idx, term in enumerate(current_terms) if idx not in used_indices]
            current_terms.extend(new_terms)

        self.core_terms = list({frozenset(term) for term in current_terms})
        print(f"Основные термы: {self.core_terms}")

    def _build_coverage_matrix(self):
        coverage_map = {}
        for imp in self.core_terms:
            coverage_map[imp] = []
            for term in self.disjunctive_terms:
                if imp.issubset(term):
                    coverage_map[imp].append(term)
        print(f"Матрица покрытия: {coverage_map}")
        return {k: v for k, v in coverage_map.items() if v}

    def _select_optimal_cover(self):
        coverage = self._build_coverage_matrix()
        if not coverage:
            raise ValueError("Матрица покрытия пуста")

        covered_terms = set()
        self.optimized_form = []

        while len(covered_terms) < len(self.disjunctive_terms):
            best_imp = None
            max_coverage = 0

            for imp, covers in coverage.items():
                current_cov = len([t for t in covers if t not in covered_terms])
                if current_cov > max_coverage:
                    max_coverage = current_cov
                    best_imp = imp

            if best_imp is None:
                self.optimized_form = self.disjunctive_terms.copy()
                break

            self.optimized_form.append(best_imp)
            covered_terms.update(coverage[best_imp])
            del coverage[best_imp]

            print(f"Выбранный импликант: {best_imp}, покрытые термы: {covered_terms}")

        self._filter_redundancies()

    def optimize(self):
        self._find_core_terms()
        self._select_optimal_cover()
        return self._format_result(self.optimized_form)

    def _format_result(self, terms):
        if not terms:
            if not self.disjunctive_terms:
                return "True"
            else:
                return "Ошибка оптимизации"
        simplified = []
        for term in terms:
            parts = sorted(term, key=lambda x: (x.startswith('¬'), x))
            simplified.append(" ∨ ".join(parts))
        result = " ∧ ".join(f'({t})' for t in simplified) if len(simplified) > 1 else simplified[0]
        print(f"Оптимизированная КНФ: {result}")
        return result

    def display_coverage_matrix(self):
        coverage = self._build_coverage_matrix()
        if not coverage:
            return

        headers = ["Импликанты \\ Термы"] + [f'({" ∨ ".join(sorted(t))})' for t in self.disjunctive_terms]
        col_width = max(len(h) for h in headers) + 2
        separator = "+".join(['-' * col_width] * len(headers))

        print("\nМатрица покрытия:")
        print(separator)
        print("|".join(h.center(col_width) for h in headers))
        print(separator)

        for imp, covers in coverage.items():
            row = [" ∨ ".join(sorted(imp)).ljust(col_width)]
            for term in self.disjunctive_terms:
                mark = "X" if term in covers else ""
                row.append(mark.center(col_width))
            print("|".join(row))
            print(separator)

def main():
    expr = "a∧b∧c∧d∨e"
    bool_expr = Formula(expr)
    knf = bool_expr.to_cnf()
    print("Исходная КНФ:", knf)

    optimizer = KNF_Optimizer(knf)
    optimized_knf = optimizer.optimize()
    print("Оптимизированная КНФ:", optimized_knf)

    optimizer.display_coverage_matrix()

if __name__ == "__main__":
    main()