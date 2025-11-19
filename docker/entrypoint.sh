#!/bin/bash
set -e

echo "[entrypoint] 🚀 Starting 10Code Intranet..."

# Esperar a que PostgreSQL esté listo
echo "[entrypoint] ⏳ Waiting for PostgreSQL..."

# Esperar a que PostgreSQL acepte conexiones usando Django
until python -c "import django; django.setup(); from django.db import connection; connection.ensure_connection()" 2>/dev/null; do
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

    echo "[entrypoint] 🔐 Setting up social applications..."
    python scripts/setup_social_app.py
fi

echo "[entrypoint] 🎯 Starting application: $@"
exec "$@"
