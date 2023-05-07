class MyBigInt:

    def __init__(self):
        self.digits = []

    def setHex(self, hexStr):
        self.digits = []
        hexStr = hexStr.lower()
        for i in range(len(hexStr) - 1, -1, -8):
            chunk = hexStr[max(0, i - 7):i + 1]
            self.digits.append(int(chunk, 16))
        self.trim()

    def getHex(self):
        return ''.join(f'{x:08x}' for x in reversed(self.digits))

    def trim(self):
        while len(self.digits) > 1 and self.digits[-1] == 0:
            self.digits.pop()

    def __str__(self):
        return self.getHex()

    def __eq__(self, other):
        return self.digits == other.digits

    def __and__(self, other):
        res = MyBigInt()
        for i in range(max(len(self.digits), len(other.digits))):
            res.digits.append(self.digits[i] & other.digits[i])
        res.trim()
        return res

    def __or__(self, other):
        res = MyBigInt()
        for i in range(max(len(self.digits), len(other.digits))):
            if i >= len(self.digits):
                res.digits.append(other.digits[i])
            elif i >= len(other.digits):
                res.digits.append(self.digits[i])
            else:
                res.digits.append(self.digits[i] | other.digits[i])
        res.trim()
        return res

    def __xor__(self, other):
        res = MyBigInt()
        for i in range(max(len(self.digits), len(other.digits))):
            if i >= len(self.digits):
                res.digits.append(other.digits[i])
            elif i >= len(other.digits):
                res.digits.append(self.digits[i])
            else:
                res.digits.append(self.digits[i] ^ other.digits[i])
        res.trim()
        return res

    def __invert__(self):
        res = MyBigInt()
        for digit in self.digits:
            res.digits.append(~digit & 0xFFFFFFFF)
        res.trim()
        return res

    def shiftL(self, n):
        res = MyBigInt()
        res.digits = self.digits.copy()
        for i in range(n // 32):
            res.digits.insert(0, 0)
        if n % 32 != 0:
            carry = 0
            for i in range(len(res.digits)):
                temp = (res.digits[i] << n % 32) | carry
                carry = res.digits[i] >> (32 - n % 32)
                res.digits[i] = temp & 0xFFFFFFFF
            if carry != 0:
                res.digits.append(carry)
        res.trim()
        return res

    def shiftR(self, n):
        if n <= 0:
            return

        num_bits = len(self.array) * 8
        if n >= num_bits:
            self.array = [0]
            return

        num_bytes = (num_bits - n) // 8
        num_bits_leftover = (num_bits - n) % 8

        result = []
        carry = 0
        for i in range(num_bytes):
            current_byte = self.array[i]
            next_byte = self.array[i + 1] if i < len(self.array) - 1 else 0
            new_byte = ((next_byte << (8 - num_bits_leftover)) | (current_byte >> n)) & 0xFF
            result.append(new_byte | carry)
            carry = current_byte << (8 - n)

        if num_bits_leftover > 0:
            current_byte = self.array[num_bytes]
            new_byte = current_byte >> n
            result.append(new_byte | carry)

        self.array = result

    def __add__(self, other):
        res = MyBigInt()
        carry = 0
        for i in range(max(len(self.digits), len(other.digits))):
            a = self.digits[i] if i < len(self.digits) else 0
            b = other.digits[i] if i < len(other.digits) else 0
            s = a + b + carry
            res.digits.append(s & 0xFFFFFFFF)
            carry = (s >> 32) & 0x1
        if carry == 1:
            res.digits.append(1)
        res.trim()
        return res

    def __sub__(self, other):
        result = MyBigInt()
        borrow = 0
        for i in range(max(len(self.digits), len(other.digits))):
            a = self.digits[i] if i < len(self.digits) else 0
            b = other.digits[i] if i < len(other.digits) else 0
            d = a - b - borrow
            borrow = 0 if d >= 0 else 1
            result.digits.append(d & 0xFFFFFFFF)
        while len(result.digits) > 1 and result.digits[-1] == 0:
            result.digits.pop()
        return result

    def __ge__(self, other):
        if len(self.digits) != len(other.digits):
            return len(self.digits) >= len(other.digits)
        else:
            for i in range(len(self.digits)-1, -1, -1):
                if self.digits[i] != other.digits[i]:
                    return self.digits[i] >= other.digits[i]
        return True

    def __mod__(self, other):
        quotient = MyBigInt()
        remainder = MyBigInt()
        divisor = MyBigInt()

        for digit in self.digits:
            remainder.digits.append(digit)
            divisor.digits.append(0)

            while remainder >= other:
                divisor += other
                remainder -= other

            quotient.digits.append(divisor.digits[-1])
            divisor.digits.pop()

        while len(quotient.digits) > 1 and quotient.digits[-1] == 0:
            quotient.digits.pop()

        return remainder

    def __mul__(self, other):
        result = MyBigInt()
        result.digits = [0] * (len(self.digits) + len(other.digits))
        for i, x in enumerate(self.digits):
            carry = 0
            for j, y in enumerate(other.digits):
                carry, z = divmod(x * y + result.digits[i + j] + carry, 0x100000000)
                result.digits[i + j] = z
            result.digits[i + len(other.digits)] = carry
        while len(result.digits) > 1 and result.digits[-1] == 0:
            result.digits.pop()
        return result



num = MyBigInt()
num2 = MyBigInt()
num3 = MyBigInt()
num.setHex("51bf608414ad5726a3c1bec098f77b1b54ffb2787f8d528a74c1d7fde6470ea4")
num2.setHex("403db8ad88a3932a0b7e8189aed9eeffb8121dfac05c3512fdb396dd73f6331c")
num3 = num.__xor__(num2)
print(num3.getHex())

###

num.setHex("36f028580bb02cc8272a9a020f4200e346e276ae664e45ee80745574e2f5ab80")
num2.setHex("70983d692f648185febe6d6fa607630ae68649f7e6fc45b94680096c06e4fadb")
num3=num.__add__(num2)
print(num3.getHex())

###

num.setHex("33ced2c76b26cae94e162c4c0d2c0ff7c13094b0185a3c122e732d5ba77efebc")
num2.setHex("22e962951cb6cd2ce279ab0e2095825c141d48ef3ca9dabf253e38760b57fe03")
num3=num.__sub__(num2)
print(num3.getHex())

###

num.setHex("7d7deab2affa38154326e96d350deee1")
num2.setHex("97f92a75b3faf8939e8e98b96476fd22")
num3=num2.__mod__(num)
print(num3.getHex())

###

num.setHex("7d7deab2affa38154326e96d350deee1")
num2.setHex("97f92a75b3faf8939e8e98b96476fd22")
num3=num.__mul__(num2)
print(num3.getHex())

