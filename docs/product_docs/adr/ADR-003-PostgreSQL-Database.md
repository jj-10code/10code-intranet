# ADR-003: PostgreSQL 18+ como Base de Datos Principal

## Metadata

- **Status**: Accepted
- **Fecha**: 2025-11-17
- **Decisor(es)**: Juanje Márquez - 10Code
- **Tags**: arquitectura, backend, base-de-datos, infraestructura

---

## Contexto y Problema

El sistema Intranet 10Code requiere una base de datos relacional robusta que soporte:

- **Transacciones ACID**: Datos financieros, control horario y nóminas requieren integridad garantizada
- **Datos relacionales complejos**: Múltiples entidades con relaciones many-to-many (proyectos, usuarios, equipos, tareas)
- **Datos semi-estructurados**: Configuraciones por proyecto, metadatos extensibles, audit trails
- **Búsquedas avanzadas**: Full-text search en documentos, proyectos y tareas
- **Escalabilidad**: Preparación para crecimiento de 20 a 100+ usuarios
- **Django ORM**: Excelente soporte y optimización con el framework elegido
- **Normativa española**: Retención de datos de fichaje durante 4 años (RGPD + normativa laboral)

**Restricciones técnicas:**

- Equipo de desarrollo pequeño (1 desarrollador + agentes IA)
- Sin budget para licencias comerciales
- Infraestructura VPS (OVH) sin Kubernetes
- Necesidad de backups y disaster recovery simples

---

## Factores de Decisión

1. **Integridad de datos**: Garantías ACID para datos críticos (financieros, horarios, nóminas)
2. **Flexibilidad de esquema**: Soporte para JSONB y datos semi-estructurados
3. **Búsquedas avanzadas**: Full-text search nativo sin dependencias externas
4. **Integración Django**: Calidad del soporte en Django ORM (select_related, prefetch, annotations)
5. **Performance**: Optimización de queries complejas con índices y explain analyze
6. **Escalabilidad**: Capacidad de crecer con read replicas y particionado
7. **Madurez y estabilidad**: Track record en producción, comunidad activa
8. **Tooling**: Herramientas de administración, monitoring y backup
9. **Costo**: TCO (Total Cost of Ownership) considerando licencias, hosting, mantenimiento
10. **Curva de aprendizaje**: Experiencia del equipo y documentación disponible

---

## Opciones Consideradas

### Opción 1: PostgreSQL 18+

**Descripción:** Base de datos relacional open-source con extensiones avanzadas (JSONB, full-text search, PostGIS).

**Pros:**

- ✅ **JSONB nativo**: Flexibilidad para configuraciones, metadatos y audit trails sin sacrificar performance
- ✅ **Full-text search integrado**: Búsquedas avanzadas en español sin necesidad de Elasticsearch
- ✅ **ACID completo**: Transacciones robustas, crítico para datos financieros y horarios
- ✅ **Excelente soporte Django ORM**: Campos específicos (ArrayField, JSONField), índices GIN/GiST
- ✅ **Performance superior**: Query planner avanzado, índices parciales, EXPLAIN ANALYZE detallado
- ✅ **Escalabilidad probada**: Read replicas, particionado por rango/hash, sharding cuando sea necesario
- ✅ **Open-source**: Sin costos de licencia, comunidad masiva, soporte comercial disponible si necesario
- ✅ **Tooling maduro**: pgAdmin, psql, pg_dump, extensiones (pg_stat_statements, pg_trgm)
- ✅ **Versión 18+**: Mejoras recientes en JSON, paralelización, y logical replication

**Cons:**

- ❌ **Complejidad inicial**: Más complejo que SQLite o MySQL para configuración inicial
- ❌ **Memoria**: Requiere más RAM que MySQL para queries complejas (buffer pool)
- ❌ **Write amplification**: MVCC (Multi-Version Concurrency Control) genera más I/O en writes
- ❌ **VACUUM**: Necesita mantenimiento periódico (aunque autovacuum lo gestiona automáticamente)

---

### Opción 2: MySQL 8+

**Descripción:** Base de datos relacional open-source, popular en aplicaciones web.

**Pros:**

- ✅ **Simplicidad**: Setup inicial más simple que PostgreSQL
- ✅ **Performance en lecturas**: InnoDB optimizado para SELECT simples
- ✅ **Menor footprint**: Consume menos memoria que PostgreSQL
- ✅ **Replicación**: Master-slave replication madura y fácil de configurar
- ✅ **JSON support**: MySQL 8+ incluye soporte JSON (aunque menos robusto que JSONB)

**Cons:**

- ❌ **JSON inferior**: JSON como string, no tipo nativo binario como JSONB
- ❌ **Full-text search limitado**: Solo para MyISAM o InnoDB con limitaciones (no índices GIN)
- ❌ **Django ORM**: Soporte menos completo (no ArrayField nativo, JSONField más básico)
- ❌ **Licencia**: Oracle ownership, preocupaciones sobre futuro open-source
- ❌ **Transacciones**: Históricamente más débil que PostgreSQL en ACID (aunque InnoDB mejoró)
- ❌ **Extensiones**: Ecosistema de extensiones más limitado
- ❌ **Advanced queries**: Window functions y CTEs agregados tardíamente vs PostgreSQL

---

### Opción 3: SQLite

**Descripción:** Base de datos embebida, single-file, sin servidor separado.

**Pros:**

- ✅ **Zero-configuration**: Sin instalación ni servidor, perfecto para desarrollo local
- ✅ **Portabilidad**: Single file, fácil backup y migración
- ✅ **Ligero**: Footprint mínimo de memoria y disco
- ✅ **Django default**: Viene por defecto en Django para desarrollo

**Cons:**

- ❌ **Concurrencia**: Locking a nivel de base de datos, no soporta múltiples escritores
- ❌ **Sin network**: No accesible remotamente, inviable para arquitectura cliente-servidor
- ❌ **Escalabilidad**: No soporta read replicas, sharding ni horizontal scaling
- ❌ **Tipos de datos**: Menos tipos nativos, sin JSONB, sin arrays
- ❌ **Full-text search**: FTS5 menos potente que PostgreSQL para español
- ❌ **No production-ready**: Para aplicaciones web multi-usuario

---

## Decisión

**Opción elegida**: **PostgreSQL 18+**

**Justificación:**

Hemos decidido usar **PostgreSQL 18+** como base de datos principal porque:

1. **Integridad de datos crítica**: ACID completo es no-negociable para datos financieros (nóminas, facturas) y control horario (normativa española 2025). PostgreSQL tiene track record probado en sectores bancarios y financieros.

2. **Flexibilidad con JSONB**: Las configuraciones específicas por proyecto (sprint duration, velocity, capacity buffer) y metadatos extensibles (audit trails, integraciones) se benefician enormemente de JSONB sin sacrificar performance. Esto evita migraciones constantes de esquema.

3. **Full-text search nativo**: Búsquedas en español (proyectos, tareas, documentos) sin necesidad de Elasticsearch reduce complejidad operativa. Extensión `unaccent` + diccionario español permite búsquedas "inteligentes".

4. **Django ORM de primera clase**: `ArrayField`, `JSONField`, índices GIN/GiST, `select_related` optimizado, `prefetch_related` con Prefetch objects. PostgreSQL es el target primario de Django ORM, MySQL es secundario.

5. **Escalabilidad sin reescritura**: Read replicas para dashboards y reportes pesados, particionado por fecha para control horario (tablas por año), logical replication para futuros multi-tenant. Todo sin cambiar código de aplicación.

6. **Open-source maduro**: Sin preocupaciones de licencia (vs Oracle/MySQL), comunidad masiva, soporte comercial si necesario (EnterpriseDB, Crunchy Data). Versión 18 trae mejoras significativas en JSON y paralelización.

7. **Tooling excepcional**: pgAdmin para administración, `pg_dump` para backups consistentes, `pg_stat_statements` para análisis de queries, extensiones (PostGIS si geolocalización futura).

**Alternativas descartadas:**

- **MySQL**: JSON inferior, Django ORM secundario, preocupaciones de licencia Oracle
- **SQLite**: Inviable para multi-usuario, sin concurrencia, no escalable

---

## Consecuencias

### Positivas

- ✅ **Integridad garantizada**: ACID completo para datos críticos (finanzas, horarios, nóminas)
- ✅ **Flexibilidad de esquema**: JSONB permite iteración rápida sin migraciones complejas
- ✅ **Búsquedas avanzadas**: Full-text search nativo en español, sin dependencias externas
- ✅ **Django ORM optimizado**: Aprovechamiento completo de features PostgreSQL-specific
- ✅ **Escalabilidad preparada**: Read replicas, particionado, sharding disponibles cuando se necesiten
- ✅ **Tooling maduro**: pgAdmin, pg_dump, pg_stat_statements, extensiones ricas
- ✅ **Comunidad activa**: Stack Overflow, documentación excelente, soporte comercial disponible
- ✅ **Sin vendor lock-in**: Open-source puro, múltiples proveedores de hosting (AWS RDS, Heroku, DigitalOcean)

### Negativas

- ❌ **Curva de aprendizaje**: Más complejo que MySQL/SQLite para configuración inicial (tunning, VACUUM, replication)
- ❌ **Recursos**: Requiere más RAM (shared_buffers, work_mem) que MySQL para queries complejas
- ❌ **Write amplification**: MVCC genera más I/O en writes vs MySQL InnoDB
- ❌ **Mantenimiento**: VACUUM periódico necesario (aunque autovacuum lo gestiona), analyze stats para query planner
- ❌ **Setup inicial**: Más pasos que SQLite (servidor separado, configuración postgresql.conf)

### Neutras

- ⚠️ **Monitoreo de performance**: Necesitamos implementar pg_stat_statements y slow query log desde MVP
- ⚠️ **Backup strategy**: Definir policy de backups (pg_dump diario + WAL archiving para PITR)
- ⚠️ **Tunning inicial**: Configurar shared_buffers, effective_cache_size según VPS (4GB RAM inicial)
- ⚠️ **Índices estratégicos**: Planificar índices GIN para JSONB, índices parciales para soft-deletes, índices compuestos para queries frecuentes
- ⚠️ **Connection pooling**: Implementar pgBouncer si concurrencia supera 50 conexiones

---

## Notas de Implementación

### Configuración Inicial PostgreSQL 18

```yaml
# docker-compose.yml (fragmento)
services:
  db:
    image: postgres:18-alpine
    environment:
      POSTGRES_DB: ${DATABASE_NAME:-10code_intranet}
      POSTGRES_USER: ${DATABASE_USER:-postgres}
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./config/postgres/postgresql.conf:/etc/postgresql/postgresql.conf
    command: postgres -c config_file=/etc/postgresql/postgresql.conf
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DATABASE_USER:-postgres}"]
      interval: 10s
      timeout: 5s
      retries: 5
    secrets:
      - db_password
```

### Tunning Inicial (4GB RAM VPS)

```conf
# config/postgres/postgresql.conf

# Conexiones
max_connections = 100

# Memoria
shared_buffers = 1GB              # 25% de RAM total
effective_cache_size = 3GB        # 75% de RAM total
work_mem = 10MB                   # shared_buffers / max_connections
maintenance_work_mem = 256MB      # Para VACUUM, CREATE INDEX

# WAL (Write-Ahead Log)
wal_buffers = 16MB
checkpoint_completion_target = 0.9

# Query planner
random_page_cost = 1.1            # SSD vs HDD (default 4.0)
effective_io_concurrency = 200    # SSD concurrent I/O

# Autovacuum
autovacuum = on
autovacuum_max_workers = 2
autovacuum_naptime = 1min
```

### Django Settings

```python
# config/settings/base.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DATABASE_NAME', default='10code_intranet'),
        'USER': env('DATABASE_USER', default='postgres'),
        'PASSWORD': read_secret('db_password', required=True),
        'HOST': env('DATABASE_HOST', default='localhost'),
        'PORT': env('DATABASE_PORT', default='5432'),
        'ATOMIC_REQUESTS': True,  # Transacciones automáticas por request
        'CONN_MAX_AGE': 600,      # Connection pooling (10 min)
        'OPTIONS': {
            'connect_timeout': 10,
            'options': '-c search_path=public',
        },
    }
}
```

### Extensiones Esenciales

```sql
-- Instalar en base de datos principal
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";      -- UUIDs nativos
CREATE EXTENSION IF NOT EXISTS "unaccent";       -- Búsquedas sin acentos
CREATE EXTENSION IF NOT EXISTS "pg_trgm";        -- Trigram matching para fuzzy search
CREATE EXTENSION IF NOT EXISTS "btree_gin";      -- Índices GIN para tipos comunes
```

### Índices Estratégicos

```python
# apps/projects/models.py
class Project(models.Model):
    # ... fields ...
    
    class Meta:
        indexes = [
            # Búsquedas por status + fecha
            models.Index(fields=['status', '-created_at']),
            
            # Índice GIN para full-text search en nombre
            GinIndex(fields=['name'], opclasses=['gin_trgm_ops']),
            
            # Índice GIN para JSONB config
            GinIndex(fields=['config']),
            
            # Índice parcial para proyectos activos (soft-delete)
            models.Index(
                fields=['client', 'status'],
                name='active_projects_idx',
                condition=models.Q(deleted_at__isnull=True)
            ),
        ]
```

### Backups Automáticos

```bash
#!/bin/bash
# scripts/backup_postgres.sh

BACKUP_DIR="/backups/postgresql"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DB_NAME="10code_intranet"
DB_USER="postgres"

# Backup completo con pg_dump (custom format, comprimido)
PGPASSWORD=$(cat /run/secrets/db_password) pg_dump \
    -U $DB_USER \
    -h localhost \
    -Fc \
    -f "$BACKUP_DIR/backup_${TIMESTAMP}.dump" \
    $DB_NAME

# Retener solo últimos 30 días
find $BACKUP_DIR -name "backup_*.dump" -mtime +30 -delete

# Notificar resultado
if [ $? -eq 0 ]; then
    echo "✅ Backup exitoso: backup_${TIMESTAMP}.dump"
else
    echo "❌ Error en backup" >&2
    exit 1
fi
```

### Monitoring con pg_stat_statements

```sql
-- Habilitar extensión
CREATE EXTENSION pg_stat_statements;

-- Query para identificar queries lentas
SELECT 
    query,
    calls,
    total_exec_time / 1000 AS total_seconds,
    mean_exec_time / 1000 AS mean_seconds,
    max_exec_time / 1000 AS max_seconds
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 20;
```

### Migraciones Django

```python
# apps/core/migrations/0001_enable_extensions.py
from django.contrib.postgres.operations import CreateExtension
from django.db import migrations

class Migration(migrations.Migration):
    initial = True
    
    operations = [
        CreateExtension('uuid-ossp'),
        CreateExtension('unaccent'),
        CreateExtension('pg_trgm'),
        CreateExtension('btree_gin'),
    ]
```

---

## Referencias

### Documentación Oficial

- [PostgreSQL 18 Documentation](https://www.postgresql.org/docs/18/)
- [Django + PostgreSQL Best Practices](https://docs.djangoproject.com/en/5.0/ref/databases/#postgresql-notes)
- [PostgreSQL Performance Tuning](https://wiki.postgresql.org/wiki/Performance_Optimization)
- [pg_stat_statements Documentation](https://www.postgresql.org/docs/18/pgstatstatements.html)

### Comparativas y Benchmarks

- [PostgreSQL vs MySQL Performance Comparison 2024](https://www.enterprisedb.com/blog/postgresql-vs-mysql-performance)
- [Django ORM with PostgreSQL-specific features](https://docs.djangoproject.com/en/5.0/ref/contrib/postgres/)
- [JSONB Performance in PostgreSQL](https://www.postgresql.org/docs/18/datatype-json.html)

### Herramientas

- [pgAdmin 4](https://www.pgadmin.org/) - GUI de administración
- [PgBouncer](https://www.pgbouncer.org/) - Connection pooler
- [pgtune](https://pgtune.leopard.in.ua/) - Generador de configuración optimizada

### Artículos Técnicos

- [Full-Text Search in PostgreSQL](https://www.postgresql.org/docs/18/textsearch.html)
- [JSONB Performance Tips](https://heap.io/blog/engineering/when-to-avoid-jsonb-in-a-postgresql-schema)
- [PostgreSQL Backup and Recovery Best Practices](https://www.postgresql.org/docs/18/backup.html)

---

## Historial

| Fecha | Evento |
|-------|--------|
| 2025-11-17 | ADR creado y aceptado por Juanje Márquez |

---

**Firmado por:**

- Juanje Márquez - Arquitecto Principal & Lead Developer - 2025-11-17
