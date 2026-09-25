#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
    echo "Usage: $0 <backup.sql>" >&2
    exit 1
fi

BACKUP_FILE="$1"

if [[ ! -f "$BACKUP_FILE" ]]; then
    echo "ERROR: backup file not found: $BACKUP_FILE" >&2
    exit 1
fi

if [[ ! -s "$BACKUP_FILE" ]]; then
    echo "ERROR: backup file is empty: $BACKUP_FILE" >&2
    exit 1
fi

echo "Restoring PostgreSQL from:"
echo "$BACKUP_FILE"

docker compose exec -T postgres \
    psql \
    -U barq_app \
    -d barq_tasks \
    -v ON_ERROR_STOP=1 \
    < "$BACKUP_FILE"

echo
echo "Restore completed successfully."

echo "Current records:"
docker compose exec -T postgres \
    psql \
    -U barq_app \
    -d barq_tasks \
    -c "SELECT id, title FROM records ORDER BY id;"
