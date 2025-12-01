# Run in Dev mode
dev:
	docker compose -f docker-compose.base.yml -f docker-compose.dev.yml up --build

# Launch shell
bash:
	docker compose -f docker-compose.base.yml -f docker-compose.dev.yml exec web bash

# Run tests
test:
	docker compose -f docker-compose.base.yml -f docker-compose.dev.yml exec web pytest --reuse-db

# Run in Prod mode
prod:
	docker compose -f docker-compose.base.yml -f docker-compose.prod.yml up --build

# Tear down everything
down:
	docker compose -f docker-compose.base.yml -f docker-compose.dev.yml down
