from typing import List, Literal, Optional
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


# Get the config directory
CONFIG_DIR = Path(__file__).parent

class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(CONFIG_DIR / 'env' / 'settings.env'),
        env_file_encoding='utf-8',
    )

    kafka_broker_address: str
    kafka_input_topic: str
    kafka_output_topic: str
    kafka_consumer_group: str
    candle_seconds: List[int]
    emit_incomplete_candles: Optional[bool] = True
    data_source: Literal['live', 'historical', 'test']


candles_config = Config()
