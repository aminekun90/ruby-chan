import asyncio

import discord
import youtube_dl

from discord.ext import commands

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    # bind to ipv4 since ipv6 addresses cause issues sometimes
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'options': '-vn',
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.1):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


def check_if_creator(ctx):
    return ctx.author.id == 525613411770433537

def check_if_allowed_user(ctx):
    return ctx.author.id not in [370180726278193164]
class Music(commands.Cog):
    def __init__(self, client):
        self.client = client



    # Events
    @commands.Cog.listener()
    async def on_playing(self, ctx, title: str):
        await self.client.change_presence(status=discord.Status.online, activity=discord.Game(f'Playing {title} 🎶'))
        print(f'Start playing: {title}')

    @commands.Cog.listener()
    async def on_stop(self, ctx):
        print('Stop playing')
    # Commands

    @commands.command()
    @commands.has_role('DJ')
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command()
    @commands.has_role('DJ')
    async def play(self, ctx, *, query):
        """Plays a file from the local filesystem"""

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        ctx.voice_client.play(source, after=lambda e: print(
            f'Player error: {e}') if e else None)
        self.client.dispatch("playing", ctx, query)
        await ctx.send(f'Now playing: {query}')

    @commands.check(check_if_creator)
    @commands.has_role('DJ')
    @commands.command()
    async def yt(self, ctx, *, url):
        """Plays from a url (almost anything youtube_dl supports)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.client.loop)
            ctx.voice_client.play(player, after=lambda e: print(
                f'Player error: {e}') if e else None)
        self.client.dispatch("playing", ctx, player.title)
        await ctx.send(f'Now playing: {player.title}')

    @commands.check(check_if_allowed_user)
    @commands.command()
    @commands.has_role('DJ')
    async def stream(self, ctx, *, url):
        """Streams from a url (same as yt, but doesn't predownload)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.client.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print(
                f'Player error: {e}') if e else None)
        self.client.dispatch("playing", ctx, player.title)
        await ctx.send(f'Now playing: {player.title}')

    @commands.check(check_if_allowed_user)
    @commands.command()
    @commands.has_role('DJ')
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Changed volume to {volume}%")

    @commands.check(check_if_allowed_user)
    @commands.command()
    @commands.has_role('DJ')
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""
        self.client.dispatch("stop", ctx)
        await ctx.voice_client.disconnect()

    @play.before_invoke
    @yt.before_invoke
    @stream.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError(
                    "Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            self.client.dispatch("stop")
            ctx.voice_client.stop()


def setup(client):
    client.add_cog(Music(client))
