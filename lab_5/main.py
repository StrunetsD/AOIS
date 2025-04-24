from karnaugh_template import KarnaughMapProcessor

digital_device_truth_table = [
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1],
    [0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1],
    [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0],
    [0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
    [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
]


def print_digital_device_truth_table():
    print('Таблица истинности цифрового устройства')
    arguments = ['q3\'', 'q2\'', 'q1\'', 'V  ', 'q3 ', 'q2 ', 'q1 ', 'h3 ', 'h2 ', 'h1 ']
    for i in range(len(digital_device_truth_table)):
        print_string = arguments[i] + ' |'
        for j in range(len(digital_device_truth_table[i])):
            print_string += f' {digital_device_truth_table[i][j]}'
        print(print_string)


def _minimize_h(h_index: int, variables: list) -> str:
    # Формируем строки таблицы истинности для 4 переменных (q3', q2', q1', V)
    truth_rows = []
    for col in range(16):
        q3 = (col >> 3) & 1
        q2 = (col >> 2) & 1
        q1 = (col >> 1) & 1
        v = col & 1
        result = digital_device_truth_table[h_index][col]
        truth_rows.append([q3, q2, q1, v, result])

    processor = KarnaughMapProcessor(
        variables=variables,
        truth_table_rows=truth_rows,
        is_conjunctive_form=False
    )
    minimized_expr = processor.compute_minimized_form()
    return str(minimized_expr)


def print_h3_minimization():
    print('Минимизация h3:')
    variables = ["q3'", "q2'", "q1'", "V"]
    minimized_h3 = _minimize_h(7, variables)
    print(minimized_h3)


def print_h2_minimization():
    print('Минимизация h2:')
    variables = ["q3'", "q2'", "q1'", "V"]
    minimized_h2 = _minimize_h(8, variables)
    print(minimized_h2)


def print_h1_minimization():
    print('Минимизация h1:')
    variables = ["q3'", "q2'", "q1'", "V"]
    minimized_h1 = _minimize_h(9, variables)
    print(minimized_h1)


def main():
    print_digital_device_truth_table()
    print_h3_minimization()
    print_h2_minimization()
    print_h1_minimization()


if __name__ == "__main__":
    main()