import os
import praw
import discord
import random
from dotenv import load_dotenv
from discord.ext import commands
from imgurpython import ImgurClient

# LOAD .env FILE
load_dotenv()


# RETRIEVE SECRETS FROM .env
TOKEN = os.getenv('DISCORD_TOKEN')
client = os.getenv('client_id')
sec = os.getenv('my_client_secret')
U_Agent = os.getenv('user_agent')
ImgurID = os.getenv('IMGUR_ID')
ImgurSecret = os.getenv('IMGUR_SECRET')
# CREATE DISCORD CLIENT INSTANCE
D_Client = discord.Client()

# LOAD IMGUR CLIENT
imgur = ImgurClient(ImgurID, ImgurSecret)

# SET BOT COMMAND PREFIX
bot = commands.Bot(command_prefix='!')

# SET praw SECRETS
reddit = praw.Reddit(
     client_id=client,
     client_secret=sec,
     user_agent=U_Agent
     )


# PRINT MESSAGE WHEN BOT HAS CONNECTED
@bot.event
async def on_ready():
    print(f'{bot.user} has connected')


# SET CHANNEL ID
channel = bot.get_channel(id(643901893231509524))


# BOT COMMAND 1
@bot.command("dziala")
async def on_message(message):
    if message.author == D_Client.user:
        return
    if commands.Bot("reddit"):
        await message.channel.send("Ty się nadajesz")


# BOT COMMAND 2
@bot.command("karol")
async def on_message(message):
    if message.author == D_Client.user:
        return
    if commands.Bot("karol"):
        album = imgur.get_album_images('8v1CcEw')
        item = album[random.randint(1, 8)]
        await message.channel.send(item.link)


bot.run(TOKEN)
