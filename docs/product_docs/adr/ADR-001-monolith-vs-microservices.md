# ADR-001: Arquitectura Monolítica vs Microservicios

## Metadata

- **Status**: Accepted
- **Fecha**: 2024-11-14
- **Decisor(es)**: Juanje Márquez (Arquitecto Principal - 10Code)
- **Tags**: arquitectura, backend, deployment, escalabilidad

---

## Contexto y Problema

La Intranet 10Code requiere gestionar múltiples dominios de negocio interconectados: RR.HH., proyectos, comercial, finanzas, control horario, estimaciones con ML, etc. Debemos decidir la arquitectura fundamental del sistema.

**Contexto técnico:**

- **Equipo**: 1 desarrollador principal + agentes de IA como asistentes de código
- **Usuarios**: ~20 empleados internos (escalable a 50+)
- **Dominio**: Sistema interno corporativo (no SaaS público)
- **Stack**: Django 5 + React + Inertia.js ya seleccionado
- **Complejidad de negocio**: Alta (10+ módulos interconectados con reglas complejas)
- **Flujos transaccionales**: Críticos (fichajes, nóminas, facturación)

**Problema a resolver:**

¿Debe el sistema implementarse como:

1. **Monolito tradicional** con todo el código en una aplicación Django
2. **Microservicios** con servicios independientes por dominio
3. **Monolito Modular** con separación lógica interna pero deployment unificado

**Fuerzas en conflicto:**

- ⚡ **Velocidad de desarrollo** vs 🏗️ **Escalabilidad futura**
- 🔧 **Simplicidad operativa** vs 🎯 **Aislamiento de fallos**
- 💰 **Costo de infraestructura** vs 🚀 **Performance distribuida**
- 🧪 **Facilidad de testing** vs 🔒 **Seguridad por aislamiento**

---

## Factores de Decisión

### Factor 1: Complejidad Operativa y Velocidad de Desarrollo

**Peso**: Crítico (⭐⭐⭐⭐⭐)

Equipo de 1 persona debe poder desplegar, monitorear y mantener el sistema sin fricción.

### Factor 2: Integridad de Datos y Transacciones

**Peso**: Crítico (⭐⭐⭐⭐⭐)

Datos financieros, horarios y nóminas requieren garantías ACID estrictas.

### Factor 3: Escalabilidad Técnica

**Peso**: Medio (⭐⭐⭐)

Sistema interno con 20-50 usuarios; escalabilidad masiva no es requisito MVP.

### Factor 4: Debugging y Observabilidad

**Peso**: Alto (⭐⭐⭐⭐)

Developer único necesita trazabilidad completa para resolver bugs rápidamente.

### Factor 5: Costo de Infraestructura

**Peso**: Alto (⭐⭐⭐⭐)

Budget limitado de startup; optimizar costos operativos es importante.

### Factor 6: Preparación para Evolución Futura

**Peso**: Medio (⭐⭐⭐)

Posible evolución a SaaS multi-tenant; arquitectura no debe bloquear futuro.

---

## Opciones Consideradas

### Opción 1: Microservicios (MSA - Microservices Architecture)

**Descripción técnica:**

Arquitectura distribuida con servicios independientes:

```markdown
Service: hr-service (Python/Django)
Service: projects-service (Python/Django)
Service: commercial-service (Python/Django)
Service: financial-service (Python/Django)
Service: api-gateway (Node.js/Kong)
Service: auth-service (OAuth2 centralizado)
Infrastructure: Kubernetes + Istio + Consul
```

**Pros:**

- ✅ **Escalabilidad independiente**: Cada servicio escala según su carga
- ✅ **Aislamiento de fallos**: Bug en un servicio no tumba todo el sistema
- ✅ **Tecnologías heterogéneas**: Cada servicio puede usar stack diferente
- ✅ **Deployment independiente**: Desplegar cambios sin afectar otros servicios
- ✅ **Ownership claro**: Equipos dedicados por servicio (en empresas grandes)

**Cons:**

- ❌ **Complejidad operativa brutal**: Kubernetes, service mesh, distributed tracing, circuit breakers
- ❌ **Overhead de red**: Latencia en cada llamada inter-servicio (80-200ms)
- ❌ **Transacciones distribuidas**: Sagas/2PC complejas; eventual consistency inevitable
- ❌ **Debugging infernal**: Stack traces fragmentados, logs distribuidos
- ❌ **Testing complejo**: Necesita contract testing, mocks de servicios, entornos integrados
- ❌ **Costo infraestructura**: Múltiples VMs/containers, load balancers, API gateway
- ❌ **Fricción en desarrollo**: Developer debe levantar 10+ servicios localmente
- ❌ **Serialización constante**: JSON en cada boundary; performance penalty

**Evaluación para 10Code:**

- ⛔ **BLOCKER**: Equipo de 1 persona no puede gestionar orquestador + 10 servicios
- ⛔ **BLOCKER**: Transacciones distribuidas incompatibles con integridad financiera
- ⛔ **BLOCKER**: Costo operativo (VPS múltiples) insostenible para startup

---

### Opción 2: Monolito Tradicional

**Descripción técnica:**

Aplicación Django única con estructura flat:

```markdown
apps/
├── views.py (todas las vistas mezcladas)
├── models.py (todos los modelos en un archivo)
├── urls.py (todas las URLs juntas)
└── services.py (lógica de negocio sin organización)
```

**Pros:**

- ✅ **Simplicidad máxima**: Un solo proceso, un solo deployment
- ✅ **Transacciones ACID nativas**: Django ORM garantiza integridad
- ✅ **Debugging trivial**: Stack trace completo en un solo lugar
- ✅ **Performance**: Sin overhead de red; queries optimizables con ORM
- ✅ **Costo mínimo**: Un solo VPS, PostgreSQL, Redis

**Cons:**

- ❌ **Acoplamiento alto**: Cambios en un módulo pueden romper otros
- ❌ **Testing difícil**: Tests unitarios contaminados por dependencias globales
- ❌ **Escalabilidad limitada**: Solo scale vertical (más CPU/RAM al VPS)
- ❌ **Deployment monolítico**: Bug en un módulo requiere redesplegar todo
- ❌ **Onboarding lento**: Nuevos developers tardan en entender codebase enorme

**Evaluación para 10Code:**

- ⚠️ **RISK**: Sin modularidad, evolución futura a SaaS es refactor masivo
- ⚠️ **RISK**: Acoplamiento alto dificulta trabajo con múltiples agentes IA
- ✅ **FIT**: Simplicidad operativa aceptable para MVP

---

### Opción 3: Monolito Modular Majestuoso (Elegida)

**Descripción técnica:**

Monolito físico con disciplina modular interna:

```markdown
apps/
├── accounts/          # Bounded Context: Identidad
│   ├── services.py    # Interfaz pública
│   ├── selectors.py   # Queries optimizadas
│   ├── models.py      # Modelos del dominio
│   └── views.py       # Inertia endpoints
├── projects/          # Bounded Context: Proyectos
│   ├── services.py    # ÚNICA entrada para crear/modificar proyectos
│   ├── selectors.py
│   └── ...
└── hr/                # Bounded Context: RR.HH.
    └── ...

# Comunicación entre bounded contexts
from apps.projects.services import ProjectService  # ✅ CORRECTO
from apps.projects.models import Project           # ❌ EVITAR (solo para FK)
```

**Patrones clave:**

1. **Service Layer Pattern**: 80% de comunicación inter-módulos vía funciones explícitas
2. **Domain-Driven Design**: Cada app Django = Bounded Context completo
3. **Inertia.js**: SPA sin necesidad de API REST separada (reduce complejidad)
4. **Async preparado**: Services pueden migrar a Celery sin cambiar interfaces

**Pros:**

- ✅ **Simplicidad operativa de monolito**: Single deployment, un proceso, debugging simple
- ✅ **Disciplina modular de MSA**: Bounded contexts, interfaces explícitas, bajo acoplamiento
- ✅ **Transacciones ACID**: `@transaction.atomic` en Django garantiza integridad
- ✅ **Performance**: Sin overhead de red; queries optimizables con select_related
- ✅ **Testing robusto**: Services testeables aisladamente; integración real sin mocks
- ✅ **Evolución futura**: Extraer app Django a servicio independiente es factible
- ✅ **IA-friendly**: Agentes pueden trabajar en bounded contexts aislados
- ✅ **Costo mínimo**: Infraestructura de monolito (1 VPS + PostgreSQL + Redis)

**Cons:**

- ❌ **Disciplina requerida**: Developers deben respetar boundaries (no importaciones salvajes)
- ❌ **Escalabilidad limitada a vertical**: Scale horizontal requiere refactor (pero factible)
- ⚠️ **Deployment acoplado**: Bug crítico requiere redesplegar todo (mitigable con feature flags)

**Evaluación para 10Code:**

- ✅ **PERFECT FIT**: Equilibrio ideal simplicidad/modularidad para equipo pequeño
- ✅ **PERFECT FIT**: Permite trabajo paralelo con agentes IA en bounded contexts
- ✅ **PERFECT FIT**: Preparado para evolución futura sin sobre-ingeniería

---

## Decisión

**Opción elegida**: **Opción 3 - Monolito Modular Majestuoso**

**Justificación:**

Implementaremos un **monolito físico** (single Django application) con **modularidad interna estricta** (Domain-Driven Design + Service Layer Pattern). Esta arquitectura proporciona:

### 1. Velocidad de Desarrollo Óptima

```python
# ✅ Crear proyecto con todas las garantías en una transacción
@transaction.atomic
def create_project(name: str, client: str, created_by: User):
    project = Project.objects.create(...)
    ProjectMember.objects.create(project=project, user=created_by)
    sync_with_google_drive.delay(project.id)  # Async opcional
    return project

# vs Microservicios ❌
# 1. POST /projects → project-service
# 2. POST /members → membership-service (puede fallar!)
# 3. POST /integrations/drive → integration-service (puede fallar!)
# 4. Implementar saga de compensación si alguno falla
```

**Impacto**: Developer puede implementar features completas en horas, no días.

### 2. Integridad de Datos Garantizada

```python
# ✅ Fichaje + imputación horaria en transacción ACID
@transaction.atomic
def close_timesheet(user_id: int, date: date):
    timesheet = Timesheet.objects.select_for_update().get(...)
    timesheet.validate_hours()  # Lanza ValidationError si < 6h
    timesheet.status = 'closed'
    timesheet.save()

    # Crear imputaciones a proyectos
    for task in timesheet.tasks.all():
        TimeEntry.objects.create(...)

    # Auditoría automática
    AuditLog.objects.create(...)

# vs Microservicios ❌
# Eventual consistency = riesgo de inconsistencias en nóminas
```

**Impacto**: Datos financieros y laborales siempre consistentes; cumplimiento legal garantizado.

### 3. Debugging y Observabilidad Simple

```python
# ✅ Stack trace completo en un solo lugar
Traceback (most recent call last):
  File "apps/projects/views.py", line 45, in create_project
  File "apps/projects/services.py", line 120, in create_project
  File "apps/hr/services.py", line 78, in assign_project_member
django.core.exceptions.ValidationError: Usuario sin disponibilidad

# vs Microservicios ❌
# Logs distribuidos en 3+ servicios; correlación de request-id necesaria
```

**Impacto**: Developer encuentra y corrige bugs en minutos, no horas.

### 4. Infraestructura Mínima y Costo Reducido

```yaml
# ✅ Stack completo en 1 VPS
services:
  web: Django + Gunicorn (4 workers)
  db: PostgreSQL 18
  cache: Redis 8.2
  worker: Celery (2 workers)

# Costo: ~50€/mes (VPS OVH)

# vs Microservicios ❌
# - 5+ VPS (uno por servicio)
# - Kubernetes cluster
# - API Gateway
# - Service mesh
# Costo: ~300-500€/mes
```

**Impacto**: ROI positivo desde día 1; budget invertido en features, no infraestructura.

### 5. Preparación para Evolución Futura

```python
# ✅ Bounded Context bien definido
# apps/estimation/services.py
class EstimationService:
    @staticmethod
    def estimate_project(requirements: dict) -> EstimationResult:
        # Lógica autocontenida
        pass

# Futuro: Extraer a servicio independiente
# 1. Copiar apps/estimation/ a nuevo repo
# 2. Exponer como REST API
# 3. Reemplazar import por HTTP call en monolito
# 4. Deploy independiente

# Minimal refactor; interfaz ya está definida
```

**Impacto**: Migración a MSA futura es incremental, no reescritura completa.

### 6. IA-Friendly: Agentes Trabajan en Paralelo

```bash
# ✅ Agente 1: Implementar apps/timetracking/
# ✅ Agente 2: Implementar apps/commercial/
# ✅ Agente 3: Implementar apps/dashboards/

# Bounded contexts aislados = zero conflictos Git
# Service Layer = contratos claros para integración
```

**Impacto**: Múltiples agentes IA pueden trabajar simultáneamente sin pisarse.

---

## Consecuencias

### Positivas

- ✅ **Time-to-market rápido**: MVP en 3 meses vs 6+ con MSA
- ✅ **Mantenibilidad alta**: Service Layer + DDD = código predecible y testeable
- ✅ **Performance superior**: Sin latencia de red; queries optimizables con ORM
- ✅ **Costo operativo mínimo**: ~50€/mes vs ~500€/mes con MSA
- ✅ **Developer experience óptimo**: Un comando para levantar todo localmente
- ✅ **Cumplimiento legal garantizado**: Transacciones ACID para datos críticos

### Negativas

- ❌ **Disciplina requerida**: Developers/agentes deben respetar Service Layer (no importaciones directas)
- ❌ **Escalabilidad limitada inicialmente**: Solo scale vertical hasta ~100 usuarios concurrentes
- ❌ **Deployment acoplado**: Bug crítico en un módulo requiere redesplegar todo (mitigable con feature flags + rollback rápido)

### Neutras

- ⚠️ **Monitoreo de boundaries**: Necesitamos CI checks para prevenir violaciones de arquitectura
- ⚠️ **Documentación crítica**: Service Layer debe estar bien documentado para onboarding futuro
- ⚠️ **Reevaluación periódica**: Revisar decisión cuando usuarios > 50 o módulos > 15

---

## Notas de Implementación

### Estructura de Apps Django (Bounded Contexts)

```bash
apps/
├── core/              # Solo infraestructura (modelos base, utils)
├── accounts/          # Bounded Context: Identidad
├── hr/                # Bounded Context: RR.HH.
├── timetracking/      # Bounded Context: Control Horario
├── projects/          # Bounded Context: Gestión Proyectos
├── commercial/        # Bounded Context: CRM
└── estimation/        # Bounded Context: Estimaciones ML
```

### Service Layer Pattern (Obligatorio)

```python
# apps/projects/services.py
class ProjectService:
    @staticmethod
    @transaction.atomic
    def create_project(
        *,
        name: str,
        client: str,
        methodology: str,
        created_by: User,
        **kwargs
    ) -> Project:
        """
        ÚNICA entrada para crear proyectos.
        Garantiza: validaciones, side effects, auditoría.
        """
        # 1. Validar permisos
        if not created_by.has_perm('projects.add_project'):
            raise PermissionDenied()

        # 2. Crear proyecto
        project = Project.objects.create(...)

        # 3. Side effects
        ProjectMember.objects.create(...)

        # 4. Tareas async
        create_drive_folder.delay(project.id)

        return project
```

### Comunicación Entre Módulos

```python
# ✅ CORRECTO: Via Service Layer
from apps.projects.services import ProjectService

def handle_opportunity_won(opportunity_id: int):
    project = ProjectService.create_project(
        name=opportunity.name,
        client=opportunity.client,
        created_by=opportunity.owner
    )

# ❌ EVITAR: Importación directa de modelos
from apps.projects.models import Project

def handle_opportunity_won(opportunity_id: int):
    project = Project.objects.create(...)  # Bypassing validaciones!
```

### CI Checks para Boundaries

```yaml
# .github/workflows/architecture-checks.yml
- name: Check architecture boundaries
  run: |
    # Verificar que views no importan modelos directamente
    ! grep -r "from apps.*.models import" apps/*/views.py

    # Verificar que no hay circular imports
    python scripts/check_circular_imports.py
```

---

## Referencias

- [Django Design Philosophies](https://docs.djangoproject.com/en/5.0/misc/design-philosophies/)
- [Monolith First - Martin Fowler](https://martinfowler.com/bliki/MonolithFirst.html)
- [Domain-Driven Design - Eric Evans](https://www.domainlanguage.com/ddd/)
- [Django Service Layer Pattern - HackSoft](https://github.com/HackSoftware/Django-Styleguide)
- [Majestic Monolith - DHH](https://m.signalvnoise.com/the-majestic-monolith/)
- [When to Split a Monolith - Sam Newman](https://www.thoughtworks.com/insights/blog/microservices/when-to-split-monolith)

---

## Historial

| Fecha | Evento |
|-------|--------|
| 2024-11-14 | ADR creado y aceptado como decisión arquitectónica fundamental |

---

**Firmado por:**

- Juanje Márquez - Arquitecto Principal - 2024-11-14
