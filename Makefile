# Run in Dev mode
dev:
	docker compose -f docker-compose.base.yml -f docker-compose.dev.yml up --build

# Run tests
bash:
	docker compose -f docker-compose.base.yml -f docker-compose.dev.yml exec web bash

# Run in Prod mode
prod:
	docker compose -f docker-compose.base.yml -f docker-compose.prod.yml up --build

# Tear down everything
down:
	docker compose -f docker-compose.base.yml -f docker-compose.dev.yml down
