import os
import praw
import time
import gevent
import requests
import json
from websocket import create_connection
from dotenv import load_dotenv
from imgurpython import ImgurClient

load_dotenv()

client = os.getenv('client_id')
sec = os.getenv('my_client_secret')
U_Agent = os.getenv('user_agent')
ImgurID = os.getenv('IMGUR_ID')
ImgurSecret = os.getenv('IMGUR_SECRET')
uri = 'wss://gateway.discord.gg/?v=8&encoding=json'

imgur = ImgurClient(ImgurID, ImgurSecret)

reddit = praw.Reddit(
     client_id=client,
     client_secret=sec,
     user_agent=U_Agent
     )


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


class HTTP(Data):

    def get_gateway(self, API_ENDPOINT):
        response = requests.get(f'{API_ENDPOINT}/gateway').json()
        data = response['url']
        print("got gateway")
        return data

    # def get_bot_gateway(self, API_ENDPOINT):
    #     response = requests.get(f'{API_ENDPOINT}/gateway/bot').json()
    #     data = response['url']
    #     print("got bot gateway")
    #     return data

    def get_heartbeat(self, data):
        conn = create_connection(data)
        result = conn.recv()
        result_json = json.loads(result)
        json_slice = result_json['d']
        heartbeat = json_slice['heartbeat_interval']
        print("got heartbeat")
        return heartbeat

    def send_heartbeat(self, data, heartbeat, opcode1):
        while True:
            print("sending heartbeat")
            conn = create_connection(data)
            packet = json.dumps(opcode1)
            conn.send(packet)
            gevent.sleep(heartbeat / 1000)
            print("heartbeat sent")

    def send_identity(self, data, pack):
        print(data)
        conn = create_connection(data)
        packet = json.dumps(pack)
        conn.send(packet)
        print("pack sent")


class Client:
    def __init__(self):
        super(Client, self).__init__()
        self.http = HTTP


HTTP.get_gateway(HTTP, API_ENDPOINT=Data.API_ENDPOINT)
HTTP.get_heartbeat(HTTP,HTTP.get_gateway(HTTP, API_ENDPOINT=Data.API_ENDPOINT))
HTTP.send_identity(HTTP, data=HTTP.get_gateway(HTTP, API_ENDPOINT=Data.API_ENDPOINT), pack=Data.pack)
gevent.spawn(HTTP.send_heartbeat(HTTP, HTTP.get_gateway(HTTP, API_ENDPOINT=Data.API_ENDPOINT),
                                 heartbeat=HTTP.get_heartbeat(HTTP, data=HTTP.get_gateway(HTTP, API_ENDPOINT=Data.API_ENDPOINT)),
                                 opcode1=Data.opcode1))

if __name__ == '__main__':
    while True:
        print('end')
        time.sleep(5)
