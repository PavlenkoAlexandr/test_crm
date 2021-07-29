import os

import requests
from local_settings import TELEGRAM_TOKEN

BASE_URL = 'https://api.telegram.org/bot'
TOKEN = os.environ.get('DJANGO_TELEGRAM_TOKEN', TELEGRAM_TOKEN)


def create_url(token, method):
    url = f'{BASE_URL}{token}/{method}'
    return url


def get_update():
    method = 'getUpdates'
    request = requests.get(create_url(TOKEN, method))
    return request


def get_chat_id(username: str):
    updates = get_update().json()
    for result in updates['result']:
        if result['message']['chat']['username'] == username.replace('@', ''):
            return result['message']['chat']['id']
    return updates


def send_message(to, text):
    method = 'sendMessage'
    params = {
        'chat_id': to,
        'text': text,
    }
    url = create_url(TOKEN, method)
    request = requests.post(url, params=params)
    return request.json()
