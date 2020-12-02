import os
from dotenv import load_dotenv
load_dotenv()


class Data:
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
                "$os": "windows",
                "$browser": "my_library",
                "$device": "my_library"
            }
        }
    }
