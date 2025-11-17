# SAD: Software Architecture Document

## [Nombre del Proyecto]

## Metadata

- **Versión del documento**: 1.0
- **Fecha de creación**: [fecha]
- **Última actualización**: [fecha]
- **Arquitecto principal**: [nombre]
- **Revisores técnicos**: [lista]
- **Estado**: [Draft / In Review / Approved / Living Document]

---

## 1. Introducción

### 1.1 Propósito del Documento

Este documento describe la arquitectura de software del **Sistema de Gestión de Proyectos Integral de 10Code**. Define las decisiones arquitectónicas clave, el stack tecnológico, patrones de diseño, y lineamientos para el desarrollo.

**Audiencia:** Equipo de desarrollo, tech leads, futuros mantenedores del sistema.

### 1.2 Alcance

Este SAD cubre:

- ✅ Arquitectura de alto nivel (sistema completo)
- ✅ Stack tecnológico y justificaciones
- ✅ Patrones de diseño aplicados
- ✅ Estructura de código y organización
- ✅ Estrategias de datos, seguridad, performance
- ✅ Infraestructura y deployment

Este SAD **NO** cubre:

- ❌ Detalles de implementación por módulo (ver FSDs)
- ❌ Requisitos funcionales (ver PRD)
- ❌ Manuales de usuario o runbooks operativos

### 1.3 Referencias

- **PRD**: [00-PRD-Intranet-10Code.md](./00-PRD-Intranet-10Code.md)
- **ADRs relacionados**: Ver carpeta `/docs/adr/`
- **Guía de desarrollo**: [intranet_dev_guide.md](./intranet_dev_guide.md)

---

## 2. Visión Arquitectónica

### 2.1 Filosofía Arquitectónica

El sistema sigue el patrón **"Majestic Modular Monolith"**:

- **Monolito físico**: Single deployment unit, infraestructura simplificada
- **Modularidad lógica**: Apps Django autocontenidas, separación de responsabilidades
- **Frontend integrado**: Inertia.js elimina complejidad de APIs REST separadas
- **Preparado para evolución**: Arquitectura permite extracción futura a microservicios si es necesario

**Principios guía:**

1. **KISS (Keep It Simple, Stupid)**: Priorizar simplicidad sobre sofisticación prematura
2. **DRY (Don't Repeat Yourself)**: Código reutilizable, evitar duplicación
3. **Separation of Concerns**: Capa de servicio, boundaries claros entre apps
4. **Convention over Configuration**: Seguir estándares Django/React
5. **Fail Fast**: Validaciones tempranas, errores explícitos

### 2.2 Arquitectura de Alto Nivel (C4 Model - Context)

```mermaid
C4Context
    title Diagrama de Contexto - Sistema Gestión Proyectos 10Code

    Person(users, "Empleados 10Code", "Usuarios del sistema: PMs, Developers, Comerciales, RRHH, Dirección")
    
    System(intranet, "Intranet 10Code", "Sistema monolítico Django + Inertia.js")
    
    System_Ext(google, "Google Workspace", "OAuth 2.0, Email")
    System_Ext(odoo, "ODOO ERP", "Nóminas, Facturas")
    System_Ext(discord, "Discord", "Notificaciones")
    System_Ext(n8n, "N8N", "Webhooks, Automatizaciones")
    
    Rel(users, intranet, "Usa", "HTTPS")
    Rel(intranet, google, "Autenticación OAuth", "HTTPS/REST")
    Rel(intranet, odoo, "Sincroniza datos financieros", "XML-RPC")
    Rel(intranet, discord, "Envía notificaciones", "Webhooks")
    Rel(n8n, intranet, "Envía leads", "Webhooks")
```

### 2.3 Decisiones Arquitectónicas Críticas

Las siguientes decisiones tienen **ADRs detallados** en `/docs/adr/`:

| Decisión | Justificación Breve | ADR |
|----------|---------------------|-----|
| **Monolito vs Microservicios** | Equipo pequeño, complejidad innecesaria, deployment simple | [001-monolith-choice.md](../adr/001-monolith-choice.md) |
| **Django + Inertia.js** | Elimina API REST duplicada, desarrollo más rápido, DX superior | [002-django-inertia.md](../adr/002-django-inertia.md) |
| **PostgreSQL** | JSONB para flexibilidad, robustez, excelente soporte Django | [003-postgresql.md](../adr/003-postgresql.md) |
| **Tiptap + WeasyPrint** | Editor moderno, generación PDF server-side, customizable | [004-docs-pdf-stack.md](../adr/004-docs-pdf-stack.md) |
| **Celery + Redis** | Tareas asíncronas, ETL, integrations, cache distribuido | [005-async-tasks.md](../adr/005-async-tasks.md) |

---

## 3. Stack Tecnológico

### 3.1 Resumen del Stack

```bash
┌─────────────────────────────────────────────────────┐
│                     Frontend                        │
│  React 18 + TypeScript + Inertia.js + Tailwind     │
│  Bundler: Vite 6                                    │
└─────────────────────────────────────────────────────┘
                        ↕ (Props JSON)
┌─────────────────────────────────────────────────────┐
│                     Backend                         │
│  Django 5 + Python 3.11+ + PostgreSQL 15           │
│  Inertia Django Adapter + Django ORM                │
└─────────────────────────────────────────────────────┘
                        ↕
┌─────────────────────────────────────────────────────┐
│              Infraestructura & Servicios            │
│  Docker + Redis + Celery + Nginx + Gunicorn        │
└─────────────────────────────────────────────────────┘
                        ↕
┌─────────────────────────────────────────────────────┐
│              Integraciones Externas                 │
│  Google OAuth + ODOO + Discord + N8N                │
└─────────────────────────────────────────────────────┘
```

### 3.2 Detalle de Tecnologías

#### **Backend**

| Componente | Versión | Propósito | Justificación |
|------------|---------|-----------|---------------|
| **Python** | 3.11+ | Lenguaje base | Type hints modernos, performance mejorado |
| **Django** | 5.0+ | Framework web | ORM maduro, admin, ecosistema rico |
| **PostgreSQL** | 15+ | Base de datos | JSONB, robustez, escalabilidad |
| **Django Inertia** | 0.6+ | Adaptador Inertia | Bridge Django ↔ React sin API REST |
| **django-allauth** | 0.57+ | Autenticación OAuth | Google OAuth integrado, probado |
| **Celery** | 5.3+ | Tareas asíncronas | ETL, integraciones, emails |
| **Redis** | 7.2+ | Cache + Broker Celery | Performance, sesiones distribuidas |
| **Gunicorn** | 21+ | WSGI server | Producción, workers múltiples |

#### **Frontend**

| Componente | Versión | Propósito | Justificación |
|------------|---------|-----------|---------------|
| **React** | 18+ | UI framework | Componentes, hooks, ecosistema |
| **TypeScript** | 5+ | Tipado estático | Menos bugs, mejor DX, refactoring seguro |
| **Inertia.js** | 2.0+ | SPA sin API | Simplifica stack, no duplicación |
| **Vite** | 6+ | Build tool | HMR rápido, dev experience superior |
| **Tailwind CSS** | 3.4+ | Styling | Utility-first, responsive, customizable |
| **shadcn/ui** | - | UI components | Accesibles, customizables, copiar-pegar |
| **Tiptap** | 2+ | Editor WYSIWYG | Moderno, extensible, markdown-friendly |

#### **Machine Learning**

| Componente | Versión | Propósito |
|------------|---------|-----------|
| **scikit-learn** | 1.4+ | Modelos ML clásicos (regresión, clustering) |
| **pandas** | 2.1+ | Manipulación datos, análisis |
| **numpy** | 1.26+ | Operaciones numéricas |

#### **Infraestructura**

| Componente | Versión | Propósito |
|------------|---------|-----------|
| **Docker** | 24+ | Containerización |
| **Docker Compose** | 2.23+ | Orquestación local |
| **Nginx** | 1.25+ | Reverse proxy, static files |
| **GitHub Actions** | - | CI/CD |

---

## 4. Arquitectura Detallada (C4 Model - Container)

### 4.1 Diagrama de Contenedores

```mermaid
C4Container
    title Diagrama de Contenedores - Sistema Intranet 10Code

    Person(user, "Usuario", "Empleado 10Code")

    Container_Boundary(c1, "Intranet 10Code - Monolito") {
        Container(web, "Web Application", "Django 5 + Inertia", "Sirve HTML + JSON props")
        Container(frontend, "Frontend SPA", "React + TypeScript", "UI/UX, formularios, dashboards")
        ContainerDb(db, "Base de Datos", "PostgreSQL 15", "Almacena usuarios, proyectos, horarios, etc.")
        Container(cache, "Cache", "Redis", "Cache de sesiones, datos frecuentes")
        Container(worker, "Async Workers", "Celery", "Tareas asíncronas, ETL, integraciones")
        Container(ml, "ML Service", "Python scripts", "Entrenamiento y predicción modelos")
    }

    System_Ext(google, "Google OAuth")
    System_Ext(odoo, "ODOO ERP")
    System_Ext(discord, "Discord")

    Rel(user, web, "Visita", "HTTPS")
    Rel(web, frontend, "Sirve props JSON")
    Rel(frontend, web, "Llamadas Inertia")
    Rel(web, db, "Lee/Escribe", "ORM Django")
    Rel(web, cache, "Lee/Escribe", "Redis protocol")
    Rel(web, worker, "Encola tareas", "Redis broker")
    Rel(worker, db, "Lee/Escribe")
    Rel(worker, ml, "Invoca entrenamientos")
    Rel(ml, db, "Lee datos históricos")
    
    Rel(web, google, "OAuth flow", "HTTPS")
    Rel(worker, odoo, "Sincroniza", "XML-RPC")
    Rel(worker, discord, "Notificaciones", "Webhooks")
```

### 4.2 Flujo de Datos Típico

#### Caso 1: Usuario carga dashboard de proyectos

```mermaid
sequenceDiagram
    actor User
    participant Browser
    participant Django
    participant Cache
    participant DB
    participant React

    User->>Browser: GET /projects/dashboard
    Browser->>Django: HTTP Request
    Django->>Cache: Check cached data
    alt Cache hit
        Cache-->>Django: Return cached dashboard
    else Cache miss
        Django->>DB: Query projects, resources, KPIs
        DB-->>Django: Return data
        Django->>Cache: Store in cache (5 min TTL)
    end
    Django->>Django: Serialize data to props
    Django->>Browser: HTML + Inertia props (JSON)
    Browser->>React: Hydrate React component
    React-->>User: Render dashboard
```

#### Caso 2: Tarea asíncrona (sincronización ODOO)

```mermaid
sequenceDiagram
    participant Celery Beat
    participant Redis
    participant Worker
    participant ODOO
    participant DB
    participant Discord

    Celery Beat->>Redis: Encolar tarea "sync_odoo_payroll"
    Redis-->>Worker: Dequeue tarea
    Worker->>ODOO: API call: Get payroll data
    ODOO-->>Worker: Return payroll JSON
    Worker->>Worker: Transform and validate
    Worker->>DB: Bulk update PayrollData
    alt Success
        Worker->>Discord: Webhook: "Sync OK - 45 registros"
    else Error
        Worker->>Discord: Webhook: "Sync FAILED - [error]"
        Worker->>DB: Log error en SyncLog
    end
```

---

## 5. Estructura de Código y Organización

### 5.1 Árbol de Directorios

```bash
10code-intranet/
├── .github/
│   └── workflows/              # CI/CD con GitHub Actions
│       ├── ci.yml
│       └── deploy.yml
│
├── apps/                       # Aplicaciones Django (Domain Layer)
│   ├── __init__.py
│   ├── core/                   # App base transversal
│   │   ├── models.py           # Abstract models (TimestampedModel, SoftDeleteModel)
│   │   ├── managers.py         # Custom QuerySet managers
│   │   ├── services.py         # Servicios core compartidos
│   │   ├── permissions.py      # Base permission classes
│   │   ├── middleware.py       # Custom middleware
│   │   └── utils.py            # Utilidades compartidas
│   │
│   ├── accounts/               # Autenticación y usuarios
│   │   ├── models.py           # User (custom), Team, Role
│   │   ├── services.py         # user_create, user_update, team_assign
│   │   ├── selectors.py        # user_list, user_get_permissions
│   │   ├── views.py            # Inertia views (login, profile, etc.)
│   │   ├── forms.py            # Django forms para validación
│   │   ├── adapters.py         # OAuth adapters (Google)
│   │   └── tests/
│   │
│   ├── projects/               # Gestión de proyectos
│   │   ├── models.py           # Project, Sprint, Milestone
│   │   ├── services.py         # project_create, sprint_start, etc.
│   │   ├── selectors.py        # project_list, project_dashboard_data
│   │   ├── views.py            # Inertia views
│   │   ├── enums.py            # ProjectStatus, SprintStatus
│   │   ├── validators.py       # Custom validators
│   │   └── tests/
│   │
│   ├── backlog/                # Épicas, historias, tareas
│   ├── resources/              # Gestión de recursos
│   ├── timetracking/           # Control horario
│   ├── estimation/             # Sistema CEPF + ML
│   ├── financial/              # Seguimiento financiero
│   ├── commercial/             # CRM y pipeline
│   ├── reporting/              # Dashboards y BI
│   └── integrations/           # Integraciones externas (ODOO, Discord)
│
├── config/                     # Configuración del proyecto
│   ├── __init__.py
│   ├── asgi.py
│   ├── wsgi.py
│   ├── celery.py               # Configuración Celery
│   ├── urls.py                 # URL routing raíz
│   └── settings/
│       ├── __init__.py
│       ├── base.py             # Settings comunes
│       ├── development.py      # Settings dev
│       ├── production.py       # Settings prod
│       └── testing.py          # Settings para tests
│
├── frontend/                   # Frontend React + Inertia
│   ├── src/
│   │   ├── main.tsx            # Entry point
│   │   ├── components/         # Componentes reutilizables
│   │   │   ├── common/         # Buttons, Inputs, Cards
│   │   │   ├── forms/          # Form components
│   │   │   ├── layouts/        # Layouts (Dashboard, Auth)
│   │   │   └── ui/             # shadcn/ui components
│   │   ├── pages/              # Inertia page components
│   │   │   ├── Auth/           # Login, Register
│   │   │   ├── Projects/       # ProjectList, ProjectDetail
│   │   │   ├── Dashboard/
│   │   │   └── ...
│   │   ├── lib/                # Utilidades, helpers
│   │   ├── hooks/              # Custom React hooks
│   │   ├── types/              # TypeScript types
│   │   └── styles/             # Global CSS, Tailwind
│   ├── public/                 # Assets estáticos
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
│
├── ml/                         # Código de Machine Learning
│   ├── models/                 # Modelos entrenados (.pkl)
│   ├── scripts/                # Scripts entrenamiento
│   │   ├── train_estimation.py
│   │   └── predict.py
│   ├── notebooks/              # Jupyter notebooks exploración
│   └── data/                   # Datos de entrenamiento
│
├── static/                     # Static files (collectstatic)
├── media/                      # User uploads
├── templates/                  # Templates Django
│   └── base.html               # Template base Inertia
│
├── docs/                       # Documentación (PRD, SAD, FSDs, ADRs)
├── docker/                     # Dockerfiles
├── scripts/                    # Scripts de utilidad
│
├── .env.example
├── .gitignore
├── docker-compose.yml
├── manage.py
├── pyproject.toml              # Poetry o uv dependencies
└── README.md
```

### 5.2 Convenciones de Código

#### Nomenclatura Python/Django

```python
# ✅ BIEN
class ProjectStatusEnum(models.TextChoices):
    PLANNING = "planning", "En Planificación"
    ACTIVE = "active", "Activo"
    ON_HOLD = "on_hold", "En Espera"

def project_create(*, title: str, owner: User, **kwargs) -> Project:
    """Service function: siempre keyword-only args después de *"""
    pass

def project_list(*, filters: dict) -> QuerySet[Project]:
    """Selector function: solo lectura, retorna QuerySet"""
    pass

# ❌ MAL
def createProject(title, owner):  # CamelCase en función
    Project.objects.create(...)   # Lógica en view, no en service
```

#### Nomenclatura React/TypeScript

```typescript
// ✅ BIEN
interface ProjectListProps {
  projects: Project[];
  filters: ProjectFilters;
}

const ProjectList: React.FC<ProjectListProps> = ({ projects, filters }) => {
  // Component logic
};

// Custom hook
const useProjectFilters = () => {
  // Hook logic
};

// ❌ MAL
const projectlist = (props) => { ... };  // lowercase component
function ProjectList(props: any) { ... }; // any type
```

---

## 6. Patrones de Diseño y Arquitectura

### 6.1 Service Layer Pattern

**Problema**: Evitar Fat Views con lógica de negocio mezclada con presentación

**Solución**: Capa de servicios dedicada

```python
# apps/projects/services.py
from typing import Optional
from django.db import transaction
from .models import Project, Sprint
from apps.accounts.models import User

@transaction.atomic
def project_create(
    *,
    title: str,
    owner: User,
    team_members: list[User],
    budget: Optional[Decimal] = None,
) -> Project:
    """
    Crea un proyecto nuevo con validaciones y lógica de negocio.
    
    Business rules:
    - Owner debe tener permiso 'can_create_project'
    - Budget no puede ser negativo
    - Team members deben ser activos
    """
    # Validaciones
    if not owner.has_perm('projects.can_create_project'):
        raise PermissionDenied("User cannot create projects")
    
    if budget and budget < 0:
        raise ValueError("Budget cannot be negative")
    
    # Crear proyecto
    project = Project.objects.create(
        title=title,
        owner=owner,
        budget=budget,
        status=ProjectStatusEnum.PLANNING
    )
    
    # Asignar equipo
    project.team_members.add(*team_members)
    
    # Lógica adicional (ej: notificaciones, logs)
    # ...
    
    return project
```

```python
# apps/projects/views.py (Inertia view)
from inertia import render
from .services import project_create
from .forms import ProjectCreateForm

def project_create_view(request):
    if request.method == 'POST':
        form = ProjectCreateForm(request.POST)
        if form.is_valid():
            # La vista NO tiene lógica de negocio, delega al service
            project = project_create(
                title=form.cleaned_data['title'],
                owner=request.user,
                team_members=form.cleaned_data['team_members'],
                budget=form.cleaned_data.get('budget')
            )
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectCreateForm()
    
    return render(request, 'Projects/Create', {
        'form': form,
    })
```

**Beneficios:**

- ✅ Lógica de negocio testeable independientemente de views
- ✅ Reutilizable desde APIs, CLI, Celery tasks
- ✅ Transaccionalidad clara con `@transaction.atomic`

### 6.2 Selector Pattern (Read Operations)

**Problema**: Queries complejas duplicadas, N+1 queries

**Solución**: Funciones selector dedicadas con optimizaciones

```python
# apps/projects/selectors.py
from django.db.models import QuerySet, Prefetch, Count, Sum
from .models import Project

def project_list(
    *,
    user: User,
    filters: Optional[dict] = None
) -> QuerySet[Project]:
    """
    Retorna queryset optimizado de proyectos según permisos del usuario.
    """
    qs = Project.objects.select_related(
        'owner',
        'client'
    ).prefetch_related(
        'team_members',
        Prefetch('sprints', queryset=Sprint.objects.filter(status='active'))
    ).annotate(
        total_hours=Sum('tasks__estimated_hours'),
        task_count=Count('tasks')
    )
    
    # Filtrar según permisos
    if not user.is_superuser:
        qs = qs.filter(
            Q(owner=user) | Q(team_members=user)
        ).distinct()
    
    # Aplicar filtros adicionales
    if filters:
        if 'status' in filters:
            qs = qs.filter(status=filters['status'])
        if 'search' in filters:
            qs = qs.filter(
                Q(title__icontains=filters['search']) |
                Q(description__icontains=filters['search'])
            )
    
    return qs.order_by('-created_at')
```

### 6.3 Repository Pattern (Opcional, para lógica DB compleja)

Solo cuando queries muy complejas o necesitas abstraer DB:

```python
# apps/projects/repositories.py
class ProjectRepository:
    @staticmethod
    def get_overbudget_projects() -> QuerySet[Project]:
        """Proyectos que exceden 80% del budget"""
        return Project.objects.annotate(
            spent_hours=Sum('tasks__actual_hours'),
            budget_percentage=F('spent_hours') / F('budget_hours') * 100
        ).filter(budget_percentage__gte=80)
```

### 6.4 Factory Pattern (para Testing)

```python
# apps/projects/tests/factories.py
import factory
from apps.accounts.tests.factories import UserFactory
from apps.projects.models import Project

class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Project
    
    title = factory.Faker('company')
    owner = factory.SubFactory(UserFactory)
    budget = factory.Faker('pydecimal', left_digits=5, right_digits=2, positive=True)
    status = ProjectStatusEnum.ACTIVE
```

---

## 7. Gestión de Datos

### 7.1 Modelo de Datos de Alto Nivel

```mermaid
erDiagram
    User ||--o{ Project : owns
    User ||--o{ Task : assigned_to
    User }o--o{ Team : belongs_to
    Project ||--|{ Sprint : has
    Project ||--|{ Epic : has
    Epic ||--|{ UserStory : contains
    UserStory ||--|{ Task : breaks_down_to
    Project }o--|| Client : for
    Task ||--o{ TimeEntry : tracks
    
    User {
        uuid id PK
        string email UK
        string first_name
        string last_name
        string employee_id UK
        decimal weekly_capacity
    }
    
    Project {
        uuid id PK
        string title
        text description
        uuid owner_id FK
        uuid client_id FK
        enum status
        decimal budget_hours
        date start_date
        date end_date
    }
    
    Task {
        uuid id PK
        string title
        uuid user_story_id FK
        uuid assigned_to_id FK
        decimal estimated_hours
        decimal actual_hours
        enum status
        int priority
    }
    
    TimeEntry {
        uuid id PK
        uuid task_id FK
        uuid user_id FK
        decimal hours
        date date
        time check_in
        time check_out
        text notes
    }
```

### 7.2 Estrategia de Migraciones

**Reglas:**

1. **Nunca editar migración ya aplicada en producción**
2. **Migraciones pequeñas y atómicas** (1 cambio conceptual = 1 migración)
3. **Datos sensibles**: Usar `migrations.RunPython` con funciones reversibles
4. **Índices grandes**: Usar `CREATE INDEX CONCURRENTLY` (PostgreSQL)

```python
# Ejemplo: migración con transformación de datos
from django.db import migrations

def migrate_old_status_to_new(apps, schema_editor):
    Project = apps.get_model('projects', 'Project')
    for project in Project.objects.filter(old_status='in_progress'):
        project.status = 'active'
        project.save(update_fields=['status'])

def reverse_migration(apps, schema_editor):
    Project = apps.get_model('projects', 'Project')
    for project in Project.objects.filter(status='active'):
        project.old_status = 'in_progress'
        project.save(update_fields=['old_status'])

class Migration(migrations.Migration):
    dependencies = [
        ('projects', '0005_add_new_status_field'),
    ]
    
    operations = [
        migrations.RunPython(
            migrate_old_status_to_new,
            reverse_migration
        ),
    ]
```

### 7.3 Estrategia de Backup

| Tipo | Frecuencia | Retención | Método |
|------|------------|-----------|--------|
| **Full backup** | Diario (03:00 AM) | 30 días | `pg_dump` completo |
| **Incremental** | Cada 6h | 7 días | WAL archiving PostgreSQL |
| **Snapshots** | Pre-deployment | Hasta siguiente deploy exitoso | DB snapshot |

---

## 8. Seguridad

### 8.1 Autenticación y Autorización

#### Autenticación (django-allauth + Google OAuth)

```python
# config/settings/base.py
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
        'APP': {
            'client_id': env('GOOGLE_OAUTH_CLIENT_ID'),
            'secret': env('GOOGLE_OAUTH_SECRET'),
        },
        # Solo emails @10code.es
        'ADAPTER': 'apps.accounts.adapters.CustomGoogleAdapter',
    }
}
```

```python
# apps/accounts/adapters.py
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class CustomGoogleAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        email = sociallogin.account.extra_data.get('email', '')
        if not email.endswith('@10code.es'):
            raise ImmediateHttpResponse(
                HttpResponseForbidden("Only @10code.es emails allowed")
            )
```

#### Autorización (RBAC)

```python
# apps/core/permissions.py
from django.contrib.auth.models import Permission
from rest_framework import permissions

class HasProjectPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Owners siempre tienen acceso
        if obj.owner == request.user:
            return True
        
        # Team members solo lectura
        if request.method in permissions.SAFE_METHODS:
            return request.user in obj.team_members.all()
        
        # Escritura solo para owners y PMs
        return request.user.has_perm('projects.change_project')
```

### 8.2 Protección de Datos Sensibles

#### Encriptación en Reposo

```python
# apps/core/fields.py
from django_cryptography.fields import encrypt

class EncryptedDecimalField(encrypt(models.DecimalField)):
    """Campo decimal encriptado para datos sensibles (salarios, costes)"""
    pass

# Uso
class PayrollData(models.Model):
    gross_salary = EncryptedDecimalField(max_digits=10, decimal_places=2)
```

#### Secrets Management

```bash
# .env (NUNCA commitear)
SECRET_KEY=...
GOOGLE_OAUTH_CLIENT_ID=...
GOOGLE_OAUTH_SECRET=...
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
ODOO_API_KEY=...
```

```python
# config/settings/base.py
import environ

env = environ.Env()
environ.Env.read_env(BASE_DIR / '.env')

SECRET_KEY = env('SECRET_KEY')
DEBUG = env.bool('DEBUG', default=False)
```

### 8.3 Compliance RGPD

- **Consentimiento explícito**: Checkbox para procesamiento datos
- **Derecho de acceso**: Endpoint para exportar datos usuario
- **Derecho de olvido**: Soft-delete con anonimización
- **Portabilidad**: Export JSON de todos los datos
- **Auditoría**: Log de accesos a datos sensibles

```python
# apps/accounts/services.py
def user_export_data(*, user: User) -> dict:
    """Exporta todos los datos del usuario (RGPD portabilidad)"""
    return {
        'profile': {
            'email': user.email,
            'name': user.full_name,
            # ...
        },
        'projects': [p.to_dict() for p in user.owned_projects.all()],
        'time_entries': [t.to_dict() for t in user.time_entries.all()],
        # ...
    }
```

---

## 9. Performance y Escalabilidad

### 9.1 Estrategia de Caching

#### Niveles de Cache

```python
# 1. Cache de bajo nivel (funciones)
from django.core.cache import cache

def get_project_dashboard_data(project_id: uuid.UUID) -> dict:
    cache_key = f'project_dashboard_{project_id}'
    data = cache.get(cache_key)
    
    if data is None:
        data = _compute_dashboard_data(project_id)
        cache.set(cache_key, data, timeout=300)  # 5 min
    
    return data

# 2. Cache de vista completa
from django.views.decorators.cache import cache_page

@cache_page(60 * 5)  # 5 minutos
def public_dashboard(request):
    # ...
    pass

# 3. Cache de template fragment (menos usado con Inertia)
{% load cache %}
{% cache 500 sidebar request.user.id %}
    ... sidebar ...
{% endcache %}
```

#### Invalidación de Cache

```python
# Invalidación tras actualización
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Project)
def invalidate_project_cache(sender, instance, **kwargs):
    cache_key = f'project_dashboard_{instance.id}'
    cache.delete(cache_key)
```

### 9.2 Optimización de Queries

```python
# ❌ MAL: N+1 query problem
projects = Project.objects.all()
for project in projects:
    print(project.owner.email)  # Query por cada proyecto!
    print(project.team_members.count())  # Otra query!

# ✅ BIEN: select_related + prefetch_related
projects = Project.objects.select_related(
    'owner'  # ForeignKey
).prefetch_related(
    'team_members'  # ManyToMany
).all()
```

### 9.3 Paginación

```python
# apps/projects/views.py
from django.core.paginator import Paginator

def project_list_view(request):
    projects = project_list(user=request.user)
    
    paginator = Paginator(projects, 25)  # 25 por página
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'Projects/List', {
        'projects': page_obj,
        'pagination': {
            'current': page_obj.number,
            'total': paginator.num_pages,
            'has_next': page_obj.has_next(),
            'has_prev': page_obj.has_previous(),
        }
    })
```

### 9.4 Tareas Asíncronas (Celery)

```python
# apps/integrations/tasks.py
from celery import shared_task
from .services import sync_odoo_payroll_data

@shared_task(bind=True, max_retries=3)
def sync_odoo_payroll_task(self):
    """Sincroniza nóminas desde ODOO mensualmente"""
    try:
        result = sync_odoo_payroll_data()
        return f"Synced {result['count']} records"
    except Exception as exc:
        # Retry con backoff exponencial
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))
```

```python
# config/celery.py
from celery import Celery
from celery.schedules import crontab

app = Celery('10code_intranet')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Tareas periódicas
app.conf.beat_schedule = {
    'sync-odoo-payroll-monthly': {
        'task': 'apps.integrations.tasks.sync_odoo_payroll_task',
        'schedule': crontab(day_of_month=1, hour=3, minute=0),
    },
    'send-daily-digest': {
        'task': 'apps.notifications.tasks.send_daily_digest_email',
        'schedule': crontab(hour=9, minute=0),
    },
}
```

---

## 10. Testing

### 10.1 Pirámide de Testing

```bash
        /\
       /  \      E2E Tests (5%)
      /____\     - Playwright/Cypress
     /      \    - Flujos críticos
    /        \   
   /__________\  Integration Tests (15%)
  /            \ - Django TestCase
 /              \ - APIs, workflows
/________________\ Unit Tests (80%)
                   - pytest
                   - Services, selectors, utils
```

### 10.2 Ejemplos de Tests

```python
# apps/projects/tests/test_services.py
import pytest
from django.contrib.auth import get_user_model
from apps.projects.services import project_create
from apps.projects.tests.factories import UserFactory

User = get_user_model()

@pytest.mark.django_db
class TestProjectCreate:
    def test_creates_project_successfully(self):
        owner = UserFactory(is_staff=True)
        team = UserFactory.create_batch(3)
        
        project = project_create(
            title="Test Project",
            owner=owner,
            team_members=team,
            budget=Decimal('10000.00')
        )
        
        assert project.title == "Test Project"
        assert project.owner == owner
        assert project.team_members.count() == 3
    
    def test_raises_error_if_owner_no_permission(self):
        owner = UserFactory(is_staff=False)  # Sin permiso
        
        with pytest.raises(PermissionDenied):
            project_create(
                title="Test",
                owner=owner,
                team_members=[]
            )
```

### 10.3 Coverage Target

```bash
# pytest.ini
[pytest]
DJANGO_SETTINGS_MODULE = config.settings.testing
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    --cov=apps
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80
```

---

## 11. Deployment e Infraestructura

### 11.1 Arquitectura de Deployment

```mermaid
graph TB
    subgraph "Producción"
        LB[Load Balancer / Nginx]
        WEB1[Django + Gunicorn - Instance 1]
        WEB2[Django + Gunicorn - Instance 2]
        CELERY[Celery Workers]
        DB[(PostgreSQL)]
        REDIS[(Redis)]
    end
    
    USER[Users] --> LB
    LB --> WEB1
    LB --> WEB2
    WEB1 --> DB
    WEB2 --> DB
    WEB1 --> REDIS
    WEB2 --> REDIS
    CELERY --> DB
    CELERY --> REDIS
```

### 11.2 Docker Compose (Desarrollo)

```yaml
# docker-compose.yml
version: '3.9'

services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: intranet_dev
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
  
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
  
  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
    environment:
      - DEBUG=True
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/intranet_dev
      - REDIS_URL=redis://redis:6379/0
  
  celery:
    build: .
    command: celery -A config worker -l info
    volumes:
      - .:/app
    depends_on:
      - db
      - redis
  
  celery-beat:
    build: .
    command: celery -A config beat -l info
    volumes:
      - .:/app
    depends_on:
      - redis

volumes:
  postgres_data:
```

### 11.3 CI/CD Pipeline

```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install poetry
          poetry install
      
      - name: Run tests
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost/test_db
        run: |
          poetry run pytest --cov
      
      - name: Lint
        run: |
          poetry run ruff check .
          poetry run mypy apps/
```

---

## 12. Monitoreo y Observabilidad

### 12.1 Logging

```python
# config/settings/production.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': '%(asctime)s %(name)s %(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'json',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/intranet/app.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
            'formatter': 'json',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
        'apps': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
    },
}
```

### 12.2 Métricas (Prometheus + Grafana - futuro)

```python
# apps/core/middleware.py
from prometheus_client import Counter, Histogram

request_count = Counter('http_requests_total', 'Total HTTP Requests', ['method', 'endpoint'])
request_latency = Histogram('http_request_duration_seconds', 'HTTP Request Latency')

class MetricsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        with request_latency.time():
            response = self.get_response(request)
        
        request_count.labels(
            method=request.method,
            endpoint=request.path
        ).inc()
        
        return response
```

---

## 13. Decisiones Técnicas Pendientes

| Decisión | Opciones | Status | Owner |
|----------|----------|--------|-------|
| **Hosting provider** | AWS / DigitalOcean / On-premise | Pending | CTO |
| **Monitoreo APM** | Sentry / Datadog / New Relic | Pending | Tech Lead |
| **Email service** | Gmail SMTP / SendGrid / AWS SES | To decide | Backend Lead |
| **Backup strategy** | Automated / Manual / Hybrid | To define | DevOps |

---

## 14. Referencias y Recursos

### 14.1 Documentación Oficial

- [Django 5 Documentation](https://docs.djangoproject.com/en/5.0/)
- [Inertia.js Django Adapter](https://inertiajs.github.io/inertia-django/)
- [PostgreSQL 15 Documentation](https://www.postgresql.org/docs/15/)
- [Celery Documentation](https://docs.celeryproject.org/)

### 14.2 Libros Recomendados

- "Two Scoops of Django" - Daniel & Audrey Greenfeld
- "Architecture Patterns with Python" - Harry Percival & Bob Gregory
- "Django for Professionals" - William Vincent

### 14.3 ADRs Relacionados

- [001 - Monolith vs Microservices](../adr/001-monolith-vs-microservices.md)
- [002 - Django + Inertia.js Stack](../adr/002-django-inertia-choice.md)
- [003 - PostgreSQL as Primary Database](../adr/003-postgresql-choice.md)
- [004 - Tiptap + WeasyPrint for Documents](../adr/004-tiptap-weasyprint-docs.md)

---

## 15. Historial de Cambios

| Versión | Fecha | Autor | Cambios |
|---------|-------|-------|---------|
| 1.0 | 2025-01-15 | [Arquitecto] | Versión inicial |
| 1.1 | 2025-02-10 | [Tech Lead] | Añadida sección de ML |

---

**Documento revisado y aprobado por:**

- [ ] CTO / Arquitecto Principal
- [ ] Tech Lead Backend
- [ ] Tech Lead Frontend
- [ ] DevOps Lead

**Fecha de aprobación**: _________________
