all:
	@echo ""
	@echo "WarehousePG cluster observability setup"
	@echo ""
	@echo "build:    (Re)build the exporter image"
	@echo "run:      Start the containers for exporter, Prometheus, Grafana"
	@echo "status:   Show Docker compose status"
	@echo "clean:    Stope containers and Remove all artifacts"


build:
	./build.sh

run:
	docker compose up -d

clean:
	docker compose down

status:
	docker ps -a
