from loguru import logger
from quixstreams import Application

from api.base import TradesAPI
from api.mock import KrakenMockAPI
from api.rest import KrakenRestAPI
from api.websocket import KrakenWebsocketAPI


def pipeline(
    kafka_broker_address: str,
    kafka_topic: str,
    trades_api: TradesAPI,
) -> None:
    """
    Pipeline that:
    1. Reads trades from the Kraken API and
    2. Pushes them to a Kafka topic.

    Args:
        kafka_broker_address: str
        kafka_topic: str
        trades_api: TradesAPI (with 2 methods: get_trades and is_done)

    Returns:
        None
    """
    logger.info('Start the trades service')

    # Initialize the Quix Streams application.
    # This class handles all the low-level details to connect to Kafka.
    app = Application(
        broker_address=kafka_broker_address,
    )

    # Define the topic where we will push the trades to
    topic = app.topic(name=kafka_topic, value_serializer='json')

    with app.get_producer() as producer:
        while not trades_api.is_done():
            trades = trades_api.get_trades()

            for trade in trades:
                # Serialize the trade to a JSON string
                message = topic.serialize(
                    key=f"{trade.pair.replace('/', '-')}",  # Unique key for the trade - overwrites the previous trade (if applicable)
                    value=trade.to_dict(),
                )

                # Push the trade to the Kafka topic
                producer.produce(topic=topic.name, value=message.value, key=message.key)

                logger.info(f'Pushed trade to Kafka (topic={kafka_topic}): {trade}')


if __name__ == '__main__':
    from config.config import api_config

    # Initialize the Kraken API depending on the data source
    if api_config.data_source == 'live':
        logger.info('Using the Kraken Websocket API')
        kraken_api = KrakenWebsocketAPI(pairs=api_config.pairs)
    elif api_config.data_source == 'historical':
        logger.info('Using the Kraken REST API')
        kraken_api = KrakenRestAPI(pairs=api_config.pairs, last_n_days=api_config.last_n_days)
    elif api_config.data_source == 'test':
        logger.info('Using the Kraken Mock API')
        kraken_api = KrakenMockAPI(pairs=api_config.pairs)
    else:
        raise ValueError(f'Invalid data source: {api_config.data_source}')

    pipeline(
        kafka_broker_address=api_config.kafka_broker_address,
        kafka_topic=api_config.kafka_topic,
        trades_api=kraken_api,
    )
