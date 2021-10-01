from discord.ext import commands
import discord

# from library.sql_query import initialize_connection, SQLQuery
from library.manager import Manager

from library import config

import os

# sql_query = SQLQuery(initialize_connection())
manager = Manager()

command_names = [alias for command in manager.command_json.values()
                 for alias in command['aliases']]


async def get_prefix(bot, message):
    prefix = ['!']
    split_contents = message.content.split()
    if len(split_contents):
        if isinstance(message.channel, discord.channel.TextChannel) and [True for name in command_names if split_contents[0].endswith(name)]:
            print(message.content, message.guild.name)

            # prefix = list(sql_query.select_data('guilds', ['prefix'], condition=[
            #               ['guild_id'], [str(message.guild.id)]])[0])

    return commands.when_mentioned_or(*prefix)(bot, message)

bot = commands.Bot(command_prefix=get_prefix, case_insensitive=True)
bot.remove_command('help')

# add sql_query attribute to bot object as not to initialize a new pool for every cog
# bot.sql_query = sql_query

if __name__ == '__main__':
    for filename in os.listdir('./library/cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'library.cogs.{filename[:-3]}')

    bot.run(config('DISCORD_BOT_TOKEN'))
