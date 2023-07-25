build:
	docker compose -f docker-compose.yml build

up:
	docker compose -f docker-compose.yml up -d

stop:
	docker compose -f docker-compose.yml stop

down:
	docker compose -f docker-compose.yml down -v

migrations: ## Crea migraciones en el proyecto
	docker compose -f docker-compose.yml exec web /bin/sh -c "alembic revision --autogenerate"

migrate: ## Crea migraciones en el proyecto
	docker compose -f docker-compose.yml exec web /bin/sh -c "alembic upgrade head"