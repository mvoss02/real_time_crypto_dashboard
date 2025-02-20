from datetime import datetime
from time import sleep
import random
from typing import List

from .trade import Trade
from .base import TradesAPI


class KrakenMockAPI(TradesAPI):
    def __init__(self, pair: str):
        self.pair = pair

    def get_trades(self) -> List[Trade]:
        """
        Returns a list of mock trades to resemble the Kraken API.
        """
        
        # Mock trades
        mock_trades = [
            Trade(
                pair=self.pair,
                price=random.randint(1, 100) + random.uniform(0, 1),
                volume=random.randint(1, 100),
                timestamp=datetime(2023, 9, 25, 7, 49, 37, 708706),
                timestamp_ms=172719357708706,
            ),
            Trade(
                pair=self.pair,
                price=random.randint(1, 100) + random.uniform(0, 1),
                volume=random.randint(1, 100),
                timestamp=datetime(2023, 9, 25, 7, 49, 37, 708706),
                timestamp_ms=172719357708706,
            ),
        ]

        # Simulate the API call taking some time
        sleep(1)

        return mock_trades
    
    def is_done(self) -> bool:
        # The mock API is never done, unless stopped manually
        return False
