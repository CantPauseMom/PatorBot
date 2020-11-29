import asyncio
import os
import praw
import discord
import time
import gevent
import random
import requests
import json
from websocket import create_connection
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
API_ENDPOINT = 'https://discord.com/api/v8'
uri = 'wss://gateway.discord.gg/?v=8&encoding=json'
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


def get_token():

    data = {
        'grant_type': 'client_credentials',
        'scope': 'bot'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    r = requests.post('%s/oauth2/token' % API_ENDPOINT, data=data, headers=headers, auth=(client, sec))
    r.raise_for_status()
    return r.json()


async def establish_connection():
    conn = create_connection(uri)
    result = conn.recv()
    heartbeat_rate = result[53:58]
    print(heartbeat_rate)
    opcode1 = {
        "op": 1,
        "d": None
    }

    async def send_opcode1():
        loop = asyncio.new_event_loop()
        json_pack = json.dumps(opcode1)
        await conn.send(json_pack)
        gevent.sleep(int(heartbeat_rate) / 1000)
        print("package sent")
        loop.run_forever()

    pack = {
        "op": 2,
        "d": {
            "token": TOKEN,
            "intents": 513,
            "properties": {
                "$os": "windows",
                "$browser": "my_library",
                "$device": "my_library"
            }
        }
    }
    pack_json = json.dumps(pack)
    conn.send(pack_json)
    print("pack sent")

print(get_token())
asyncio.run(establish_connection())

while True:
    time.sleep(5)
