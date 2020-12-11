import os
from dotenv import load_dotenv
load_dotenv()
client_id = os.getenv('client_id')


class Data:

    bot_link = f'https://discord.com/api/oauth2/authorize?client_id={client_id}&scope=bot&permissions=1'
    API_ENDPOINT = 'https://discord.com/api/v8'

    uri = "wss://gateway.discord.gg/"
    TOKEN = os.getenv('DISCORD_TOKEN')

    credentials = {
        'grant_type': 'client_credentials',
        'scope': 'bot'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    opcode1 = {
        "op": 1,
        "d": None
    }
    pack = {
        "op": 2,
        "d": {
            "token": TOKEN,
            "intents": 513,
            "properties": {
                "$os": "android",
                "$browser": "my_library",
                "$device": "my_library",
                "presence": {
                       "activities": [{
                           "name": "Senpai works on me",
                           "type": 0
                       }],
                       "status": "dnd",
                       "since": 91879201,
                       "afk": "false"
                },
            }
        }
    }
