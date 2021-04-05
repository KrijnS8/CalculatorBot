from abc import ABC
from math import sqrt


class Expression(ABC):
    def evaluate(self) -> float:
        pass


class Number(Expression):
    value: float = None

    def __init__(self, v):
        self.value = v

    def evaluate(self) -> float:
        print(f'Evaluate number: {self.value}')
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
        print(f'Evaluate addition: {v1, v2}')
        return v1 + v2


class Subtraction(BinaryFunction):
    def evaluate(self) -> float:
        v1 = self.e1.evaluate()
        v2 = self.e2.evaluate()
        print(f'Evaluate subtraction: {v1, v2}')
        return v1 - v2


class Multiplication(BinaryFunction):
    def evaluate(self) -> float:
        v1 = self.e1.evaluate()
        v2 = self.e2.evaluate()
        print(f'Evaluate multiplication: {v1, v2}')
        return v1 * v2


class Division(BinaryFunction):
    def evaluate(self) -> float:
        v1 = self.e1.evaluate()
        v2 = self.e2.evaluate()

        if v2 == 0:
            raise Exception('Division by zero')

        print(f'Evaluate division: {v1, v2}')
        return v1 / v2


class UnaryFunction(Expression):
    e: Expression = None

    def __init__(self, e):
        self.e = e


class Minus(UnaryFunction):
    def evaluate(self) -> float:
        v = self.e.evaluate()
        print(f'Evaluate minus: {-v}')
        return -v


class Sqrt(UnaryFunction):
    def evaluate(self) -> float:
        v = self.e.evaluate()
        print(f'Evaluate sqrt: {v}')
        return sqrt(v)


class Parenthesis(UnaryFunction):
    def evaluate(self) -> float:
        v = self.e.evaluate()
        print(f'Evaluate parenthesis: {v}')
        return v


class Zero(Expression):
    def evaluate(self) -> float:
        print('Evaluate zero: 0')
        return 0


# e1 = Division(Number(42), Zero())
# print(e1.evaluate())
# # e = Addition(Minus(Number(42)), Sqrt(Number(420)))
# # print(e.evaluate())


def parse(s: str) -> Expression:
    if s.startswith('sqrt(') and s.endswith(')'):
        return Sqrt(parse(s[5:-1]))

    if s[0].isdigit():
        return Number(float(s[0]))


e = parse('sqrt(sqrt(3))')
print(e.evaluate())
