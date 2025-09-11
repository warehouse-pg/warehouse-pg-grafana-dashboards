build:
	./build.sh

run:
	docker compose up -d

clean:
	docker compose down

status:
	docker ps -a
