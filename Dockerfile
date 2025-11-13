# syntax=docker/dockerfile:1

# ============================================================================
# STAGE 1: Builder - Instalar dependencias con uv
# ============================================================================
FROM python:3.14-slim-trixie AS builder

WORKDIR /tmp/build

# Copiar uv desde imagen oficial (más rápido que instalarlo)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Variables para optimizar uv
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never \
    PYTHONDONTWRITEBYTECODE=1

# Argumentos para control granular de dependencias
ARG INSTALL_DEV=false
ARG INSTALL_ML=false

# System dependencies para compilar paquetes Python
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar solo archivos de dependencias (maximiza cache)
COPY pyproject.toml uv.lock ./

# Instalar dependencias con control granular
RUN --mount=type=cache,target=/root/.cache/uv \
    if [ "$INSTALL_DEV" = "false" ] && [ "$INSTALL_ML" = "false" ]; then \
        echo "📦 Installing PRODUCTION dependencies only (base)..."; \
        uv sync --frozen --no-dev --no-install-project; \
    elif [ "$INSTALL_DEV" = "true" ] && [ "$INSTALL_ML" = "false" ]; then \
        echo "📦 Installing DEVELOPMENT dependencies (base + dev, without ML ~1GB)..."; \
        uv sync --frozen --no-install-project --group dev; \
    elif [ "$INSTALL_DEV" = "true" ] && [ "$INSTALL_ML" = "true" ]; then \
        echo "📦 Installing ALL dependencies (base + dev + ML ~6GB)..."; \
        echo "⚠️  This will take several minutes due to TensorFlow & PyTorch..."; \
        uv sync --frozen --no-install-project --group dev --group ml; \
    else \
        echo "⚠️  Invalid combination: INSTALL_DEV=$INSTALL_DEV, INSTALL_ML=$INSTALL_ML"; \
        echo "📦 Falling back to production dependencies..."; \
        uv sync --frozen --no-dev --no-install-project; \
    fi

# ============================================================================
# STAGE 2: Runtime - Imagen final minimalista
# ============================================================================
FROM python:3.14-slim-trixie AS runtime

WORKDIR /app

# Variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DJANGO_SETTINGS_MODULE=config.settings.production \
    PATH="/app/.venv/bin:$PATH"

# Runtime dependencies (solo libpq para PostgreSQL)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copiar venv desde builder
COPY --from=builder /tmp/build/.venv /app/.venv

# Crear usuario no-root (SEGURIDAD)
RUN groupadd -r appuser && \
    useradd -r -g appuser -u 1000 -m -s /sbin/nologin appuser && \
    mkdir -p /app/staticfiles /app/media && \
    chown -R appuser:appuser /app

# Copiar código de aplicación
COPY --chown=appuser:appuser . .

# Asegurar que entrypoint.sh sea ejecutable (antes de cambiar de usuario)
RUN chmod +x /app/docker/entrypoint.sh

# Cambiar a usuario no-root
USER appuser

# Collectstatic se ejecutará en entrypoint después de migraciones

# Healthcheck (verifica DB connection)
HEALTHCHECK --interval=30s --timeout=5s --start-period=40s --retries=3 \
    CMD python -c "import django; django.setup(); from django.db import connection; connection.ensure_connection()" || exit 1

EXPOSE 8000

# Entrypoint para migraciones automáticas
ENTRYPOINT ["/app/docker/entrypoint.sh"]

# Comando por defecto (Gunicorn para producción)
CMD ["gunicorn", "config.wsgi:application", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "3", \
     "--timeout", "60", \
     "--access-logfile", "-", \
     "--error-logfile", "-"]
