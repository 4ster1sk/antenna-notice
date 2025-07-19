import logging
import websocket
import traceback
import json
from config import Config

logger = logging.getLogger(__name__)

class MisskeyWs():
    def __init__(self ,config:Config):
        self.is_alive = True
        self.ws = None
        self.config = config


    def on_error(self, ws, error):
        if (isinstance(error, KeyboardInterrupt)):
            logger.debug(f'KeyboardInterrupt')
            self.is_alive = False
            return
        
        logger.error(f'Error: {type(error)} - {error}')
        logger.error('Stack trace:\n' + ''.join(traceback.format_exception(type(error), error, error.__traceback__)))

    def on_close(self, ws, close_status_code, close_msg):
        logger.info('### closed reconnect###')
        if (self.is_alive):
            return

    def on_open(self, ws):
        logger.info('Connected')
        
        _reqs = []
        _reqs.append({'type': 'connect', 'body': {'channel': 'main', 'id': '0'}})
        if (self.config.antenna_id):
            _reqs.append({'type': 'connect','body': {'channel': 'antenna','id': '1','params':{'antennaId': self.config.antenna_id}}})
        #_reqs.append({'type': 'connect','body': {'channel': 'homeTimeline','id': '2','params':{}}})
        #_reqs.append({'type': 'connect', 'body': {'channel': 'queueStats', 'id': '9'}})

        for l in _reqs:
            s = json.dumps(l)
            ws.send(s)
            logger.info('Sent Request'+s)
            

    def connect(self,
                on_note = None,
                on_stats = None,
                on_notification = None):
        self.on_note = on_note
        self.on_stats = on_stats
        self.on_notification = on_notification

        logger.info(f'Connecting... host:{self.config.host}')
        self.ws = websocket.WebSocketApp(
            f'wss://{self.config.host}/streaming?i={self.config.token}',
            on_message = self.on_message,
            on_error = self.on_error,
            on_close = self.on_close,
            on_open = self.on_open)
        
        self.ws.run_forever(ping_interval=10, reconnect=10)

    def stop(self):
        logger.debug('Stop')
        if (self.ws is not None):
            self.ws.close()
    
    def on_message(self, ws, message: str):
        j = json.loads(message)
        if (j['type'] == 'channel' and 'body' in j):
            match(j['body']['type']):
                case 'note':
                    self.on_note(j['body']['body'])
                    return
                
                case 'stats':
                    self.on_stats(j['body']['body'])
                    return

                case 'readAllNotifications' | 'notification' | 'unreadNotification':
                    self.on_notification(j['body']['type'], j['body']['body'])
                    return
                
                case 'registryUpdated':
                    return
                
                case _:
                    logger.debug(j)
                    return