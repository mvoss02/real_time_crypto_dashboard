run-dev-live:
	@echo "Running live upload to candle feature group"
	cp ./config/env/live.settings.env ./config/env/settings.env
	uv run python run.py

run-dev-historical:
	@echo "Running historical upload to candle feature group"
	cp ./config/env/historical.settings.env ./config/env/settings.env
	uv run python run.py

build:
	docker build -f Dockerfile -t feature_store .

run-with-docker: build
	docker run -it \
		--network redpanda_network \
		-e KAFKA_BROKER_ADDRESS=redpanda:9092 \
		feature_store