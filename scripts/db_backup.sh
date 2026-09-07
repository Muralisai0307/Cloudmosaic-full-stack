#!/bin/bash
# scripts/db_backup.sh
# Performs a pg_dump of the PostgreSQL database inside the Docker container

set -e

BACKUP_DIR="./backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
DB_CONTAINER="cloudmosaic-db-1" # Based on standard docker-compose naming
DB_USER="postgres"
DB_NAME="cloudmosaic_db"

mkdir -p "$BACKUP_DIR"
BACKUP_FILE="${BACKUP_DIR}/cloudmosaic_db_backup_${TIMESTAMP}.sql"

echo "Starting backup of ${DB_NAME} from container ${DB_CONTAINER}..."

# Execute pg_dump using native command if available or via docker container
if command -v pg_dump &> /dev/null; then
    echo "Using host/container pg_dump..."
    pg_dump -h "${DB_HOST:-localhost}" -p "${DB_PORT:-5432}" -U "$DB_USER" -d "$DB_NAME" -F c -f "$BACKUP_FILE"
elif command -v docker &> /dev/null; then
    echo "Using docker exec with container ${DB_CONTAINER}..."
    docker exec -t "$DB_CONTAINER" pg_dump -U "$DB_USER" -d "$DB_NAME" -F c > "$BACKUP_FILE"
else
    echo "Error: Neither pg_dump nor docker command found in PATH."
    exit 1
fi

echo "Backup created successfully at: ${BACKUP_FILE}"

# Retention policy: Remove backups older than 14 days
find "$BACKUP_DIR" -type f \( -name "*.sql" -o -name "*.dump" \) -mtime +14 -exec rm -f {} \;
echo "Old backups cleaned up."
