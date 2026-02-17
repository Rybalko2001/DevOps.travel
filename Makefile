up:
	docker compose up -d --build

down:
	docker compose down -v

logs:
	docker compose logs -f

test:
	curl -s http://localhost:8080/healthz