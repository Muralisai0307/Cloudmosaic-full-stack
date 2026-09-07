#!/bin/sh
# scripts/db_backup_cron.sh
# Performs a pg_dump connecting directly to the PostgreSQL container

set -e

BACKUP_DIR="/backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
DB_HOST=${DB_HOST:-db}
DB_USER=${DB_USER:-postgres}
DB_NAME=${DB_NAME:-cloudmosaic_db}

mkdir -p "$BACKUP_DIR"
BACKUP_FILE="${BACKUP_DIR}/cloudmosaic_db_backup_${TIMESTAMP}.sql"

echo "Starting backup of ${DB_NAME} from host ${DB_HOST}..."

# Execute pg_dump connecting via network (requires PGPASSWORD environment variable)
pg_dump -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -F c > "$BACKUP_FILE"

echo "Backup created successfully at: ${BACKUP_FILE}"

# Keep only last 7 days of backups
find "$BACKUP_DIR" -type f -name "*.sql" -mtime +7 -exec rm {} \;
echo "Old backups cleaned up."
