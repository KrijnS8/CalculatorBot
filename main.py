import discord
import logging
import yaml

with open(r'config.yml') as file:
    config = yaml.full_load(file)

logging.basicConfig(level=logging.INFO)

client = discord.Client()


@client.event
async def on_ready():
    print('Bot is ready!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('.calculate'):

        content = ''
        for i in range(len('.calculate '), len(message.content)):
            content += message.content[i]

        if not valid(content):
            await message.channel.send('Forbidden characters found!')
            return

        await message.channel.send(f'The answer is {calculate(group_parts(content))}')


def valid(content):
    """
    Checks for invalid characters
    :param content: message to check
    :return: true or false
    """
    allowed_chars = set('1234567890+-x/()')

    for char in range(len(content)):
        if not any((c in allowed_chars) for c in content[char]):
            return False

    return True


def calculate(parts):
    """
    Calculates the equation given
    :param parts: equation to calculate
    :return: answer to equation
    """
    output = 0

    while len(parts) > 1:
        index = 0

        if '(' in parts:
            opening_bracket = parts.index('(')
            closing_bracket = list_rindex(parts, ')')

            parts[closing_bracket] = calculate(parts[opening_bracket + 1:closing_bracket])
            del parts[opening_bracket:closing_bracket]

        if '/' in parts:
            index = parts.index('/')
        elif 'x' in parts:
            index = parts.index('x')
        elif '+' in parts:
            index = parts.index('+')
        elif '-' in parts:
            index = parts.index('-')

        first_number = int(parts[index - 1])
        operator = parts[index]
        second_number = int(parts[index + 1])

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


def list_rindex(lst, value):
    return len(lst) - lst[-1::-1].index(value) - 1


def group_parts(content):
    """
    Groups message into appropriate parts
    :param content: message to check
    :return: list with all parts
    """
    parts = ['']
    numbers = set('1234567890')
    selection = 0

    for i in range(len(content) - 1):
        if any((n in numbers) for n in content[i]):
            if any((n in numbers) for n in content[i + 1]):
                parts[selection] += content[i]
                continue

        parts[selection] += content[i]
        selection += 1
        parts.append('')
    parts[selection] += content[len(content) - 1]

    return parts


client.run(config['apiKey'])
