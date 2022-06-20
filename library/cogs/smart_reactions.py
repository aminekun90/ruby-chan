import asyncio
import discord
import json
from discord.ext import commands
import emoji


class SmartReactions(commands.Cog):
    def __init__(self, client):
        self.client = client

    @classmethod
    def load_apple_poop_words(self):
        path = 'static/text/apple_products.json'
        with open(path, 'r') as descriptor:
            return json.load(descriptor)
    # Events

    @commands.Cog.listener()
    async def on_message(self, message):
        found_apple = next(iter([product for product in self.load_apple_poop_words(
        ) if product.lower() in message.content.lower().replace(' ', '')]), None)
        if found_apple:
            await message.add_reaction(emoji.emojize(':pile_of_poo:'))
            return
        if self.client.user.mentioned_in(message):
            await message.channel.send(f"Plop {message.author.mention}! here is a :candy: for you!")
            await message.add_reaction(emoji.emojize(':eyes:'))

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        # await discord.utils.get(member.guild.channels, name="general").send(
        #     f"Hey {member.mention} you are {'Muted' if after.self_mute else 'Not muted'} {emoji.emojize(':eyes:')}")
        if after.self_mute and member.voice.channel.id == 859921243386150924:  # General
            await asyncio.sleep(60*60)
            await member.move_to(discord.utils.get(member.guild.channels, name="-AFK-"))
            print(f"{member} sent to AFK")
        if not after.self_mute and member.voice.channel.id == 933836469095759892:
            await member.move_to(discord.utils.get(member.guild.channels, name="General"))
            print(f"{member} sent to General")


def setup(client):
    client.add_cog(SmartReactions(client))
