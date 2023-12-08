import discord
from discord.ext import commands

import subprocess
import shlex
import asyncio
import os

TOKEN = 'MTE4MTg2MTkyNTU5Njk3NTExNA.GERYJz.4M1GHLpjBJao9m_6jmSQDtTM9FBogtJJou1XB0'
intents = discord.Intents.default()
intents.typing = True
intents.presences = True
intents.guilds = True
intents.messages = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user.name}')

@bot.command()
async def shell(ctx):
    user_folder = f"user_{ctx.author.id}"

    if not os.path.exists(user_folder):
        os.makedirs(user_folder)

    await ctx.send("Vous êtes maintenant en mode Terminal (Linux). Entrez vos commandes.")

    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    while True:
        try:
            # Attend la prochaine commande de l'utilisateur
            user_input = await bot.wait_for('message', check=check, timeout=60.0)
            command = user_input.content.strip()

            if command.lower() == '/exit':
                await ctx.send("Sortie du mode Terminal.")
                break

            # Exécute la commande dans le terminal
            result = subprocess.run(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=user_folder)

            # Enregistre la commande dans un fichier
            with open(f"{user_folder}/SHELL.txt", 'a') as file:
                file.write(f"{command}\n")
                file.write(result.stdout)
                file.write(result.stderr)
                file.write("\n\n")

            # Envoie le résultat au chat Discord
            await ctx.send(f"```\n{result.stdout}{result.stderr}\n```")

        except asyncio.TimeoutError:
            await ctx.send("Timeout. Sortie du mode Terminal.")
            break

@bot.command()
async def show_save(ctx):
    user_folder = f"user_{ctx.author.id}"
    file_path = f"{user_folder}/SHELL.txt"

    # Affiche le contenu du fichier d'enregistrement
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            content = file.read()
        await ctx.send(f"Contenu du fichier d'enregistrement :```\n{content}\n```")
    else:
        await ctx.send("Aucun enregistrement trouvé.")

bot.run('MTE4MTg2MTkyNTU5Njk3NTExNA.GERYJz.4M1GHLpjBJao9m_6jmSQDtTM9FBogtJJou1XB0')
