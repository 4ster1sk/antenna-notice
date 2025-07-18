from logging import Logger
import websocket
import traceback
import json

from config import Config

class MisskeyWs():
    def __init__(self, logger:Logger ,config:Config):
        self.logger = logger
        self.is_alive = True
        self.ws = None
        self.config = config


    def on_error(self, ws, error):
        self.logger.error(f'Error: {type(error)} - {error}')
        self.logger.error('Stack trace:\n' + ''.join(traceback.format_exception(type(error), error, error.__traceback__)))
        if (isinstance(error, KeyboardInterrupt)):
            self.logger.debug(f'KeyboardInterrupt')
            self.is_alive = False

    def on_close(self, ws, close_status_code, close_msg):
        self.logger.info('### closed reconnect###')
        if (self.is_alive):
            return

    def on_open(self, ws):
        self.logger.info('Connected')
        
        _reqs = []
        #_reqs.append({'type': 'connect','body': {'channel': 'antenna','id': '1','params':{'antennaId': self.config.antenna_id}}})
        _reqs.append({'type': 'connect','body': {'channel': 'homeTimeline','id': '2','params':{}}})

        for l in _reqs:
            s = json.dumps(l)
            ws.send(s)
            self.logger.info('Sent Requests'+s)
            

    def connect(self, on_message):
        self.logger.info(f'HOST:{self.config.host} Connecting...')
        self.ws = websocket.WebSocketApp(
            f'wss://{self.config.host}/streaming?i={self.config.token}',
            on_message = on_message,
            on_error = self.on_error,
            on_close =self. on_close,
            on_open = self.on_open)
        
        self.ws.run_forever(ping_interval=10, reconnect=10)

    def stop(self):
        self.logger.debug('Stop')
        if (self.ws is not None):
            self.ws.close()