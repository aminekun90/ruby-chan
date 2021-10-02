import asyncio
import random
import json
import discord
from discord.ext import commands, tasks
from itertools import cycle
from library.converters import DurationConverter


class Basics(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.statuses = cycle([
            'Learning stuff',
            'I’m not immature; I just know how to have fun',
            'I’d grill your cheese! ~me, flirting',
            'If I agreed with you we’d both be wrong',
            'I used to be indecisive. Now I’m not sure.',
            'Doing needlework and fashion!'
        ])

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        '''On ready'''
        self.update_status.start()
        print("Ruby chan is ready!")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        with open('static/text/prefixes.json', 'r') as descriptor:
            prefixes = json.load(descriptor)
        prefixes[str(guild.id)] = '!'

        with open('static/text/prefixes.json', 'w') as descriptor:
            json.dump(prefixes, descriptor, indent=4)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        with open('static/text/prefixes.json', 'r') as descriptor:
            prefixes = json.load(descriptor)
        prefixes.pop(str(guild.id))

        with open('static/text/prefixes.json', 'w') as descriptor:
            json.dump(prefixes, descriptor, indent=4)

    @commands.command(aliases=['chprefix'])
    @commands.has_permissions(manage_messages=True)
    async def change_prefix(self, ctx, prefix='!'):
        with open('static/text/prefixes.json', 'r') as descriptor:
            prefixes = json.load(descriptor)
        prefixes[str(ctx.guild.id)] = prefix

        with open('static/text/prefixes.json', 'w') as descriptor:
            json.dump(prefixes, descriptor, indent=4)
        await ctx.send(f'Prefix changed to: {prefix}')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        print(f'Error: {error}')
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Humm! Is it me or you are missing something ... !!')
            return
        elif isinstance(error, commands.CommandNotFound):
            await ctx.send('Humm! For some reason I dont know that command.')
            return
        elif isinstance(error, commands.MissingPermissions) or isinstance(error, commands.MissingRole):
            await ctx.send('Yo do not have permission for that (è_é).')
            return
        await ctx.send('Humm! For some reason I could not execute this command.')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f'{member} has joined the server.')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f'{member} has left the server.')

    # Tasks
    @tasks.loop(minutes=10)
    async def update_status(self):
        await self.client.change_presence(status=discord.Status.online, activity=discord.Game(next(self.statuses)))

    # Commands
    @commands.command()
    async def load(self, ctx, extension=None):
        if not extension:
            await ctx.send(f'Bakka! I dont understand what do you want to load')
            return
        self.client.load_extension(f'library.cogs.{extension}')

    @commands.command()
    async def unload(self, ctx, extension=None):
        if not extension:
            await ctx.send(f'Bakka! I dont understand what do you want to unload')
            return
        self.client.unload_extension(f'library.cogs.{extension}')

    @commands.command()
    async def reload(self, ctx, extension=None):
        if not extension:
            await ctx.send(f'Bakka! I dont understand what do you want to reload')
            return
        await self.unload(ctx, extension)
        await self.load(ctx, extension)

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong :ping_pong:  |  {round(self.client.latency, 3)} ms')

    @commands.command(aliases=['hi', 'hello', 'yo'])
    async def hellos(self, ctx):
        user_id = 525613411770433537
        await ctx.send(f'Hi (>_<)33 @{ctx.author}')

    @commands.command(aliases=['wru', 'about'])
    async def who_are_you(self, ctx):
        await ctx.send(f'Hi I am Ruby Kurosawa --version genesis-- :flushed: Pigii!!! ')

    @commands.command(aliases=['8ball', '8b'])
    async def eight_ball(self, ctx, *, question):
        responses = ["As I see it, yes.", "Ask again later.", "Better not tell you now.", "Cannot predict now.",
                     "Concentrate and ask again.", "Don’t count on it.", "It is certain.", "It is decidedly so.",
                     "Most likely.", "My reply is no.", "My sources say no.", "I'm afraid it's not looking good.", "Of course.",
                     "Reply hazy, try again.", "Signs point to yes.", "Very doubtful.", "Without a doubt.", "Yes.",
                     "Yes – definitely.", "You may rely on it."]
        print(f"Question {question}")
        await ctx.send(f'{random.choice(responses)}')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount)

    @commands.command()
    async def kick(self, ctx, member, *, reason=None):
        try:
            if hasattr(member, "mention"):
                await member.kick(reason=reason)
            else:
                raise commands.errors.MemberNotFound
        except Exception as e:
            if isinstance(e, commands.errors.MemberNotFound):
                await ctx.send(f'{member.mention if hasattr(member,"mention") else member} is not here!')
                return
            print(f'Error: {e}')
            await ctx.send(f'Could not kick {member.mention if hasattr(member,"mention") else member} for some obscure reason!')

    @commands.command()
    async def ban(self, ctx, member: commands.MemberConverter, duration: DurationConverter, *, reason=None):
        await ctx.guild.ban(member, reason=reason)
        await ctx.send(f'Do no come back you filthy animal (è_é)~o {member.mention}.')

    @commands.command()
    async def tempban(self, ctx, member: commands.MemberConverter, duration: DurationConverter, *, reason=None):
        multiplier = {
            's': 1,
            'm': 60,
            'h': 60*60,
            'd': 60*60*24,
            'w': 60*60*24*7,
            'M': 60*60*24*30
        }
        amount, unit = duration
        await ctx.guild.ban(member, reason=reason)
        await ctx.send(f'{member.mention} has been banned for {amount}{unit}.')
        await asyncio.sleep(amount*multiplier[unit])
        await ctx.guild.unban(member)

    @commands.command()
    async def unban(self, ctx, *, member):
        try:
            banned_users = await ctx.guild.bans()
            member_name, member_discriminator = member.split('#')
            found_user: discord.Member = next(iter(filter(lambda banned_user: (
                banned_user.user.name, banned_user.user.discriminator) == (member_name, member_discriminator), banned_users)), None)
            if found_user:
                await ctx.guild.unban(found_user)
                await ctx.send(f'Unbanned {found_user.mention} Ganbarubii!!')
                return
        except Exception as e:
            print(e)
            await ctx.send(f'User must be <user name>#<number> :pleading_face:')
            return
        await ctx.send(f'Sorry !! {member} is not banned :pleading_face:')


def setup(client):
    client.add_cog(Basics(client))
