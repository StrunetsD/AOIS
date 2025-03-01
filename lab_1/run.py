class Methods:
    TOTAL_BITS = 32
    MAX_BITS = 31
    BIN_127 = '01111111'
    num_0 = 0
    num_1 = 1
    num_9 = 9
    num_32 = 32

    @classmethod
    def get_positive_binary_number(cls, decimal_number: int) -> str:
        if decimal_number < 0:
            raise ValueError("Только для положительных чисел")
        binary = ""
        while decimal_number > 0:
            binary = str(decimal_number % 2) + binary
            decimal_number //= 2
        return '0' + binary.zfill(cls.MAX_BITS)

    @classmethod
    def get_negative_binary_number(cls, decimal_number: int) -> str:
        abs_number = abs(decimal_number)
        positive_binary = cls.get_positive_binary_number(abs_number)[1:]
        return '1' + positive_binary.zfill(cls.MAX_BITS)

    @staticmethod
    def add_one(binary: str) -> str:
        carry = 1
        result = []
        for bit in reversed(binary):
            if bit == '1' and carry:
                result.append('0')
            elif bit == '0' and carry:
                result.append('1')
                carry = 0
            else:
                result.append(bit)
        if carry:
            result.append('1')
        return ''.join(reversed(result))

    @classmethod
    def convert_to_decimal(cls, binary_number: str) -> int:
        if binary_number[0] == '1':
            inverted = ''.join('1' if b == '0' else '0' for b in binary_number[1:])
            return -cls.binary_to_decimal_number(inverted) - 1
        return cls.binary_to_decimal_number(binary_number)

    @staticmethod
    def binary_to_decimal_number(binary: str) -> int:
        decimal = sum(int(bit) * (2 ** idx) for idx, bit in enumerate(reversed(binary)))
        return decimal

    @classmethod
    def convert_to_binary_number(cls, decimal_number: int) -> str:
        return cls.get_positive_binary_number(
            decimal_number) if decimal_number >= 0 else cls.get_negative_binary_number(decimal_number)

    @classmethod
    def direct_sum_of_binary_numbers(cls, num1: int, num2: int) -> str:
        bin1 = cls.convert_to_binary_number(num1).zfill(cls.TOTAL_BITS)
        bin2 = cls.convert_to_binary_number(num2).zfill(cls.TOTAL_BITS)
        result, carry = [], 0

        for i in range(cls.TOTAL_BITS - 1, -1, -1):
            sum_bit = int(bin1[i]) + int(bin2[i]) + carry
            result.append(str(sum_bit % 2))
            carry = sum_bit // 2

        return ''.join(reversed(result))

    @classmethod
    def convert_to_reverse_binary(cls, decimal_number: int) -> str:
        if decimal_number >= 0:
            return cls.get_positive_binary_number(decimal_number)
        positive = cls.get_positive_binary_number(abs(decimal_number))
        inverted = ''.join('1' if b == '0' else '0' for b in positive[1:])
        return '1' + inverted

    @classmethod
    def convert_to_additional_binary(cls, decimal_number: int) -> str:
        if decimal_number > 0:
            return cls.convert_to_reverse_binary(decimal_number)
        binary_number = cls.convert_to_reverse_binary(decimal_number)
        return cls.add_one(binary_number)

    @classmethod
    def sum_of_additional_binary(cls, num1: int, num2: int) -> str:
        bin1 = cls.convert_to_additional_binary(num1)
        bin2 = cls.convert_to_additional_binary(num2)
        carry = 0
        result = []

        for i in range(cls.TOTAL_BITS - 1, -1, -1):
            total = int(bin1[i]) + int(bin2[i]) + carry
            result.append(str(total % 2))
            carry = total // 2

        return ''.join(reversed(result))

    @classmethod
    def subtract_of_additional_binary(cls, number1: int, number2: int) -> str:
        return cls.sum_of_additional_binary(number1, -number2)

    @classmethod
    def multi_of_binary_numbers(cls, a: int, b: int) -> int:
        result = 0
        a_abs, b_abs = abs(a), abs(b)

        for i in range(cls.TOTAL_BITS):
            if (b_abs >> i) & 1:
                result += a_abs << i

        return -result if (a < 0) ^ (b < 0) else result

    @staticmethod
    def print_ieee754(binary_float_one: str):
        print(binary_float_one[0:1], " ", binary_float_one[1:9], " ", binary_float_one[9:33])

    @staticmethod
    def convert_float_to_binary_numbers(f: float) -> str:
        if f == 0.0:
            return '0' * 32

        sign_bit = '0' if f >= 0 else '1'
        f = abs(f)
        exponent, mantissa = 0, ''

        if f >= 1.0:
            while f >= 2.0:
                f /= 2.0
                exponent += 1
        else:
            while f < 1.0:
                f *= 2.0
                exponent -= 1

        exponent_bits = f"{exponent + 127:08b}"
        f -= 1.0

        for _ in range(23):
            f *= 2.0
            bit = '1' if f >= 1.0 else '0'
            mantissa += bit
            if f >= 1.0:
                f -= 1.0

        return sign_bit + exponent_bits + mantissa

    @classmethod
    def sum_of_floats_numbers(cls, float_one: float, float_two: float) -> str:
        binary_one = cls.convert_float_to_binary_numbers(float_one)
        binary_two = cls.convert_float_to_binary_numbers(float_two)

        return cls.process_float_sum(binary_one, binary_two)

    @classmethod
    def process_float_sum(cls, binary_one: str, binary_two: str) -> str:
        sign1, exponent1, mantissa1 = binary_one[cls.num_0], binary_one[cls.num_1:cls.num_9], binary_one[cls.num_9:cls.num_32]
        sign2, exponent2, mantissa2 = binary_two[cls.num_0], binary_two[cls.num_1:cls.num_9], binary_two[cls.num_9:cls.num_32]

        exp1 = int(exponent1, 2) - 127
        exp2 = int(exponent2, 2) - 127

        mantissa1_int = int('1' + mantissa1, 2)
        mantissa2_int = int('1' + mantissa2, 2)

        if exp1 != exp2:
            mantissa1_int, mantissa2_int, exp1, exp2 = cls.align_exponents(mantissa1_int, mantissa2_int, exp1, exp2)

        return cls.calculate_sum(mantissa1_int, mantissa2_int, sign1, sign2, exp1)

    @classmethod
    def align_exponents(cls, mantissa1_int: int, mantissa2_int: int, exp1: int, exp2: int):
        if exp1 > exp2:
            shift = exp1 - exp2
            mantissa2_int = mantissa2_int >> shift
            exp2 = exp1
        else:
            shift = exp2 - exp1
            mantissa1_int = mantissa1_int >> shift
            exp1 = exp2
        return mantissa1_int, mantissa2_int, exp1, exp2

    @classmethod
    def calculate_sum(cls, mantissa1_int: int, mantissa2_int: int, sign1: str, sign2: str, exp1: int) -> str:
        if sign1 == sign2:
            mantissa_sum = mantissa1_int + mantissa2_int
            result_sign = sign1
        else:
            if mantissa1_int >= mantissa2_int:
                mantissa_sum = mantissa1_int - mantissa2_int
                result_sign = sign1
            else:
                mantissa_sum = mantissa2_int - mantissa1_int
                result_sign = sign2

        if mantissa_sum == 0:
            return '0' * 32

        return cls.normalize_sum(mantissa_sum, result_sign, exp1)

    @classmethod
    def normalize_sum(cls, mantissa_sum: int, result_sign: str, exp1: int) -> str:
        leading_one_pos = mantissa_sum.bit_length()

        if leading_one_pos > 24:
            shift = leading_one_pos - 24
            mantissa_sum >>= shift
            exp1 += shift
        elif leading_one_pos < 24:
            shift = 24 - leading_one_pos
            mantissa_sum <<= shift
            exp1 -= shift

        exponent_sum = exp1 + 127
        if exponent_sum > 255 or exponent_sum < 0:
            raise OverflowError("Переполнение экспоненты")

        mantissa_sum_bin = f"{mantissa_sum:023b}".zfill(23)
        exponent_sum_bin = f"{exponent_sum:08b}"
        return result_sign + exponent_sum_bin + mantissa_sum_bin

    @classmethod
    def div_of_binary_numbers(cls, binary_num_one: str, binary_num_two: str) -> str:
        if all(c == '0' for c in binary_num_two):
            raise ZeroDivisionError("Деление на ноль")

        sign = ''
        if (binary_num_one[0] == '-' and binary_num_two[0] != '-') or \
                (binary_num_one[0] != '-' and binary_num_two[0] == '-'):
            sign = '-'

        dividend = binary_num_one.lstrip('-')
        divisor = binary_num_two.lstrip('-')

        quotient, remainder = '', ''
        precision = 5

        for bit in dividend:
            remainder += bit
            cmp = cls.binary_compare(remainder, divisor)
            if cmp >= 0:
                quotient += '1'
                remainder = cls.binary_subtract(remainder, divisor)
            else:
                quotient += '0'

        return cls.finalize_division(quotient, remainder, precision, sign, divisor)

    @staticmethod
    def binary_compare(a: str, b: str) -> int:
        a = a.lstrip('0') or '0'
        b = b.lstrip('0') or '0'
        if len(a) > len(b): return 1
        if len(a) < len(b): return -1
        return 1 if a > b else 0 if a == b else -1

    @staticmethod
    def binary_subtract(a: str, b: str) -> str:
        max_len = max(len(a), len(b))
        a = a.zfill(max_len)
        b = b.zfill(max_len)
        result, borrow = [], 0

        for i in range(max_len - 1, -1, -1):
            a_bit = int(a[i]) - borrow
            b_bit = int(b[i])
            if a_bit < b_bit:
                a_bit += 2
                borrow = 1
            else:
                borrow = 0
            result.append(str(a_bit - b_bit))
        return ''.join(reversed(result)).lstrip('0') or '0'

    @classmethod
    def finalize_division(cls, quotient: str, remainder: str, precision: int, sign: str, divisor: str) -> str:
        if remainder != '0' and precision > 0:
            quotient += '.'
            for _ in range(precision):
                remainder += '0'
                cmp = cls.binary_compare(remainder, divisor)
                if cmp >= 0:
                    quotient += '1'
                    remainder = cls.binary_subtract(remainder, divisor)
                else:
                    quotient += '0'

        quotient = quotient.lstrip('0') or '0'
        return sign + (quotient.rstrip('0').rstrip('.') or '0')

    @classmethod
    def divide(cls, first: int, second: int) -> float:
        if second == 0:
            raise ZeroDivisionError("Деление на ноль")

        bin1 = cls.convert_to_binary_number(abs(first))
        bin2 = cls.convert_to_binary_number(abs(second))

        binary_result = cls.div_of_binary_numbers(bin1, bin2)
        return cls.convert_binary_to_float(binary_result, first, second)

    @classmethod
    def convert_binary_to_float(cls, binary_result: str, first: int, second: int) -> float:
        if '.' in binary_result:
            integer_part, fractional_part = binary_result.split('.')
        else:
            integer_part = binary_result
            fractional_part = '0'

        integer = cls.binary_to_decimal_number(integer_part)
        fractional = sum(int(bit) * (2 ** -i) for i, bit in enumerate(fractional_part, 1))

        result = integer + fractional
        return -result if (first < 0) ^ (second < 0) else result


def main():
    method = Methods()
    print("Сложение:")
    num1 = int(input("Ввод числа №1: "))
    print(f"Число введено: {num1}")
    print(f"Прямой код: {method.convert_to_binary_number(num1)}")
    print(f"Обратный код: {method.convert_to_reverse_binary(num1)}")
    print(f"Дополнительный код: {method.convert_to_additional_binary(num1)}")

    num2 = int(input("Ввод числа №2: "))
    print(f"Число введено: {num2}")
    print(f"Прямой код: {method.convert_to_binary_number(num2)}")
    print(f"Обратный код: {method.convert_to_reverse_binary(num2)}")
    print(f"Дополнительный код: {method.convert_to_additional_binary(num2)}")

    result = method.sum_of_additional_binary(num1, num2)
    print(f"Результат: {method.convert_to_decimal(result)}")
    print(f"Прямой код: {method.convert_to_binary_number(method.convert_to_decimal(result))}")
    print(f"Обратный код: {method.convert_to_reverse_binary(method.convert_to_decimal(result))}")
    print(f"Дополнительный код: {method.convert_to_additional_binary(method.convert_to_decimal(result))}")

    print("\nВычитание:")
    result = method.subtract_of_additional_binary(num1, num2)
    print(f"Результат: {method.convert_to_decimal(result)}")
    print(f"Прямой код: {method.convert_to_binary_number(method.convert_to_decimal(result))}")
    print(f"Обратный код: {method.convert_to_reverse_binary(method.convert_to_decimal(result))}")
    print(f"Дополнительный код: {method.convert_to_additional_binary(method.convert_to_decimal(result))}")

    print("\nУмножение:")
    result = method.multi_of_binary_numbers(num1, num2)
    print(f"Результат: {result}")

    print("\nДеление:")
    result = method.divide(num1, num2)
    print(f"Результат: {result}")

    print("\nСложение чисел с плавающей точкой:")
    float1 = method.convert_float_to_binary_numbers(float(input("Ввод числа №1: ")))
    float2 = method.convert_float_to_binary_numbers(float(input("Ввод числа №2: ")))
    method.print_ieee754(float2)
    result = method.sum_of_floats_numbers(21.75, 1.125)
    method.print_ieee754(result)

if __name__ == '__main__':
    main()