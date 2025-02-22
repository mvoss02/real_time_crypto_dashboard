# Redpanda-related Commands
start-redpanda:
	@echo "Starting Redpanda"
	docker compose -f redpanda.yml up -d

stop-redpanda:
	@echo "Stopping Redpanda"
	docker compose -f redpanda.yml down


# Data Pieplines
## for live data
build-dashboard-pipeline-live:
	docker compose -f dashboard-pipeline-live.yaml build

start-dashboard-pipeline-live: build-dashboard-pipeline-live
	docker compose -f dashboard-pipeline-live.yaml up -d

stop-dashboard-pipeline-live:
	docker compose -f dashboard-pipeline-live.yaml down

## for historical data
build-data-backfill-historical:
	docker compose -f data-backfill-historical.yml build
	
backfill-data: build-data-backfill-historical
	$(eval RUN_ID := $(shell uuidgen))
	@echo "Starting backfill with RUN_ID: $(RUN_ID)"
	RUN_ID=$(RUN_ID) docker compose -f data-backfill-historical.yaml up -d


# Remove unused Kafka topic after backfill operations
clean-backfill-kakfa-topics:
	@echo "Removing all Kafka topics that contain the word historical"
	docker compose -f redpanda.yml exec redpanda rpk topic delete -r ".*historical.*"

# Remove Kafka topics related to changelogs
clean-changelog-kafka-topics:
	@echo "Removing all Kafka topics that contain the word changelog"
	docker compose -f redpanda.yml exec redpanda rpk topic delete -r ".*changelog.*"