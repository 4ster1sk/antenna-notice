import json
import dataclasses
import re
import sys
import os
import logging
import requests
import rel
import threading
from pprint import pprint
from logging import StreamHandler, FileHandler, Formatter
from config import Config
from ws import MisskeyWs

logger = logging.getLogger(__name__)

CONFIG_PATH=f'{os.path.dirname(os.path.abspath(__file__))}/config.json'

def filter(text:str) -> bool:
    for pattern in config.deny_filter:
        if (re.search(pattern, text)):
            logger.debug(f"Deny Filter: {pattern} / {text}")
            return False
    
    '''
    for pattern in config.accept_filter:
        if (re.search(pattern, text)):
            logger.debug(f"Accept Filter: {pattern} / {text}")
            break
    '''
    
    return True

def notice(username : str, avatar_url:str, content:str) -> None:
    payload = {
        'username': username,
        'avatar_url': avatar_url,
        'content': content
    }

    headers = {'Content-Type': 'application/json'}
    response = requests.post(
        config.discord_webhook,
        json.dumps(payload),
        headers=headers)

def on_message(ws, message):
    js = json.loads(message)
    if "body" in js:
        body = js['body']['body']
        username : str = body['user']['name']
        avatar_url : str = body['user']['avatarUrl']
        content : str = f'https://{config.host}/notes/{body["id"]}'
        if (filter(content)):
            logger.info(f"{username} / {content}")
            notice(username, avatar_url, content)

def save(config:Config, latest_id: str):
    _c = dataclasses.replace(config)
    #_c.since_id = latest_id
    with open(CONFIG_PATH, 'w') as f:
        json.dump(dataclasses.asdict(_c), fp=f, ensure_ascii=False, indent=4)

def init():
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def app_quit():
    sys.exit()

if __name__ == "__main__":    
    init()
    with open(CONFIG_PATH, 'r') as f:
        config = Config(**json.load(f))

    m = MisskeyWs(logger,config)
    m_task = threading.Thread(target=m.connect, args=(on_message,))
    m_task.start()
    logger.debug("Started")
    rel.signal(2, app_quit)  # Keyboard Interrupt
