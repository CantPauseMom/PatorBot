import os
import time
from dotenv import load_dotenv
from http import HTTP
load_dotenv()

client = os.getenv('client_id')
sec = os.getenv('my_client_secret')
U_Agent = os.getenv('user_agent')
ImgurID = os.getenv('IMGUR_ID')
ImgurSecret = os.getenv('IMGUR_SECRET')
uri = 'wss://gateway.discord.gg/?v=8&encoding=json'

HTTP.get_gateway()

if __name__ == '__main__':
    while True:
        print('end')
        time.sleep(5)