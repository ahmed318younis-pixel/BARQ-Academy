#!/usr/bin/env bash
set -euo pipefail

BACKUP_DIR="./backups"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
BACKUP_FILE="${BACKUP_DIR}/barq_tasks_${TIMESTAMP}.sql"

mkdir -p "$BACKUP_DIR"

if [[ -e "$BACKUP_FILE" ]]; then
    echo "ERROR: backup file already exists: $BACKUP_FILE" >&2
    exit 1
fi

echo "Creating PostgreSQL backup..."

docker compose exec -T postgres \
    pg_dump \
    -U barq_app \
    -d barq_tasks \
    --clean \
    --if-exists \
    > "$BACKUP_FILE"

if [[ ! -s "$BACKUP_FILE" ]]; then
    echo "ERROR: backup file is empty." >&2
    rm -f "$BACKUP_FILE"
    exit 1
fi

echo "Backup created successfully:"
echo "$BACKUP_FILE"
echo "Backup size: $(du -h "$BACKUP_FILE" | cut -f1)"
