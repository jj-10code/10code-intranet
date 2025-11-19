#!/bin/bash
set -e

echo "🧹 Limpieza completa de Docker antes de rebuild..."

echo "🛑 Deteniendo todos los contenedores..."
docker compose down --remove-orphans 2>/dev/null || true

echo "🗑️  Eliminando contenedores..."
docker compose rm -f -s -v 2>/dev/null || true

echo "🧹 Limpiando builder cache de Docker..."
docker builder prune -af

echo "🗑️  Limpiando imágenes dangling..."
docker image prune -f

echo "🗑️  Eliminando imágenes del proyecto..."
docker images | grep 10code-intranet | awk '{print $3}' | xargs -r docker rmi -f 2>/dev/null || true

echo "🏗️  Reconstruyendo desde cero sin caché..."
DOCKER_BUILDKIT=1 docker compose build --no-cache --pull --progress=plain

echo "✅ Limpieza y rebuild completados"
echo "▶️  Ejecuta 'make up && sleep 10 && make migrate' para iniciar"
