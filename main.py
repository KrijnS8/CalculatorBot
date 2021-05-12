import discord
import logging
import yaml
import calculate
import expression

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

    if message.content.startswith('!calculate'):

        content = message.content[len('!calculate '):]

        if not expression.validate(content):
            await message.channel.send('Invalid characters found!')
            return

        solution = expression.parser(expression.infix_converter(content, 'postfix'))
        await message.channel.send(f'The answer is {solution}')


client.run(config['apiKey'])
