from itertools import combinations
from formula import Formula


class PerfectDNF_Optimizer:
    def __init__(self, input_expression):
        self.initial_expression = input_expression
        self.conjunctive_terms = self._parse_expression(input_expression)
        self.essential_primes = []
        self.optimized_result = []

    @staticmethod
    def _parse_expression(logical_str):
        if logical_str == "False" or not logical_str.strip():
            return []
        components = logical_str.split(" ∨ ")
        parsed_components = []
        for component in components:
            component = component.strip("()")
            variables = component.split(" ∧ ")
            parsed_components.append(frozenset(variables))
        return parsed_components

    @staticmethod
    def _check_merge_condition(term_A, term_B):
        difference = term_A.symmetric_difference(term_B)
        if len(difference) != 2:
            return False
        var_X, var_Y = difference
        return var_X == f'¬{var_Y}' or var_Y == f'¬{var_X}'

    def _combine_implicants(self, term_A, term_B):
        return term_A.intersection(term_B)

    def _extract_prime_implicants(self):
        current_terms = self.conjunctive_terms.copy()
        self.essential_primes = []

        while True:
            new_terms = []
            processed_indices = set()

            for i in range(len(current_terms)):
                for j in range(i + 1, len(current_terms)):
                    term_A = current_terms[i]
                    term_B = current_terms[j]
                    if self._check_merge_condition(term_A, term_B):
                        combined = self._combine_implicants(term_A, term_B)
                        new_terms.append(combined)
                        processed_indices.update((i, j))

            for idx, term in enumerate(current_terms):
                if idx not in processed_indices:
                    if all(not term.issuperset(prime) for prime in self.essential_primes):
                        self.essential_primes.append(term)

            if not new_terms:
                break

            current_terms = new_terms

        if not self.essential_primes:
            self.essential_primes = self.conjunctive_terms.copy()

        self.essential_primes = list({frozenset(term) for term in self.essential_primes})

    def _construct_coverage_matrix(self):
        coverage_map = {}
        for prime in self.essential_primes:
            coverage_map[prime] = []
            for term in self.conjunctive_terms:
                if prime.issubset(term):
                    coverage_map[prime].append(term)
        return {k: v for k, v in coverage_map.items() if v}

    def _eliminate_redundant_primes(self):
        essential_terms = []
        for i in range(len(self.optimized_result)):
            current_prime = self.optimized_result[i]
            temp_result = self.optimized_result[:i] + self.optimized_result[i + 1:]
            if all(any(current_prime.issubset(t) for t in temp_result) for term in self.conjunctive_terms):
                continue
            essential_terms.append(current_prime)
        self.optimized_result = essential_terms

    def _select_optimal_coverage(self):
        coverage_data = self._construct_coverage_matrix()
        if not coverage_data:
            raise ValueError("Матрица покрытия пуста")

        covered_terms = set()
        self.optimized_result = []

        while len(covered_terms) < len(self.conjunctive_terms):
            best_prime = None
            max_coverage = 0

            for prime, covered in coverage_data.items():
                current_count = len([t for t in covered if t not in covered_terms])
                if current_count > max_coverage:
                    max_coverage = current_count
                    best_prime = prime

            if best_prime is None:
                self.optimized_result = self.conjunctive_terms.copy()
                break

            self.optimized_result.append(best_prime)
            covered_terms.update(coverage_data[best_prime])
            del coverage_data[best_prime]

        self._eliminate_redundant_primes()

    def optimize(self):
        self._extract_prime_implicants()
        self._select_optimal_coverage()
        return self._format_output(self.optimized_result)

    def _format_output(self, prime_terms):
        if not prime_terms:
            return "False"
        simplified = []
        for term in prime_terms:
            sorted_vars = sorted(term, key=lambda x: (x.startswith('¬'), x))
            simplified.append(" ∧ ".join(sorted_vars))
        return " ∨ ".join(f'({t})' for t in simplified) if len(simplified) > 1 else simplified[0]

    def display_coverage_matrix(self):
        coverage_data = self._construct_coverage_matrix()
        if not coverage_data:
            return

        headers = ["Простые импликанты \\ Термы"] + [f'({" ∧ ".join(sorted(t))})' for t in self.conjunctive_terms]
        column_width = max(len(h) for h in headers) + 2
        separator = "+".join(['-' * column_width] * len(headers))

        print("\nМатрица покрытия:")
        print(separator)
        print("|".join(h.center(column_width) for h in headers))
        print(separator)

        for prime, covered in coverage_data.items():
            row = [" ∧ ".join(sorted(prime)).ljust(column_width)]
            for term in self.conjunctive_terms:
                marker = "X" if term in covered else ""
                row.append(marker.center(column_width))
            print("|".join(row))
            print(separator)


def main():
    expression = "!a→(!(b∨c)∨d)"
    bool_expr = Formula(expression)
    dnf_form = bool_expr.to_dnf()
    optimizer = PerfectDNF_Optimizer(dnf_form)
    optimized_form = optimizer.optimize()

    print("Исходная СДНФ:", dnf_form)
    print("Оптимизированная форма:", optimized_form)
    optimizer.display_coverage_matrix()


if __name__ == "__main__":
    main()