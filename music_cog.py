from ast import alias
import discord
from discord.ext import commands
from youtubesearchpython import VideosSearch
from yt_dlp import YoutubeDL
import asyncio

class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.is_playing = False
        self.is_paused = False
        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio/best'}
        self.FFMPEG_OPTIONS = {'options': '-vn'}
        self.vc = None
        self.ytdl = YoutubeDL(self.YDL_OPTIONS)

    def search_yt(self, item):
        if item.startswith("https://"):
            title = self.ytdl.extract_info(item, download=False)["title"]
            return {'source': item, 'title': title}
        search = VideosSearch(item, limit=1)
        return {'source': search.result()["result"][0]["link"], 'title': search.result()["result"][0]["title"]}

    async def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']
            self.music_queue.pop(0)
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: self.ytdl.extract_info(m_url, download=False))
            song = data['url']
            if self.vc:
                self.vc.play(discord.FFmpegPCMAudio(song, executable="ffmpeg.exe", **self.FFMPEG_OPTIONS), after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(), self.bot.loop))
        else:
            self.is_playing = False

    async def play_music(self, ctx_or_interaction):
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']
            if self.vc is None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()
                if self.vc is None:
                    if isinstance(ctx_or_interaction, commands.Context):
                        await ctx_or_interaction.send("```Could not connect to the voice channel```")
                    else:
                        await ctx_or_interaction.response.send_message("Konnte nicht mit dem Voice-Channel verbinden.", ephemeral=True)
                    return
            else:
                await self.vc.move_to(self.music_queue[0][1])
            self.music_queue.pop(0)
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: self.ytdl.extract_info(m_url, download=False))
            song = data['url']
            self.vc.play(discord.FFmpegPCMAudio(song, executable="ffmpeg.exe", **self.FFMPEG_OPTIONS), after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(), self.bot.loop))
        else:
            self.is_playing = False

    async def play(self, ctx_or_interaction, query: str):
        # Überprüfen, ob der Aufruf von einem Textbefehl oder einem Slash-Befehl stammt
        if isinstance(ctx_or_interaction, commands.Context):
            ctx = ctx_or_interaction
            interaction = None
        else:
            interaction = ctx_or_interaction
            ctx = None

        try:
            # Voice-Channel des Benutzers abrufen
            if ctx:
                voice_channel = ctx.author.voice.channel
            else:
                voice_channel = interaction.user.voice.channel
        except:
            # Fehlermeldung senden, wenn der Benutzer nicht in einem Voice-Channel ist
            if ctx:
                await ctx.send("```You need to connect to a voice channel first!```")
            else:
                await interaction.response.send_message("Du musst in einem Voice-Channel sein, um Musik abzuspielen!", ephemeral=True)
            return

        if self.is_paused:
            self.vc.resume()
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                if ctx:
                    await ctx.send("```Could not download the song. Incorrect format try another keyword. This could be due to playlist or a livestream format.```")
                else:
                    await interaction.response.send_message("Konnte den Song nicht herunterladen. Versuche ein anderes Stichwort.", ephemeral=True)
            else:
                if self.is_playing:
                    if ctx:
                        await ctx.send(f"**#{len(self.music_queue)+2} -'{song['title']}'** added to the queue")
                    else:
                        await interaction.response.send_message(f"**#{len(self.music_queue)+2} -'{song['title']}'** wurde zur Warteschlange hinzufügt.")
                else:
                    if ctx:
                        await ctx.send(f"**'{song['title']}'** added to the queue")
                    else:
                        await interaction.response.send_message(f"**'{song['title']}'** wurde zur Warteschlange hinzufügt.")
                self.music_queue.append([song, voice_channel])
                if not self.is_playing:
                    if ctx:
                        await self.play_music(ctx)
                    else:
                        await self.play_music(interaction)

    @commands.command(name="play", aliases=["p", "playing"], help="Plays a selected song from youtube")
    async def play_command(self, ctx, *args):
        query = " ".join(args)
        await self.play(ctx, query)

    @commands.command(name="pause", help="Pauses the current song being played")
    async def pause(self, ctx, *args):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
        elif self.is_paused:
            self.is_paused = False
            self.is_playing = True
            self.vc.resume()

    @commands.command(name="resume", aliases=["r"], help="Resumes playing with the discord bot")
    async def resume(self, ctx, *args):
        if self.is_paused:
            self.is_paused = False
            self.is_playing = True
            self.vc.resume()

    @commands.command(name="skip", aliases=["s"], help="Skips the current song being played")
    async def skip(self, ctx):
        if self.vc and self.vc.is_playing():
            self.vc.stop()
            await self.play_music(ctx)

    @commands.command(name="queue", aliases=["q"], help="Displays the current songs in queue")
    async def queue(self, ctx):
        retval = ""
        for i in range(0, len(self.music_queue)):
            retval += f"#{i+1} -" + self.music_queue[i][0]['title'] + "\n"
        if retval != "":
            await ctx.send(f"```queue:\n{retval}```")
        else:
            await ctx.send("```No music in queue```")

    @commands.command(name="clear", aliases=["c", "bin"], help="Stops the music and clears the queue")
    async def clear(self, ctx):
        if self.vc and self.is_playing:
            self.vc.stop()
        self.music_queue = []
        await ctx.send("```Music queue cleared```")

    @commands.command(name="stop", aliases=["disconnect", "l", "d"], help="Kick the bot from VC")
    async def dc(self, ctx):
        self.is_playing = False
        self.is_paused = False
        if self.vc:
            await self.vc.disconnect()

    @commands.command(name="remove", help="Removes last song added to queue")
    async def re(self, ctx):
        if self.music_queue:
            self.music_queue.pop()
            await ctx.send("```last song removed```")
        else:
            await ctx.send("```No songs in queue```")