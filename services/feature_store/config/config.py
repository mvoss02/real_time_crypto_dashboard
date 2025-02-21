from pathlib import Path

from typing import Literal, Optional

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Get the config directory
CONFIG_DIR = Path(__file__).parent

class HopsworksSettingsConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(CONFIG_DIR / 'env' / 'settings.env'),
        env_file_encoding='utf-8',
    )

    kafka_broker_address: str
    kafka_input_topic: str
    kafka_consumer_group: str

    feature_group_name: str
    feature_group_version: int
    feature_group_primary_keys: list[str]
    feature_group_event_time: str
    feature_group_materialization_interval_minutes: Optional[int] = 15

    data_source: Literal['live', 'historical', 'test']


hopsworksSettingsConfig = HopsworksSettingsConfig()


class HopsworksCredentialsConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(CONFIG_DIR  / 'env' / 'hopsworks_credentials.env'),
        env_file_encoding='utf-8',
    )

    api_key: str
    project_name: str


hopsworksCredentialsConfig = HopsworksCredentialsConfig()
