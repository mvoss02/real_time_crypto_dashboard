run-dev-live:
	@echo "Running live candle transformation"
	cp ./config/env/live.settings.env ./config/env/settings.env
	uv run python trades_to_candles.py

run-dev-historical:
	@echo "Running historical candle transformation"
	cp ./config/env/historical.settings.env ./config/env/settings.env
	uv run python trades_to_candles.py

build:
	@echo "Building candles image"
	docker build -f Dockerfile -t candles .

run-with-docker: build
	@echo "Running candles image"
	docker run -it \
		--network redpanda_network \
		-e KAFKA_BROKER_ADDRESS=redpanda:9092 \
		candles