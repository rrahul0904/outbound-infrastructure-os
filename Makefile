.PHONY: up down logs verify
up:
	docker compose up --build
down:
	docker compose down
logs:
	docker compose logs -f
verify:
	python3 -m compileall services/api/app services/worker/app
	python3 scripts/verify_foundation.py
