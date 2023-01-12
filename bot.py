import os
import discord
import json
from discord.ext import commands
from library import config
from library.commands import CustomHelpCommand


def get_prefix(client, message):
    with open('static/text/prefixes.json', 'r') as descriptor:
        prefixes = json.load(descriptor)
    prefix = prefixes[str(message.guild.id)]
    return commands.when_mentioned_or(*prefix)(client, message)


client = commands.Bot(command_prefix=get_prefix,
                      case_insensitive=True, help_command=CustomHelpCommand())

if __name__ == '__main__':
    for filename in os.listdir('./library/cogs'):
        if filename.endswith('.py'):
            client.load_extension(f'library.cogs.{filename[:-3]}')
    client.run(config('DISCORD_BOT_TOKEN'))
