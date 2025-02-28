import re
from itertools import product


class Formula:
    MAX_BITS = 7

    def __init__(self, formula):
        self.operators = {
            "!": {"priority": 4, "unary": True},
            "&": {"priority": 3, "unary": False},
            "|": {"priority": 2, "unary": False},
            "->":{"priority": 1, "unary": False},
            "~": {"priority": 0, "unary": False},
        }
        self.expression = formula.replace('∨', '|').replace('∧', '&').replace('→', '->').replace('↔', '~')

    @classmethod
    def get_positive_binary_number(cls, decimal_number) :
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
            inverted = ''.join('1' if b == '0' else '0' for b in binary_number[1:])
            return -cls.binary_to_decimal_number(inverted) - 1
        return cls.binary_to_decimal_number(binary_number)

    def get_variables(self):
        return sorted(set(re.findall(r'[a-zA-Z]', self.expression)))

    def combinations(self):
        variables = self.get_variables()
        for combination in product([False, True], repeat=len(variables)):
            yield dict(zip(variables, combination))

    def tokenize(self):
        tokens = []
        i = 0
        while i < len(self.expression):
            if self.expression[i] in "()!&|~":
                if self.expression[i] == "-" and i + 1 < len(self.expression) and self.expression[i + 1] == ">":
                    tokens.append("->")
                    i += 2
                    continue
                tokens.append(self.expression[i])
                i += 1
            elif self.expression[i].isalpha():
                var = []
                while i < len(self.expression) and self.expression[i].isalpha():
                    var.append(self.expression[i])
                    i += 1
                tokens.append("".join(var))
            else:
                i += 1
        return tokens

    def to_postfix(self, tokens):
        output = []
        stack = []
        for token in tokens:
            if token == "(":
                stack.append(token)
            elif token == ")":
                while stack[-1] != "(":
                    output.append(stack.pop())
                stack.pop()
            elif token in self.operators:
                while stack and stack[-1] != "(" and self.operators[token]["priority"] <= \
                        self.operators.get(stack[-1], {"priority": -1})["priority"]:
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
                if self.operators[token]["unary"]:
                    operand = stack.pop()
                    result = not operand
                else:
                    b = stack.pop()
                    a = stack.pop() if token != "->" else stack.pop()
                    if token == "&":
                        result = a and b
                    elif token == "|":
                        result = a or b
                    elif token == "->":
                        result = (not a) or b
                    elif token == "~":
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
            row = list(combo.values()) + [result]
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
                    if row[i]:
                        clause.append(f'¬{var}')
                    else:
                        clause.append(var)
                cnf.append(f"({' ∨ '.join(clause)})")

        return " ∧ ".join(cnf) if cnf else "True"

    def to_dnf(self):
        table, headers, result_of_expr = self.create_table_of_truth()
        variables = headers[:-1]
        dnf = []

        for row in table:
            if row[-1]:
                clause = []
                for i, var in enumerate(variables):
                    if row[i]:
                        clause.append(var)
                    else:
                        clause.append(f'¬{var}')
                dnf.append(f"({' ∧ '.join(clause)})")

        return " ∨ ".join(dnf) if dnf else "False"

    def get_number_forms(self):
        table, headers, result_of_expr = self.create_table_of_truth()
        variables = headers[:-1]
        number_form_of_disjunction = []
        number_form_of_conjunction = []
        for row in table:
            if row[-1]:
                binary = ''.join(str(int(v)) for v in row[:-1])
                number_form_of_disjunction.append(self.binary_to_decimal_number(binary))
            else:
                binary = ''.join(str(int(v)) for v in row[:-1])
                number_form_of_conjunction.append(self.binary_to_decimal_number(binary))
        return  "(" +  ",".join(map(str,number_form_of_disjunction))+ ")" + " v" \
               "\n""(" + ",".join(map(str,  number_form_of_conjunction)) + ")" + " ∧"


def main():
    expr = '(a∨b)∧!c'
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
    result_string = "".join(map(str,(map(int, result_of_expr))))
    print("\nИндексная форма: ",result_string+" -",formula.binary_to_decimal_number(result_string))


if __name__ == '__main__':
    main()

# (a∨b∨c) ∧ (a∨b∨¬c) ∧ (a∨¬b∨¬c) ∧ (¬a∨b∨¬c) ∧ (¬a∨¬b∨¬c) - (СKНФ)
# ¬ab¬c ∨ a¬b¬c ∨ ab¬c - (СДНФ)