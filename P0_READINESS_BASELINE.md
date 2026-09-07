# P0 READINESS BASELINE

| Area | Current Status | Evidence | Required Action |
| ---- | -------------- | -------- | --------------- |
| Frontend | React 19.2.7 | `package.json` | None. Keep native Fetch. |
| Backend | Django 5.0.3, DRF 3.15.1 | `requirements/base.txt` | None. Ensure `manage.py check` passes. |
| Docker Files | Exist and valid | `Dockerfile`, `nginx/Dockerfile` | Ensure minimal privilege. |
| Docker Compose | Exists with Nginx/Gunicorn/Postgres | `docker-compose.yml` | Healthchecks and no docker socket mount. |
| Nginx | Proxy configured | `nginx.conf` | Validate proxy headers for HTTPS. |
| Gunicorn | Production server bound | `docker-compose.yml` | None. |
| PostgreSQL | DB isolated, not exposed | `docker-compose.yml` | None. |
| Environment | Variables used | `settings/production.py` | None. |
| Backups | Script exists, dedicated container | `scripts/db_backup_cron.sh` | Need off-site config. |
| Security | HTTPS headers ready | `settings/production.py` | DNS deployment pending. |
| Tests | Unit tests passing | `python manage.py test` | Needs E2E verification. |
