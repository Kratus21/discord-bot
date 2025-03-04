import config
import discord
from discord.ext import commands
from discord import app_commands

# Definiere eine Klasse für den Bot, die von commands.Bot erbt
class Client(commands.Bot):
    # Diese Methode wird aufgerufen, wenn der Bot erfolgreich gestartet ist
    async def on_ready(self):
        print(f"bot {self.user} ist online")  # Gibt eine Nachricht aus, dass der Bot online ist
        try:
            # Definiere eine spezifische Guild (Server) für Slash-Befehle
            guild = discord.Object("1346599283704463422")
            # Synchronisiere die Slash-Befehle mit der Guild
            synced = await self.tree.sync(guild=guild)
            print(f"synchronisiert {len(synced)} commands to guild {guild.id}")  # Gibt die Anzahl der synchronisierten Befehle aus
        except Exception as e:
            print(f"bot konnte nicht synchronisiert werden {e}")  # Fehlermeldung, falls die Synchronisierung fehlschlägt

    # Diese Methode wird aufgerufen, wenn eine Nachricht gesendet wird
    async def on_message(self, message):
        if message.author == self.user:  # Ignoriere Nachrichten, die vom Bot selbst stammen
            return

        if message.content.startswith("just"):  # Reagiere auf Nachrichten, die mit "just" beginnen
            await message.channel.send(f"put the fries in the bag bro {message.author}")  # Sende eine Antwortnachricht

# Definiere eine spezifische Guild (Server) für Slash-Befehle
Guild_ID = discord.Object(id="1346599283704463422")

# Konfiguriere die Intents (Berechtigungen) für den Bot
intentss = discord.Intents.default()
intentss.message_content = True  # Erlaube dem Bot, Nachrichteninhalte zu lesen

# Initialisiere den Bot mit dem Präfix "!" und den konfigurierten Intents
client = Client(command_prefix="!", intents=intentss)

# Definiere einen Slash-Befehl namens "antwort"
@client.tree.command(name="antwort", description="das ist ein test", guild=Guild_ID)
async def test(interaction: discord.Interaction, antwort: str):
    await interaction.response.send_message(antwort)  # Sende die eingegebene Antwort zurück

# Definiere einen Slash-Befehl namens "embed"
@client.tree.command(name="embed", description="das ist ein test", guild=Guild_ID)
async def test(interaction: discord.Interaction,):
    # Erstelle ein Embed mit einem Titel, einer URL, einer Beschreibung und einer Farbe
    embedd = discord.Embed(
        title="Klick auf diesen Link",
        url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        description="das ist ein test",
        color=discord.Color.blue()
    )
    embedd.set_thumbnail(url="https://i.imgur.com/M6sbDof.png")  # Setze ein Thumbnail-Bild
    await interaction.response.send_message(embed=embedd)  # Sende das Embed als Antwort

# Definiere einen Slash-Befehl namens "embed2"
@client.tree.command(name="embed2", description="das ist ein test", guild=Guild_ID)
async def test(interaction: discord.Interaction,):
    # Erstelle ein weiteres Embed mit einem Titel, einer URL, einer Beschreibung und einer Farbe
    embedd = discord.Embed(
        title="klick auf diesen Link",
        url="https://youtu.be/OKi9QCIpc6o?si=w3y1_zW25kq89r33&t=39",
        description="",
        color=discord.Color.red()
    )
    embedd.set_thumbnail(url="https://media1.tenor.com/m/19iF9aRGdbkAAAAd/king-von-king-von-stare.gif")  # Setze ein Thumbnail-Bild
    embedd.add_field(name="", value="Wie hendrik mich anguckt weil ich um 3 uhr nachts nicht mehr im voice chillen möchte")  # Füge ein Feld hinzu
    embedd.set_author(name="King Von", icon_url="https://i.ytimg.com/vi/8OXlDMNRu_Q/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLBrRvVdU8r9K15kZfPCjjszwAsn4w")  # Setze den Autor des Embeds
    await interaction.response.send_message(embed=embedd)  # Sende das Embed als Antwort

# Definiere eine Klasse für eine interaktive View mit einem Button
class View(discord.ui.View):
    # Definiere einen Button mit der Beschriftung "klick nicht drauf!" und einem Emoji
    @discord.ui.button(label="klick nicht drauf!", style=discord.ButtonStyle.red, emoji="💀")
    async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Erstelle ein Embed mit einer Beschreibung und einer Farbe
        embed = discord.Embed(
            description="das gefällt mir garnicht",
            color=discord.Color.red()
        )
        embed.set_image(url="https://media.tenor.com/WdOoQoAnB2wAAAAe/king-von-rapper.png")  # Setze ein Bild im Embed
        await interaction.response.send_message(embed=embed)  # Sende das Embed als Antwort

# Definiere einen Slash-Befehl namens "button"
@client.tree.command(name="button", description="das ist ein test", guild=Guild_ID)
async def button(interaction: discord.Interaction):
    await interaction.response.send_message(view=View())  # Sende die View mit dem Button als Antwort

# Starte den Bot mit dem Token aus der config-Datei
client.run(config.token)
