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
from config import Config
from ws import MisskeyWs

logger = logging.getLogger(__name__)

CONFIG_PATH=f'{os.path.dirname(os.path.abspath(__file__))}/config.json'

LOG_LEVELS = {
    "CRITICAL": logging.CRITICAL,
    "ERROR": logging.ERROR,
    "WARNING": logging.WARNING,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
    "NOTSET": logging.NOTSET,
}

def filter(text:str) -> bool:
    if (config.allow_filter):
        for pattern in config.allow_filter:
            if (re.search(pattern, text)):
                return True
    
    for pattern in config.deny_filter:
        if (re.search(pattern, text)):
            return False
    
    return config.is_filter_allow_mode

def notice(name:str, avatar_url:str, content:str):
    payload = {
        'username': name,
        'avatar_url': avatar_url,
        'content': content
    }

    headers = {'Content-Type': 'application/json'}
    requests.post(
        config.discord_webhook,
        json.dumps(payload),
        headers=headers)

def on_note(body:dict):
    #logger.debug(f'on_note(): {body}')
    name : str = body['user']['name']
    avatar_url : str = body['user']['avatarUrl']
    content : str = f'https://{config.host}/notes/{body["id"]}'
    if (filter(content)):
        logger.info(f'{name} / {content}')
        notice(name, avatar_url, content)

def on_stats(body:dict):
    pass

def on_notification(body_type:str, body:dict):
    pass


def save(config:Config, latest_id: str):
    _c = dataclasses.replace(config)
    _c.since_id = latest_id
    with open(CONFIG_PATH, 'w') as f:
        json.dump(dataclasses.asdict(_c), fp=f, ensure_ascii=False, indent=4)

def app_quit():
    sys.exit()

if __name__ == '__main__':
    with open(CONFIG_PATH, 'r') as f:
        config = Config(**json.load(f))
        
    logging_format = '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    logging.basicConfig(
        level=LOG_LEVELS.get(config.loglevel.upper(), logging.INFO),
        format=logging_format)

    m = MisskeyWs(config)
    m_task = threading.Thread(
        target=m.connect,
        kwargs={'on_note': on_note,
                'on_stats': on_stats,
                'on_notification': on_notification})
    
    m_task.start()
    logger.info('Started')
    rel.signal(2, app_quit)  # Keyboard Interrupt
