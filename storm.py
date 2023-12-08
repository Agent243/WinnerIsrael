import os
import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import random
from googlesearch import search

TOKEN = os.environ.get('MTE4MTU2MzYzMDc1NjU3MzI5NQ.GfFRKh.vF8xXJMjxcef4jiIwD5dJtP1t9M5yWH0oS1Nos')

intents = discord.Intents.default()
intents.typing = True
intents.presences = True
intents.guilds = True
intents.messages = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

xp_dict = {}
actions = ["Danse", "Chante", "Fais une grimace", "Fais une blague", "Fais une imitation"]
verites = ["As-tu déjà menti à un ami proche?", "Quel est ton plus grand secret?", "Quel est ton rêve le plus fou?"]

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
        await verifier_roles(message.author)

    if message.content.lower().startswith('/texttogif'):
        await text_to_gif(message)

    # Nouvelles fonctionnalités
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

async def text_to_gif(message):
    text = message.content[len('/texttogif '):]

    image = create_text_image(text)

    image.save('output.gif', save_all=True, append_images=[image], duration=100, loop=0)

    with open('output.gif', 'rb') as f:
        file = discord.File(f)
        await message.channel.send(file=file)

def create_text_image(text):
    width, height = 400, 200
    image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(image)

    font_path = "arial.ttf"
    try:
        font = ImageFont.truetype(font_path, size=20)
    except IOError:
        font = ImageFont.load_default()

    text_width, text_height = draw.textsize(text, font)
    x = (width - text_width) // 2
    y = (height - text_height) // 2

    draw.text((x, y), text, font=font, fill='black')

    return image

@bot.command()
async def xp(ctx):
    user_id = str(ctx.author.id)
    xp = xp_dict.get(user_id, 0)
    await ctx.send(f"{ctx.author.mention}, tu as actuellement {xp} points d'expérience.")

@bot.command()
async def mute(ctx, *users: discord.Member):
    for user in users:
        await user.edit(mute=True)
    await ctx.send(f"{', '.join([user.mention for user in users])} a/ont été rendu(s) muet(s).")

@bot.command()
async def unmute(ctx, *users: discord.Member):
    for user in users:
        await user.edit(mute=False)
    await ctx.send(f"{', '.join([user.mention for user in users])} a/ont été rendu(s) muet(s).")

@bot.command()
async def mention_everyone(ctx):
    await ctx.send("@everyone")

@bot.command()
async def google(ctx, *query):
    query = ' '.join(query)
    results = list(search(query, num=5, stop=5, pause=1))

    response = "Voici ce que j'ai trouvé :\n"
    for i, result in enumerate(results, start=1):
        response += f"{i}. {result}\n"

    await ctx.send(response)

@bot.command()
async def predictions(ctx):
    predictions_list = ["Aujourd'hui, vous rencontrerez quelqu'un de spécial.",
                        "La chance vous sourira dans une entreprise importante.",
                        "Prenez le temps de vous détendre et de vous reposer aujourd'hui.",
                        "Vous devriez avoir une petite surprise durant cette semaine.",
                        "Vous ne devez faire de vagues ces temps-ci,sinon,il sera trop tard,et il ce porrait que ce soit grave dans votre memoire pour longtemps",
                        "Je ne sais pas vous...mais moi,je me sens hypra bien",
                        "Je vais vous dire un petit secret... http://instagram.com/israel2.3 c'est le compte insta de mon createur"]

    prediction = random.choice(predictions_list)
    await ctx.send(f"Prédiction du jour : {prediction}")

@bot.event
async def on_member_join(member):
    channel = member.guild.system_channel
    if channel:
        await channel.send(f"Faites du bruit pour accueillir {member.mention} !")

@bot.event
async def on_member_remove(member):
    channel = member.guild.system_channel
    if channel:
        await channel.send(f"R.I.P... {member.mention} nous a quitté.")

bot.run('MTE4MTU2MzYzMDc1NjU3MzI5NQ.GfFRKh.vF8xXJMjxcef4jiIwD5dJtP1t9M5yWH0oS1Nos')
