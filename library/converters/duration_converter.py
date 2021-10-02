from discord.ext import commands


class DurationConverter(commands.Converter):
    async def convert(self, ctx, argument):
        try:
            amount = argument[:-1]
            unit = argument[-1]
            if amount.isdigit() and unit in ['s', 'm', 'h', 'd', 'w', 'M']:
                return (int(amount), unit)
        except:
            raise commands.BadArgument(message="Not duration provided")
