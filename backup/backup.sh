#!/bin/bash
set -euo pipefail

# Create timestamped backup
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
BACKUP_FILE="/backups/backup_$TIMESTAMP.dump"

echo "📦 Creating backup at $BACKUP_FILE"
pg_dump -h db -U "${POSTGRES_USER}" -d "${POSTGRES_DB}" -F c -f "$BACKUP_FILE"
echo "✅ Backup complete"

# Auto-delete logic: keep only the latest 7 backups
MAX_BACKUPS=7
echo "🧹 Checking for old backups to delete..."

cd /backups
ls -1t backup_*.dump | tail -n +$((MAX_BACKUPS + 1)) | while read -r old_file; do
  echo "🗑️ Deleting old backup: $old_file"
  rm -f "$old_file"
done
