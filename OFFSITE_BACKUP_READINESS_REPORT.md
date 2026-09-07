# OFF-SITE BACKUP READINESS REPORT

**Status:** DEPLOYMENT REQUIRED

Local backups are appropriately configured via the isolated `backup` cron container and written to a persistent Docker volume. However, these backups currently only reside on the host filesystem.

An off-site backup pipeline (e.g., AWS S3, Backblaze B2, Cloudflare R2) has NOT been implemented because cloud credentials and provider selection are unavailable in this environment.

## Required Target Architecture
```text
PostgreSQL
    ↓
pg_dump (Local backup volume)
    ↓
AWS CLI / s3cmd (Encrypted transfer)
    ↓
AWS S3 Bucket (cloudmosaic-db-backups)
```

## Implementation Requirements for Deployment
1. **Credentials**: Inject `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` via `.env`. DO NOT commit these to the repository.
2. **Script Update**: Modify `scripts/db_backup_cron.sh` to include an upload step:
   ```bash
   aws s3 cp "$BACKUP_FILE" s3://my-bucket/backups/ --sse AES256
   ```
3. **Retention**: Configure bucket lifecycle policies to automatically transition backups to deep archive (Glacier) after 30 days and delete after 365 days.
4. **Validation**: Test the download and restore from the S3 bucket to verify integrity.
