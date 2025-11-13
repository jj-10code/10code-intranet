# 10Code Intranet =€

> Suite de herramientas internas para la gestión integral de 10Code

[![Django](https://img.shields.io/badge/Django-5.2-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.14-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-18-61dafb.svg)](https://reactjs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-336791.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED.svg)](https://www.docker.com/)

## =Ö Descripción

**10Code Intranet** es una plataforma interna completa diseñada para gestionar todos los aspectos operativos de 10Code. Implementa una arquitectura de **Monolito Modular Majestuoso** usando Django 5 + Inertia.js + React, proporcionando una experiencia de Single Page Application sin la complejidad de una API REST tradicional.

### Funcionalidades Principales

- = **SSO con Google Auth** - Autenticación restringida a `@10code.es`
- =e **Gestión de Equipo** - Control de capacidad y horario (normativa española 2026)
- =¼ **CRM & Oportunidades** - Gestión de ofertas y funnel con ML/IA
- =Ê **Gestión de Proyectos** - Ciclo de vida completo y control de tiempos (tipo Jira)
- =È **Cuadros de Mando** - KPIs de desempeño y financieros
- > **Estimaciones CEPF + ML** - Sistema inteligente de estimación de proyectos

## =à Stack Tecnológico

### Backend
- **Django 5.2** - Framework web Python (Monolito Modular)
- **Inertia.js** - Puente Django-React (SPA sin API REST)
- **PostgreSQL 18** - Base de datos relacional
- **Redis 8.2** - Cache y message broker
- **Celery 5.5** - Tareas asíncronas y programadas

### Frontend
- **React 18** - Librería UI
- **Vite** - Build tool con HMR
- **TypeScript** - Tipado estático
- **shadcn/ui** - Componentes UI
- **TailwindCSS** - Utility-first CSS

### DevOps
- **Docker** - Contenedores con multi-stage builds
- **uv** - Gestor de paquetes Python ultrarrápido
- **pytest** - Testing framework
- **GitHub Actions** - CI/CD

### Machine Learning (Opcional)
- **TensorFlow 2.x** - Framework principal de ML
- **PyTorch** - Framework alternativo de ML
- **scikit-learn** - Algoritmos clásicos de ML
- **spaCy** - Procesamiento de lenguaje natural

> =¡ Las dependencias de ML (~6GB) son opcionales y solo necesarias para el módulo de estimaciones CEPF.

## =Ë Requisitos Previos

Antes de empezar, asegúrate de tener instalado:

- **Docker Engine** 20.10 o superior
- **Docker Compose** v2 o superior (comando `docker compose` con espacio)
- **Make** (recomendado, opcional)
- **Git** para clonar el repositorio

### Verificar Instalación

```bash
docker --version          # Docker Engine 20.10+
docker compose version    # Docker Compose v2+
make --version           # GNU Make (opcional)
```

## =€ Instalación Rápida

### Setup Inicial (Primera Vez)

```bash
# 1. Clonar el repositorio
git clone <repo-url>
cd 10code-intranet

# 2. Setup automático (recomendado)
make dev-setup
# Este comando:
# - Copia archivos de ejemplo (.env, secrets)
# - Construye las imágenes Docker
# - Levanta todos los servicios
# - Ejecuta migraciones automáticamente

# 3. Crear superusuario para acceder al admin
make createsuperuser

# 4. ¡Listo! Acceder a la aplicación
```

### Accesos

| Servicio | URL | Descripción |
|----------|-----|-------------|
| **Backend** | http://localhost:8000 | Django + Inertia.js |
| **Frontend** | http://localhost:5173 | Vite dev server (HMR) |
| **Admin** | http://localhost:8000/admin | Django Admin |
| **PostgreSQL** | localhost:5432 | Base de datos |
| **Redis** | localhost:6379 | Cache/Celery broker |

### Stack de Servicios

| Servicio | Puerto | Descripción |
|----------|--------|-------------|
| `web` | 8000 | Django backend (runserver con auto-reload) |
| `frontend` | 5173 | Vite dev server con HMR |
| `db` | 5432 | PostgreSQL 18 |
| `redis` | 6379 | Redis 8.2 (cache + Celery broker) |
| `celery_worker` | - | Procesamiento de tareas asíncronas |
| `celery_beat` | - | Tareas programadas (cron) |

## =» Desarrollo

### Uso Diario

```bash
# Levantar todos los servicios
make up

# Ver logs en tiempo real
make logs

# Detener servicios (mantiene datos)
make down

# Reiniciar servicios
make restart

# Ver estado de servicios
make ps

# Ver todos los comandos disponibles
make help
```

### Comandos Django

```bash
# Acceder al shell de Django
make shell

# Crear migraciones
make makemigrations

# Aplicar migraciones
make migrate

# Crear superusuario
make createsuperuser

# Recolectar archivos estáticos
make collectstatic

# Acceder al contenedor web
make bash-web
```

### Testing

```bash
# Ejecutar todos los tests
make test

# Tests con cobertura de código
make test-coverage

# Tests rápidos (sin migraciones)
make test-fast

# Tests de una app específica
docker compose exec web pytest apps/projects/tests/

# Tests con verbose
docker compose exec web pytest -v
```

**Cobertura mínima requerida:** 80%

### Base de Datos

```bash
# Acceder al shell de PostgreSQL
make db-shell

# Backup de base de datos
make db-backup

# Resetear base de datos (¡CUIDADO! Borra todos los datos)
make db-reset

# Ver logs de PostgreSQL
make logs-db
```

### Frontend

```bash
# Ver logs del frontend
make logs-frontend

# Reinstalar dependencias npm (si hay problemas)
make frontend-install

# Reiniciar solo frontend
docker compose restart frontend

# Build de producción
cd frontend && npm run build
```

El frontend usa **Vite** con HMR (Hot Module Replacement), por lo que los cambios en React se reflejan instantáneamente sin recargar la página.

### Logs y Debugging

```bash
# Logs de todos los servicios
make logs

# Logs de un servicio específico
make logs-web         # Backend Django
make logs-frontend    # Frontend Vite
make logs-db          # PostgreSQL
make logs-redis       # Redis
make logs-celery      # Celery worker

# Seguir logs en tiempo real (follow)
docker compose logs -f web

# Ver últimas 50 líneas
docker compose logs --tail=50 web
```

## > Desarrollo con Machine Learning

El proyecto incluye soporte opcional para **Machine Learning** (TensorFlow, PyTorch, scikit-learn) necesario para el módulo de **estimaciones CEPF**.

### ¿Cuándo Necesitas ML?

** Usa modo ML cuando:**
- Desarrollas el módulo de estimaciones CEPF
- Entrenas o pruebas modelos de ML
- Trabajas con procesamiento de lenguaje natural
- Necesitas TensorFlow o PyTorch

**L NO necesitas ML para:**
- Desarrollo de frontend
- Trabajo en módulos de proyectos, recursos, timetracking
- Testing general de la aplicación
- Desarrollo de APIs y vistas

### Setup con ML

```bash
# Setup completo con ML (primera vez)
make ml-setup

# O agregar ML a proyecto existente
make down
make ml-build    # Tarda ~10-15 min la primera vez
make ml-up
```

### Comandos ML

```bash
make ml-build      # Build de imágenes con ML (~10-15 min)
make ml-up         # Levantar servicios con ML
make ml-down       # Detener servicios con ML
make ml-logs       # Ver logs de servicios con ML
```

### Verificar Instalación de ML

```bash
make bash-web

# Dentro del contenedor
python -c "import tensorflow as tf; print(f'TensorFlow {tf.__version__}')"
python -c "import torch; print(f'PyTorch {torch.__version__}')"
python -c "import sklearn; print(f'scikit-learn {sklearn.__version__}')"

exit
```

### Recursos y Tiempos

| Configuración | Primera Build | Rebuilds | Tamaño |
|--------------|---------------|----------|--------|
| **Sin ML** (dev) | 2-3 min | 30-60 seg | ~1GB |
| **Con ML** | 10-15 min | 5-10 min | ~7GB |

**Requisitos mínimos para ML:**
- RAM: 8GB (16GB recomendado)
- Disco: 10GB libres
- CPU: 4 cores (8 cores recomendado)

> =Ú **Documentación completa:** Ver [docker/ML_README.md](docker/ML_README.md) para detalles sobre ML development.

## <× Arquitectura del Proyecto

El proyecto implementa una arquitectura de **Monolito Modular Majestuoso** con los siguientes principios:

### Principios Fundamentales

1. **Service Layer Pattern** - Toda lógica de negocio en `services.py`
2. **Thin Views, Fat Services** - Views solo routing HTTP
3. **Domain-Driven Design** - Apps organizadas por dominio de negocio
4. **Separation of Concerns** - Backend y Frontend físicamente separados
5. **Testing Obligatorio** - No merge sin tests (cobertura mínima 80%)

### Estructura del Proyecto

```
10code-intranet/
   apps/                    # Aplicaciones Django (módulos de dominio)
      core/               # Utilidades compartidas
      accounts/           # Usuarios y autenticación
      projects/           # Gestión de proyectos
      resources/          # Gestión de recursos humanos
      financial/          # Seguimiento financiero
      timetracking/       # Control horario
      estimation/         # Sistema CEPF + ML
      backlog/            # Gestión de backlog
      reporting/          # Reporting y BI

   config/                 # Configuración del proyecto
      settings/           # Settings (base, dev, prod)
      urls.py            # URLs principales
      wsgi.py / asgi.py  # WSGI/ASGI entry points

   frontend/               # Frontend React + Vite
      src/
          components/     # Componentes UI reutilizables
          pages/          # Páginas Inertia (rutas)
          lib/            # Utilidades y helpers

   docker/                 # Configuración Docker
      entrypoint.sh      # Script de inicialización
      ML_README.md       # Guía de ML development

   secrets/               # Secrets para desarrollo (gitignored)
   staticfiles/           # Archivos estáticos compilados
   media/                 # Media files (uploads)

   Dockerfile             # Multi-stage Docker build
   compose.yml           # Docker Compose base
   compose.override.yml  # Overrides para desarrollo
   compose.ml.yml        # Overlay para ML
   Makefile              # Comandos de desarrollo
   pyproject.toml        # Dependencias Python (uv)
   pytest.ini            # Configuración de tests
```

### Estructura Interna de Cada App

Cada aplicación Django sigue esta estructura obligatoria:

```
apps/[nombre_app]/
   models.py           # Solo estructura de datos + métodos simples
   services.py         #  WRITE operations - Lógica de negocio
   selectors.py        #  READ operations - Consultas optimizadas
   views.py            # Solo routing y props para Inertia
   urls.py             # URLs de la app
   admin.py            # Admin de Django
   managers.py         # Custom QuerySet managers
   enums.py            # Enumerations (choices)
   validators.py       # Validaciones custom
   signals.py          # Señales (usar con moderación)
   tasks.py            # Celery tasks
   tests/              # Tests completos
       factories.py    # Factory Boy fixtures
       test_models.py
       test_services.py
       test_selectors.py
       test_views.py
```

### Patrón Service Layer (Ejemplo)

```python
# apps/projects/services.py
from django.db import transaction

class ProjectService:
    @staticmethod
    @transaction.atomic
    def create_project(*, name: str, client: str, created_by: User):
        """Crear proyecto con validaciones y side effects."""
        # Validaciones de negocio
        if Project.objects.filter(name=name, client=client).exists():
            raise ValidationError("Proyecto ya existe")

        # Crear proyecto
        project = Project.objects.create(name=name, client=client)

        # Side effects
        ProjectMember.objects.create(project=project, user=created_by, role='PM')
        send_notification_task.delay(project.id)

        return project
```

### Patrón Selectors (Ejemplo)

```python
# apps/projects/selectors.py
def get_projects_list(*, user: User, filters: dict = None):
    """READ-only operations con optimizaciones."""
    qs = Project.objects.select_related(
        'created_by', 'client'
    ).prefetch_related(
        Prefetch('members', queryset=ProjectMember.objects.select_related('user'))
    )

    # Aplicar permisos
    if not user.is_staff:
        qs = qs.filter(Q(created_by=user) | Q(members__user=user)).distinct()

    return qs.order_by('-created_at')
```

### Views con Inertia (Thin Views)

```python
# apps/projects/views.py
from inertia import render
from .selectors import get_projects_list

@login_required
def projects_index(request):
    """View solo hace routing y prepara props."""
    projects = get_projects_list(user=request.user)

    return render(request, 'Projects/Index', props={
        'projects': [serialize_project(p) for p in projects],
        'permissions': {
            'can_create': request.user.has_perm('projects.add_project')
        }
    })
```

> =Ú **Documentación arquitectónica completa:** Ver [CLAUDE.md](CLAUDE.md) para reglas de desarrollo detalladas.

## =¢ Despliegue a Producción

### Build de Producción

```bash
# Build sin dependencias de desarrollo
docker compose -f compose.yml build --no-cache

# O usando make
make prod-build
```

### Variables de Entorno Críticas

En producción, configurar las siguientes variables en `.env`:

```bash
# Django
DEBUG=False
SECRET_KEY=<secret-key-from-django-secret-key.txt>
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DJANGO_SETTINGS_MODULE=config.settings.production

# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Redis
REDIS_URL=redis://redis:6379/0

# OAuth Google
GOOGLE_CLIENT_ID=xxx
GOOGLE_CLIENT_SECRET=xxx
ALLOWED_EMAIL_DOMAIN=10code.es

# Seguridad
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### Secrets Management

En producción, usar **Docker Secrets** o **Variables de Entorno** del hosting:

```bash
# Ejemplo con Docker Secrets
echo "your-secret-password" | docker secret create db_password -
echo "your-django-secret-key" | docker secret create django_secret_key -
```

### Checklist Pre-Deploy

- [ ] `DEBUG=False` en producción
- [ ] Configurar `ALLOWED_HOSTS` correctamente
- [ ] Usar secrets management (no archivos .txt)
- [ ] Configurar backups automáticos de PostgreSQL
- [ ] Configurar SSL/TLS (HTTPS)
- [ ] Configurar logs centralizados
- [ ] Tests pasando al 100%
- [ ] Cobertura de tests >80%
- [ ] Ejecutar `collectstatic` antes del deploy
- [ ] Configurar healthchecks y monitoring

### Arquitectura de Producción

Para producción se recomienda:

1. **Servidor Web:** Gunicorn + WhiteNoise (incluido)
2. **Proxy Reverso:** Nginx o Traefik (opcional, para HTTPS y load balancing)
3. **Base de Datos:** PostgreSQL 18 (managed service recomendado)
4. **Cache:** Redis (managed service recomendado)
5. **Storage:** S3-compatible para media files
6. **Monitoring:** Sentry para errores, Prometheus + Grafana para métricas

## =' Troubleshooting

### El frontend no carga

```bash
# Reinstalar dependencias npm
make frontend-install

# Reiniciar frontend
docker compose restart frontend

# Limpiar cache de Vite
docker compose exec frontend sh -c "rm -rf node_modules/.vite"
```

### Error de migraciones

```bash
# Ver migraciones pendientes
make shell
python manage.py showmigrations

# Ejecutar migraciones manualmente
make migrate

# Fake migration si es necesario
docker compose exec web python manage.py migrate --fake [app_name]
```

### Puerto 8000 o 5173 ocupado

```bash
# Cambiar puertos en .env
echo "WEB_PORT=8001" >> .env
echo "FRONTEND_PORT=5174" >> .env

# Reiniciar servicios
make down
make up
```

### Error: ModuleNotFoundError

```bash
# Verificar que estás usando la imagen correcta
docker compose ps

# Rebuild con dependencias correctas
make clean
make build
```

### Contenedores no inician

```bash
# Ver logs detallados
make logs

# Verificar salud de servicios
docker compose ps

# Reiniciar servicios problemáticos
docker compose restart web
```

### Base de datos no conecta

```bash
# Verificar que PostgreSQL está corriendo
docker compose ps db

# Ver logs de PostgreSQL
make logs-db

# Probar conexión manual
docker compose exec web python -c "import psycopg; psycopg.connect('postgresql://postgres:postgres@db:5432/10code_intranet')"
```

### Resetear Todo (Última Opción)

```bash
# CUIDADO: Esto borra TODOS los datos
make clean
make dev-setup
make createsuperuser
```

### Problemas con ML

Ver [docker/ML_README.md - Troubleshooting](docker/ML_README.md#-troubleshooting)

## =Ú Documentación Adicional

- **[CLAUDE.md](CLAUDE.md)** - Reglas arquitectónicas y de desarrollo del proyecto
- **[docker/ML_README.md](docker/ML_README.md)** - Guía completa para desarrollo con Machine Learning
- **[.env.example](.env.example)** - Variables de entorno disponibles
- **[Makefile](Makefile)** - Todos los comandos disponibles

### Recursos Externos

- [Django 5.2 Documentation](https://docs.djangoproject.com/en/5.2/)
- [Inertia.js Documentation](https://inertiajs.com/)
- [React Documentation](https://react.dev/)
- [Docker Compose Specification](https://docs.docker.com/compose/compose-file/)
- [uv Documentation](https://github.com/astral-sh/uv)

## > Contribuir

### Workflow de Desarrollo

1. **Crear rama** desde `develop`:
   ```bash
   git checkout develop
   git pull
   git checkout -b feature/nombre-feature
   ```

2. **Desarrollar** siguiendo las reglas de [CLAUDE.md](CLAUDE.md):
   - Service Layer Pattern obligatorio
   - Thin Views, Fat Services
   - Tests con cobertura >80%
   - Type hints en Python
   - Docstrings descriptivos

3. **Tests** antes de commit:
   ```bash
   make test
   make test-coverage
   ```

4. **Commit** con mensajes descriptivos:
   ```bash
   git commit -m "feat: agregar módulo de estimaciones CEPF"
   git commit -m "fix: corregir cálculo de disponibilidad de recursos"
   ```

5. **Push** y crear Pull Request:
   ```bash
   git push origin feature/nombre-feature
   ```

### Estándares de Código

- **Python:** Black, isort, flake8
- **TypeScript:** ESLint, Prettier
- **Commits:** Conventional Commits (`feat:`, `fix:`, `refactor:`, etc.)
- **Tests:** pytest con cobertura mínima 80%

### Code Review

Todos los PRs requieren:
-  Tests pasando (CI green)
-  Cobertura de código >80%
-  Code review aprobado
-  Sin conflictos con `develop`

## =Ý Licencia

Este proyecto es propiedad de **10Code** y es de uso interno exclusivo.

**Copyright © 2024 10Code. Todos los derechos reservados.**

---

## <˜ ¿Necesitas Ayuda?

Si tienes problemas:

1. **Revisa los logs:** `make logs`
2. **Consulta la documentación:** [CLAUDE.md](CLAUDE.md)
3. **Troubleshooting:** Ver sección de troubleshooting arriba
4. **Contacta al equipo:** Slack #dev-intranet

---

**¿Listo para desarrollar? =€**

```bash
make dev-setup
make createsuperuser
make logs
```

**Backend:** http://localhost:8000
**Frontend:** http://localhost:5173
**Admin:** http://localhost:8000/admin

---

<div align="center">
  <p>Desarrollado con =™ por el equipo de <strong>10Code</strong></p>
  <p><em>Django 5.2 " React 18 " Inertia.js " PostgreSQL 18 " Docker</em></p>
</div>
