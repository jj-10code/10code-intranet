# SAD: Software Architecture Document

## Intranet 10Code - Sistema Integral de Gestión Empresarial

## Metadata

- **Versión del documento**: 1.5
- **Fecha de creación**: 2024-11-14
- **Última actualización**: 2025-11-17
- **Arquitecto principal**: Juanje Márquez - 10Code
- **Revisores técnicos**: Pendiente
- **Estado**: Living Document

---

## 1. Introducción

### 1.1 Propósito del Documento

Este documento describe la arquitectura de software de la **Intranet 10Code - Sistema Integral de Gestión Empresarial**. Define las decisiones arquitectónicas clave, el stack tecnológico, patrones de diseño, y lineamientos técnicos para el desarrollo.

**Audiencia:** Desarrollador principal (Juanje), agentes de IA de codificación, futuros desarrolladores del equipo, mantenedores del sistema.

### 1.2 Alcance

Este SAD cubre:

- ✅ Arquitectura de alto nivel (sistema completo)
- ✅ Stack tecnológico con justificaciones técnicas
- ✅ Patrones de diseño y comunicación entre módulos
- ✅ Estructura de código y organización de apps Django
- ✅ Estrategias de datos, seguridad, performance, testing
- ✅ Infraestructura, deployment y CI/CD

Este SAD **NO** cubre:

- ❌ Detalles de implementación por módulo (ver FSDs específicos)
- ❌ Requisitos funcionales de negocio (ver PRD)
- ❌ Manuales de usuario o documentación operativa
- ❌ Historias de usuario específicas (ver FSDs)

---

## 2. Visión Arquitectónica

### 2.1 Filosofía Arquitectónica: Monolito Modular Majestuoso

El sistema sigue el patrón **"Majestic Modular Monolith"**, una arquitectura que combina lo mejor de ambos mundos:

**¿Por qué Monolito?**

- ✅ **Simplicidad operativa**: Single deployment unit, un solo proceso a desplegar
- ✅ **Velocidad de desarrollo**: Sin overhead de comunicación entre servicios
- ✅ **Transacciones ACID**: Integridad de datos garantizada sin distributed transactions
- ✅ **Debugging simple**: Stack trace completo, no hay network calls misteriosos
- ✅ **Equipo pequeño**: Un desarrollador principal puede gestionar todo el sistema
- ✅ **Infraestructura mínima**: PostgreSQL + Redis, sin orquestadores complejos

**¿Por qué NO Microservicios (ahora)?**

- ❌ Complejidad operativa prematura innecesaria
- ❌ Overhead en comunicación entre servicios (latencia, serialización)
- ❌ Gestión de datos distribuidos compleja
- ❌ Fricción en desarrollo para equipo de 1 persona + agentes IA
- ❌ Necesidad de orquestadores (Kubernetes), service mesh, etc.

#### **Modularidad Interna (La Clave del "Majestuoso")**

Aunque es un monolito físico, internamente está estructurado como microservicios lógicos:

- 📦 **Apps Django autocontenidas**: Cada módulo es un "bounded context" en DDD
- 🔒 **Interfaces claras**: Service Layer como API interna entre módulos
- 🧩 **Bajo acoplamiento**: Comunicación explícita, no importaciones salvajes
- 🏗️ **Alta cohesión**: Todo el código de un dominio junto
- 🚀 **Preparado para MSA futuro**: Si escala a SaaS, extraer apps es factible

#### **Habilitador Clave: Inertia.js**

Inertia.js elimina la complejidad de mantener una API REST separada:

- **Frontend moderno (React SPA)** + **Backend tradicional (Django server-rendered)**
- Sin necesidad de serializers DRF, endpoints REST, gestión de estado compleja
- Backend envía props JSON directamente a componentes React
- Navegación SPA sin página completa reload
- Simplifica testing: No hay dos codebases (API + Frontend) a testear

### 2.2 Principios Guía SOLID & Best Practices

1. **KISS (Keep It Simple, Stupid)**: Priorizar simplicidad sobre sofisticación prematura
2. **YAGNI (You Ain't Gonna Need It)**: No construir funcionalidad hasta que sea necesaria
3. **DRY (Don't Repeat Yourself)**: Código reutilizable, evitar duplicación
4. **Separation of Concerns**: Service Layer separa lógica de negocio de views/models
5. **Convention over Configuration**: Seguir estándares Django/React donde sea posible
6. **Fail Fast**: Validaciones tempranas, errores explícitos mejor que silenciosos
7. **Explicit > Implicit**: Type hints, nombres claros, docstrings

### 2.3 Arquitectura de Alto Nivel (C4 Model - Context)

```mermaid
C4Context
    title Sistema de Contexto - Intranet 10Code
    
    Person(employees, "Empleados 10Code", "Usuarios internos: Directivos, PM, Developers, Comerciales, RRHH")
    
    System(intranet, "Intranet 10Code", "Monolito Django 5 + Inertia.js<br/>Gestión integral: RR.HH., Proyectos, Comercial, Finanzas")
    
    System_Ext(google, "Google Workspace", "OAuth 2.0, Gmail, Google Drive")
    System_Ext(github, "GitHub", "Repositorios, Commits, Webhooks")
    System_Ext(odoo, "ODOO ERP", "Facturas, Nóminas, Contabilidad")
    System_Ext(discord, "Discord", "Notificaciones a equipos")
    System_Ext(openrouter, "OpenRouter", "LLM API (Claude, GPT, etc.)")
    
    Rel(employees, intranet, "Usa", "HTTPS")
    Rel(intranet, google, "Autenticación + Docs + Email", "OAuth 2.0 / Drive API / SMTP")
    Rel(intranet, github, "Sincroniza repos + commits", "GitHub API + Webhooks")
    Rel(intranet, odoo, "Importa datos financieros", "XML-RPC / REST")
    Rel(intranet, discord, "Envía notificaciones", "Webhooks")
    Rel(intranet, openrouter, "Consulta LLMs", "REST API")
```

**Flujo de Datos Principal:**

1. Usuario se autentica con Google OAuth (@10code.es)
2. Navega SPA (Inertia.js) sin recargas de página
3. Django procesa requests, consulta PostgreSQL, cachea en Redis
4. Tareas pesadas (sincronizaciones, ML) se ejecutan en Celery workers
5. Integraciones externas (GitHub, ODOO, Drive) vía APIs REST/Webhooks
6. LLMs consultados vía OpenRouter para estimaciones y asistencia

### 2.4 Decisiones Arquitectónicas Críticas

Este proyecto documenta decisiones arquitectónicas significativas mediante **Architecture Decision Records (ADRs)**. Los ADRs son documentos inmutables que registran el contexto, opciones consideradas y justificación de decisiones técnicas importantes.

Las siguientes decisiones tienen **ADRs detallados** que se crearán en `/docs/adr/`:

| ID  | Decisión | Justificación Breve | Estado ADR |
|-----|----------|---------------------|------------|
| ADR-001 | **Monolito vs Microservicios** | Equipo pequeño, complejidad innecesaria, deployment simple | Pendiente |
| ADR-002 | **Django + inertia-django** | Elimina API REST duplicada, desarrollo más rápido, DX superior | Pendiente |
| ADR-003 | **PostgreSQL** | JSONB para flexibilidad, robustez, excelente soporte Django ORM | Pendiente |
| ADR-004 | **uv como gestor de dependencias** | 10-100x más rápido que pip, compatible con pyproject.toml | Pendiente |
| ADR-005 | **Tiptap + WeasyPrint** | Editor moderno WYSIWYG, generación PDF server-side confiable | Pendiente |
| ADR-006 | **Celery + Redis** | Tareas asíncronas (ETL, integraciones), cache distribuido | Pendiente |
| ADR-007 | **OpenRouter para LLMs** | Acceso multi-modelo, cost-effective, sin vendor lock-in | Pendiente |
| ADR-008 | **Service Layer Pattern** | Desacoplamiento, transacciones, testabilidad, evolución a async | Pendiente |

---

## 3. Stack Tecnológico

### 3.1 Resumen Visual del Stack

```bash
┌─────────────────────────────────────────────────────────────┐
│                      FRONTEND (Client)                       │
│  React 19 + TypeScript + Inertia.js Client                  │
│  UI: Tailwind CSS 4 + shadcn/ui components                  │
│  Editor: Tiptap (WYSIWYG/Markdown)                          │
│  Build: Vite 7 (HMR, optimizado)                            │
└─────────────────────────────────────────────────────────────┘
                              ↕ (Props JSON via Inertia)
┌─────────────────────────────────────────────────────────────┐
│                      BACKEND (Server)                        │
│  Django 5.2.8+ (Python 3.14+) + PostgreSQL 18              │
│  inertia-django (Adapter) + Django ORM                      │
│  Service Layer + Selector Pattern                           │
│  django-allauth (Google OAuth)                              │
└─────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────┐
│            ASYNC & CACHE (Background Tasks)                 │
│  Celery 5.5.3+ (workers) + Redis 8.2 (broker + cache)       │
│  Celery Beat (scheduled tasks)                              │
└─────────────────────────────────────────────────────────────┘
                             ↕
┌─────────────────────────────────────────────────────────────┐
│               INTEGRACIONES & ML (External)                 │
│  Google APIs, GitHub API, ODOO, Discord Webhooks           │
│  OpenRouter → Claude, GPT-4, etc. (LLM access)             │
│  scikit-learn, pandas (ML cuando se implemente)            │
└─────────────────────────────────────────────────────────────┘
                             ↕
┌─────────────────────────────────────────────────────────────┐
│             INFRAESTRUCTURA (Deployment)                    │
│  Docker + Docker Compose                                    │
│  Nginx (reverse proxy + static files)                      │
│  Gunicorn (WSGI server, workers)                           │
│  GitHub Actions (CI/CD)                                     │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 Detalle de Tecnologías por Capa

#### **Backend Core**

| Componente | Versión | Propósito | Justificación Técnica |
|------------|---------|-----------|----------------------|
| **Python** | 3.14+ | Lenguaje base | Type hints modernos, pattern matching, performance superior, características más recientes |
| **Django** | 5.2.8+ | Framework web | ORM maduro, admin auto-generado, seguridad built-in, ecosistema rico |
| **PostgreSQL** | 18+ | Base de datos relacional | JSONB nativo, full-text search, robustez ACID, escalabilidad horizontal futura |
| **uv** | 0.4+ | Gestor de dependencias | 10-100x más rápido que pip, compatible pyproject.toml, Rust-based |
| **inertia-django** | 1.2.0+ | Adaptador Inertia.js | Puente Django ↔ React sin API REST, reduce complejidad |
| **django-allauth** | 65.13.0+ | Autenticación OAuth | Google OAuth out-of-the-box, probado en producción, versión actual estable |
| **Celery** | 5.5.3+ | Task queue asíncrona | ETL, integraciones, emails, reportes pesados |
| **Redis** | 8.2+ | Cache + Broker Celery | Performance, sesiones distribuidas, pub/sub |
| **Gunicorn** | 23.0.0+ | WSGI server | Multi-worker, estable en producción, fácil configuración |
| **Pydantic** | 2.8+ | Validación de datos | Type hints avanzados, validación automática, conversión de tipos, mejor DX |

**Razón de Django sobre FastAPI/Flask:**

- ORM de clase mundial vs SQLAlchemy más verboso
- Admin panel automático para gestión rápida
- Ecosistema de paquetes maduro (allauth, celery, etc.)
- Seguridad por defecto (CSRF, XSS, SQL injection protection)
- Inertia.js elimina necesidad de API REST pura (ventaja de FastAPI)

#### **Frontend Stack**

| Componente | Versión | Propósito | Justificación Técnica |
|------------|---------|-----------|----------------------|
| **React** | 19+ | UI framework | Hooks, Suspense, Concurrent rendering, ecosistema masivo |
| **TypeScript** | 5+ | Tipado estático | Menos bugs en runtime, IntelliSense, refactoring seguro |
| **Inertia.js** | 2+ | SPA sin API tradicional | Elimina API REST separada, simplifica stack, mejor DX |
| **Vite** | 7+ | Build tool & dev server | HMR instantáneo, builds optimizados, ESM nativo |
| **Tailwind CSS** | 4+ | Utility-first CSS | Desarrollo rápido, mobile-first, tree-shaking automático |
| **shadcn/ui** | - | Component library | Componentes accesibles (ARIA), customizables, copy-paste (no NPM bloat) |
| **Tiptap** | 2+ | Editor WYSIWYG | Basado en ProseMirror, extensible, markdown-friendly |
| **React Hook Form** | 7+ | Gestión de formularios | Performance (uncontrolled), validación, integración con yup/zod |
| **TanStack Query** | 5+ | Data fetching (si necesario) | Cache inteligente, refetch automático, optimistic updates |

**Razón de React sobre Vue/Svelte:**

- Inertia.js tiene adaptador oficial más maduro para React
- shadcn/ui (componentes de calidad) solo disponible para React
- Ecosistema de librerías más amplio
- Experiencia previa del equipo

#### **Machine Learning & Data Science**

| Componente | Versión | Propósito | Fase de Uso |
|------------|---------|-----------|-------------|
| **OpenRouter** | - | Gateway multi-modelo LLM | **MVP**: Estimaciones con prompting |
| **scikit-learn** | 1.4+ | ML clásico (regresión, clustering) | **Fase 2+**: Si se valida necesidad de ML entrenado |
| **pandas** | 2.1+ | Manipulación de datos, análisis | **Fase 2+**: Para análisis de datos históricos |
| **numpy** | 1.26+ | Operaciones numéricas | **Fase 2+**: Base de scikit-learn |

**Estrategia ML:**

1. **MVP**: Sin ML tradicional, usar LLMs vía OpenRouter (Claude, GPT-4) para estimaciones con prompting
2. **Fase 2**: Si prompting no es suficiente, entrenar modelos con scikit-learn sobre datos históricos
3. **Fase 3**: Si volumen lo justifica, considerar TensorFlow/PyTorch para deep learning

#### **Infraestructura & DevOps**

| Componente | Versión | Propósito |
|------------|---------|-----------|
| **Docker** | 24+ | Containerización de aplicación |
| **Docker Compose** | 2.23+ | Orquestación local & staging |
| **Nginx** | 1.25+ | Reverse proxy, servir static files, SSL termination |
| **GitHub Actions** | - | CI/CD pipelines automáticos |
| **pytest** | 7+ | Testing framework Python |
| **Playwright** | 1.40+ | End-to-end testing |

### 3.3 Gestión de Dependencias con `uv`

**Archivo [`pyproject.toml`](pyproject.toml) (PEP 621):**

El archivo `pyproject.toml` contiene la configuración completa del proyecto incluyendo:

- Metadatos del proyecto (nombre, versión, descripción, autores)
- Dependencias de producción, desarrollo y ML
- Configuración de herramientas de desarrollo (Ruff, Black, MyPy, pytest)
- Sistema de construcción con Hatchling
- Configuración de empaquetado y distribución

**Comandos `uv` principales:**

```bash
# Instalar dependencias (10-100x más rápido que pip)
uv pip install -e .

# Instalar con dependencias de desarrollo
uv pip install -e ".[dev]"

# Sincronizar exactamente con pyproject.toml
uv pip sync

# Actualizar dependencias
uv pip install --upgrade django celery

# Crear virtualenv con uv (opcional)
uv venv
source .venv/bin/activate
```

**Ventajas de `uv`:**

- ⚡ 10-100x más rápido que pip (escrito en Rust)
- 📦 Compatible 100% con pip y pyproject.toml
- 🔒 Lock files automáticos para reproducibilidad
- 🚀 Instalaciones paralelas
- 💾 Cache global inteligente

---

## 4. Arquitectura Detallada (C4 Model - Container)

### 4.1 Diagrama de Contenedores

```mermaid
C4Container
    title Diagrama de Contenedores - Intranet 10Code
    
    Person(user, "Usuario", "Empleado 10Code")
    
    Container_Boundary(monolith, "Intranet 10Code - Monolito") {
        Container(web, "Web Application", "Django 5 + Gunicorn", "Lógica de negocio, vistas Inertia, API interna")
        Container(frontend, "Frontend SPA", "React 18 + TypeScript + Vite", "UI/UX, componentes, formularios")
        ContainerDb(db, "Base de Datos", "PostgreSQL 15", "Usuarios, proyectos, horarios, finanzas, backlog")
        Container(cache, "Cache & Broker", "Redis 7", "Cache de sesiones, queries, broker Celery")
        Container(worker, "Async Workers", "Celery Workers", "ETL, integraciones, emails, reportes")
        Container(beat, "Scheduler", "Celery Beat", "Tareas programadas (sync ODOO, cleanup)")
    }
    
    System_Ext(google, "Google Workspace", "OAuth, Gmail, Drive")
    System_Ext(github, "GitHub API", "Repos, commits, issues")
    System_Ext(odoo, "ODOO ERP", "Facturas, nóminas")
    System_Ext(discord, "Discord Webhooks", "Notificaciones")
    System_Ext(openrouter, "OpenRouter", "LLM access")
    
    Rel(user, web, "Visita & usa", "HTTPS")
    Rel(web, frontend, "Sirve HTML + JSON props", "Inertia protocol")
    Rel(frontend, web, "Llamadas XHR/Fetch", "Inertia.visit()")
    
    Rel(web, db, "Lee/Escribe", "Django ORM / SQL")
    Rel(web, cache, "Get/Set cache", "Redis protocol")
    Rel(web, worker, "Encola tareas", "Celery via Redis")
    
    Rel(worker, db, "Lee/Escribe")
    Rel(worker, cache, "Lee cache")
    Rel(beat, worker, "Dispara tareas programadas")
    
    Rel(web, google, "OAuth + Drive + Gmail", "HTTPS/REST")
    Rel(worker, github, "Webhook receiver + API calls", "HTTPS/REST")
    Rel(worker, odoo, "Sincroniza datos", "XML-RPC")
    Rel(worker, discord, "Notificaciones", "Webhooks")
    Rel(web, openrouter, "Consulta LLMs", "HTTPS/REST")
```

### 4.2 Flujos de Datos Críticos

Los siguientes flujos de datos críticos conectan los módulos del sistema Intranet 10Code, asegurando la integridad y el flujo de información en tiempo real entre módulos y con sistemas externos. Cada flujo se describe de manera básica y simple, y será detallado en el FSD correspondiente según el marco de documentación técnica.

#### Flujos de Datos Críticos Identificados

1. **Autenticación → Todos los módulos**: Proporciona datos de usuarios, roles y permisos para acceso controlado.
   *Detallado en FSD - Autenticación y Usuarios y referenciado en cada FSD de módulo.*

2. **RR.HH. → Planificación**: Transfiere datos de capacidad, ausencias y disponibilidad de recursos humanos.
   *Detallado en FSD - Módulo RR.HH. y Control Horario y FSD - Módulo Planificación de Recursos.*

3. **RR.HH. → Producción**: Alimenta datos de tiempo trabajado y capacidad para imputación y seguimiento.
   *Detallado en FSD - Módulo RR.HH. y Control Horario y FSD - Módulo Gestión de Proyectos.*

4. **Comercial → Producción**: Convierte oportunidades aceptadas en proyectos activos con requisitos iniciales.
   *Detallado en FSD - Módulo Comercial + CRM y FSD - Módulo Gestión de Proyectos.*

5. **Estimación → Comercial**: Proporciona estimaciones de esfuerzo para generar ofertas y contratos.
   *Detallado en FSD - Sistema de Estimación y FSD - Módulo Comercial + CRM.*

6. **Planificación → Producción**: Asigna recursos humanos a proyectos con porcentajes de dedicación.
   *Detallado en FSD - Módulo Planificación de Recursos y FSD - Módulo Gestión de Proyectos.*

7. **Producción → Planificación**: Actualiza carga real de trabajo y progreso para recalcular disponibilidad.
   *Detallado en FSD - Módulo Gestión de Proyectos y FSD - Módulo Planificación de Recursos.*

8. **Producción → Dashboards**: Envía métricas de progreso, tiempo imputado y estado de proyectos.
   *Detallado en FSD - Módulo Gestión de Proyectos y FSD - Módulo Dashboards.*

9. **Todos los módulos → Dashboards**: Consolida KPIs financieros, comerciales, de RR.HH. y productivos.
   *Detallado en FSD - Módulo Dashboards y referenciado en cada FSD de módulo fuente.*

10. **Producción → Documentación**: Vincula documentos de proyecto, actas y entregas.
    *Detallado en FSD - Módulo Gestión de Proyectos y FSD - Módulo Documentación.*

11. **Integraciones Externas → Sistema**: Importa commits de GitHub, datos financieros de ODOO y documentos de Google Drive.
    *Detallado en FSD correspondiente al módulo receptor (ej. Producción para GitHub, Dashboards para ODOO) y en especificaciones de integración.*

Estos flujos críticos aseguran la trazabilidad completa desde la oportunidad comercial hasta la entrega del proyecto, con datos centralizados y en tiempo real. Cada FSD detallará los modelos de datos, validaciones, APIs y lógica de negocio específica para implementar estos flujos de manera robusta y escalable.

---

## 5. Estructura de Código y Organización

### 5.1 Estructura de Directorios Completa

```bash
10code-intranet/
├── .github/workflows/          # CI/CD
├── apps/                       # Django apps (Bounded Contexts)
│   ├── core/                   # Solo infraestructura
│   ├── accounts/               # Autenticación
│   ├── hr/                     # RR.HH.
│   ├── timetracking/           # Control horario
│   ├── commercial/             # CRM
│   ├── projects/               # Proyectos
│   ├── backlog/                # Backlog
│   ├── resources/              # Planificación recursos
│   ├── financial/              # Finanzas
│   ├── documents/              # Documentación
│   ├── estimation/             # Estimaciones
│   ├── dashboards/             # Cuadros mando
│   ├── integrations_google/    # Integración Google Workspace
│   ├── integrations_github/    # Integración GitHub
│   ├── integrations_odoo/      # Integración ODOO ERP
│   ├── integrations_discord/   # Integración Discord
│   └── integrations_openrouter/ # Integración OpenRouter (LLMs)
├── config/                     # Configuración Django
├── frontend/                   # React + Inertia
├── docs/                       # Documentación
├── tests/                      # Tests integración
├── pyproject.toml
└── docker-compose.yml
```

> **Nota sobre integraciones:** Las integraciones externas se implementan como apps Django separadas para mantener modularidad, facilitar pruebas independientes y permitir activación/desactivación por entorno. Esto sigue las mejores prácticas de Django para bounded contexts.

### 5.2 Patrón Service Layer (80% comunicación)

**¿Por qué Fat Services?** Usamos servicios 'gordos' (fat services) que contienen toda la lógica de negocio, validaciones y orquestación. Esto desacopla la lógica de negocio de las vistas y modelos, facilitando testing, reutilización y evolución hacia async. Los servicios manejan transacciones atómicas, side effects y logging centralizado.

**Template de Service:**

```python
# apps/projects/services.py
from django.db import transaction
from typing import Optional
from decimal import Decimal

class ProjectService:
    @staticmethod
    @transaction.atomic
    def create_project(
        *,
        name: str,
        client: str,
        methodology: str,
        created_by: User,
        budget: Optional[Decimal] = None,
        **kwargs
    ) -> Project:
        """
        Crear proyecto con validaciones completas.

        Args:
            name: Nombre del proyecto
            client: Cliente asociado
            methodology: scrum | kanban | waterfall | hybrid
            created_by: Usuario creador
            budget: Presupuesto opcional

        Returns:
            Proyecto creado

        Raises:
            ValidationError: Si datos inválidos
            PermissionError: Si usuario sin permisos
        """
        # 1. Validar permisos
        if not created_by.has_perm('projects.add_project'):
            raise PermissionDenied(...)

        # 2. Validar negocio
        if Project.objects.filter(name=name, client=client).exists():
            raise ValidationError(...)

        # 3. Crear entidad
        project = Project.objects.create(...)

        # 4. Side effects
        ProjectMember.objects.create(...)

        # 5. Tareas async
        create_project_drive_folder.delay(project.id)

        # 6. Logging
        logger.info(...)

        return project
```

**Template de Selector (Lectura):**

```python
# apps/projects/selectors.py
from typing import Optional, Dict
from django.db.models import QuerySet, Q, Prefetch

def get_projects_list(
    *,
    user: User,
    filters: Optional[Dict] = None
) -> QuerySet[Project]:
    """
    Obtener lista de proyectos optimizada.

    Args:
        user: Usuario para permisos
        filters: Filtros opcionales

    Returns:
        QuerySet optimizado
    """
    # Base optimizado
    qs = Project.objects.select_related(
        'created_by'
    ).prefetch_related(
        Prefetch(
            'members',
            queryset=ProjectMember.objects.select_related('user')
        )
    )

    # Permisos
    if not user.is_staff:
        qs = qs.filter(
            Q(created_by=user) | Q(members__user=user)
        ).distinct()

    # Filtros
    if filters:
        if 'status' in filters:
            qs = qs.filter(status=filters['status'])

    return qs.order_by('-created_at')
```

---

## 6. Base de Datos y Modelo de Datos

### 6.1 Estrategia de Datos

#### PostgreSQL como Base de Datos Principal

**Justificación técnica:**

- **JSONB nativo**: Flexibilidad para datos semi-estructurados (configuraciones, metadatos)
- **Full-text search**: Búsquedas avanzadas sin necesidad de ElasticSearch
- **Robustez ACID**: Garantía de integridad transaccional crítica para datos financieros
- **Escalabilidad**: Read replicas y particionado horizontal disponibles
- **Madurez del ORM Django**: Excelente soporte con Django ORM

#### Redis como Cache y Message Broker

**Usos principales:**

- Cache de sesiones de usuario
- Cache de consultas frecuentes (dashboards, listas)
- Broker de Celery para tareas asíncronas
- Rate limiting de APIs y endpoints críticos
- Cache de permisos de usuario

### 6.2 Principios de Diseño de Datos

#### Normalización con Pragmatismo

- **3FN como base**: Normalización hasta tercera forma normal por defecto
- **Desnormalización estratégica**: Para dashboards y reportes de alto rendimiento
- **JSONB para flexibilidad**: Metadatos, configuraciones, audit trails
- **Soft deletes**: Campos `deleted_at` para trazabilidad, no borrados físicos

#### Modelos por Módulo

Cada app Django tiene sus propios modelos siguiendo DDD (Domain-Driven Design). Los modelos representan entidades de negocio claras y autocontenidas.

**Referencia detallada**: Ver FSDs de cada módulo para estructura completa de modelos.

### 6.3 Patrones de Modelado

**¿Por qué Thin Models?** Los modelos deben ser delgados (thin models), conteniendo solo estructura de datos y métodos simples. Toda lógica de negocio reside en services, facilitando testing, reutilización y mantenibilidad. Los modelos incluyen propiedades calculadas básicas sin queries complejas.

#### Modelo Base Abstracto

```python
# apps/core/models.py
from django.db import models
from django.utils import timezone

class TimestampedModel(models.Model):
    """Modelo base con timestamps automáticos."""
    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class SoftDeletableModel(TimestampedModel):
    """Modelo base con soft delete."""
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def is_deleted(self) -> bool:
        return self.deleted_at is not None
```

#### Choices como Enums

```python
class Project(models.Model):
    """Modelo de Proyecto."""

    class Status(models.TextChoices):
        DRAFT = 'draft', 'Borrador'
        ACTIVE = 'active', 'Activo'
        COMPLETED = 'completed', 'Completado'
        ARCHIVED = 'archived', 'Archivado'

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
        db_index=True
    )
```

#### Campos JSONB para Flexibilidad

```python
class ProjectConfig(models.Model):
    """Configuración específica de proyecto."""

    project = models.OneToOneField(Project, on_delete=models.CASCADE)

    # Configuraciones específicas por metodología
    config = models.JSONField(default=dict)
    # Ejemplo: {'sprint_duration': 14, 'velocity': 40, 'capacity_buffer': 0.15}

    # Metadatos extensibles
    metadata = models.JSONField(default=dict)
```

### 6.4 Migraciones

#### Estrategia de Migraciones

- **Migraciones automáticas**: Usar `makemigrations` para cambios de esquema
- **Migraciones de datos**: Separar en archivos distintos con `RunPython`
- **Nombres descriptivos**: `--name` con descripción clara del cambio
- **Reversibilidad**: Implementar `reverse_code` en migraciones de datos cuando sea posible
- **Testing**: Probar migraciones en copia de producción antes de deploy

#### Ejemplo de Migración de Datos

```python
# apps/projects/migrations/0005_populate_default_config.py

def populate_default_config(apps, schema_editor):
    Project = apps.get_model('projects', 'Project')
    for project in Project.objects.filter(config__isnull=True):
        project.config = {
            'sprint_duration': 14,
            'velocity': 0,
            'capacity_buffer': 0.15
        }
        project.save()

class Migration(migrations.Migration):
    dependencies = [
        ('projects', '0004_project_config'),
    ]

    operations = [
        migrations.RunPython(populate_default_config, reverse_code=migrations.RunPython.noop),
    ]
```

### 6.5 Indexación y Optimización

#### Índices Estratégicos

```python
class Project(models.Model):
    # ...

    class Meta:
        indexes = [
            # Queries frecuentes por status y fecha
            models.Index(fields=['status', '-created_at']),

            # Búsquedas por cliente
            models.Index(fields=['client', 'status']),

            # Filtros de equipo
            models.Index(fields=['created_by', 'status']),
        ]
```

#### Constraints de Base de Datos

```python
class ProjectMember(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    allocation_percentage = models.IntegerField()

    class Meta:
        # Evitar duplicados
        constraints = [
            models.UniqueConstraint(
                fields=['project', 'user'],
                name='unique_project_member'
            ),
            models.CheckConstraint(
                check=models.Q(allocation_percentage__gte=0) & models.Q(allocation_percentage__lte=100),
                name='valid_allocation_percentage'
            ),
        ]
```

---

## 7. Seguridad

### 7.1 Autenticación y Autorización

#### OAuth 2.0 con Google Workspace

**Flujo de autenticación:**

1. Usuario visita `/login`
2. Redirección a Google OAuth (scope: email, profile)
3. Google valida credenciales y retorna token
4. Backend verifica dominio `@10code.es`
5. Crea sesión Django y redirige a dashboard

**Implementación:**

```python
# apps/accounts/views.py
from django.contrib.auth import login
from allauth.socialaccount.models import SocialAccount

def google_callback(request):
    # django-allauth maneja el flujo OAuth
    social_account = SocialAccount.objects.get(user=request.user)

    # Validar dominio corporativo
    email = social_account.extra_data.get('email')
    if not email.endswith('@10code.es'):
        raise PermissionDenied("Solo usuarios @10code.es")

    login(request, request.user)
    return redirect('dashboard')
```

#### RBAC (Role-Based Access Control)

Sistema de permisos granular basado en roles:

```python
# apps/accounts/permissions.py

class Permission:
    # Proyectos
    VIEW_PROJECT = 'projects.view_project'
    ADD_PROJECT = 'projects.add_project'
    CHANGE_PROJECT = 'projects.change_project'
    DELETE_PROJECT = 'projects.delete_project'

    # RR.HH.
    VIEW_TIMETRACKING = 'timetracking.view_timeentry'
    APPROVE_TIMETRACKING = 'timetracking.approve_timeentry'

# Verificación en views
@login_required
def projects_create(request):
    if not request.user.has_perm('projects.add_project'):
        raise PermissionDenied()
    # ...
```

**Patrón "Props como Permisos":**

```python
# apps/projects/views.py
def projects_index(request):
    return render(request, 'Projects/Index', props={
        'projects': serialize_projects(projects),
        'permissions': {
            'can_create': request.user.has_perm('projects.add_project'),
            'can_edit': request.user.has_perm('projects.change_project'),
            'can_delete': request.user.has_perm('projects.delete_project'),
        }
    })
```

### 7.2 Protección de Datos

#### RGPD y Protección de Datos Sensibles

**Datos sensibles identificados:**

- Información de salud (bajas médicas)
- Datos salariales
- Fichajes y control horario (retención 4 años)
- Datos personales de empleados

**Medidas implementadas:**

1. **Encriptación en tránsito**: HTTPS obligatorio (TLS 1.3)
2. **Encriptación en reposo**: Campos sensibles encriptados en BD
3. **Acceso granular**: Permisos estrictos por rol
4. **Auditoría completa**: Log de accesos a datos sensibles
5. **Retención de datos**: Políticas de retención por tipo de dato
6. **Derecho al olvido**: Procedimiento de anonimización

#### Auditoría y Logging

```python
# apps/core/audit.py
import structlog

audit_logger = structlog.get_logger('audit')

def log_data_access(user, resource_type, resource_id, action):
    """Log acceso a datos sensibles."""
    audit_logger.info(
        'data_access',
        user_id=user.id,
        user_email=user.email,
        resource_type=resource_type,
        resource_id=resource_id,
        action=action,
        ip_address=get_client_ip(request),
        timestamp=timezone.now().isoformat()
    )
```

### 7.3 Seguridad de Aplicación

#### Protección contra Vulnerabilidades Comunes

**OWASP Top 10:**

1. **SQL Injection**: Django ORM con parametrización automática
2. **XSS**: React escapa HTML automáticamente; sanitización en backend para HTML permitido
3. **CSRF**: Django CSRF middleware + Inertia maneja tokens automáticamente
4. **Autenticación rota**: OAuth con Google + sesiones Django seguras
5. **Exposición de datos**: Serializers explícitos, no exponer modelos directamente
6. **Control de acceso**: RBAC granular verificado en backend
7. **Configuración incorrecta**: Secrets en variables de entorno, no en código
8. **Deserialización insegura**: Validación estricta de JSON inputs
9. **Componentes vulnerables**: Dependabot para updates automáticos
10. **Logging insuficiente**: Auditoría completa con structured logging

#### Validación de Inputs

> **Recomendación: Usar Pydantic para validaciones robustas**

Pydantic proporciona validación automática, conversión de tipos, y mejores mensajes de error. Es especialmente útil para inputs complejos y APIs.

```python
# apps/projects/services.py
from pydantic import BaseModel, Field, ValidationError as PydanticValidationError
from django.core.exceptions import ValidationError
from decimal import Decimal

class CreateProjectInput(BaseModel):
    """Modelo Pydantic para validación de entrada de proyecto."""
    name: str = Field(..., min_length=1, max_length=200, description="Nombre del proyecto")
    budget: Decimal = Field(..., ge=0, description="Presupuesto (debe ser >= 0)")
    methodology: str = Field(..., pattern=r'^(scrum|kanban|waterfall|hybrid)$', description="Metodología de desarrollo")

    class Config:
        # Configuración Pydantic v2
        str_strip_whitespace = True  # Sanitiza automáticamente strings

class ProjectService:
    @staticmethod
    def create_project(*, name: str, budget: Decimal, methodology: str, **kwargs):
        # Validación con Pydantic
        try:
            input_data = CreateProjectInput(
                name=name,
                budget=budget,
                methodology=methodology
            )
        except PydanticValidationError as e:
            # Convertir errores Pydantic a Django ValidationError
            raise ValidationError(e.errors())

        # Ahora usar input_data.name, input_data.budget, etc. (ya validados y sanitizados)

        # ...
```

### 7.4 Gestión de Secrets

#### Patrón de Gestión de Secrets (KISS)

**Filosofía**: Priorizar archivos sobre variables de entorno para Docker + VPS. Los archivos no aparecen en `docker inspect` ni en procesos del sistema.

**Implementación**: Módulo `config/secrets.py` con función `read_secret()` que busca en orden de prioridad:

```python
# config/secrets.py - Función principal
def read_secret(
    secret_name: str,
    *,
    required: bool = True,
    default: str | None = None,
) -> str:
    """
    Lee secreto desde archivos o variables de entorno.

    Prioridad:
    1. /run/secrets/{nombre} - Docker Secrets (producción)
    2. secrets/{nombre}.txt - Archivos locales (desarrollo)
    3. Variable de entorno {nombre} - Fallback
    4. Default (si se proporciona)
    """
```

**Uso en settings:**

```python
# config/settings/base.py
from config.secrets import read_secret, validate_secret_key

# SECRET_KEY con validación automática
SECRET_KEY = read_secret("django_secret_key", required=True)
if not validate_secret_key(SECRET_KEY, environment=ENVIRONMENT):
    raise ValueError("SECRET_KEY no cumple requisitos de seguridad")

# Database password con fallback
DATABASES = {
    'default': {
        'PASSWORD': read_secret("db_password", required=False, default="postgres"),
        # ... otros settings
    }
}
```

#### Estructura de Archivos de Secrets

```bash
10code-intranet/
├── config/secrets.py          # ✅ Módulo de gestión de secrets
├── secrets/                   # ✅ Carpeta para secrets (permisos 700)
│   ├── django_secret_key.txt  # ✅ SECRET_KEY (permisos 600)
│   ├── db_password.txt        # ✅ Database password (permisos 600)
│   └── README.md              # 📖 Documentación
├── .env                       # ✅ Variables NO sensibles
└── .gitignore                 # ✅ Incluye secrets/ y .env
```

#### Docker Secrets (Producción)

**Configuración real en `compose.yml`:**

```yaml
# Servicios que usan secrets
services:
  db:
    image: postgres:18-alpine
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password  # ✅ Password desde archivo
    secrets:
      - db_password

  web:
    secrets:
      - db_password
      - django_secret_key

  celery_worker:
    secrets:
      - db_password
      - django_secret_key

  celery_beat:
    secrets:
      - db_password
      - django_secret_key

# Definición de secrets
secrets:
  db_password:
    file: ./secrets/db_password.txt
  django_secret_key:
    file: ./secrets/django_secret_key.txt
```

Los secrets se montan automáticamente en `/run/secrets/` dentro del contenedor. PostgreSQL usa `POSTGRES_PASSWORD_FILE` para leer la password desde el archivo de secrets.

#### Validación de SECRET_KEY

```python
# config/secrets.py
def validate_secret_key(secret_key: str, *, environment: str = "production") -> bool:
    """Valida que SECRET_KEY cumpla requisitos de seguridad."""
    min_length = 50 if environment == "production" else 30

    if len(secret_key) < min_length:
        logger.error(f"SECRET_KEY debe tener al menos {min_length} caracteres")
        return False

    # Detectar claves inseguras
    insecure_patterns = ["django-insecure-", "change-me", "secret"]
    for pattern in insecure_patterns:
        if pattern in secret_key.lower():
            logger.error(f"SECRET_KEY contiene patrón inseguro: '{pattern}'")
            return False

    return True
```

#### Rotación de Secrets

- **SECRET_KEY**: Rotar cada 90 días mínimo, después de brechas de seguridad
- **Database passwords**: Cambiar en PostgreSQL + actualizar archivo
- **API tokens**: Con expiración automática, renovar antes de vencer
- **Backup de secrets**: Encriptados y versionados fuera del repositorio

**Comando de rotación:**

```bash
# Generar nueva SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())" > secrets/django_secret_key.txt
chmod 600 secrets/django_secret_key.txt

# Reiniciar aplicación
docker compose restart web
```

---

## 8. Performance y Escalabilidad

### 8.1 Objetivos de Performance

| Métrica | Target MVP | Target Producción |
|---------|-----------|-------------------|
| Tiempo respuesta p95 (vistas) | < 500ms | < 300ms |
| Tiempo respuesta p95 (dashboards) | < 2s | < 1s |
| Throughput | 50 req/s | 200 req/s |
| Usuarios concurrentes | 20 | 50 |
| Uptime | 99% | 99.9% |

### 8.2 Estrategias de Optimización

#### Optimización de Queries (CRÍTICO)

##### **Patrón obligatorio: select_related / prefetch_related**

```python
# ❌ MAL - N+1 queries
projects = Project.objects.all()
for p in projects:
    print(p.created_by.email)  # Query por cada proyecto!

# ✅ BIEN - 1 query
projects = Project.objects.select_related('created_by')
for p in projects:
    print(p.created_by.email)
```

**Prefetch para relaciones complejas:**

```python
from django.db.models import Prefetch

projects = Project.objects.select_related(
    'created_by',
    'client'
).prefetch_related(
    Prefetch(
        'members',
        queryset=ProjectMember.objects.select_related('user')
    ),
    'tasks__assigned_to'
)
```

#### Caché Estratégico con Redis

**Niveles de caché:**

1. **Template fragment cache**: Para componentes costosos
2. **Query cache**: Para queries frecuentes e inmutables
3. **Session cache**: Sesiones de usuario en Redis
4. **API response cache**: Para endpoints públicos o semi-públicos

**Ejemplo de caché:**

```python
from django.core.cache import cache

def get_dashboard_stats(user_id: int):
    cache_key = f'dashboard_stats_{user_id}'
    stats = cache.get(cache_key)

    if stats is None:
        # Query costoso
        stats = calculate_stats(user_id)
        cache.set(cache_key, stats, timeout=300)  # 5 minutos

    return stats
```

#### Paginación Obligatoria

```python
from django.core.paginator import Paginator

def get_projects_list(request):
    projects = Project.objects.all().order_by('-created_at')
    paginator = Paginator(projects, 25)  # 25 por página
    page = paginator.get_page(request.GET.get('page', 1))

    return render(request, 'Projects/Index', props={
        'projects': serialize_projects(page.object_list),
        'pagination': {
            'current': page.number,
            'total_pages': paginator.num_pages,
            'has_next': page.has_next(),
            'has_previous': page.has_previous(),
        }
    })
```

### 8.3 Tareas Asíncronas con Celery

#### Casos de Uso para Celery

- **Sincronizaciones externas**: ODOO, GitHub, Google Drive
- **Generación de reportes**: PDFs, Excel, análisis pesados
- **Procesamiento de datos**: Cálculos ML, agregaciones masivas
- **Envío de emails**: Notificaciones, alertas
- **Limpieza de datos**: Tareas de mantenimiento

**Ejemplo de tarea Celery:**

```python
# apps/projects/tasks.py
from celery import shared_task
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def sync_github_repository(self, project_id: int):
    """Sincronizar proyecto con repositorio GitHub."""
    try:
        project = Project.objects.get(id=project_id)
        # Lógica de sincronización...
        logger.info(f"GitHub sync completado: {project_id}")
    except Exception as exc:
        logger.error(f"Error syncing GitHub: {exc}")
        raise self.retry(exc=exc, countdown=60)
```

**Celery Beat para tareas programadas:**

```python
# config/settings/base.py
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'sync-odoo-daily': {
        'task': 'apps.integrations.odoo.tasks.sync_odoo_data',
        'schedule': crontab(hour=2, minute=0),  # 2 AM diario
    },
    'cleanup-old-sessions': {
        'task': 'apps.core.tasks.cleanup_expired_sessions',
        'schedule': crontab(hour=3, minute=0),
    },
}
```

### 8.4 Escalabilidad Futura

#### Escalado Horizontal

**Preparación para crecimiento:**

- **Stateless application**: Sesiones en Redis, no en memoria
- **Read replicas PostgreSQL**: Para queries de solo lectura
- **Load balancer (Nginx)**: Distribuir carga entre múltiples instancias Django
- **CDN para estáticos**: Servir JS/CSS/imágenes desde CDN

#### Monitoring de Performance

```python
# Middleware para medir performance
import time
from django.utils.deprecation import MiddlewareMixin

class PerformanceMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = time.time()

    def process_response(self, request, response):
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            logger.info(
                'request_duration',
                path=request.path,
                method=request.method,
                duration_ms=duration * 1000,
                status_code=response.status_code
            )
        return response
```

---

## 9. Testing Strategy

### 9.1 Pirámide de Tests

```txt
           /\
          /  \        10% - E2E Tests (Playwright)
         /____\       Critical user journeys
        /      \
       /        \     20% - Integration Tests (pytest-django)
      /__________\    View + Service + DB integration
     /            \
    /              \  70% - Unit Tests (pytest)
   /________________\ Services, Selectors, Utils
```

### 9.2 Unit Tests (70%)

**Objetivo**: Testear lógica de negocio aislada.

**Template de test de Service:**

```python
# apps/projects/tests/test_services.py
import pytest
from apps.projects.services import ProjectService
from apps.projects.tests.factories import UserFactory

@pytest.mark.django_db
class TestProjectService:

    def test_create_project_success(self):
        user = UserFactory(permissions=['projects.add_project'])

        project = ProjectService.create_project(
            name="Test Project",
            client="Test Client",
            methodology="scrum",
            created_by=user
        )

        assert project.id is not None
        assert project.name == "Test Project"
        assert project.members.filter(user=user, role='project_manager').exists()

    def test_create_project_without_permission(self):
        user = UserFactory()  # Sin permisos

        with pytest.raises(PermissionDenied):
            ProjectService.create_project(
                name="Test",
                client="Client",
                methodology="scrum",
                created_by=user
            )
```

**Template de test de Selector:**

```python
# apps/projects/tests/test_selectors.py
import pytest
from apps.projects.selectors import get_projects_list
from apps.projects.tests.factories import ProjectFactory, UserFactory

@pytest.mark.django_db
class TestProjectSelectors:

    def test_get_projects_list_optimized(self):
        user = UserFactory()
        ProjectFactory.create_batch(5, created_by=user)

        # Verificar que no hay N+1 queries
        with pytest.assertNumQueries(2):  # 1 para projects + 1 para related
            projects = list(get_projects_list(user=user))
            for p in projects:
                _ = p.created_by.email  # No debe generar query

    def test_get_projects_list_filters_by_permission(self):
        user = UserFactory()
        other_user = UserFactory()

        my_project = ProjectFactory(created_by=user)
        other_project = ProjectFactory(created_by=other_user)

        projects = get_projects_list(user=user)

        assert my_project in projects
        assert other_project not in projects
```

### 9.3 Integration Tests (20%)

**Objetivo**: Testear flujos completos view → service → database.

```python
# apps/projects/tests/test_views.py
import pytest
from django.urls import reverse

@pytest.mark.django_db
class TestProjectViews:

    def test_create_project_integration(self, client, authenticated_user):
        url = reverse('projects.store')
        data = {
            'name': 'New Project',
            'client': 'Client X',
            'methodology': 'scrum'
        }

        response = client.post(url, data)

        assert response.status_code == 302  # Redirect after create
        assert Project.objects.filter(name='New Project').exists()
```

### 9.4 E2E Tests (10%)

**Objetivo**: Testear flujos críticos de usuario end-to-end.

```javascript
// tests/e2e/projects.spec.ts
import { test, expect } from '@playwright/test'

test.describe('Project Management', () => {
  test('should create new project', async ({ page }) => {
    await page.goto('/login')
    await page.fill('input[name="email"]', 'test@10code.es')
    await page.click('button[type="submit"]')

    await page.goto('/projects/create')
    await page.fill('input[name="name"]', 'E2E Test Project')
    await page.fill('input[name="client"]', 'Test Client')
    await page.selectOption('select[name="methodology"]', 'scrum')
    await page.click('button[type="submit"]')

    await expect(page).toHaveURL(/\/projects\/\d+/)
    await expect(page.locator('h1')).toContainText('E2E Test Project')
  })
})
```

### 9.5 Test Fixtures con Factory Boy

```python
# apps/projects/tests/factories.py
import factory
from apps.projects.models import Project, ProjectMember
from apps.accounts.tests.factories import UserFactory

class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Project

    name = factory.Sequence(lambda n: f'Project {n}')
    client = factory.Faker('company')
    methodology = 'scrum'
    status = Project.Status.ACTIVE
    created_by = factory.SubFactory(UserFactory)

class ProjectMemberFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProjectMember

    project = factory.SubFactory(ProjectFactory)
    user = factory.SubFactory(UserFactory)
    role = 'developer'
    allocation_percentage = 100
```

### 9.6 Cobertura de Tests

**Objetivo mínimo**: 80% de cobertura en lógica crítica.

#### Comandos Directos

```bash
# Ejecutar tests con cobertura
pytest --cov=apps --cov-report=html --cov-report=term-missing

# Ver reporte HTML
open htmlcov/index.html
```

#### Comandos Makefile (Docker)

```bash
# Ejecutar todos los tests
make test

# Ejecutar tests con cobertura
make test-coverage

# Ejecutar tests sin migraciones (más rápido)
make test-fast
```

**Áreas críticas con 100% cobertura obligatoria:**

- Services con lógica de negocio compleja
- Cálculos financieros
- Validaciones de seguridad
- Procesamiento de datos sensibles (fichajes, nóminas)

---

## 10. Deployment e Infraestructura

### 10.1 Arquitectura de Deployment

```txt
┌─────────────────────────────────────────────┐
│               Internet                       │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│         Nginx (Reverse Proxy + SSL)         │
│  - Terminación SSL (TLS 1.3)                │
│  - Servir estáticos desde /static/          │
│  - Load balancing (futuro)                  │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│      Django + Gunicorn (4 workers)          │
│  - Aplicación principal                      │
│  - Inertia.js renderer                       │
└─────┬────────────────────────────────┬──────┘
      │                                │
      ▼                                ▼
┌─────────────────┐          ┌─────────────────┐
│  PostgreSQL 15  │          │    Redis 7      │
│  - Datos        │          │  - Cache        │
│  - Backups      │          │  - Sessions     │
│    diarios      │          │  - Celery queue │
└─────────────────┘          └─────────────────┘
                                      │
                                      ▼
                             ┌─────────────────┐
                             │  Celery Workers │
                             │  - Tasks async  │
                             │  - Beat scheduler│
                             └─────────────────┘
```

### 10.2 Docker Multi-Stage Build

**Estrategia de containers:**

Ver implementación completa en [`Dockerfile`](../Dockerfile).

**Implementación realizada:** El Dockerfile actual utiliza un enfoque multi-stage optimizado con uv para gestión de dependencias, incluyendo:

- Stage builder con uv para instalación eficiente de dependencias
- Stage runtime minimalista con usuario no-root por seguridad
- Healthchecks integrados para monitoreo de contenedores
- Variables de entorno optimizadas para producción
- Cache mounts para acelerar builds

```dockerfile
# Dockerfile (extracto simplificado - ver archivo completo)

# Stage 1: Builder - Instalar dependencias con uv
FROM python:3.14-slim-trixie AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# Stage 2: Runtime - Imagen final minimalista
FROM python:3.14-slim-trixie AS runtime
COPY --from=builder /tmp/build/.venv /app/.venv
RUN groupadd -r appuser && useradd -r -g appuser -u 1000 -m -s /sbin/nologin appuser
USER appuser
HEALTHCHECK --interval=30s --timeout=5s --start-period=40s --retries=3 \
    CMD python -c "import django; django.setup(); from django.db import connection; connection.ensure_connection()" || exit 1
EXPOSE 8000
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
```

### 10.3 Docker Compose para Desarrollo

Ver implementación completa en [`compose.yml`](../compose.yml).

**Implementación realizada:** La configuración Docker Compose incluye servicios completos para desarrollo y producción con:

- PostgreSQL 18 con healthchecks y secrets management
- Redis 8.2 con persistencia de datos
- Servicios separados para web, celery worker y celery beat
- Gestión de secrets mediante archivos Docker
- Redes y volúmenes optimizados para desarrollo
- Variables de entorno configurables

```yaml
# compose.yml (extracto - ver archivo completo)
services:
  db:
    image: postgres:18-alpine
    environment:
      POSTGRES_DB: ${DATABASE_NAME:-10code_intranet}
      POSTGRES_USER: ${DATABASE_USER:-postgres}
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - db_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DATABASE_USER:-postgres}"]
    networks:
      - backend

  redis:
    image: redis:8.2-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
    networks:
      - backend

  web:
    build:
      context: .
      dockerfile: Dockerfile
      target: runtime
    environment:
      - DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-config.settings.development}
      - DATABASE_HOST=db
      - REDIS_URL=redis://redis:6379/0
    secrets:
      - db_password
      - django_secret_key
    ports:
      - "${WEB_PORT:-8000}:8000"
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy

  celery_worker:
    build:
      context: .
      dockerfile: Dockerfile
      target: runtime
    command: celery -A config worker --loglevel=info --concurrency=2
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/1
    secrets:
      - db_password
      - django_secret_key
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy

volumes:
  postgres_data:
  redis_data:

networks:
  backend:

secrets:
  db_password:
    file: ./secrets/db_password.txt
  django_secret_key:
    file: ./secrets/django_secret_key.txt
```

### 10.4 CI/CD con GitHub Actions

```yaml
# .github/workflows/ci.yml
name: CI Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:18-alpine
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.14'

      - name: Install uv
        run: pip install uv

      - name: Install dependencies
        run: uv pip install --system -e ".[dev]"

      - name: Run linters
        run: |
          ruff check apps/
          black --check apps/

      - name: Run tests
        run: pytest --cov=apps --cov-report=xml
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost/test_db

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml

  build:
    runs-on: ubuntu-latest
    needs: test

    steps:
      - uses: actions/checkout@v3

      - name: Build Docker image
        run: docker build -t intranet:${{ github.sha }} .

      - name: Push to registry
        run: |
          echo "${{ secrets.DOCKER_PASSWORD }}" | docker login -u "${{ secrets.DOCKER_USERNAME }}" --password-stdin
          docker push intranet:${{ github.sha }}
```

### 10.5 Configuración de Entornos

#### Estructura de Settings

La configuración se organiza en módulos separados por entorno siguiendo las mejores prácticas de Django:

```python
config/settings/
├── __init__.py          # Importa configuración base
├── base.py              # Configuración común a todos los entornos
├── development.py       # Configuración para desarrollo local
└── production.py        # Configuración para producción
```

#### Configuración Base (`base.py`)

Contiene la configuración común: apps instaladas, base de datos, middleware, validadores de password, internacionalización, archivos estáticos, y configuración de secrets mediante el módulo `config.secrets`.

#### Configuración de Producción (`production.py`)

**Extracto clave:**

```python
# Seguridad reforzada
SECURE_SSL_REDIRECT = env("SECURE_SSL_REDIRECT", default="True") == "True"
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

# Logging estructurado a stdout (Docker-friendly)
LOGGING = {
    "version": 1,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": env("LOG_LEVEL", default="INFO"),
    },
}

# Caché Redis y Celery para tareas asíncronas
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env("REDIS_URL", default="redis://localhost:6379/0"),
    }
}
CELERY_BROKER_URL = env("CELERY_BROKER_URL", default="redis://localhost:6379/1")
```

**Características principales:**

- **Seguridad por defecto**: SSL obligatorio, cookies seguras, protección XSS/CSRF
- **Logging estructurado**: Salida a stdout para contenedores Docker
- **Caché distribuido**: Redis para sesiones, queries y datos temporales
- **Tareas asíncronas**: Celery con Redis como broker para ETL y notificaciones
- **Variables de entorno**: Configuración flexible vía `environ.Env`

#### Configuración de Desarrollo (`development.py`)

Incluye herramientas de desarrollo: Django Debug Toolbar, django-extensions, CORS permisivo, y hosts abiertos para facilitar el desarrollo local.

**Por qué esta estructura:**

- **Separación clara**: Configuración específica por entorno sin duplicación
- **Seguridad**: Producción con configuraciones reforzadas, desarrollo con herramientas útiles
- **Flexibilidad**: Variables de entorno permiten configuración sin cambios de código
- **Mantenibilidad**: Configuración modular y bien documentada

### 10.6 Backups y Disaster Recovery

#### Estrategia de Backups

- **Base de datos**: Backups diarios automáticos, retención 30 días
- **Archivos estáticos**: Sincronizados a bucket S3/similar
- **Configuración**: Versionada en Git
- **Secrets**: Almacenados en gestor de secrets (AWS Secrets Manager, Vault)

**Script de backup:**

```bash
#!/bin/bash
# scripts/backup_db.sh

BACKUP_DIR="/backups/postgresql"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DB_NAME="intranet_db"

pg_dump -Fc $DB_NAME > "$BACKUP_DIR/backup_${TIMESTAMP}.dump"

# Mantener solo últimos 30 días
find $BACKUP_DIR -name "backup_*.dump" -mtime +30 -delete
```

---

## 11. Monitoreo y Observabilidad

### 11.1 Logging Básico (MVP)

#### Configuración de Logging

**En producción** (Docker-friendly):

```python
# config/settings/production.py

# Logging a stdout (Docker-friendly)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": env("LOG_LEVEL", default="INFO"),
    },
}
```

**En desarrollo** (hereda configuración base):

```python
# config/settings/development.py
# Sin configuración específica de logging - usa configuración por defecto
```

#### Uso de Logging Básico

```python
import logging

logger = logging.getLogger(__name__)

class ProjectService:
    @staticmethod
    def create_project(name: str, client: str, created_by, **kwargs):
        logger.info(
            f"Creating project '{name}' for client '{client}' by user {created_by.id}"
        )

        # ... lógica de negocio ...

        logger.info(
            f"Project created successfully with ID {project.id}"
        )

        return project
```

#### Estrategia de Logging para MVP

**¿Por qué logging básico en MVP?**

- **Simplicidad**: Enfocarnos en funcionalidad core antes que en observabilidad avanzada
- **Suficiente para debugging**: Logging estándar cubre necesidades de desarrollo y producción básica
- **Docker-friendly**: Salida a stdout/stderr funciona perfectamente en contenedores
- **Evolución futura**: Preparado para migrar a structured logging cuando sea necesario

**Plan para fases futuras:**

- **Fase 2**: Implementar structured logging con `structlog` para mejor parseabilidad
- **Fase 3**: Centralización de logs con ELK stack o Loki
- **Fase 4**: Métricas y monitoring avanzado con Prometheus/Grafana

### 11.2 Métricas y Monitoring

#### Métricas Clave a Monitorear

##### **Enfoque MVP: Métricas de Negocio Exclusivamente**

En la fase MVP, las métricas que se van a medir y monitorear serán exclusivamente las de negocio, ya que estas son las que aportan valor directo al negocio y permiten validar el éxito del producto.

Las métricas de aplicación (performance, errores) e infraestructura (CPU, memoria) se implementarán en fases posteriores cuando sea necesario para optimización y escalabilidad.

**Business metrics (MVP):**

Las métricas de negocio específicas dependerán de cada módulo y serán definidas en el FSD correspondiente:

- **Módulo RR.HH.**: Horas registradas diarias, usuarios activos diarios/semanales
- **Módulo Gestión de Proyectos**: Proyectos activos, progreso de proyectos
- **Módulo Comercial**: Oportunidades comerciales por estado, conversiones
- **Módulo Dashboards**: KPIs consolidados de todos los módulos

Cada FSD detallará las métricas específicas de negocio que se van a monitorear para ese módulo.

### 11.3 Alertas

#### Configuración de Alertas Críticas

```yaml
# alerts.yml (ejemplo conceptual)
alerts:
  - name: high_error_rate
    condition: error_rate > 5%
    duration: 5m
    severity: critical
    notify: ['email', 'discord']

  - name: slow_response_time
    condition: p95_latency > 2s
    duration: 10m
    severity: warning
    notify: ['discord']

  - name: database_connections_high
    condition: db_connections > 80%
    duration: 5m
    severity: warning
    notify: ['email']

  - name: celery_queue_backed_up
    condition: celery_queue_size > 1000
    duration: 15m
    severity: warning
    notify: ['discord']
```

### 11.4 Herramientas de Observabilidad

**Para consideración futura:**

- **Sentry**: Error tracking y performance monitoring
- **Prometheus + Grafana**: Métricas y dashboards
- **ELK Stack** o **Loki**: Centralización de logs
- **Django Debug Toolbar**: Debugging en desarrollo
- **django-silk**: Profiling de requests en staging

---

## 12. Referencias y Recursos

### 12.1 Documentación del Proyecto

**Documentos maestros:**

- **PRD**: `docs/product_docs/PRD_Intranet_10Code.md` - Requisitos de producto
- **SAD**: Este documento - Arquitectura de software
- **Marco de documentación**: `docs/product_docs/.framework/marco-documentacion-tecnica-10code.md`
- **Reglas de desarrollo**: `CLAUDE.md` - Reglas para agentes IA

**Reglas arquitectónicas:**

- `.rules/ARCHITECTURE_RULES.md` - Comunicación entre módulos
- `.rules/DJANGO_PATTERNS.md` - Patrones Django obligatorios
- `.rules/INERTIA_FRONTEND.md` - Patrones frontend React + Inertia

**FSDs por módulo** (a crear):

- `docs/product_docs/modules/authentication/FSD-Authentication.md`
- `docs/product_docs/modules/hr/FSD-TimeTracking.md`
- `docs/product_docs/modules/commercial/FSD-Commercial.md`
- `docs/product_docs/modules/projects/FSD-Projects.md`
- *(otros módulos según priorización)*

### 12.2 Documentación Técnica Externa

**Django:**

- Django 5 Documentation: <https://docs.djangoproject.com/en/5.0/>
- Django ORM Performance: <https://docs.djangoproject.com/en/5.0/topics/db/optimization/>
- Django Security: <https://docs.djangoproject.com/en/5.0/topics/security/>

**Inertia.js:**

- Inertia.js Documentation: <https://inertiajs.com/>
- React Adapter: <https://inertiajs.com/client-side-setup#react>

**React y Frontend:**

- React 18 Documentation: <https://react.dev/>
- TypeScript Handbook: <https://www.typescriptlang.org/docs/>
- shadcn/ui Components: <https://ui.shadcn.com/>
- Tailwind CSS: <https://tailwindcss.com/docs>

**Base de Datos:**

- PostgreSQL 15 Documentation: <https://www.postgresql.org/docs/15/>
- Django + PostgreSQL Best Practices: <https://www.postgresql.org/docs/15/django.html>

**Testing:**

- pytest Documentation: <https://docs.pytest.org/>
- pytest-django: <https://pytest-django.readthedocs.io/>
- Playwright: <https://playwright.dev/>

**Deployment:**

- Docker Documentation: <https://docs.docker.com/>
- Gunicorn: <https://docs.gunicorn.org/>
- Nginx: <https://nginx.org/en/docs/>

### 12.3 Libros y Recursos de Referencia

- **Two Scoops of Django**: Best practices de Django
- **Domain-Driven Design (Eric Evans)**: Fundamentos de DDD
- **Clean Architecture (Robert C. Martin)**: Principios arquitectónicos
- **The Pragmatic Programmer**: Best practices generales

### 12.4 Herramientas de Desarrollo

**Backend:**

- Python 3.14+
- Django 5.2.8+
- inertia-django
- Celery 5.5.3+
- pytest

**Frontend:**

- Node.js 20+
- React 19+
- TypeScript 5+
- Vite 6+
- Playwright

**Infraestructura:**

- Docker & Docker Compose
- PostgreSQL 18
- Redis 7
- Nginx

---

## 13. Historial de Cambios

| Versión | Fecha | Autor | Cambios |
|---------|-------|-------|---------|
| **1.0** | 2024-11-14 | Juanje Márquez | Creación inicial del SAD (secciones 1-5) |
| **1.1** | 2024-11-17 | Juanje Márquez | Completado secciones 6-15: Base de Datos, Seguridad, Performance, Testing, Deployment, Monitoreo, ADRs, Referencias |
| **1.2** | 2024-11-17 | Juanje Márquez | Actualización estructura integraciones: apps separadas en lugar de subcarpetas |
| **1.3** | 2025-11-17 | Juanje Márquez | Incorporación de Pydantic para validaciones de input en backend |
| **1.4** | 2025-11-17 | Juanje Márquez | Referencias a archivos Docker implementados y explicación básica de la implementación |
| **1.5** | 2025-11-17 | Juanje Márquez | Actualización sección de logging para coherencia con implementación MVP (logging básico vs structlog) |

### Próximas Actualizaciones Previstas

- **v2.0**: Revisión completa tras finalización del MVP

---

## 14. Aprobaciones

### Estado de Aprobación

- ✅ **Arquitecto Principal** (Juanje - 10Code): Aprobado para implementación
- 🔲 **Tech Lead**: Pendiente de revisión (mismo rol que arquitecto en MVP)
- 🔲 **Product Owner**: Pendiente de validación de alineación con PRD

### Criterios de Aprobación

Este documento se considera aprobado cuando:

1. ✅ Coherencia verificada con PRD
2. ✅ Alineación con reglas arquitectónicas (`.rules/`)
3. ✅ Patrones definidos claramente para desarrollo
4. ⏳ ADRs críticos creados (ADR-001, ADR-002, ADR-008)
5. ⏳ Primer FSD creado usando este SAD como referencia

### Vigencia

Este SAD es un **living document** que evolucionará con el proyecto. Se revisará:

- Tras completar cada fase del MVP
- Cuando se tomen decisiones arquitectónicas significativas
- Semestralmente para asegurar relevancia

---

## 16. Conclusión

Este Software Architecture Document define la arquitectura técnica completa de la Intranet 10Code. Los principios y patrones aquí establecidos son **obligatorios** para mantener la coherencia, calidad y mantenibilidad del sistema.

### Principios Clave a Recordar

1. **Monolito Modular Majestuoso**: Simplicidad operativa con disciplina modular
2. **Service Layer Pattern**: Obligatorio para toda lógica de negocio (80% de comunicación)
3. **Inertia.js como puente**: SPA moderna sin complejidad de API REST separada
4. **DDD y Bounded Contexts**: Cada app Django es un dominio autocontenido
5. **Optimización de queries**: select_related/prefetch_related siempre
6. **Testing obligatorio**: 80% cobertura mínima en lógica crítica
7. **Seguridad by design**: RBAC, RGPD, auditoría completa

### Documentos Complementarios

- **Para requisitos funcionales**: Ver PRD
- **Para implementación de módulos**: Ver FSDs específicos
- **Para decisiones arquitectónicas**: Ver ADRs individuales
- **Para desarrollo con IA**: Ver CLAUDE.md y `.rules/`

### Contacto

**Arquitecto Principal**: Juanje Márquez (10Code)
**Última actualización**: 2025-11-17
**Versión del documento**: 1.5

---

> **Fin del Software Architecture Document - Intranet 10Code v1.5**
>
> *Este SAD define el CÓMO técnico del sistema. Junto con el PRD (QUÉ y POR QUÉ), forma la base de documentación del proyecto.*
