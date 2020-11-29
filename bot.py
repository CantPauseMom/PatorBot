import asyncio
import os
import praw
import discord
import time
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

class Connection():
    def get_token(self):

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

    def get_gateway(self):
        request = requests.get('%s/gateway' % API_ENDPOINT)
        request.raise_for_status()
        return request.json()

    def get_info(self):
        uri = 'wss://gateway.discord.gg/?v=8&encoding=json'
        conn = create_connection(uri)
        global result
        result = conn.recv()

        J_File = json.dumps(result)
        test = json.loads(J_File)

        return result

    def get_heartbeatrate(self):
        heartbeat_rate = result[53:58]
        return heartbeat_rate

    def connect(self):
        uri = 'wss://gateway.discord.gg/?v=8&encoding=json'

        send_opcode1 ={
        "op": 1,
        "d": None
        }


    print(get_gateway())
    print(get_token())
    print(get_info())
    print(get_heartbeatrate())
while True:
    print('got into loop')
    time.sleep(20)
