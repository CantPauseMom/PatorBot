import os
import praw
import discord
import random
import requests
from dotenv import load_dotenv
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


# SET praw SECRETS
reddit = praw.Reddit(
     client_id=client,
     client_secret=sec,
     user_agent=U_Agent
     )

bot.run(TOKEN)
