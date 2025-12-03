О деплое (кратко)

Сервисы: web (gunicorn/uvicorn), PostgreSQL (managed or hosted), брокер (Redis/RabbitMQ), worker(s).

В production: использовать systemd / container orchestration (k8s) или supervisor для запуска web+workers; nginx/ingress перед веб-сервисом. Настроить секреты и переменные окружения, использовать connection pooling и healthchecks.

Запуск: миграции при деплое, затем поднять web, затем worker(s). Логирование и мониторинг (Sentry, Prometheus) — рекомендую.
