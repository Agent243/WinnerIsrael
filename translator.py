import os
import discord
from discord.ext import commands
from googletrans import Translator

TOKEN = os.environ.get('MTE4MTU4NDc4NjIwMDk4NTYyMQ.GvR9iL.aOE-pdY6ST4kl1iwlnZXwcT-tUAaGf0j_LGTAY')
intents = discord.Intents.default()
intents.typing = True
intents.presences = True
intents.guilds = True
intents.messages = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)
translator = Translator()

@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user.name}')
    await bot.change_presence(activity=discord.Game(name="Forza Horizon"))

@bot.command(name='translate')
async def translate(ctx, lang, *, text):
    translated_text = translator.translate(text, dest=lang)
    await ctx.send(f"Traduction vers {lang}: {translated_text.text}")

bot.run('MTE4MTU4NDc4NjIwMDk4NTYyMQ.GvR9iL.aOE-pdY6ST4kl1iwlnZXwcT-tUAaGf0j_LGTAY')
