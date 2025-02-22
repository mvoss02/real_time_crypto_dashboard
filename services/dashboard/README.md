# Dashboard Service

A service component of the Real Time Crypto Dashboard that provides an interactive Streamlit interface for visualizing cryptocurrency candlestick data. The dashboard fetches data from the Hopsworks Feature Store and displays real-time and historical price movements using Plotly charts.

## Features

- **Interactive Visualization**: Real-time candlestick charts with Plotly
- **Multiple Time Windows**: Support for different candle intervals
- **Multiple Trading Pairs**: View different cryptocurrency pairs
- **Historical Data View**: Access and display historical price data
- **Real-time Updates**: Live data updates from Feature Store
- **Docker Support**: Containerized deployment ready

## Prerequisites

- Python 3.12+
- Hopsworks account and API key
- Docker (for containerized deployment)
- Network access to Hopsworks Feature Store

## Installation

Initialize the service environment:

```bash
cd services/dashboard
uv init
```

## Configuration

The configurations can be changed under ./config/env/ -> Go to the corresponding settings file

## Usage

### Local Development

Run the dashboard locally:

```bash
make run-dev-dashboard
```

Test the feature reader component:

```bash
make run-dev-feature-reader
```

### Docker Deployment

Build and run the containerized service:

```bash
make run-with-docker
```

## Data Flow

1. **Data Fetching**:

   - Connects to Hopsworks Feature Store
   - Retrieves candlestick data for selected pairs
   - Handles both historical and real-time data

2. **Data Processing**:

   - Formats data for Plotly visualization
   - Calculates additional metrics if needed
   - Manages data update intervals

3. **Visualization**:
   - Renders interactive candlestick charts
   - Updates displays in real-time
   - Handles user interactions and filters

## Error Handling

The service implements the following error handling strategies:

- Graceful handling of Feature Store connection issues
- Data validation before visualization
- Automatic retry on failed data fetches
- User-friendly error messages

## Monitoring

Key metrics tracked by the service:

- Dashboard response time
- Data fetch latency
- Feature Store connection status
- Error occurrences
- User interaction metrics

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

- `streamlit`: Web application framework
- `plotly`: Interactive visualizations
- `hopsworks`: Feature Store client
- `pydantic`: Data validation
- `pydantic-settings`: Configuration management
- `loguru`: Logging utility

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request
