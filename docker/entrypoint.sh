#!/bin/bash
set -e

echo "[entrypoint] 🚀 Starting 10Code Intranet..."

# Esperar a que PostgreSQL esté listo
echo "[entrypoint] ⏳ Waiting for PostgreSQL..."

# Usar la librería read_secret para obtener la contraseña
DB_PASSWORD=""
if [ -f "/run/secrets/db_password" ]; then
    DB_PASSWORD=$(cat /run/secrets/db_password)
elif [ -f "/app/secrets/db_password.txt" ]; then
    DB_PASSWORD=$(cat /app/secrets/db_password.txt)
elif [ -n "$DATABASE_PASSWORD" ]; then
    DB_PASSWORD="$DATABASE_PASSWORD"
else
    DB_PASSWORD="postgres"
fi

# Wait for PostgreSQL
until python -c "import psycopg; psycopg.connect('postgresql://$DATABASE_USER:$DB_PASSWORD@$DATABASE_HOST:$DATABASE_PORT/$DATABASE_NAME')" 2>/dev/null; do
    echo "   PostgreSQL not ready, retrying in 2s..."
    sleep 2
done
echo "[entrypoint] ✅ PostgreSQL is ready!"

# Ejecutar migraciones (solo si no es worker de Celery)
if [ "$1" != "celery" ]; then
    echo "[entrypoint] 🔄 Running migrations..."
    python manage.py migrate --noinput

    echo "[entrypoint] 📦 Collecting static files..."
    python manage.py collectstatic --noinput --clear
fi

echo "[entrypoint] 🎯 Starting application: $@"
exec "$@"
