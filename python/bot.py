import json

import requests
import logging
import emoji

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s-%(name)s-%(levelname)s-%(message)s')

logger = logging.getLogger()

with open('token.txt', 'r') as f:
    TOKEN = json.load(f)['token']

GET_UPDATES = "getUpdates"
SEND_MESSAGE = "sendMessage"


def send_request(method_name, params={}):
    url = "https://api.telegram.org/bot{}/".format(TOKEN) + method_name
    response = requests.get(url, params)
    content = json.loads(response.content.decode("utf8"))
    if not content['ok']:
        raise RuntimeError(url, content)
    return content


def get_updates(update_id):
    params = {'allowed_updates': 'message',
              'timeout': 10}  # Allows to use long polling
    if update_id is not None:
        params['offset'] = update_id
    response = send_request(GET_UPDATES, params)
    return response['result']


def send_message(text, chat_id):
    logger.info(f"Answered to {chat_id}")
    try:
        send_request(SEND_MESSAGE, params={"text": text,
                                           "chat_id": chat_id})
    except:
        logger.info(f"Couldn't send a message to user {chat_id}")


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

    elif "миу" in text:
        send_message("миу", chat_id)
    elif "мяу" in text:
        send_message('не "мяу", а "миу"!', chat_id)
    elif "гав" in text:
        send_message('не "гав", а "/woof"! ', chat_id)
