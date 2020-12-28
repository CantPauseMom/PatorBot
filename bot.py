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

    def get_heartbeat():
        result = conn.recv()
        result_json = json.loads(result)
        json_slice = result_json['d']
        heartbeat = json_slice['heartbeat_interval']
        return heartbeat

    def send_heartbeat():
        while True:
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
                break

    tr = threading.Thread(target=get_ready)
    tr.daemon = True
    tr.start()


    def listen():
        while True:
            #time.sleep(0.2)
            result = conn.recv()

            json_object = json.loads(result)
            name = json_object['t']
            print(str(result))
            if name == "MESSAGE_CREATE":
                sliced = json_object['d']['content']
                if sliced == '!hello':
                    id = json_object['d']['channel_id']
                    name = json_object['d']['author']['username']
                    example = {
                        "content": f"Hello, {name}",
                        "tts": False
                    }
                    headers = {'Content-Type': 'application/json',
                               'Authorization': f'Bot {token}'}
                    msg = json.dumps(example)
                    print(msg)
                    new1 = requests.session()
                    new = new1.post(f'{API_endpoint}/channels/{id}/messages',
                                    headers=headers, data=msg)
                    new.raise_for_status()
                    print(new)
                if sliced == '!temp':
                    id = json_object['d']['channel_id']
                    name = json_object['d']['author']['username']
                    example = {
                        "content": f"Ty się {name} nadajesz",
                        "tts": False
                    }
                    headers = {'Content-Type': 'application/json',
                               'Authorization': f'Bot {token}'}
                    msg = json.dumps(example)
                    print(msg)
                    new1 = requests.session()
                    new = new1.post(f'{API_endpoint}/channels/{id}/messages',
                                    headers=headers, data=msg)
                    new.raise_for_status()
                    print(new)
                if sliced == '!help':
                    id = json_object['d']['channel_id']
                    example = {
                        "content": f"Available commands:\n"
                                   f"!help\n"
                                   f"!hello\n"
                                   f"!temp",
                        "tts": False
                    }
                    headers = {'Content-Type': 'application/json',
                               'Authorization': f'Bot {token}'}
                    msg = json.dumps(example)
                    new1 = requests.session()
                    new = new1.post(f'{API_endpoint}/channels/{id}/messages',
                                    headers=headers, data=msg)
                    new.raise_for_status()
                if sliced == '!voice':
                    json_object = json.loads(result)
                    guild_id = json_object['d']['guild_id']
                    voice1 = {
                        "op": 4,
                        "d": {
                            "guild_id": f"{guild_id}",
                            "channel_id": "643895289081495566",
                            "self_mute": False,
                            "self_deaf": False
                        }
                    }
                    voice = json.dumps(voice1)
                    conn.send(voice)



    listener = threading.Thread(target=listen)
    listener.daemon = True
    listener.start()

    try:
        pass
    except KeyboardInterrupt:
        print('end')
        conn.close()
        exit()
        #--audio-format FORMAT

    #https: // www.youtube.com / watch?v = Kd8EDlm83Fc & feature = youtu.be
if __name__ == '__main__':
    connection()
    while True:
        time.sleep(5)

