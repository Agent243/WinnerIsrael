import os
import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import random
import urllib.parse
import aiohttp

TOKEN = os.environ.get('MTE2MzEzNTEzMDE5NDQxOTc0Mw.GlytTx.WLIfo1pB3D_tTQEdQwzlBuwi3cDW8UD2UUpYLE')

intents = discord.Intents.default()
intents.typing = True
intents.presences = True
intents.guilds = True
intents.messages = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

xp_dict = {}

@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user.name}')
    await bot.change_presence(activity=discord.Game(name="Uncharted"))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('/Ping'):
        await message.channel.send('tu veux jouer au ping pong sans raquettes..?😂️')

    if '/hello' in message.content:
        await message.channel.send(f"Salut {message.author.mention}!")

    if message.content.lower().startswith('/actionouverite'):
        await action_ou_verite(message)

    if message.content.lower().startswith('/devinenumero'):
        await devine_le_numero(message)

    if message.content.lower().startswith('/gagnerxp'):
        await gagner_xp(message)
        await verifier_roles(message.author)  # Vérifie les rôles après avoir gagné de l'XP

    if message.content.lower().startswith('/texttogif'):
        await text_to_gif(message)

    # Nouvelles intégrations
    if message.content.lower().startswith('/mute'):
        await mute_user(message)

    if message.content.lower().startswith('/mentioneveryone'):
        await mention_everyone(message)

    if message.content.lower().startswith('/googlesearch'):
        await google_search(message)

    if message.content.lower().startswith('/xpoint'):
        await display_xp(message)

    await bot.process_commands(message)

# ... Vos autres fonctions restent inchangées

async def mute_user(message):
    # Assurez-vous que l'auteur du message est un administrateur
    if message.author.guild_permissions.administrator:
        member = message.author
        await member.edit(mute=True)
        await message.channel.send(f"{member.mention} est maintenant muet.")

async def mention_everyone(message):
    # Assurez-vous que l'auteur du message est un administrateur
    if message.author.guild_permissions.administrator:
        await message.channel.send("@everyone")

async def google_search(message):
    query = message.content[len('/googlesearch '):]
    search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"

    async with aiohttp.ClientSession() as session:
        async with session.get(search_url) as resp:
            if resp.status == 200:
                await message.channel.send(f"Voici ce que j'ai trouvé : {search_url}")
            else:
                await message.channel.send("Erreur lors de la recherche sur Google.")

async def display_xp(message):
    user_id = str(message.author.id)
    xp = xp_dict.get(user_id, 0)
    await message.channel.send(f"{message.author.mention}, tu as actuellement {xp} points d'expérience.")

# ... Vos autres fonctions restent inchangées

bot.run('MTE2MzEzNTEzMDE5NDQxOTc0Mw.GlytTx.WLIfo1pB3D_tTQEdQwzlBuwi3cDW8UD2UUpYLE')
