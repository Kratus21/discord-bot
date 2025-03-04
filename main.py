import config
import discord
from discord.ext import commands
from discord import app_commands
import yt_dlp
import asyncio

'''
class Client(commands.Bot):
    async def on_ready(self):
        print(f"bot {self.user} ist online")
        try:
            guild= discord.Object("905458434135191562")
            synced = await self.tree.sync(guild=guild)
            print(f"synchronisiert {len(synced)} commands to guild {guild.id}") 
        except Exception as e:
            print(f"bot konnte nicht synchronisiert werden {e}")

    async def on_message(self,message):
       if message.author == self.user:
        return

       if message.content.startswith("just"):
            await message.channel.send(f"put the fries in the bag bro {message.author}")
'''

Guild_ID = discord.Object(id="905458434135191562")
intentss = discord.Intents.default()
intentss.message_content = True
intentss.voice_states = True
#client = Client(command_prefix="!", intents = intentss)
FFMPEG_OPTIONS = {"options" : "-vn"}
YDL_OPTIONS = {"format" : "bestaudio" , "noplaylist" : True}


class MusicBot(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.queue = []
@commands.command()
async def play(self, ctx,*, search):
    voice_channel = ctx.author.voice.channel if ctx.author.voice else None
    if not voice_channel:
        return await ctx.send("du bist nicht im vc")
    if not ctx.voice_client:
        await voice_channel.connect()

    async with ctx.typing():
        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(f"ytsearch:{search}", download = False)
            if "entrie" in info:
                info = info["entries"][0]
            url = info["url"]
            title = info["title"]
            self.queue.append((url,title))
            await ctx.send(f"zur warteschlange hinzugefügt: **{title}**")
        if not ctx.voice_client.is_playing():
            await self.play_next(ctx)

async def play_next(self,ctx):
    if self.queue:
        url, title = self.queue.pop(0)
        source = await discord.FFmpegOpusAudio.from_probe(url, **FFMPEG_OPTIONS)
        ctx.voice_client.play(source,after=lambda _:self.client.loop.create_task(self.play_next(ctx)))
        await ctx.send(f"jetzt spielt **{title}**")
    elif not ctx.voice_client.is_playing():
        await ctx.send("queue is empty!")

@commands.command()
async def skip (self,ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("geskipt")
client = commands.Bot(command_prefix="!", intents = intentss)

async def main():
    await client.add_cog(MusicBot(client))
    await client.start(config.token)



asyncio.run(main())
