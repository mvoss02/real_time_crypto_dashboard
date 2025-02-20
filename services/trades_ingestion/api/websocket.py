import ssl
import certifi

import json
from typing import List

from loguru import logger
from websocket import create_connection

from .base import TradesAPI
from .trade import Trade


class KrakenWebsocketAPI(TradesAPI):
    URL = 'wss://ws.kraken.com/v2'

    def __init__(self, pairs: List[str]):
        self.pairs = pairs

        # Create a websocket client
        self._ws_client = create_connection(
            self.URL,
            sslopt={"cert_reqs": ssl.CERT_REQUIRED, "ca_certs": certifi.where()},
        )

        # Subscribe to the websocket
        self._subscribe()

    def get_trades(self) -> List[Trade]:
        """
        Fetches the trades fromm the Kraken Websocket APIs and returns them as a list of Trade objects.

        Returns:
            List[Trade]: A list of Trade objects.
        """
        
        # Receive data from the websocket client
        data = self._ws_client.recv()

        if 'heartbeat' in data:
            logger.info('Heartbeat received')
            return []

        # Transform raw string data to JSON object
        try:
            data = json.loads(data)
        except json.JSONDecodeError as e:
            logger.error(f'Error decoding JSON: {e}')
            return []

        try:
            trades_data = data['data']
        except KeyError as e:
            logger.error(f'No `data` field with trades in the message {e}')
            return []

        trades = [
            Trade.from_kraken_websocket_api_response(
                pair=trade['symbol'],
                price=trade['price'],
                volume=trade['qty'],
                timestamp=trade['timestamp'],
            )
            for trade in trades_data
        ]
        
        return trades

    def is_done(self) -> bool:
        return False

    def _subscribe(self):
        """
        Subscribes to the websocket and waits for the initial snapshot.
        """
       
        # Sends the subscription message to the websocket
        self._ws_client.send(
            json.dumps(
                {
                    'method': 'subscribe',
                    'params': {
                        'channel': 'trade',
                        'symbol': self.pairs,
                        'snapshot': False,
                    },
                }
            )
        )

        for _ in self.pairs:
            _ = self._ws_client.recv()