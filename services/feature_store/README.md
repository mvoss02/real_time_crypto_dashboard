# Feature Store Service

A service component of the Real Time Crypto Dashboard that manages the persistence of candlestick data to Hopsworks Feature Store. This service handles both historical and real-time data uploads, ensuring data is properly stored and versioned for downstream applications.

## Features

- **Dual Operation Modes**: Supports both historical and real-time data ingestion
- **Hopsworks Integration**: Direct connection to Hopsworks Feature Store
- **Data Validation**: Ensures data quality before persistence
- **Configurable Upload Patterns**: Flexible configuration for different upload strategies
- **Docker Support**: Containerized deployment ready

## Prerequisites

- Python 3.12+
- Hopsworks account and API key
- Running Kafka/Redpanda instance
- Docker (for containerized deployment)

## Installation

Initialize the service environment:

```bash
cd services/feature-store
uv init
```

## Configuration

The configurations can be changed under ./config/env/ -> Go to the corresponding settings file

## Usage

### Local Development

For real-time data upload:

```bash
make run-dev-live
```

For historical data upload:

```bash
make run-dev-historical
```

### Docker Deployment

Build and run the containerized service:

```bash
make run-with-docker
```

## Data Flow

1. **Data Ingestion**:

   - Consumes candle data from Kafka topic
   - Validates data structure and types
   - Batches records for efficient upload

2. **Feature Store Upload**:

   - Connects to Hopsworks Feature Store
   - Creates or updates feature groups
   - Handles data insertion and updates
   - Manages feature group versions

3. **Error Handling**:
   - Retries failed uploads
   - Logs upload statistics
   - Reports connection issues

## Error Handling

The service implements the following error handling strategies:

- Automatic reconnection to Hopsworks
- Data validation before upload
- Failed record tracking
- Detailed error logging

## Monitoring

Key metrics tracked by the service:

- Records processed
- Upload success rate
- Processing latency
- Connection status
- Error counts

### Adding New Features

1. Create a new branch:

```bash
git checkout -b feature/your-feature-name
```

2. Implement your changes following the project's code style
3. Add tests for new functionality
4. Submit a pull request

## Docker Support

Build the container:

```bash
make build
```

Run with Docker:

```bash
make run-with-docker
```

## Dependencies

- `hopsworks`: Hopsworks Feature Store client
- `pandas`: Data manipulation
- `pyarrow`: Efficient data serialization
- `pydantic-settings`: Configuration management
- `quixstreams`: Kafka client
- `loguru`: Logging utility

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request
