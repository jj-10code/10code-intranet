# ADR-006: Celery + Redis para Tareas Asíncronas y Cache

## Metadata

- **Status**: Accepted
- **Fecha**: 2025-11-17
- **Decisor(es)**: Juanje Márquez (Arquitecto Principal)
- **Tags**: backend, infraestructura, performance, async

---

## Contexto y Problema

La Intranet 10Code requiere procesamiento asíncrono para operaciones que no pueden bloquear el flujo de usuario:

**Casos de uso identificados:**

- Sincronizaciones con sistemas externos (ODOO, GitHub, Google Drive) - pueden tardar 10-60 segundos
- Generación de reportes complejos (PDFs multi-página, análisis de datos) - 5-30 segundos
- Procesamiento ML para estimaciones - 2-15 segundos según volumen
- Envío de emails y notificaciones - sin bloquear response
- Tareas de mantenimiento programadas (limpieza de sesiones, backups)

**Restricciones técnicas:**

- Arquitectura monolítica Django 5
- Equipo pequeño (1 developer principal + agentes IA)
- Presupuesto limitado para infraestructura
- Necesidad de cache distribuido para performance (dashboards, sesiones)

**Requerimientos:**

- Queue persistence (no perder tareas en restart)
- Retry logic con backoff exponencial
- Task scheduling para operaciones periódicas
- Monitoring básico de estado de tareas
- Cache distribuido para múltiples workers Django

---

## Factores de Decisión

- **Facilidad de integración**: Tiempo de setup y configuración con Django
- **Madurez del ecosistema**: Documentación, community support, estabilidad
- **Performance**: Latencia de encolado y throughput
- **Persistence**: Garantía de no perder tareas críticas
- **Operabilidad**: Complejidad de deployment y monitoring
- **Costo total**: Infraestructura + mantenimiento
- **Escalabilidad**: Capacidad de crecer con el proyecto

---

## Opciones Consideradas

### Opción 1: Celery + Redis

**Descripción:** Task queue distribuida con Redis como message broker. Celery es el estándar de facto en Django para tareas asíncronas.

**Pros:**

- ✅ Integración nativa con Django (`django-celery-beat`, `django-celery-results`)
- ✅ Ecosystem maduro: monitoring (Flower), debugging, extensive docs
- ✅ Soporta task scheduling (Celery Beat), retries, chaining, groups
- ✅ Redis ya necesario para cache - sin infraestructura adicional
- ✅ Persistencia mediante Redis AOF/RDB
- ✅ Horizontal scaling: agregar workers sin cambio de código

**Cons:**

- ❌ Curva de aprendizaje moderada (configuración inicial compleja)
- ❌ Overhead para tareas muy simples vs RQ
- ❌ Requiere proceso separado (worker + beat scheduler)

---

### Opción 2: RQ (Redis Queue)

**Descripción:** Task queue minimalista diseñada para simplicidad. Usa Redis como backend.

**Pros:**

- ✅ Setup extremadamente simple (5 líneas de código)
- ✅ Menor overhead que Celery para tareas simples
- ✅ Dashboard web incluido (rq-dashboard)
- ✅ Pythonic API intuitiva

**Cons:**

- ❌ Sin scheduling nativo (necesita rq-scheduler separado)
- ❌ Menos features avanzadas (no task chaining, groups limitados)
- ❌ Ecosystem más pequeño que Celery
- ❌ No soporta múltiples brokers (solo Redis)

---

### Opción 3: APScheduler

**Descripción:** Python scheduler sin broker externo. Ejecuta tareas en procesos separados o threads.

**Pros:**

- ✅ Zero external dependencies (no Redis necesario)
- ✅ Muy simple para scheduling periódico
- ✅ Lightweight

**Cons:**

- ❌ Sin persistence robusta (tareas se pierden en crash)
- ❌ No distribuido (no múltiples workers)
- ❌ Sin retry logic sofisticado
- ❌ No apto para workloads pesados (sincronizaciones, ML)

---

### Opción 4: AWS SQS + Lambda

**Descripción:** Solución cloud-native con SQS como queue y Lambda para ejecución.

**Pros:**

- ✅ Fully managed, zero ops overhead
- ✅ Auto-scaling infinito
- ✅ Pay-per-use

**Cons:**

- ❌ Vendor lock-in total (incompatible con VPS auto-hospedado)
- ❌ Costo variable impredecible
- ❌ Latencia cold start en Lambdas
- ❌ Requiere refactor completo de architecture (no monolito)

---

## Decisión

**Opción elegida**: Celery + Redis

**Justificación:**

Celery + Redis es la elección correcta para este proyecto por:

1. **Ecosystem Django maduro**: Integración probada en miles de proyectos producción. `django-celery-beat` permite scheduling desde Django admin sin configuración externa.

2. **Redis dual-purpose**: Ya necesitamos Redis para cache de sesiones y queries. Reutilizarlo como broker elimina complejidad infraestructura (un solo servicio adicional vs dos).

3. **Feature completeness**: Casos de uso requieren scheduling (sincronizaciones diarias ODOO), retries con backoff (GitHub webhooks pueden fallar), chaining (generar PDF → subir a Drive → notificar). Celery soporta todo nativamente.

4. **Escalabilidad futura**: Si el proyecto crece a SaaS multi-tenant, Celery escala horizontalmente agregando workers sin refactor. APScheduler y RQ no escalan igual.

5. **Operabilidad aceptable**: Aunque Celery requiere 2 procesos adicionales (worker + beat), Docker Compose abstrae complejidad. Monitoring con Flower es plug-and-play.

**Trade-offs aceptados:**

- Curva aprendizaje inicial Celery (mitigable con docs y ejemplos en codebase)
- Overhead para tareas triviales (aceptable dado que mayoría son operaciones pesadas)

---

## Consecuencias

### Positivas

- ✅ **Single source of truth para async**: Todo procesamiento asíncrono usa Celery, no mixtos
- ✅ **Retry automático**: Sincronizaciones externas resilientes a fallos transitorios
- ✅ **Scheduling sin cron**: Tareas programadas gestionadas desde Django admin
- ✅ **Monitoring built-in**: Flower dashboard muestra estado tareas en real-time
- ✅ **Cache distribuido**: Redis cache compartido entre workers Django y Celery

### Negativas

- ❌ **Complejidad operativa**: 3 procesos a deployar (web, celery_worker, celery_beat)
- ❌ **Debugging más difícil**: Logs distribuidos entre Django y Celery workers
- ❌ **Memory footprint**: Workers Celery consumen ~150MB RAM cada uno

### Neutras

- ⚠️ **Configuración inicial**: Requiere definir CELERY_BROKER_URL, CELERY_RESULT_BACKEND, Beat schedule - documentado en SAD
- ⚠️ **Redis SPOF**: Si Redis cae, tanto cache como tasks fallan (mitigable con Redis Sentinel futuro)

---

## Notas de Implementación

### Configuración Base

```python
# config/settings/base.py
CELERY_BROKER_URL = env("CELERY_BROKER_URL", default="redis://localhost:6379/1")
CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND", default="redis://localhost:6379/2")
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/Madrid'

# Retry policy por defecto
CELERY_TASK_ACKS_LATE = True
CELERY_TASK_REJECT_ON_WORKER_LOST = True
```

### Celery Beat Schedule

```python
# config/settings/base.py
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'sync-odoo-daily': {
        'task': 'apps.integrations_odoo.tasks.sync_odoo_data',
        'schedule': crontab(hour=2, minute=0),  # 2 AM diario
    },
    'cleanup-expired-sessions': {
        'task': 'apps.core.tasks.cleanup_sessions',
        'schedule': crontab(hour=3, minute=0),
    },
}
```

### Template de Task

```python
# apps/projects/tasks.py
from celery import shared_task
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def sync_github_repository(self, project_id: int):
    """
    Sincronizar proyecto con repositorio GitHub.
    
    Retry automático 3 veces con 60s entre intentos.
    """
    try:
        from apps.projects.services import ProjectService
        ProjectService.sync_with_github(project_id=project_id)
        logger.info(f"GitHub sync completado: project_id={project_id}")
    except Exception as exc:
        logger.error(f"Error syncing GitHub: {exc}", extra={'project_id': project_id})
        raise self.retry(exc=exc)
```

### Docker Compose Services

```yaml
# compose.yml (extracto)
services:
  celery_worker:
    build: .
    command: celery -A config worker --loglevel=info --concurrency=2
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/1
    depends_on:
      - db
      - redis

  celery_beat:
    build: .
    command: celery -A config beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/1
    depends_on:
      - db
      - redis
```

### Dependencias

```toml
# pyproject.toml
dependencies = [
    "celery[redis]>=5.5.3",
    "django-celery-beat>=2.5.0",  # Scheduling desde Django admin
    "django-celery-results>=2.5.0",  # Resultados en DB
    "flower>=2.0.1",  # Monitoring UI
]
```

---

## Referencias

- [Celery Documentation](https://docs.celeryq.dev/)
- [django-celery-beat](https://django-celery-beat.readthedocs.io/)
- [Redis as Celery Broker](https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/redis.html)
- [Flower Monitoring](https://flower.readthedocs.io/)
- [Django + Celery Best Practices](https://realpython.com/asynchronous-tasks-with-django-and-celery/)

---

## Historial

| Fecha | Evento |
|-------|--------|
| 2025-11-17 | ADR-006 creado y aceptado |

---

**Firmado por:**

- Juanje Márquez - Arquitecto Principal - 2025-11-17
