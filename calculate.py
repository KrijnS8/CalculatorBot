from typing import List


def calculate(content):
    """
    Calculates the equation given
    :param content: equation to calculate (string or array)
    :return: answer to equation (float)
    """
    output = 0

    if isinstance(content, str):
        parts = group_parts(content)
    else:
        parts = content

    if len(parts) == 1:
        return float(parts[0])

    if not valid(parts):
        return False

    while len(parts) > 1:
        index = 0

        if '(' in parts:
            opening_bracket = parts.index('(')
            closing_bracket = list_rindex(parts, ')')

            parts[closing_bracket] = calculate(parts[opening_bracket + 1:closing_bracket])
            del parts[opening_bracket:closing_bracket]

            if len(parts) == 1:
                return parts[0]

        if '/' in parts:
            index = parts.index('/')
        elif 'x' in parts:
            index = parts.index('x')
        elif '+' in parts:
            index = parts.index('+')
        elif '-' in parts:
            index = parts.index('-')

        first_number = float(parts[index - 1])
        operator = parts[index]
        second_number = float(parts[index + 1])

        if operator == '+':
            output = first_number + second_number
        if operator == '-':
            output = first_number - second_number
        if operator == 'x':
            output = first_number * second_number
        if operator == '/':
            output = first_number / second_number

        parts[index + 1] = output
        del parts[index - 1:index + 1]

    return output


def valid(parts) -> bool:
    """
    Checks if equation is valid
    :param parts: equation to check (array)
    :return: true or false (boolean)
    """
    allowed_chars = set('1234567890+-x/()')
    operators = '+-x/'

    for i in range(len(parts)):
        if not set(parts[i]) <= allowed_chars:
            print('Invalid characters found')
            return False

        if parts[i] in operators and parts[i + 1] in operators:
            print('Multiple operators in between numbers')
            return False

        if parts[0] in operators or parts[len(parts) - 1] in operators:
            print('Equation starts or ends with operator')
            return False

    return True


def group_parts(content) -> List[str]:
    """
    Groups equation into appropriate parts
    :param content: equation to check (string)
    :return: list with all parts (array)
    """
    parts = ['']
    numbers = set('1234567890')
    selection = 0

    for i in range(len(content) - 1):
        if set(content[i]) <= numbers and set(content[i + 1]) <= numbers:
            parts[selection] += content[i]
            continue

        parts[selection] += content[i]
        selection += 1
        parts.append('')
    parts[selection] += content[len(content) - 1]

    return parts


def list_rindex(lst, value):
    return len(lst) - lst[-1::-1].index(value) - 1
