all:
	@echo ""
	@echo "WarehousePG cluster observability setup"
	@echo ""
	@echo "build:    (Re)build the exporter image"
	@echo "run:      Start the containers for exporter, Prometheus, Grafana"
	@echo "status:   Show Docker compose status"
	@echo "stop:     Stops containers and Remove all artifacts"
	@echo "clean:    Remove all data dirs"


build:
	./build.sh

run:
	docker compose up -d

stop:
	docker compose down

.IGNORE: clean
clean:
	docker compose down
	rm ./docker-compose.yaml
	rm -rf ./prometheus/*
	rm -rf ./grafana/provisioning/datasources/*
	rm -rf ./warehouse-pg-observability-exporter/*
	rm -rf ./warehouse-pg-observability-exporter/.[!.]*
	rm -rf ./warehouse-pg-observability-exporter/..?*
	rmdir ./warehouse-pg-observability-exporter
	docker rmi whpg_exporter

status:
	docker ps -a
