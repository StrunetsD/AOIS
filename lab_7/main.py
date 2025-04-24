class DiagonalMatrix:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.matrix = [[0 for _ in range(cols)] for _ in range(rows)]

    def get_column(self, col):
        return [row[col] for row in self.matrix]

    def set_word(self, word, start_row, col):
        for i, val in enumerate(word):
            self.matrix[(start_row + i) % self.rows][col] = val

    def operation(self, col1, col2, static_func):
        word1 = self.get_column(col1)
        word2 = self.get_column(col2)
        return [int(static_func(bool(word1[i]), bool(word2[i]))) for i in range(self.rows)]

    def F1_operation(self, col1, col2): # Логическое И
        return self.operation(col1, col2, self.F1)

    def F14_operation(self, col1, col2):  # Операция Шеффера (NAND)
        return self.operation(col1, col2, self.F14)

    def F3_operation(self, col1, col2): # Повторение первого аргумента
        return self.operation(col1, col2, self.F3)

    def F12_operation(self, col1, col2): # Отрицание первого аргумента
        return self.operation(col1, col2, self.F12)

    @staticmethod
    def F1(a, b):  # Логическое И
        return a and b

    @staticmethod
    def F14(a, b):  # Операция Шеффера (NAND)
        return not (a and b)

    @staticmethod
    def F3(a, b):  # Повторение первого аргумента
        return a

    @staticmethod
    def F12(a, b):  # Отрицание первого аргумента
        return not a

    def closest_word_find(self, input_word: str, is_greater: bool = True):
        if len(input_word) != self.rows:
            raise ValueError(f"Входное слово должно быть длиной {self.rows} бит.")

        candidates = []

        for col_index in range(self.cols):
            word = ''.join(str(bit) for bit in self.get_column(col_index))
            if self._compare_words(input_word, word, is_greater):
                candidates.append((word, col_index))

        if not candidates:
            raise ValueError("Нет слов, удовлетворяющих условию сравнения.")

        closest_word, closest_index = candidates[0]

        for word, index in candidates[1:]:
            if self._is_closer(input_word, word, closest_word, is_greater):
                closest_word = word
                closest_index = index

        return closest_word, closest_index

    @staticmethod
    def _compare_words(input_word: str, stored_word: str, is_greater: bool) -> bool:
        greater = False
        less = False

        for i in range(16):
            if input_word[i] != stored_word[i]:
                if input_word[i] == '1' and stored_word[i] == '0':
                    greater = True
                elif input_word[i] == '0' and stored_word[i] == '1':
                    less = True
                break

        return greater if is_greater else less

    @staticmethod
    def _is_closer(input_word: str, word1: str, word2: str, is_greater: bool) -> bool:
        def hamming_distance(w1, w2):
            return sum(bit1 != bit2 for bit1, bit2 in zip(w1, w2))

        return hamming_distance(input_word, word1) < hamming_distance(input_word, word2)

    @staticmethod
    def sum_of_binary_numbers(A, B):
        carry = 0
        result = []
        max_len = max(len(A), len(B))
        for i in range(max_len):
            bit_a = A[i] if i < len(A) else 0
            bit_b = B[i] if i < len(B) else 0
            sum_bit = bit_a + bit_b + carry
            result.append(sum_bit % 2)
            carry = sum_bit // 2
        if carry:
            result.append(carry)
        return result

    def sum_fields_by_indexs(self, column_indices):
        if not column_indices:
            return

        for row_index in range(self.rows):
            row_values = [self.matrix[row_index][col] for col in column_indices]
            header_bits = row_values[:3]
            data_bits = row_values[3:]
            part_length = len(data_bits) // 2
            part_A = data_bits[:part_length]
            part_B = data_bits[part_length:]
            binary_sum_result = self.sum_of_binary_numbers(part_A, part_B)
            new_row_value = header_bits + part_A + part_B + binary_sum_result
            self.set_word(new_row_value, row_index, column_indices[0])


def main():
    dm = DiagonalMatrix(rows=16, cols=16)

    dm.set_word([1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1], 0, 0)
    dm.set_word([1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0], 1, 1)
    dm.set_word([0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1], 2, 2)

    print("Матрица после записи слов и адресных столбцов:")
    for row in dm.matrix:
        print(row)



    test_columns = [(0, 1), (3, 5)]

    for col1, col2 in test_columns:
        print(f"\nОперации над столбцами {col1} и {col2}:")
        print(f"Столбец {col1}: {dm.get_column(col1)[:5]}...")
        print(f"Столбец {col2}: {dm.get_column(col2)[:5]}...")

        print(f"F1 (И): {dm.F1_operation(col1, col2)[:5]}...")
        print(f"F14 (NAND): {dm.F14_operation(col1, col2)[:5]}...")
        print(f"F3 (Повтор 1-го): {dm.F3_operation(col1, col2)[:5]}...")
        print(f"F12 (Отрицание 1-го): {dm.F12_operation(col1, col2)[:5]}...")

    result = dm.closest_word_find("1000000000000000", is_greater=False)
    result1 = dm.closest_word_find("1000000000000000", is_greater=True)
    print("Ближайшее слово:", result)
    print("Ближайшее слово:", result1)
    dm.sum_fields_by_indexs([1, 0, 1])
    print("\nМатрица после сложения полей:")
    for row in dm.matrix:
        print(row)

if __name__ == "__main__":
    main()