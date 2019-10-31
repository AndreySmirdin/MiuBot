import json

import requests
import logging
import emoji

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s-%(name)s-%(levelname)s-%(message)s')

logger = logging.getLogger()

with open('token.txt', 'r') as f:
    TOKEN = json.load(f)['token']

URL = "https://api.telegram.org/bot{}/".format(TOKEN)


def send_request(url, params={}):
    response = requests.get(url, params)
    content = json.loads(response.content.decode("utf8"))
    if not content['ok']:
        logger.error(f"Request to {url} returned {content}")
    return content


def get_updates(update_id):
    url = URL + "getUpdates"
    params = {'allowed_updates': 'message'}
    if update_id is not None:
        params['offset'] = update_id
    response = send_request(url, params)
    return response['result']


def send_message(text, chat_id):
    logger.info(f"Answered to {chat_id}")
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    send_request(url)


def process_new_message(message):
    message = message["message"]
    chat_id = message["chat"]["id"]
    text = message["text"]
    text = text.lower()

    if 'entities' in message and message['entities'][0]['type'] == 'bot_command':
        if text == '/woof':
            send_message(emoji.emojize(':thumbs_down:'), chat_id)
        if text == '/miu':
            send_message(emoji.emojize(':thumbs_up:'), chat_id)
        return

    if "миу" in text:
        send_message("миу", chat_id)
    if "мяу" in text:
        send_message('не "мяу", а "миу"!', chat_id)
    if "гав" in text:
        send_message('не "гав", а "/woof"! ', chat_id)
