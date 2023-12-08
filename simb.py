import os
import discord
from discord.ext import commands
import random

TOKEN = os.environ.get('MTE2MzM4NDU4MjM4OTkwNzUwOA.GGWUYq.VHWXo0hov4yS6dgPpOJ9vQVGbL-1ogvZd439jw')

intents = discord.Intents.default()
intents.typing = True
intents.presences = True
intents.guilds = True
intents.messages = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

xp_dict = {}

games = {
    "1": "Action ou Vérité",
    "2": "Devine le Nombre",
}

@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user.name}')
    await bot.change_presence(activity=discord.Game(name="Call Of Duty"))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('/Ping'):
        await message.channel.send('tu veux jouer au ping pong sans raquettes..?😂️')

    if '/hello' in message.content:
        await message.channel.send(f"Salut {message.author.mention}!")

    if message.content.lower().startswith('/jeux'):
        await afficher_jeux(message)

    if message.content.lower().startswith('/actionouverite'):
        await action_ou_verite(message)

    if message.content.lower().startswith('/devinenumero'):
        await devine_le_numero(message)

    if message.content.lower().startswith('/gagnerxp'):
        await gagner_xp(message)
        await verifier_roles(message.author)

    await bot.process_commands(message)

async def verifier_roles(user):
    user_id = str(user.id)
    xp = xp_dict.get(user_id, 0)

    if xp >= 1000:
        role_xperimente = discord.utils.get(user.guild.roles, name="XPérimenté/e")
        if role_xperimente and role_xperimente not in user.roles:
            await user.add_roles(role_xperimente)
            await user.send(f"Félicitations, tu as obtenu le rôle XPérimenté/e!")

    if xp >= 1500:
        role_futur_king_queen = discord.utils.get(user.guild.roles, name="Futur King/Queen")
        if role_futur_king_queen and role_futur_king_queen not in user.roles:
            await user.add_roles(role_futur_king_queen)
            await user.send(f"Félicitations, tu as obtenu le rôle Futur King/Queen!")

async def action_ou_verite(message):
    choix = random.choice(["action", "verite"])

    if choix == "action":
        action = random.choice(actions)
        await message.channel.send(f"{message.author.mention}, Action : {action}")
    else:
        verite = random.choice(verites)
        await message.channel.send(f"{message.author.mention}, Vérité : {verite}")

async def devine_le_numero(message):
    nombre_secret = random.randint(1, 100)
    essais_restants = 5

    await message.channel.send("Je pense à un nombre entre 1 et 100. Devine!")

    while essais_restants > 0:
        try:
            guess = await bot.wait_for('message', timeout=30, check=lambda m: m.author == message.author and m.channel == message.channel)
            guess = int(guess.content)

            if guess == nombre_secret:
                await message.channel.send(f"Bien joué, {message.author.mention}! Tu as deviné le nombre.")
                break
            elif guess < nombre_secret:
                await message.channel.send("Le nombre est plus grand. Essaye encore.")
            else:
                await message.channel.send("Le nombre est plus petit. Essaye encore.")

            essais_restants -= 1

        except asyncio.TimeoutError:
            await message.channel.send("Désolé, le temps est écoulé. Le nombre était {}".format(nombre_secret))
            break

async def gagner_xp(message):
    xp_gagne = random.randint(1, 10)
    user_id = str(message.author.id)
    xp_dict[user_id] = xp_dict.get(user_id, 0) + xp_gagne
    await message.channel.send(f"{message.author.mention}, tu as gagné {xp_gagne} points d'expérience!")

@bot.command()
async def xp(ctx):
    user_id = str(ctx.author.id)
    xp = xp_dict.get(user_id, 0)
    await ctx.send(f"{ctx.author.mention}, tu as actuellement {xp} points d'expérience.")

async def afficher_jeux(message):
    jeux_liste = "\n".join([f"{key}: {value}" for key, value in games.items()])
    await message.channel.send(f"Choisissez un jeu en tapant `/jeu [numéro]`:\n{jeux_liste}")

bot.run('MTE2MzM4NDU4MjM4OTkwNzUwOA.GGWUYq.VHWXo0hov4yS6dgPpOJ9vQVGbL-1ogvZd439jw')
