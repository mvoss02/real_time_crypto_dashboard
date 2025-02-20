# Real Time Crypto Dashboard

This project will display crypto candles for various crypto currencies in a Dashboard, using Kafka and Hopsworks as a Feature Store. The feature store is added to account for historic data. Also, the project acts as groundwork to build upon. For example, one could add a prediction service or news ingestion service. For now, it mainly focuses on the real-time data ingestion part.

## Initialize Project

1. Initialize a service

```bash
cd services
uv init SERVICE_NAME
```

2. Add ruff with uv:

```bash
uv tool install ruff
```

3. Add pre-commit:

In addition, one needs to add

```bash
uv tool install pre-commit
```

4. In order to automatically run pre-commit hooks add the
   following to files (search for files to your liking on the web):

- .pre-commit-config.yaml
- ruff.toml

5. Install pre-commit hooks:

```bash
pre-commit install
```

## Usage

1. Neuer Service

```bash
cd services
uv init NAME_OF_SERVICE
```

2. Packages
   2.1. Creating a package

```bash
uv init --lib MY_PACKAGE_NAME
```

- Project Structure:

```
real_time_pipeline/
├── packages/
│   ├── src/
│   │   ├── common/
│   │   │   ├── __init__.py
│   │   │   └── kafka_config.py
│   ├── pyproject.toml
│   └── requirements.lock
├── api_reader/
│   ├── src/
│   │   ├── __init__.py
│   │   └── api_reader.py   # API → OHLC → Kafka
│   ├── Dockerfile
│   ├── pyproject.toml
│   └── requirements.lock
├── dashboard/
│   ├── src/
│   │   ├── __init__.py
│   │   └── app.py         # Kafka → Streamlit
│   ├── Dockerfile
│   ├── pyproject.toml
│   └── requirements.lock
├── docker-compose.yml
└── README.md
```

2.2. Building a package

```bash
uv build
uv pip install pip install dist/MY_PACKAGE_NAME-0.1.0-py3-none-any.whl
```

2.3. Install package in development mode -> does not have to be re-installed with every change made

```bash
uv pip install -e .
```

- Weitere Informationen: [https://sarahglasmacher.com/how-to-build-python-package-uv/]
