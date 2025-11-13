# 🚀 Docker Quick Start - 10Code Intranet

Guía rápida para empezar a desarrollar con Docker en menos de 5 minutos.

## ⚡ Setup Rápido (Primera Vez)

```bash
# 1. Clonar el repositorio
git clone <repo-url>
cd 10code-intranet

# 2. Setup automático (recomendado)
make dev-setup

# 3. Crear superusuario
make createsuperuser

# 4. ¡Listo! Acceder a la aplicación
# Backend: http://localhost:8000
# Frontend: http://localhost:5173
# Admin: http://localhost:8000/admin
```

## 🎯 Uso Diario

```bash
# Levantar servicios
make up

# Ver logs
make logs

# Detener servicios
make down

# Ver todos los comandos disponibles
make help
```

## 📋 Stack de Servicios

| Servicio | Puerto | Descripción |
|----------|--------|-------------|
| **web** | 8000 | Django backend (runserver) |
| **frontend** | 5173 | Vite dev server (HMR) |
| **db** | 5432 | PostgreSQL 18 |
| **redis** | 6379 | Redis 8.2 (cache/Celery) |
| **celery_worker** | - | Tareas asíncronas |
| **celery_beat** | - | Tareas programadas |

## 🔑 Requisitos Previos

- Docker Engine 20.10+
- Docker Compose v2+
- Make (opcional, pero recomendado)

## 📖 Comandos Más Usados

### Desarrollo

```bash
make up              # Levantar servicios
make logs            # Ver logs
make logs-web        # Ver logs del backend
make logs-frontend   # Ver logs del frontend
make restart         # Reiniciar servicios
make ps              # Ver estado de servicios
```

### Django Management

```bash
make shell           # Django shell
make migrate         # Ejecutar migraciones
make makemigrations  # Crear migraciones
make createsuperuser # Crear superusuario
make collectstatic   # Recolectar estáticos
```

### Testing

```bash
make test            # Ejecutar tests
make test-coverage   # Tests con cobertura
make test-fast       # Tests rápidos (sin migraciones)
```

### Database

```bash
make db-shell        # Abrir PostgreSQL shell
make db-backup       # Backup de base de datos
make db-reset        # Resetear DB (¡CUIDADO!)
```

### Limpieza

```bash
make clean           # Limpiar contenedores y volúmenes
make down            # Detener servicios
```

## 🔧 Troubleshooting

### El frontend no carga

```bash
# Reinstalar dependencias npm
make frontend-install

# Reiniciar frontend
docker compose restart frontend
```

### Error de migraciones

```bash
# Ejecutar migraciones manualmente
make migrate
```

### Puerto 8000 o 5173 ocupado

```bash
# Editar .env y cambiar puertos
WEB_PORT=8001
# Luego:
make down
make up
```

### Resetear todo

```bash
# Eliminar todo y empezar de cero
make clean
make dev-setup
```

## 📚 Documentación Completa

- [Docker README](docker/README.md) - Documentación completa de Docker
- [CLAUDE.md](CLAUDE.md) - Reglas de desarrollo del proyecto
- [README.md](README.md) - Información general del proyecto

## 🆘 Ayuda

Si tienes problemas:

1. Verifica que Docker esté corriendo: `docker ps`
2. Revisa los logs: `make logs`
3. Lee la documentación completa: [docker/README.md](docker/README.md)
4. Consulta con el equipo en Discord/Slack

## 📝 Nota sobre Docker Compose

Este proyecto usa la **Compose Specification moderna**:
- Comando: `docker compose` (con espacio, no guion)
- Archivo: `compose.yml` (no `docker-compose.yml`)
- Sin línea `version` en los archivos YAML

---

**¿Listo para desarrollar? 🚀**

```bash
make dev-setup
make createsuperuser
make logs
```

**Backend:** http://localhost:8000
**Frontend:** http://localhost:5173
**Admin:** http://localhost:8000/admin
