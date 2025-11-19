# ============================================================================
# Makefile - 10Code Intranet
# ============================================================================
# Comandos útiles para desarrollo con Docker

.PHONY: help build up down logs shell test migrate createsuperuser clean restart

# Variables
COMPOSE = docker compose
SERVICE_WEB = web
SERVICE_FRONTEND = frontend
SERVICE_DB = db

# ============================================================================
# COMANDOS PRINCIPALES
# ============================================================================

help: ## Mostrar esta ayuda
	@echo "🚀 10Code Intranet - Comandos disponibles:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

build: ## Construir imágenes de Docker
	$(COMPOSE) build

up: ## Levantar servicios en background
	$(COMPOSE) up -d
	@echo "✅ Servicios levantados"
	@echo "🌐 Backend: http://localhost:8000"
	@echo "⚡ Frontend: http://localhost:5173"

down: ## Detener servicios
	$(COMPOSE) down

restart: ## Reiniciar servicios
	$(COMPOSE) restart

logs: ## Ver logs de todos los servicios
	$(COMPOSE) logs -f

logs-web: ## Ver logs del backend Django
	$(COMPOSE) logs -f $(SERVICE_WEB)

logs-frontend: ## Ver logs del frontend Vite
	$(COMPOSE) logs -f $(SERVICE_FRONTEND)

ps: ## Ver estado de servicios
	$(COMPOSE) ps

# ============================================================================
# DJANGO MANAGEMENT
# ============================================================================

shell: ## Abrir Django shell
	$(COMPOSE) exec $(SERVICE_WEB) python manage.py shell

migrate: ## Ejecutar migraciones
	$(COMPOSE) exec $(SERVICE_WEB) python manage.py migrate

makemigrations: ## Crear nuevas migraciones
	$(COMPOSE) exec $(SERVICE_WEB) python manage.py makemigrations

createsuperuser: ## Crear superusuario
	$(COMPOSE) exec $(SERVICE_WEB) python manage.py createsuperuser

collectstatic: ## Recolectar archivos estáticos
	$(COMPOSE) exec $(SERVICE_WEB) python manage.py collectstatic --noinput

# ============================================================================
# TESTING
# ============================================================================

test: ## Ejecutar todos los tests
	$(COMPOSE) exec $(SERVICE_WEB) pytest

test-coverage: ## Ejecutar tests con cobertura
	$(COMPOSE) exec $(SERVICE_WEB) pytest --cov=apps --cov-report=html

test-fast: ## Ejecutar tests sin migraciones
	$(COMPOSE) exec $(SERVICE_WEB) pytest --nomigrations

# ============================================================================
# DATABASE
# ============================================================================

db-shell: ## Abrir shell de PostgreSQL
	$(COMPOSE) exec $(SERVICE_DB) psql -U postgres -d 10code_intranet

db-backup: ## Backup de base de datos
	$(COMPOSE) exec $(SERVICE_DB) pg_dump -U postgres 10code_intranet > backup_$$(date +%Y%m%d_%H%M%S).sql
	@echo "✅ Backup creado"

db-reset: ## Resetear base de datos (¡CUIDADO!)
	@echo "⚠️  ¿Estás seguro? Esto borrará toda la base de datos. [Ctrl+C para cancelar]"
	@read -p "Escribe 'SI' para confirmar: " confirm && [ "$$confirm" = "SI" ]
	$(COMPOSE) down -v
	$(COMPOSE) up -d $(SERVICE_DB)
	@sleep 5
	$(MAKE) migrate
	@echo "✅ Base de datos reseteada"

# ============================================================================
# LIMPIEZA
# ============================================================================

clean: ## Limpiar contenedores, imágenes y volúmenes
	$(COMPOSE) down -v --remove-orphans
	docker system prune -f

clean-all: ## Limpieza completa (¡CUIDADO! Borra TODO)
	@echo "⚠️  ¿Estás seguro? Esto borrará TODOS los contenedores, imágenes y volúmenes. [Ctrl+C para cancelar]"
	@read -p "Escribe 'SI' para confirmar: " confirm && [ "$$confirm" = "SI" ]
	$(COMPOSE) down -v --remove-orphans
	docker system prune -a -f --volumes

# ============================================================================
# DESARROLLO
# ============================================================================

dev-setup: ## Setup inicial para desarrollo
	@echo "🔧 Configurando entorno de desarrollo..."
	@test -f .env || cp .env.example .env
	@test -f secrets/db_password.txt || cp secrets/db_password.example.txt secrets/db_password.txt
	@test -f secrets/django_secret_key.txt || cp secrets/django_secret_key.example.txt secrets/django_secret_key.txt
	$(MAKE) build
	$(MAKE) up
	@sleep 10
	$(MAKE) migrate
	@echo "✅ Setup completo"
	@echo "🚀 Crea un superusuario con: make createsuperuser"

frontend-install: ## Instalar dependencias del frontend
	$(COMPOSE) exec $(SERVICE_FRONTEND) npm install

frontend-build: ## Build del frontend para producción
	cd frontend && npm run build

# ============================================================================
# MACHINE LEARNING
# ============================================================================

ml-build: ## Build con dependencias de ML (TensorFlow, PyTorch, etc.)
	@echo "🤖 Building with ML dependencies (this will take longer)..."
	docker compose -f compose.yml -f compose.override.yml -f compose.ml.yml build

ml-up: ## Levantar servicios con ML
	@echo "🤖 Starting services with ML dependencies..."
	docker compose -f compose.yml -f compose.override.yml -f compose.ml.yml up -d
	@echo "✅ Servicios con ML levantados"
	@echo "🌐 Backend: http://localhost:8000"
	@echo "⚡ Frontend: http://localhost:5173"

ml-setup: ## Setup completo con ML
	@echo "🤖 Configurando entorno de desarrollo con ML..."
	@test -f .env || cp .env.example .env
	@test -f secrets/db_password.txt || cp secrets/db_password.example.txt secrets/db_password.txt
	@test -f secrets/django_secret_key.txt || cp secrets/django_secret_key.example.txt secrets/django_secret_key.txt
	$(MAKE) ml-build
	$(MAKE) ml-up
	@sleep 10
	$(MAKE) migrate
	@echo "✅ Setup con ML completo"
	@echo "🚀 Crea un superusuario con: make createsuperuser"

ml-down: ## Detener servicios de ML
	docker compose -f compose.yml -f compose.override.yml -f compose.ml.yml down

ml-logs: ## Ver logs de servicios con ML
	docker compose -f compose.yml -f compose.override.yml -f compose.ml.yml logs -f

# ============================================================================
# UTILIDADES
# ============================================================================

exec-web: ## Ejecutar comando en contenedor web (uso: make exec-web CMD="python manage.py ...")
	$(COMPOSE) exec $(SERVICE_WEB) $(CMD)

bash-web: ## Abrir bash en contenedor web
	$(COMPOSE) exec $(SERVICE_WEB) /bin/bash

bash-frontend: ## Abrir shell en contenedor frontend
	$(COMPOSE) exec $(SERVICE_FRONTEND) /bin/sh

stats: ## Ver estadísticas de recursos
	docker stats

# ============================================================================
# PRODUCCIÓN
# ============================================================================

prod-build: ## Build para producción
	docker compose -f compose.yml build --no-cache

prod-up: ## Levantar en modo producción
	docker compose -f compose.yml up -d

prod-logs: ## Ver logs en producción
	docker compose -f compose.yml logs -f

rebuild: ## Reconstruir imágenes desde cero (sin caché)
	@echo "🔨 Reconstruyendo imágenes sin caché..."
	$(COMPOSE) down
	$(COMPOSE) build --no-cache --pull
	@echo "✅ Rebuild completado. Ejecuta 'make up' para iniciar"

clean-rebuild: ## Limpieza completa y rebuild (soluciona errores de caché)
	@echo "🧹 Limpieza completa de Docker y rebuild..."
	@bash scripts/clean-rebuild.sh
