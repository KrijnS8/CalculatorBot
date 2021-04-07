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


def infix_to_prefix(s) -> str:
    stack: list = ['(']
    infix: str = f'{reverse_string(s)})'
    output: str = ''

    for char in infix:
        if char.isdigit():
            output = f'{output}{char}'

        if char == '(':
            stack.append(char)

        if char in '+-x/':
            while precedence(char) <= precedence(stack[-1]):
                output = f'{output}{stack.pop()}'
            stack.append(char)

        if char == ')':
            while True:
                c = stack.pop()
                if c == '(':
                    break
                output = f'{output}{c}'

    return reverse_string(output)


def reverse_string(s: str) -> str:
    output: str = ''

    for char in s:
        if char == '(':
            output = f'){output}'
        elif char == ')':
            output = f'({output}'
        else:
            output = f'{char}{output}'
    return output


def precedence(char: str) -> int:
    if char == '+' or char == '-':
        return 2
    if char == 'x' or char == '/':
        return 3
    return 1


print(infix_to_prefix('21x(5+16)'))
