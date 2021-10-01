from discord.ext import commands
from discord.ext.commands import CommandNotFound

from library import config
import os

bot = commands.Bot(command_prefix='###')
bot.remove_command('help')


@ bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return

if __name__ == '__main__':
    for filename in os.listdir('./library/cogs_web'):
        if filename.endswith('.py'):
            bot.load_extension(f'library.cogs_web.{filename[:-3]}')

    bot.run(config('DISCORD_BOT_TOKEN'))
