from datetime import timedelta
from typing import Any, List, Optional, Tuple
from dataclasses import dataclass
from loguru import logger
from quixstreams import Application
from quixstreams.dataframe.dataframe import StreamingDataFrame
from quixstreams.models import TimestampType
import time


@dataclass
class CandleLength:
    window_seconds: int
    description: str
    

class MultiTimeframeStreamReader:
    @staticmethod
    def custom_ts_extractor(
        value: Any,
        headers: Optional[List[Tuple[str, bytes]]],
        timestamp: float,
        timestamp_type: TimestampType,
    ) -> int:
        return value['timestamp_ms']
    
    def __init__(
        self,
        kafka_broker_address: str,
        kafka_input_topic: str,
        kafka_output_topic: str,
        kafka_consumer_group: str,
        candle_configs: List[CandleLength],
        data_source: str,
        emit_incomplete_candles: bool,
        inactivity_timeout_seconds: int = 60  # Default 60 seconds timeout
    ):
        self.candle_configs = candle_configs
        self.data_source = data_source
        self.emit_incomplete_candles = emit_incomplete_candles
        self.inactivity_timeout_seconds = inactivity_timeout_seconds
        self.last_message_time = None
        
        # Initialize the Quix Streams application
        self._app = Application(
            broker_address=kafka_broker_address,
            consumer_group=kafka_consumer_group,
            auto_offset_reset='latest' if data_source == 'live' else 'earliest',
        )

        # Define input and output topics
        self.input_topic = self._app.topic(
            name=kafka_input_topic,
            key_deserializer='string',
            value_deserializer='json',
            timestamp_extractor=self.custom_ts_extractor,
        )
        
        self.output_topic = self._app.topic(
            name=kafka_output_topic,
            value_serializer='json',
        )

    @staticmethod
    def _init_candle(trade: dict) -> dict:
        return {
            'open': trade['price'],
            'high': trade['price'],
            'low': trade['price'],
            'close': trade['price'],
            'volume': trade['volume'],
            'timestamp_ms': trade['timestamp_ms'],
            'pair': trade['pair'],
        }

    @staticmethod
    def _update_candle(candle: dict, trade: dict) -> dict:
        candle['close'] = trade['price']
        candle['high'] = max(candle['high'], trade['price'])
        candle['low'] = min(candle['low'], trade['price'])
        candle['volume'] += trade['volume']
        candle['timestamp_ms'] = trade['timestamp_ms']
        candle['pair'] = trade['pair']
        return candle

    def process_timeframe(self, streaming_df: StreamingDataFrame, window_length: CandleLength):
        """Process a single timeframe and output candles"""
        
        # Aggregation of trades into candles using tumbling windows
        candle_df = (
            streaming_df.tumbling_window(timedelta(seconds=window_length.window_seconds))
            .reduce(
                reducer=self._update_candle,
                initializer=self._init_candle
            )
        )

        # Check if we want to include only complete candles or also partial ones
        if self.emit_incomplete_candles:
            candle_df = candle_df.current()  # Partial
        else:
            candle_df = candle_df.final()  # Complete

        # Extract fields from the dataframe
        candle_df['open'] = candle_df['value']['open']
        candle_df['high'] = candle_df['value']['high']
        candle_df['low'] = candle_df['value']['low']
        candle_df['close'] = candle_df['value']['close']
        candle_df['volume'] = candle_df['value']['volume']
        candle_df['timestamp_ms'] = candle_df['value']['timestamp_ms']
        candle_df['pair'] = candle_df['value']['pair']
        candle_df['window_start_ms'] = candle_df['start']
        candle_df['window_end_ms'] = candle_df['end']

        # Keep only the relevant columns
        candle_df = candle_df[
            [
                'pair',
                'timestamp_ms',
                'open',
                'high',
                'low',
                'close',
                'volume',
                'window_start_ms',
                'window_end_ms',
            ]
        ]

        # Add the window seconds
        candle_df['candle_seconds'] = window_length.window_seconds

        # Log candles
        candle_df = candle_df.update(lambda value: logger.info(f'Candle: {value}'))
        
        # Add inactivity checking to the stream
        candle_df = candle_df.update(self.check_inactivity)

        # Push to output topic
        candle_df.to_topic(self.output_topic)

    def process_all_timeframes(self, streaming_df: StreamingDataFrame):
        """Process all timeframes in parallel"""
        for config in self.candle_configs:
            self.process_timeframe(streaming_df, config)
    
    def check_inactivity(self, value: dict) -> None:
        """Update the last message time and check for inactivity"""
        current_time = time.time()
        self.last_message_time = current_time
        
    def is_inactive(self) -> bool:
        """Check if the stream has been inactive"""
        if self.last_message_time is None:
            return False
            
        current_time = time.time()
        inactive_duration = current_time - self.last_message_time
        
        if inactive_duration > self.inactivity_timeout_seconds:
            logger.warning(f"Stream inactive for {inactive_duration:.2f} seconds. Stopping processing.")
            return True
            
        return False

    def run(self) -> None:
        """Main processing loop with different behavior for live/historical"""
        try:
            streaming_df = self._app.dataframe(topic=self.input_topic)
            self.process_all_timeframes(streaming_df)
            
            if self.data_source == 'historical':
                # Historical processing with inactivity monitoring
                logger.info("Starting historical data processing...")
                while not self.is_inactive():
                    self._app.run()  # Process with timeout
                    time.sleep(0.1)  # Small delay to prevent CPU spinning
                logger.warning("Historical processing complete - stopping manually")
            else:
                # Live processing - continuous stream
                logger.info("Starting live data processing...")
                self._app.run()
                
        except Exception as e:
            logger.error(f"Error in processing: {str(e)}")
            raise


# Example usage:
if __name__ == "__main__":
    from config.config import candles_config
    
    window_lengths = [
        CandleLength(window_seconds=sec, description=str(sec) + 'sec') 
        for sec in candles_config.candle_seconds
    ]
    
    reader = MultiTimeframeStreamReader(
        kafka_broker_address=candles_config.kafka_broker_address,
        kafka_input_topic=candles_config.kafka_input_topic,
        kafka_output_topic=candles_config.kafka_output_topic,
        kafka_consumer_group=candles_config.kafka_consumer_group,
        candle_configs=window_lengths,
        data_source=candles_config.data_source,
        emit_incomplete_candles=candles_config.emit_incomplete_candles,
        inactivity_timeout_seconds=60  # Adjust this value based on your needs
    )
    
    reader.run()