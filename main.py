import config
import discord
from discord.ext import commands
from discord import app_commands


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


Guild_ID = discord.Object(id="905458434135191562")
intentss = discord.Intents.default()
intentss.message_content = True
client = Client(command_prefix="!", intents = intentss)

@client.tree.command(name="antwort", description="das ist ein test", guild=Guild_ID)

async def test(interaction: discord.Interaction, antwort:str):
    await interaction.response.send_message(antwort)

@client.tree.command(name="embed", description="das ist ein test", guild=Guild_ID)


async def test(interaction: discord.Interaction,):
    embedd = discord.Embed(title="Klick auf diesen Link", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ", description="das ist ein test", color=discord.Color.blue())
    embedd.set_thumbnail(url="https://i.imgur.com/M6sbDof.png")
    await interaction.response.send_message(embed=embedd)

@client.tree.command(name="embed2", description="das ist ein test", guild=Guild_ID)
async def test(interaction: discord.Interaction,):
    embedd = discord.Embed(title="klick auf diesen Link", url="https://youtu.be/OKi9QCIpc6o?si=w3y1_zW25kq89r33&t=39", description="", color=discord.Color.red())
    embedd.set_thumbnail(url="https://media1.tenor.com/m/19iF9aRGdbkAAAAd/king-von-king-von-stare.gif")
    embedd.add_field(name="", value="Wie hendrik mich anguckt weil ich um 3 uhr nachts nicht mehr im voice chillen möchte")
    embedd.set_author(name="King Von" , icon_url="https://i.ytimg.com/vi/8OXlDMNRu_Q/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLBrRvVdU8r9K15kZfPCjjszwAsn4w")
    await interaction.response.send_message(embed=embedd)

class View(discord.ui.View):
    @discord.ui.button(label="klick nicht drauf!", style=discord.ButtonStyle.red, emoji="💀")
    async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        
        embed = discord.Embed(
            description="das gefällt mir garnicht",  
            color=discord.Color.red()  
        )
        embed.set_image(url="https://media.tenor.com/WdOoQoAnB2wAAAAe/king-von-rapper.png") 
        
        # Sende das Embed
        await interaction.response.send_message(embed=embed)

@client.tree.command(name="button", description="das ist ein test", guild=Guild_ID)
async def button(interaction: discord.Interaction):
    await interaction.response.send_message(view=View())   

client.run(config.token)