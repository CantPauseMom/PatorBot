import asyncio

from gevent import monkey

monkey.patch_all()
import threading
import json
import os
import time
import gevent
import requests
from websocket import create_connection
from dotenv import load_dotenv
from data import Data

load_dotenv()

client = os.getenv('client_id')
sec = os.getenv('my_client_secret')
U_Agent = os.getenv('user_agent')
ImgurID = os.getenv('IMGUR_ID')
ImgurSecret = os.getenv('IMGUR_SECRET')
token = os.getenv('DISCORD_TOKEN')
uri = 'wss://gateway.discord.gg/?v=8&encoding=json'
API_endpoint = 'https://discord.com/api/v8'


def connection():
    response = requests.get(f'{API_endpoint}/gateway').json()
    data = response['url']
    conn = create_connection(data)
    print('conn made')

    def get_heartbeat():
        result = conn.recv()
        result_json = json.loads(result)
        json_slice = result_json['d']
        heartbeat = json_slice['heartbeat_interval']
        print("got heartbeat")
        print('Heartbeat =', heartbeat)
        return heartbeat

    def send_heartbeat():
        while True:
            print("sending heartbeat")
            packet = json.dumps(Data.opcode1)
            conn.send(packet)
            gevent.sleep(41250 / 1000)

    thread = threading.Thread(target=send_heartbeat)
    thread.daemon = True
    thread.start()

    def send_token():
        packet = json.dumps(Data.pack)
        conn.send(packet)

    send_token()

    def get_ready():
        while True:
            time.sleep(1)
            result = conn.recv()
            result_json = json.loads(result)
            json_slice = result_json['op']
            if json_slice == 11:
                time.sleep(1)
                readymsg = conn.recv()
                print("Connection is ready")
                print(str(readymsg))
                test = conn.recv()
                print(str(test))
                break

    tr = threading.Thread(target=get_ready)
    tr.daemon = True
    tr.start()

    def listen():
        while True:
            print('in listen')
            time.sleep(0.2)
            result = conn.recv()
            print(result)

    listener = threading.Thread(target=listen)
    listener.daemon = True
    listener.start()

connection()


def get_me():
    response = requests.get(f'{API_endpoint}/oauth2/applications/@me').json()
    print(response)


def get_message():
    tex = requests.session()
    response = tex.get(f'{API_endpoint}/channels/788843646669422603/messages',
                       headers={'Authorization': f'Bot {token}'}).json()
    print(response)


def create_message():
    example = {
        "content": "Hello, World!",
        "tts": False,
        "embed": {
            "title": "Hello, Embed!",
            "description": "This is an embedded message."
        }
    }
    msg = json.dumps(example)
    print(msg)
    new = requests.post(f'{API_endpoint}/channels/788843646669422603/messages',
                        json=msg,
                        headers={'Authorization': f'Bot {token}',
                                 'Content-Type': 'application/json'})
    print(str(new))

create_message()
if __name__ == '__main__':
    while True:
        print('end')

        #get_message()
        time.sleep(5)
