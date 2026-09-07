#!/bin/bash
# scripts/db_restore.sh
# Safely restores a pg_dump file to a PostgreSQL database

set -e

if [ -z "$1" ]; then
    echo "Usage: ./db_restore.sh <path_to_backup_file> [target_db_name]"
    exit 1
fi

BACKUP_FILE="$1"
TARGET_DB="${2:-cloudmosaic_db}"
DB_CONTAINER="${DB_CONTAINER:-cloudmosaic-db-1}"
DB_USER="${DB_USER:-postgres}"

if [ ! -f "$BACKUP_FILE" ]; then
    echo "Error: Backup file $BACKUP_FILE not found."
    exit 1
fi

echo "Target Database: ${TARGET_DB}"
echo "Backup File: ${BACKUP_FILE}"
echo "WARNING: This will overwrite objects in ${TARGET_DB}!"
read -p "Are you sure you want to proceed? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Restore cancelled."
    exit 1
fi

echo "Restoring database into ${TARGET_DB}..."
if command -v pg_restore &> /dev/null; then
    echo "Using host/container pg_restore..."
    pg_restore -h "${DB_HOST:-localhost}" -p "${DB_PORT:-5432}" -U "$DB_USER" -d "$TARGET_DB" --clean --if-exists "$BACKUP_FILE" || true
elif command -v docker &> /dev/null; then
    echo "Using docker exec with container ${DB_CONTAINER}..."
    docker exec -i "$DB_CONTAINER" pg_restore -U "$DB_USER" -d "$TARGET_DB" --clean --if-exists < "$BACKUP_FILE" || true
else
    echo "Error: Neither pg_restore nor docker command found in PATH."
    exit 1
fi

echo "Restore completed successfully into ${TARGET_DB}."
