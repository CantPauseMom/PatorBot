import requests
import gevent
import json
import data
from websocket import create_connection


class HTTP:

    def __init__(self):


    def get_gateway(self):
        response = requests.get(f'{data.API_ENDPOINT}/gateway').json()
        data = response['url']
        print("got gateway")
        return data

    def make_connection(self, data):
        conn = create_connection(data)
        return conn

    def get_heartbeat(self, conn):
        result = conn.recv()
        result_json = json.loads(result)
        json_slice = result_json['d']
        heartbeat = json_slice['heartbeat_interval']
        print("got heartbeat")
        return heartbeat

    def send_heartbeat(self, heartbeat, opcode1, conn):
        while True:
            print("sending heartbeat")
            packet = json.dumps(opcode1)
            conn.send(packet)
            gevent.sleep(heartbeat / 1000)
            print("heartbeat sent")

    def send_identity(self, data, pack, conn):
        print(data)
        packet = json.dumps(pack)
        conn.send(packet)
        print("pack sent")