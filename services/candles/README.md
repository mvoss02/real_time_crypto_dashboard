# Candles Service

A service component of the Real Time Crypto Dashboard that transforms raw trade data into OHLC (Open, High, Low, Close) candlestick data. The service supports multiple cryptocurrency pairs, flexible time windows, and both historical and real-time processing modes.

## Features

- **Flexible Time Windows**: Configurable candle intervals (1m, 5m, 15m, 1h, 4h, 1d)
- **Multi-Pair Support**: Process multiple trading pairs simultaneously
- **Real-time Processing**: Stream-based trade to candle conversion
- **Historical Aggregation**: Batch processing of historical trade data
- **Data Validation**: Ensures data consistency and completeness
- **Window Management**: Handles edge cases like missing data and time boundaries
- **Efficient Processing**: Uses sliding window aggregation for optimal performance

## Architecture

The service follows a stream processing architecture:

1. Consumes trade data from the `trades` Kafka topic
2. Groups trades by pair and time window
3. Calculates OHLC metrics for each window
4. Publishes completed candles to the `candles` topic

## Prerequisites

- Python 3.12+
- Running Kafka/Redpanda instance
- Access to the trades topic

## Installation

Initialize the service environment:

```bash
cd services/candles
uv init
```

## Configuration

The configurations can be changed under ./config/env/ -> Go to the corresponding settings file

## Usage

### Starting the Service

For real-time processing:

```bash
make run-dev-live
```

### Processing Historical Data

For batch processing of historical data:

```bash
make run-dev-historical
```

## Data Format

### Output Candle Data

```python
{
    "pair": str,           # Trading pair
    "candle_seconds": int,    # Candle interval in seconds
    "start_time": float,   # Window start timestamp
    "end_time": float,     # Window end timestamp
    "open": float,         # Opening price
    "high": float,         # Highest price
    "low": float,          # Lowest price
    "close": float,        # Closing price
    "volume": float,       # Total volume
}
```

## Algorithm

The service uses a sliding window algorithm for candle generation:

1. **Window Creation**:

   - Determines window boundaries based on trade timestamps
   - Maintains separate windows for each pair and interval

2. **Trade Processing**:

   - Updates running OHLC values for active windows
   - Tracks volume and trade counts
   - Calculates VWAP (Volume-Weighted Average Price)

3. **Window Completion**:
   - Emits candles when window time is reached
   - Handles partial windows at stream boundaries
   - Ensures no data loss during window transitions

## Error Handling

The service implements robust error handling:

- Detects and logs data gaps
- Handles out-of-order trades
- Manages memory usage for long-running windows
- Provides clear error messages for invalid configurations

## Monitoring

Key metrics tracked by the service:

- Trades processed per second
- Candles generated per window
- Processing lag
- Memory usage
- Error rates

## Development

### Adding New Features

1. Create a new branch:

```bash
git checkout -b feature/your-feature-name
```

2. Implement your changes following the project's code style
3. Add tests for new functionality
4. Submit a pull request

## Dependencies

Primary dependencies include:

- `quixstreams`: Kafka client library
- `pydantic`: Data validation
- `numpy`: Numerical computations
- `loguru`: Logging utility

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request
