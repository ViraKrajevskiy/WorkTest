.PHONY: help run migrate makemigrations test shell worker

help:
	@echo "Commands: run migrate makemigrations test worker shell"

run:
	docker-compose up --build -d

migrate:
	docker-compose exec web python manage.py migrate

makemigrations:
	docker-compose exec web python manage.py makemigrations

worker:
	docker-compose exec worker celery -A app.celery.celery_app worker --loglevel=info

test:
	docker-compose exec web pytest -q

shell:
	docker-compose exec web python manage.py shell
