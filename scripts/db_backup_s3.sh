#!/bin/sh
# scripts/db_backup_s3.sh
# Performs local pg_dump backup and synchronizes to off-site S3/R2 bucket

set -e

BACKUP_DIR="${BACKUP_DIR:-/backups}"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
DB_HOST=${DB_HOST:-db}
DB_USER=${DB_USER:-postgres}
DB_NAME=${DB_NAME:-cloudmosaic_db}

mkdir -p "$BACKUP_DIR"
BACKUP_FILE="${BACKUP_DIR}/cloudmosaic_db_backup_${TIMESTAMP}.dump"

echo "Creating compressed pg_dump..."
pg_dump -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -F c -f "$BACKUP_FILE"

echo "Backup created at ${BACKUP_FILE}"

# Compute SHA256 checksum
if command -v sha256sum >/dev/null 2>&1; then
    sha256sum "$BACKUP_FILE" > "${BACKUP_FILE}.sha256"
elif command -v shasum >/dev/null 2>&1; then
    shasum -a 256 "$BACKUP_FILE" > "${BACKUP_FILE}.sha256"
fi

if [ -n "$S3_BUCKET_NAME" ]; then
    echo "Uploading backup to S3/R2: s3://${S3_BUCKET_NAME}/backups/..."
    if command -v aws >/dev/null 2>&1; then
        aws s3 cp "$BACKUP_FILE" "s3://${S3_BUCKET_NAME}/backups/$(basename "$BACKUP_FILE")" \
            --sse AES256 ${S3_ENDPOINT_URL:+--endpoint-url "$S3_ENDPOINT_URL"}
        if [ -f "${BACKUP_FILE}.sha256" ]; then
            aws s3 cp "${BACKUP_FILE}.sha256" "s3://${S3_BUCKET_NAME}/backups/$(basename "${BACKUP_FILE}.sha256")" \
                --sse AES256 ${S3_ENDPOINT_URL:+--endpoint-url "$S3_ENDPOINT_URL"}
        fi
        echo "Off-site upload completed successfully with AES-256 encryption."
    else
        echo "WARNING: aws-cli not found in environment. Off-site sync skipped."
    fi
else
    echo "NOTICE: S3_BUCKET_NAME not set. Retaining local backup only."
fi

# Retain 14 days locally
find "$BACKUP_DIR" -type f \( -name "*.dump" -o -name "*.sha256" \) -mtime +14 -exec rm -f {} \;
echo "Local backup retention pruning complete."
