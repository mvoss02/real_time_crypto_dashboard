# Trades Ingestion Service

A service component of the Real Time Crypto Dashboard that handles both historical and real-time trade data ingestion from the Kraken cryptocurrency exchange. This service supports two modes of operation:

- Historical data ingestion via the REST API
- Real-time data streaming via WebSocket

## Features

- **Dual Ingestion Modes**: Flexible data collection from both REST and WebSocket APIs
- **Historical Backfilling**: Ability to fetch and process historical trade data
- **Real-time Streaming**: Live trade data ingestion via WebSocket connection
- **Kafka Integration**: Pushes processed trade data to a dedicated Kafka topic
- **Error Handling**: Robust error management for API failures and connection issues
- **Data Validation**: Uses Pydantic models to ensure data integrity

## Prerequisites

- Python 3.12+
- Kraken API credentials (for authenticated endpoints)
- Running Kafka/Redpanda instance
- Network access to Kraken's API endpoints

## Installation

Initialize the service environment:

```bash
cd services/trades_ingestion
uv init
```

## Configuration

The configurations can be changed under ./config/env/ -> Go to the corresponding settings file

## Usage

### Historical Data Ingestion

To backfill historical trade data:

```bash
make run-dev-historical
```

NOTE: If you want to change settings go to ./config/env/

### Real-time Data Streaming

To start real-time trade ingestion:

```bash
make run-dev-live
```

NOTE: If you want to change settings go to ./config/env/

## Error Handling

The service implements the following error handling strategies:

- Automatic WebSocket reconnection on connection loss
- Exponential backoff for REST API rate limiting
- Detailed logging of all errors and warnings
- Graceful shutdown on critical failures

## Monitoring

The service logs important metrics and events using the `loguru` library:

- Connection status changes
- Trade ingestion rates
- Error occurrences and types
- API rate limit status

## Development

### Adding New Features

1. Create a new branch:

```bash
git checkout -b feature/your-feature-name
```

2. Implement your changes following the project's code style
3. Add tests for new functionality
4. Submit a pull request

### Code Style

This service follows the project's global code style guidelines:

- Uses `ruff` for linting and formatting
- Follows PEP 8 conventions
- Requires type hints for all functions

## Dependencies

- `requests`: HTTP client for REST API calls
- `websocket-client`: WebSocket client for real-time data
- `quixstreams`: Kafka client library
- `pydantic`: Data validation
- `loguru`: Logging utility

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request
