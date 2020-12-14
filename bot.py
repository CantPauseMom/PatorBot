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

    # send_heartbeat(heartbeat=get_heartbeat())
    thread = threading.Thread(target=send_heartbeat)
    thread.daemon = True
    thread.start()

    def send_token():
        packet = json.dumps(Data.pack)
        conn.send(packet)
        print('packet sent')

    send_token()

    def get_ready():
        time.sleep(1)
        readymsg = conn.recv()
        print("in on_ready func")
        print(str(readymsg))

    tr = threading.Thread(target=get_ready)
    tr.daemon = True
    tr.start()


def somefunc():
    print('someloop')
    time.sleep(2)


connection()

if __name__ == '__main__':
    while True:
        print('end')
        time.sleep(5)
