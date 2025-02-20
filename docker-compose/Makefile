# Redpanda-related Commands
start-redpanda:
	@echo "Starting Redpanda"
	docker compose -f redpanda.yml up -d

stop-redpanda:
	@echo "Stopping Redpanda"
	docker compose -f redpanda.yml down

# Remove unused Kafka topic after backfill operations
clean-backfill-kakfa-topics:
	@echo "Removing all Kafka topics that contain the word historical"
	docker compose -f redpanda.yml exec redpanda rpk topic delete -r ".*historical.*"

# Remove Kafka topics related to changelogs
clean-changelog-kafka-topics:
	@echo "Removing all Kafka topics that contain the word changelog"
	docker compose -f redpanda.yml exec redpanda rpk topic delete -r ".*changelog.*"