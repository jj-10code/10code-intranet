# Docker Setup - 10Code Intranet

Configuración profesional de Docker para desarrollo y producción.

## 🚀 Quick Start (Desarrollo)

```bash
# 1. Clonar repositorio
git clone <repo-url>
cd 10code-intranet

# 2. Configurar entorno
cp .env.example .env
cp secrets/db_password.example.txt secrets/db_password.txt
cp secrets/django_secret_key.example.txt secrets/django_secret_key.txt

# 3. Levantar servicios
docker-compose up -d

# 4. Ver logs
docker-compose logs -f web

# 5. Acceder a la aplicación
# Backend: http://localhost:8000
# Frontend (Vite HMR): http://localhost:5173
```

## 📦 Servicios Incluidos

### Backend Stack
- **web**: Django 5.2 + Python 3.14 (runserver en dev, gunicorn en prod)
- **db**: PostgreSQL 18
- **redis**: Redis 8.2 (cache + Celery broker)
- **celery_worker**: Worker para tareas asíncronas
- **celery_beat**: Scheduler para tareas periódicas

### Frontend Stack
- **frontend**: Vite dev server (solo desarrollo) - Node 22 con HMR

## 🛠️ Comandos Útiles

### Gestión de Servicios

```bash
# Levantar servicios
docker-compose up -d

# Ver logs de todos los servicios
docker-compose logs -f

# Ver logs de un servicio específico
docker-compose logs -f web
docker-compose logs -f celery_worker

# Parar servicios
docker-compose down

# Parar y eliminar volúmenes (¡CUIDADO! Borra la DB)
docker-compose down -v

# Rebuilds
docker-compose build
docker-compose build --no-cache  # Sin cache
```

### Django Management Commands

```bash
# Ejecutar comando dentro del contenedor web
docker-compose exec web python manage.py <command>

# Ejemplos:
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py shell
docker-compose exec web python manage.py collectstatic
docker-compose exec web python manage.py makemigrations
```

### Database Operations

```bash
# Acceder a PostgreSQL
docker-compose exec db psql -U postgres -d 10code_intranet

# Backup de base de datos
docker-compose exec db pg_dump -U postgres 10code_intranet > backup.sql

# Restore de base de datos
docker-compose exec -T db psql -U postgres 10code_intranet < backup.sql
```

### Frontend Operations

```bash
# Instalar nueva dependencia npm
docker-compose exec frontend npm install <package>

# Rebuild frontend
docker-compose exec frontend npm run build

# Ver logs frontend
docker-compose logs -f frontend
```

### Testing

```bash
# Ejecutar tests
docker-compose exec web pytest

# Con cobertura
docker-compose exec web pytest --cov=apps

# Tests específicos
docker-compose exec web pytest apps/projects/tests/
```

## 🏗️ Arquitectura

### Multi-Stage Dockerfile

El `Dockerfile` usa multi-stage builds para optimizar:

1. **Builder Stage**: Instala dependencias con `uv`
2. **Runtime Stage**: Imagen minimalista solo con lo necesario

### Docker Compose

- `docker-compose.yml`: Base para desarrollo y producción
- `docker-compose.override.yml`: Específico para desarrollo (se aplica automáticamente)

### Volúmenes en Desarrollo

Para hot reload, el código se monta como volumen:

```yaml
volumes:
  - .:/app                 # Todo el código
  - /app/.venv             # Excluir venv
  - /app/node_modules      # Excluir node_modules
```

## 🔐 Gestión de Secretos

Los secretos se leen en este orden de prioridad:

1. `/run/secrets/{nombre}` - Docker Secrets (producción)
2. `secrets/{nombre}.txt` - Archivos locales (desarrollo)
3. Variable de entorno `{NOMBRE}` - Fallback

### Secretos Requeridos

```bash
secrets/
├── db_password.txt           # Contraseña PostgreSQL
└── django_secret_key.txt     # Django SECRET_KEY
```

Ver `secrets/README.md` para más detalles.

## 🎯 Entornos

### Desarrollo (Default)

```bash
# Usa docker-compose.override.yml automáticamente
docker-compose up -d

# Django runserver con hot reload
# Vite dev server con HMR
# CORS permisivo
# Debug Toolbar habilitado
```

### Producción

```bash
# Ignorar override.yml
docker-compose -f docker-compose.yml up -d

# Gunicorn con 3 workers
# Frontend pre-buildeado en staticfiles/
# Debug=False
# WhiteNoise para estáticos
```

## 🐛 Troubleshooting

### Problema: "No module named 'X'"

```bash
# Rebuild imagen
docker-compose build --no-cache web
docker-compose up -d
```

### Problema: Database connection refused

```bash
# Verificar que PostgreSQL está corriendo
docker-compose ps

# Ver logs de DB
docker-compose logs db

# Esperar a healthcheck
docker-compose exec web python -c "from django.db import connection; connection.ensure_connection()"
```

### Problema: Frontend no recarga (HMR no funciona)

```bash
# Verificar que frontend está corriendo
docker-compose ps frontend

# Ver logs
docker-compose logs -f frontend

# Restart frontend
docker-compose restart frontend
```

### Problema: Permisos de archivos

```bash
# Si tienes problemas de permisos, ajustar ownership
sudo chown -R $USER:$USER .
```

## 📊 Monitoreo

### Ver estado de servicios

```bash
docker-compose ps
```

### Verificar salud de contenedores

```bash
docker-compose exec web python -c "from django.db import connection; connection.ensure_connection()"
docker-compose exec redis redis-cli ping
docker-compose exec db pg_isready -U postgres
```

### Inspeccionar recursos

```bash
docker stats
```

## 🚢 Deploy a Producción

### Paso 1: Configurar Secretos

```bash
# Generar SECRET_KEY seguro
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())' > secrets/django_secret_key.txt

# Contraseña segura para PostgreSQL
openssl rand -base64 32 > secrets/db_password.txt
```

### Paso 2: Configurar Variables de Entorno

```bash
# Editar .env
DJANGO_SETTINGS_MODULE=config.settings.production
DEBUG=False
ALLOWED_HOSTS=intranet.10code.es
```

### Paso 3: Build Frontend

```bash
cd frontend
npm run build
cd ..
```

### Paso 4: Deploy

```bash
docker-compose -f docker-compose.yml up -d
```

## 📚 Referencias

- [Docker Compose Docs](https://docs.docker.com/compose/)
- [Django Docker Best Practices](https://docs.djangoproject.com/en/stable/howto/deployment/)
- [PostgreSQL Official Image](https://hub.docker.com/_/postgres)
- [Redis Official Image](https://hub.docker.com/_/redis)
- [Python Official Image](https://hub.docker.com/_/python)

---

**Desarrollado con 💙 por 10Code Team**
