class Methods:
    TOTAL_BITS = 32
    MAX_BITS = 31
    BIN_127 = '01111111'
    num_0 = 0
    num_9 = 9
    num_32 = 32
    num_1 = 1

    @classmethod
    def get_positive_binary_number(cls, decimal_number: int) -> str:
        if decimal_number < 0:
            raise ValueError("Только для положительных чисел")
        binary = ""
        num = decimal_number
        while num > 0:
            binary = str(num % 2) + binary
            num = num // 2
        binary = binary.zfill(cls.MAX_BITS)
        return '0' + binary

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
            if bit == '1' and carry == 1:
                result.append('0')
                carry = 1
            elif bit == '0' and carry == 1:
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
        decimal = 0
        length = len(binary)
        for i in range(length):
            if binary[i] == '1':
                decimal += 2 ** (length - i - 1)
        return decimal

    @classmethod
    def convert_to_binary_number(cls, decimal_number: int) -> str:
        if decimal_number >= 0:
            return cls.get_positive_binary_number(decimal_number)
        return cls.get_negative_binary_number(decimal_number)

    @classmethod
    def direct_sum_of_binary_numbers(cls, num1: int, num2: int) -> str:
        bin1 = cls.convert_to_binary_number(num1).zfill(cls.TOTAL_BITS)
        bin2 = cls.convert_to_binary_number(num2).zfill(cls.TOTAL_BITS)

        result = []
        carry = 0

        for i in range(cls.TOTAL_BITS - 1, -1, -1):
            sum_bit = int(bin1[i]) + int(bin2[i]) + carry
            result.append(str(sum_bit % 2))
            carry = sum_bit // 2

        result = ''.join(reversed(result))
        return result[-cls.TOTAL_BITS:]

    @classmethod
    def convert_to_reverse_binary(cls, decimal_number: int) -> str:
        if decimal_number >= 0:
            return cls.get_positive_binary_number(decimal_number)
        positive = cls.get_positive_binary_number(abs(decimal_number))
        inverted = ''.join('1' if b == '0' else '0' for b in positive[1:])
        return '1' + inverted

    @classmethod
    def convert_to_additional_binary(cls, decimal_number: int):
        if decimal_number > 0:
            return cls.convert_to_reverse_binary(decimal_number)
        else:
            binary_number = cls.convert_to_reverse_binary(decimal_number)
            binary_number = cls.add_one(binary_number)
            return binary_number

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

        result = ''.join(reversed(result))
        return result[-cls.TOTAL_BITS:]

    @classmethod
    def subtract_of_additional_binary(cls, number1: int, number2: int) -> str:
        negative_num2 = -number2
        return cls.sum_of_additional_binary(number1, negative_num2)

    @classmethod
    def multi_of_binary_numbers(cls, a: int, b: int) -> int:
        result = 0
        a_abs = abs(a)
        b_abs = abs(b)

        for i in range(cls.TOTAL_BITS):
            if (b_abs >> i) & 1:
                result += a_abs << i

        if (a < 0) ^ (b < 0):
            return -result
        return result

    @classmethod
    def float_to_binary_fraction(cls, fraction: float) -> str:
        binary_fraction = ""
        while fraction != 0 and len(binary_fraction) < cls.TOTAL_BITS:
            fraction *= 2
            if fraction >= 1:
                binary_fraction += "1"
                fraction -= 1
            else:
                binary_fraction += "0"
        return binary_fraction

    @staticmethod
    def print_ieee754(binary_float_one: str):
        print(binary_float_one[0:1], " ", binary_float_one[1:9], " ", binary_float_one[9:33])

    @staticmethod
    def convert_float_to_binary(f: float) -> str:
        if f == 0.0:
            return '0' * 32

        sign_bit = '0' if f >= 0 else '1'
        f = abs(f)

        if f >= 1.0:
            exponent = 0
            while f >= 2.0:
                f /= 2.0
                exponent += 1
        else:
            exponent = 0
            while f < 1.0:
                f *= 2.0
                exponent -= 1

        exponent_bias = exponent + 127
        if exponent_bias < 0 or exponent_bias > 255:
            raise ValueError("Число выходит за пределы диапазона IEEE 754 (32 бита)")

        exponent_bits = f"{exponent_bias:08b}"

        f -= 1.0
        mantissa = ''
        for _ in range(23):
            f *= 2.0
            bit = '1' if f >= 1.0 else '0'
            mantissa += bit
            if f >= 1.0:
                f -= 1.0

        ieee754_bits = sign_bit + exponent_bits + mantissa
        return ieee754_bits

    @classmethod
    def sum_of_floats(cls, float_one: float, float_two: float) -> float:
        binary_one = cls.convert_float_to_binary(float_one)
        binary_two = cls.convert_float_to_binary(float_two)

        sign1, exponent1, mantissa1 = binary_one[cls.num_0], binary_one[cls.num_1:cls.num_9], binary_one[cls.num_1:cls.num_32]
        sign2, exponent2, mantissa2 = binary_two[cls.num_0], binary_two[cls.num_1:cls.num_9], binary_two[cls.num_9:cls.num_32]

        exp1 = int(exponent1, 2) - 127
        exp2 = int(exponent2, 2) - 127

        if exp1 != exp2:
            if exp1 > exp2:
                shift = exp1 - exp2
                mantissa2 = '1' + mantissa2
                mantissa2 = mantissa2[:-shift] if shift <= len(mantissa2) else '0'
                exp2 = exp1
            else:
                shift = exp2 - exp1
                mantissa1 = '1' + mantissa1
                mantissa1 = mantissa1[:-shift] if shift <= len(mantissa1) else '0'
                exp1 = exp2

        mantissa1_int = int('1' + mantissa1, 2)
        mantissa2_int = int('1' + mantissa2, 2)

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
            return 0.0

        leading_one_pos = mantissa_sum.bit_length()

        if leading_one_pos > 24:
            shift = leading_one_pos - 24
            mantissa_sum >>= shift
            exp1 += shift
        elif leading_one_pos < 24:
            shift = 24 - leading_one_pos
            mantissa_sum <<= shift
            exp1 -= shift

        mantissa_sum_bin = f"{mantissa_sum:024b}"
        mantissa_sum_bin = mantissa_sum_bin[1:].ljust(cls.TOTAL_BITS, '0')[:cls.TOTAL_BITS]

        exponent_sum = exp1 + 127
        if exponent_sum > 255:
            raise OverflowError("Переполнение экспоненты")
        elif exponent_sum < 0:
            raise OverflowError("Антипереполнение экспоненты")

        exponent_sum_bin = f"{exponent_sum:08b}"
        binary_sum = result_sign + exponent_sum_bin + mantissa_sum_bin
        return cls.convert_binary_to_float(binary_sum)

    @classmethod
    def convert_binary_to_float(cls, binary: str) -> float:
        sign_bit = int(binary[cls.num_0])
        exponent_bits = binary[cls.num_1:cls.num_9]
        mantissa_bits = binary[cls.num_9:cls.num_32]

        sign = (-1) ** sign_bit
        exponent = int(exponent_bits, 2) - 127
        mantissa = 1.0
        for i, bit in enumerate(mantissa_bits):
            mantissa += int(bit) * (2 ** -(i + 1))

        return sign * mantissa * (2 ** exponent)

    @classmethod
    def div_of_binary_numbers(cls, binary_num_one: str, binary_num_two: str) -> str:
        num1 = cls.convert_to_decimal(binary_num_one)
        num2 = cls.convert_to_decimal(binary_num_two)

        if num2 == 0:
            raise ValueError("Деление на ноль!")

        result = round(num1 / num2, 5)
        return cls.convert_float_to_binary(result)


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
    result = method.div_of_binary_numbers(method.convert_to_binary_number(num1), method.convert_to_binary_number(num2))
    print(f"Результат: {result}")

    print("\nСложение чисел с плавающей точкой:")
    float1 = method.convert_float_to_binary(float(input("Ввод числа №1: ")))
    float2 = method.convert_float_to_binary(float(input("Ввод числа №2: ")))
    method.print_ieee754(float1)
    method.print_ieee754(float2)
    result = method.sum_of_floats(method.convert_binary_to_float(float1), method.convert_binary_to_float(float2))
    print(f"Результат: {result}")


if __name__ == '__main__':
    main()
# [name_of_task] Added sum_of_binary_floats