from formula import *

class DNFMinimizer:
    def __init__(self, dnf_expression):
        self.original_dnf = dnf_expression
        self.terms = self.parse_expression(dnf_expression)
        self.stages = []

    @staticmethod
    def parse_expression(dnf):
        if dnf == "False":
            return []
        if dnf == "True":
            return [set()]
        terms = dnf.split(" ∨ ")
        parsed_terms = []
        for term in terms:
            term = term.strip("()")
            literals = term.split(" ∧ ")
            parsed_terms.append(set(literals))
        return parsed_terms

    @staticmethod
    def can_combine(term1, term2):
        diff = term1.symmetric_difference(term2)
        if len(diff) != 2:
            return False
        lit1, lit2 = diff
        return lit1 == f'¬{lit2}' or lit2 == f'¬{lit1}'

    @staticmethod
    def combine_terms(term1, term2):
        merged = term1.intersection(term2)
        return merged

    @staticmethod
    def remove_redundant_terms( terms):
        terms = [t.copy() for t in terms]
        unique = []
        for t1 in terms:
            absorbed = False
            for t2 in terms:
                if t1 != t2 and t2.issubset(t1):
                    absorbed = True
                    break
            if not absorbed and t1 not in unique:
                unique.append(t1)
        return unique

    def minimize_expression(self):
        current_terms = self.terms.copy()
        stage = 0
        changed = True

        while changed:
            changed = False
            new_terms = []
            merged_pairs = set()

            for i in range(len(current_terms)):
                for j in range(i + 1, len(current_terms)):
                    t1 = current_terms[i]
                    t2 = current_terms[j]
                    if self.can_combine(t1, t2):
                        merged = self.combine_terms(t1, t2)
                        new_terms.append(merged)
                        merged_pairs.update((i, j))
                        changed = True

            for idx, term in enumerate(current_terms):
                if idx not in merged_pairs:
                    new_terms.append(term.copy())

            current_terms = []
            seen = []
            for term in new_terms:
                if term not in seen:
                    current_terms.append(term)
                    seen.append(term)

            prev_len = len(current_terms)
            current_terms = self.remove_redundant_terms(current_terms)
            if len(current_terms) != prev_len:
                changed = True

            self.stages.append({
                "stage": stage,
                "terms": [t.copy() for t in current_terms],
                "merged": new_terms.copy()
            })

            stage += 1

        self.minimized_dnf = current_terms
        return self.format_expression(current_terms)

    @staticmethod
    def format_expression( terms):
        if not terms:
            return "False"
        if any(len(term) == 0 for term in terms):
            return "True"
        dnf = []
        for term in terms:
            if not term:
                continue
            dnf.append(f'({" ∧ ".join(sorted(term))})')
        return " ∨ ".join(dnf) if dnf else "False"

    def print_stages(self):
        print("Этапы склеивания:")
        for stage in self.stages:
            print(f"\nЭтап {stage['stage']}:")
            print("Конъюнкты:")
            for term in stage['terms']:
                print(f"  ({' ∧ '.join(sorted(term))})" if term else "  True")
            if stage['merged']:
                print("Склеенные пары:")
                for t1, t2, merged in stage['merged']:
                    t1_str = f"({' ∧ '.join(sorted(t1))})" if t1 else "True"
                    t2_str = f"({' ∧ '.join(sorted(t2))})" if t2 else "True"
                    merged_str = f"({' ∧ '.join(sorted(merged))})" if merged else "True"
                    print(f"  {t1_str}  и  {t2_str} → {merged_str}")

def main():
    expr = ('!a→(!(b∨c)∨d)')
    formula = Formula(expr)
    print(f"Логическое выражение: {expr}")
    dnf = formula.get_dnf_for_minimization()
    print("\nИсходная ДНФ:", dnf)

    minimizer = DNFMinimizer(dnf)
    minimized_dnf = minimizer.minimize_expression()
    print("\nМинимизированная ДНФ:", minimized_dnf)

if __name__ == "__main__":
    main()
