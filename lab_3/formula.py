import re
from itertools import product


class Formula:
    MAX_BITS = 7

    def __init__(self, formula):
        self.operators = {
            "!": {"priority": 4, "unary": True},
            "&": {"priority": 3, "unary": False},
            "|": {"priority": 2, "unary": False},
            "->": {"priority": 1, "unary": False},
            "~": {"priority": 0, "unary": False},
        }
        self.expression = formula.replace('∨', '|').replace(
            '∧', '&').replace('→', '->').replace('↔', '~')

    @classmethod
    def get_positive_binary_number(cls, decimal_number):
        if decimal_number < 0:
            raise ValueError("Только для положительных чисел")
        binary = ""
        num = decimal_number
        while num > 0:
            binary = str(num % 2) + binary
            num = num // 2
        binary = binary.zfill(cls.MAX_BITS)
        return '0' + binary

    @staticmethod
    def binary_to_decimal_number(binary):
        decimal = 0
        length = len(binary)
        for i in range(length):
            if binary[i] == '1':
                decimal += 2 ** (length - i - 1)
        return decimal

    @classmethod
    def convert_to_decimal(cls, binary_number):
        if binary_number[0] == '1':
            inverted = ''.join(
                '1' if b == '0' else '0' for b in binary_number[1:])
            return -cls.binary_to_decimal_number(inverted) - 1
        return cls.binary_to_decimal_number(binary_number)

    def get_variables(self):
        return sorted(set(re.findall(r'\b[a-zA-Z]+\b', self.expression)))

    def combinations(self):
        variables = self.get_variables()
        for combination in product([False, True], repeat=len(variables)):
            yield dict(zip(variables, combination))

    def tokenize(self):
        tokens = []
        i = 0
        while i < len(self.expression):
            if self.expression[i] == '-' and i + 1 < len(self.expression) and self.expression[i + 1] == '>':
                tokens.append('->')
                i += 2
            elif self.expression[i] in "()!&|~":
                tokens.append(self.expression[i])
                i += 1
            elif self.expression[i].isalpha():
                var = []
                while i < len(self.expression) and (self.expression[i].isalpha() or self.expression[i].isdigit()):
                    var.append(self.expression[i])
                    i += 1
                tokens.append(''.join(var))
            else:
                i += 1
        return tokens

    def to_postfix(self, tokens):
        output = []
        stack = []
        for token in tokens:
            if token == '(':
                stack.append(token)
            elif token == ')':
                while stack[-1] != '(':
                    output.append(stack.pop())
                stack.pop()
            elif token in self.operators:
                while stack and stack[-1] != '(' and self.operators[token]["priority"] <= self.operators.get(stack[-1], {"priority": -1})["priority"]:
                    output.append(stack.pop())
                stack.append(token)
            else:
                output.append(token)
        while stack:
            output.append(stack.pop())
        return output

    def evaluate_postfix(self, postfix, variables):
        stack = []
        for token in postfix:
            if token in self.operators:
                op = self.operators[token]
                if op["unary"]:
                    a = stack.pop()
                    result = not a
                else:
                    b = stack.pop()
                    a = stack.pop()
                    if token == '&':
                        result = a and b
                    elif token == '|':
                        result = a or b
                    elif token == '->':
                        result = (not a) or b
                    elif token == '~':
                        result = a == b
                stack.append(result)
            else:
                stack.append(variables[token])
        return stack[0]

    def evaluate_of_expr(self, **variables):
        tokens = self.tokenize()
        missing = set(t for t in tokens if t.isalpha()) - set(variables.keys())
        if missing:
            raise ValueError(f"Не указаны переменные: {missing}")
        postfix = self.to_postfix(tokens)
        return self.evaluate_postfix(postfix, variables)

    def create_table_of_truth(self):
        variables = self.get_variables()
        combinations = list(self.combinations())
        result_of_expr = []
        table = []
        for combo in combinations:
            result = self.evaluate_of_expr(**combo)
            result_of_expr.append(result)
            row = [combo[var] for var in variables] + [result]
            table.append(row)
        return table, variables + ["Result"], result_of_expr

    def to_cnf(self):
        table, headers, result_of_expr = self.create_table_of_truth()
        variables = headers[:-1]
        cnf = []
        for row in table:
            if not row[-1]:
                clause = []
                for i, var in enumerate(variables):
                    clause.append(f'¬{var}' if row[i] else var)
                cnf.append(f'({" ∨ ".join(clause)})')
        return " ∧ ".join(cnf) if cnf else "True"

    def to_dnf(self):
        table, headers, result_of_expr = self.create_table_of_truth()
        variables = headers[:-1]
        dnf = []
        for row in table:
            if row[-1]:
                clause = []
                for i, var in enumerate(variables):
                    clause.append(var if row[i] else f'¬{var}')
                dnf.append(f'({" ∧ ".join(clause)})')
        return " ∨ ".join(dnf) if dnf else "False"

    def get_number_forms(self):
        table, headers, result_of_expr = self.create_table_of_truth()
        variables = headers[:-1]
        disjunction = []
        conjunction = []
        for row in table:
            binary = ''.join(str(int(v)) for v in row[:-1])
            decimal = self.binary_to_decimal_number(binary)
            if row[-1]:
                disjunction.append(decimal)
            else:
                conjunction.append(decimal)
        return (f"({','.join(map(str, disjunction))}) ∨\n"
                f"({','.join(map(str, conjunction))}) ∧")

    def get_cnf_for_minimization(self):
        cnf = self.to_cnf()
        return cnf

    def get_dnf_for_minimization(self):
        dnf = self.to_dnf()
        return dnf


def main():
    expr = ('!a→(!(b∨c))c'
            ''
            '')
    formula = Formula(expr)
    table, headers, result_of_expr = formula.create_table_of_truth()
    print(f"Логическое выражение: {expr}")
    print("Таблица истинности:")
    print(" | ".join(headers))
    for row in table:
        print(" | ".join(str(int(x)) for x in row))
    print("\nСовершенная ДНФ (СДНФ):", formula.to_dnf())
    print("Совершенная КНФ (СКНФ):", formula.to_cnf())
    print("\nЧисловые формы:\n", formula.get_number_forms())
    result_string = "".join(str(int(r)) for r in result_of_expr)
    print("\nИндексная форма: ", result_string, "-",
          formula.binary_to_decimal_number(result_string))


if __name__ == '__main__':
    main()
