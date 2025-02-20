run-dev-live:
	@echo "Running live trades ingestion"
	cp ./config/env/live.settings.env ./config/env/settings.env
	uv run python etl_pipeline.py

run-dev-historical:
	@echo "Running historical trades ingestion"
	cp ./config/env/historical.settings.env ./config/env/settings.env
	uv run python etl_pipeline.py

build:
	@echo "Building trades image"
	docker build -f Dockerfile -t trades .

run-with-docker: build
	@echo "Running trades image"
	docker run -it \
		--network redpanda_network \
		-e KAFKA_BROKER_ADDRESS=redpanda:9092 \
		trades