#!/bin/bash
set -e

echo "🔨 Reconstruyendo contenedores desde cero..."

echo "🛑 Deteniendo contenedores..."
docker compose down

echo "🗑️  Limpiando imágenes viejas..."
docker compose rm -f

echo "🏗️  Reconstruyendo sin caché..."
docker compose build --no-cache --pull

echo "✅ Rebuild completado"
echo "▶️  Ejecuta 'make dev-setup' para iniciar"
