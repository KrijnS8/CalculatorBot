from abc import ABC
from math import sqrt, pi
import re


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


class Root(BinaryFunction):
    def evaluate(self) -> float:
        v1 = self.e1.evaluate()
        v2 = self.e2.evaluate()
        return v1 ** v2


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


def parser(postfix: str, stack=None) -> float:
    if stack is None:
        stack = []
    stack: list = stack
    if len(postfix) == 0:
        return stack[0].evaluate()
    postfix: str = postfix

    if postfix[0].isdigit() or postfix[0] == '.':
        n = 1
        while postfix[n].isdigit() or postfix[n] == '.':
            n += 1
        stack.append(Number(float(postfix[0:n])))
        return parser(postfix[n+1:], stack)

    if postfix[0] == '+':
        n2 = stack.pop()
        n1 = stack.pop()
        stack.append(Addition(n1, n2))
        return parser(postfix[1:], stack)

    if postfix[0] == '-':
        n2 = stack.pop()
        n1 = stack.pop()
        stack.append(Subtraction(n1, n2))
        return parser(postfix[1:], stack)

    if postfix[0] == 'x':
        n2 = stack.pop()
        n1 = stack.pop()
        stack.append(Multiplication(n1, n2))
        return parser(postfix[1:], stack)

    if postfix[0] == '/':
        n2 = stack.pop()
        n1 = stack.pop()
        stack.append(Division(n1, n2))
        return parser(postfix[1:], stack)

    if postfix[0] == '^':
        n2 = stack.pop()
        n1 = stack.pop()
        stack.append(Root(n1, n2))
        return parser(postfix[1:], stack)

    if postfix[0] == '$':
        n1 = stack.pop()
        stack.append(Sqrt(n1))
        return parser(postfix[1:], stack)


def infix_converter(s: str, option: str) -> str:
    stack: list = ['(']
    if option != 'postfix' and option != 'prefix':
        raise Exception('Wrong option inputted')
    infix: str = f'{s})' if option == 'postfix' else f'{reverse_string(s)})'
    output: str = ''

    for i in range(len(infix)):
        if infix[i].isdigit() or infix[i] == '.':
            n = i + 1 if option == 'postfix' else i - 1
            if infix[n] == '.' or infix[n].isdigit():
                output = f'{output}{infix[i]}'
            else:
                output = f'{output}{infix[i]}!' if option == 'postfix' else f'{output}!{infix[i]}'

        if infix[i] == '(':
            stack.append(infix[i])

        if infix[i] in '+-x/^$':
            while precedence(infix[i]) <= precedence(stack[-1]):
                output = f'{output}{stack.pop()}'
            stack.append(infix[i])

        if infix[i] == ')':
            while True:
                c = stack.pop()
                if c == '(':
                    break
                output = f'{output}{c}'

    return output if option == 'postfix' else reverse_string(output)


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
    if char == '^' or char == '$':
        return 4
    return 1


def validate(s: str) -> bool:
    allowed_chars = re.compile(r'[^0-9.+-/x^$() ]')
    s = allowed_chars.search(s)
    return not bool(s)


# print(infix_converter('5+$(5+6)', 'postfix'))
# print(infix_converter('21/(5+16)', 'postfix'))
# print(parser(infix_converter('21/(5+16)', 'postfix')))
# print(infix_converter('(5x(6+8)+3)x(9+54)', 'postfix'))
# print(parser(infix_converter('(5x(6+8)+3)x(9+54)', 'postfix')))
# print(infix_converter('(365+34)x(5x(76+3))', 'postfix'))
# print(parser(infix_converter('(365+34)x(5x(76+3))', 'postfix')))
