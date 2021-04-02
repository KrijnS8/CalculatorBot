import discord
import logging
from discord.ext import commands
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

        await message.channel.send(f'The answer to {content} is {calculate(content)}')


def valid(content):
    """
    Checks for invalid characters
    :param content: message to check
    :return: true or false
    """
    allowed_chars = set('1234567890+-*/')

    for char in range(len(content)):
        if not any((c in allowed_chars) for c in content[char]):
            return False

    return True


def calculate(content):
    """
    Calculates the equation given
    :param content: equation to calculate
    :return: answer to equation
    """
    parts = group_parts(content)
    output = 0

    while len(parts) > 1:
        first_number = 0
        second_number = 0
        operator = ''
        index = 0

        if '/' in parts:
            index = parts.index('/')
        elif '*' in parts:
            index = parts.index('*')
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
        if operator == '*':
            output = first_number * second_number
        if operator == '/':
            output = first_number / second_number

        parts[index + 1] = output
        del parts[index - 1:index + 1]

    return output


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
