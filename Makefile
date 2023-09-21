run-dev:
	hupper -m flask run

migrate:
	@read -p "Enter migration message: " message; \
	alembic revision --autogenerate -m "$$message"

upgrade:
	alembic upgrade head

downgrade:
	alembic downgrade -1

renew-migrate:
	@current_version=$$(alembic current 2>/dev/null | grep -Eo '^[a-f0-9]{12}' | tail -n 1); \
	migration_file=$$(ls alembic/versions/ | grep "$${current_version}"); \
	if [ -n "$$migration_file" ]; then \
		alembic downgrade -1; \
		rm "alembic/versions/$$migration_file"; \
	else \
		echo "Migration file not found!"; \
		exit 1; \
	fi; \
	make migrate
