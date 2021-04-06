from abc import ABC
from math import sqrt, pi


class Expression(ABC):
    def evaluate(self) -> float:
        pass


class Number(Expression):
    value: float = None

    def __init__(self, v):
        self.value = v

    def evaluate(self) -> float:
        return self.value


class BinaryFunction(Expression):
    e1: Expression = None
    e2: Expression = None

    def __init__(self, e1, e2):
        self.e1 = e1
        self.e2 = e2


class Addition(BinaryFunction):
    def evaluate(self) -> float:
        v1 = self.e1.evaluate()
        v2 = self.e2.evaluate()
        return v1 + v2


class Subtraction(BinaryFunction):
    def evaluate(self) -> float:
        v1 = self.e1.evaluate()
        v2 = self.e2.evaluate()
        return v1 - v2


class Multiplication(BinaryFunction):
    def evaluate(self) -> float:
        v1 = self.e1.evaluate()
        v2 = self.e2.evaluate()
        return v1 * v2


class Division(BinaryFunction):
    def evaluate(self) -> float:
        v1 = self.e1.evaluate()
        v2 = self.e2.evaluate()

        if v2 == 0:
            raise Exception('Division by zero')

        return v1 / v2


class UnaryFunction(Expression):
    e: Expression = None

    def __init__(self, e):
        self.e = e


class Minus(UnaryFunction):
    def evaluate(self) -> float:
        v = self.e.evaluate()
        return -v


class Sqrt(UnaryFunction):
    def evaluate(self) -> float:
        v = self.e.evaluate()
        return sqrt(v)


class Parenthesis(UnaryFunction):
    def evaluate(self) -> float:
        v = self.e.evaluate()
        return v


class PI(Expression):
    def evaluate(self) -> float:
        return pi


def parse(s: str) -> Expression:
    if s[0].isdigit():
        l1 = number_length(s)
        if l1 < len(s) and s[l1] == '/':
            l2: int = number_length(s[l1 + 1:])
            n1 = Number(float(s[0: l1]))
            n2 = Number(float(s[l1 + 1: l1 + l2 + 1]))
            return parse(str(Division(n1, n2).evaluate()) + s[l1 + l2 + 1:])

        if l1 < len(s) and s[l1] == 'x':
            l2: int = number_length(s[l1 + 1:])
            n1 = Number(float(s[0: l1]))
            n2 = Number(float(s[l1 + 1: l1 + l2 + 1]))
            return parse(str(Multiplication(n1, n2).evaluate()) + s[l1 + l2 + 1:])

        if l1 < len(s) and s[l1] == '+':
            n1 = Number(float(s[0: l1]))
            return Addition(n1, parse(s[l1 + 1:]))

        if l1 < len(s) and s[l1] == '-':
            n1 = Number(float(s[0: l1]))
            return Subtraction(n1, parse(s[l1 + 1:]))

        return Number(float(s[0:l1]))


def number_length(s: str) -> int:
    length = 1
    if not s[0].isdigit():
        raise Exception('The first character in the string is not a digit')
    while 1:
        if length > len(s) - 1 or not s[length].isdigit() and s[length] != '.':
            return length
        length += 1


x = parse('7x4')
print(x.evaluate())
