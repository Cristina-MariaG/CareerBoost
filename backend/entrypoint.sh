#!/bin/sh

echo "Waiting for PostgreSQL..."
until pg_isready -h "${POSTGRES_HOST:-db}" -U "${POSTGRES_USER}" > /dev/null 2>&1; do
  sleep 1
done
echo "PostgreSQL ready."

python manage.py migrate --no-input
python manage.py runserver 0.0.0.0:8000
