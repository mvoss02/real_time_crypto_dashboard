run-dev-dashboard:
	@echo "Run dashboard in local development mode..."
	uv run streamlit run dashboard_run.py

run-dev-feature-reader:
	@echo "Testing the feature reader without dashboard..."
	uv run python -m utils.feature_reader

build:
	docker build -f Dockerfile -t dashboard .

run-with-docker: build
	@echo "Running the dashboard with docker..."
	docker run -it \
		--network redpanda_network \
		-e KAFKA_BROKER_ADDRESS=redpanda:9092 \
		-p 8501:8501 \
		dashboard