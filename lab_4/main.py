from karnaugh_template import KarnaughMapProcessor, TruthTableData


ODS_3_truth_table = \
    [
        [0, 0, 0, 0, 1, 1, 1, 1],  # P_i perenos from previous
        [0, 0, 1, 1, 0, 0, 1, 1],  # A
        [0, 1, 0, 1, 0, 1, 0, 1],  # B
        [0, 1, 1, 0, 1, 0, 0, 1],  # S sum
        [0, 0, 0, 1, 0, 1, 1, 1],  # P_i+1 perenos to the next
    ]

D8421_plus_9_truth_table = [
    [0, 0, 0, 0, 1, 0, 0, 1],  # 0 +9=9  → 1001
    [0, 0, 0, 1, 1, 0, 1, 0],  # 1 +9=10 →1010
    [0, 0, 1, 0, 1, 0, 1, 1],  # 2 +9=11 →1011
    [0, 0, 1, 1, 1, 1, 0, 0],  # 3 +9=12 →1100
    [0, 1, 0, 0, 1, 1, 0, 1],  # 4 +9=13 →1101
    [0, 1, 0, 1, 1, 1, 1, 0],  # 5 +9=14 →1110
    [0, 1, 1, 0, 1, 1, 1, 1],  # 6 +9=15 →1111
    [0, 1, 1, 1, 0, 0, 0, 0],  # 7 +9=16 →0000 (mod16)
    [1, 0, 0, 0, 0, 0, 0, 1],  # 8 +9=17 →0001
    [1, 0, 0, 1, 0, 0, 1, 0],  # 9 +9=18 →0010
    [1, 0, 1, 0, 0, 0, 1, 1],  # 10 +9=19 →0011
    [1, 0, 1, 1, 0, 1, 0, 0],  # 11 +9=20 →0100
    [1, 1, 0, 0, 0, 1, 0, 1],  # 12 +9=21 →0101
    [1, 1, 0, 1, 0, 1, 1, 0],  # 13 +9=22 →0110
    [1, 1, 1, 0, 0, 1, 1, 1],  # 14 +9=23 →0111
    [1, 1, 1, 1, 1, 0, 0, 0],  # 15 +9=24 →1000 (mod16)
]

def print_ODS_3_truth_table():
    print('Таблица истинности ОДС3:')
    bits = ['P_i:  ', 'A:    ', 'B:    ', 'S_sum:', 'P_i+1:']
    for i in range(5):
        line_to_print = ''
        for j in range(len(ODS_3_truth_table[i])):
            line_to_print += str(ODS_3_truth_table[i][j]) + ' '
        print(bits[i] + line_to_print)
    print("=======================")

def print_D8421_plus9_truth_table():
    print('Таблица истинности Д8421+9:')
    print('A  B  C  D  A\' B\' C\' D\'')
    for row in D8421_plus_9_truth_table:
        print('  '.join(map(str, row[:4])) + '  ' + '  '.join(map(str, row[4:])))
    print("=======================")


def process_minimization(output_index, output_name):
    variables = ['A', 'B', 'C', 'D']
    table_content = []
    for row in D8421_plus_9_truth_table:
        input_vars = row[:4]
        output = row[4 + output_index]
        table_row = input_vars + [output]
        table_content.append(table_row)

    truth_table = TruthTableData(variables, table_content)
    processor_dnf = KarnaughMapProcessor(
        variables=variables,
        truth_table_rows=table_content,
        is_conjunctive_form=False
    )
    processor_cnf = KarnaughMapProcessor(
        variables=variables,
        truth_table_rows=table_content,
        is_conjunctive_form=True
    )
    print(f'\nМинимизация для {output_name}:')
    print('СДНФ:', processor_dnf.compute_minimized_form())
    print('СКНФ:', processor_cnf.compute_minimized_form())

print_D8421_plus9_truth_table()
print_ODS_3_truth_table()
process_minimization(0, "A'")
process_minimization(1, "B'")
process_minimization(2, "C'")
process_minimization(3, "D'")



