import discord
import logging
import yaml
import calculate

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

        content = ''
        for i in range(len('!calculate '), len(message.content)):
            content += message.content[i]

        solution = calculate.calculate(content)

        if not solution and solution != 0:
            await message.channel.send('The given equation is invalid')
            return

        await message.channel.send(f'The answer is {solution}')


client.run(config['apiKey'])
