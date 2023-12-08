import os
import discord
from discord.ext import commands, tasks
from PIL import Image, ImageDraw, ImageFont
import random
import asyncio

TOKEN = os.environ.get('MTE4MTg0NjI4MDQ2OTc0MTY2MA.GENypk.-8N82y0ZZQOI-biEqdHfKKMnuBXvAJDZ30CR70')

intents = discord.Intents.default()
intents.typing = True
intents.presences = True
intents.guilds = True
intents.messages = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

xp_dict = {}

# Variables pour le jeu de voiture
car_emoji = "🚗"
track_length = 10
race_track = ["🏁"] * track_length
car_position = 0

@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user.name}')
    await bot.change_presence(activity=discord.Game(name="Destiny2"))
    race_loop.start()

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

    if message.content.lower().startswith('/start'):
        await start_race(message)

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
        action = random.choice(["Faire une danse", "Chanter une chanson", "Imiter un animal"])
        await message.channel.send(f"{message.author.mention}, Action : {action}")
    else:
        verite = random.choice(["Quel est ton plus grand rêve?", "As-tu déjà menti à un ami?", "Ta plus grande peur"])
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

    # Create an image with the text
    image = create_text_image(text)

    # Save the image
    image.save('output.gif', save_all=True, append_images=[image], duration=100, loop=0)

    # Upload the image to the channel
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

async def start_race(message):
    global race_track, car_position
    race_track = ["🏁"] * track_length
    car_position = 0
    await display_race(message)

@tasks.loop(seconds=2)
async def race_loop():
    global car_position
    if random.choice([True, False]):
        car_position += 1
        await display_race()

async def display_race(message=None):
    global car_emoji, race_track, car_position, track_length

    # Move the car on the track
    race_track[car_position] = car_emoji

    # Display the race track
    track_display = " ".join(race_track)
    race_embed = discord.Embed(title="Course de Voiture", description=track_display, color=0x00ff00)

    # Display the car's position in the embed footer
    race_embed.set_footer(text=f"Position de la voiture: {car_position + 1}/{track_length}")

    if message:
        await message.edit(embed=race_embed)
    else:
        await bot.get_channel(1181849491981209641).send(embed=race_embed)

bot.run('MTE4MTg0NjI4MDQ2OTc0MTY2MA.GENypk.-8N82y0ZZQOI-biEqdHfKKMnuBXvAJDZ30CR70')
