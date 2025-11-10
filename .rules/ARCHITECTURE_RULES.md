# Reglas Arquitectónicas - 10Code Intranet

# Patrones Estructurales y de Comunicación

## 🏛️ ARQUITECTURA: MONOLITO MODULAR MAJESTUOSO

### Filosofía Central

El sistema implementa un **Monolito Modular Majestuoso** que combina:

- Simplicidad operativa de un monolito
- Disciplina modular de microservicios
- Experiencia SPA moderna sin API REST tradicional
- Preparado para escalar a SaaS en el futuro

### Por Qué NO Microservicios (Ahora)

- ❌ Complejidad operativa prematura
- ❌ Overhead en comunicación entre servicios
- ❌ Gestión de datos distribuidos compleja
- ❌ Fricción en desarrollo para equipo pequeño
- ✅ Maximizar velocidad de desarrollo
- ✅ Minimizar complejidad inicial
- ✅ Evolución gradual hacia MSA si necesario

### Inertia.js: El Puente Majestuoso

Inertia permite:

- Experiencia SPA completa sin API REST separada
- Backend clásico server-driven
- Frontend moderno client-rendered
- Elimina necesidad de serializers y endpoints
- Mantiene simplicidad del monolito

## 📦 MODULARIDAD POR DOMINIOS (DDD)

### Apps Como Módulos de Negocio

Cada app Django representa un **Bounded Context** en DDD:

```txt
apps/
├── accounts/          # Dominio: Identidad y Autenticación
├── projects/          # Dominio: Gestión de Proyectos
├── resources/         # Dominio: Recursos Humanos
├── financial/         # Dominio: Financiero
├── timetracking/      # Dominio: Control Horario
├── estimation/        # Dominio: Estimaciones IA
├── backlog/           # Dominio: Product Management
├── reporting/         # Dominio: Business Intelligence
└── integrations/      # Dominio: Conectores Externos
```

### Características de un Bounded Context

1. **Autocontenido**: Tiene sus propios models, services, views
2. **Responsabilidad Única**: Gestiona un dominio de negocio claro
3. **Interfaz Clara**: Expone funcionalidad via service layer
4. **Bajo Acoplamiento**: Mínimas dependencias con otros contexts
5. **Alta Cohesión**: Todo el código relacionado está junto

### Anti-Patrón: App "core" con Lógica de Negocio

```python
# ❌ MAL - core NO debe tener lógica de negocio
apps/core/
├── business_logic.py    # NO! Esto debe ir en app específica
├── project_utils.py     # NO! Va en apps/projects/
└── user_helpers.py      # NO! Va en apps/accounts/

# ✅ BIEN - core solo para infraestructura compartida
apps/core/
├── models.py           # Solo modelos abstractos base
├── middleware.py       # Middleware genérico
├── utils.py            # Utilidades genéricas (dates, strings)
├── decorators.py       # Decoradores reutilizables
└── management/         # Comandos de gestión genéricos
```

## 🔗 COMUNICACIÓN ENTRE APLICACIONES

### Patrón 1: Service Layer (PRIMARIO - 80% casos)

La comunicación principal es a través de funciones de servicio:

```python
# ❌ MAL - Importación directa de modelo
# en apps/documents/views.py
from apps.users.models import User  # Acoplamiento fuerte

def create_document(request):
    user = User.objects.get(id=request.user.id)  # NO!
    user.increment_document_count()  # Lógica de users en documents!

# ✅ BIEN - Llamada a service layer
# en apps/documents/views.py
from apps.users.services import UserService

def create_document(request):
    document = DocumentService.create_document(
        user=request.user,
        data=request.POST.dict()
    )
    
    # Incrementar contador en dominio correcto
    UserService.increment_document_count(user_id=request.user.id)
```

#### Reglas del Service Layer

1. **Contratos Explícitos**: Firma de función es el contrato
2. **Type Hints Obligatorios**: Para claridad y tooling
3. **Keyword-Only Args**: Usar `*` para forzar kwargs
4. **Transacciones Atómicas**: Usar `@transaction.atomic`
5. **Single Responsibility**: Una función, una responsabilidad

#### Template de Service Function

```python
from django.db import transaction
from typing import Optional

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
        
        Esta función es el ÚNICO punto de entrada para crear proyectos.
        Garantiza: validaciones de negocio, side effects, notificaciones.
        
        Args:
            name: Nombre único del proyecto
            client: Cliente asociado
            methodology: scrum | kanban | waterfall | hybrid
            created_by: Usuario que crea (será asignado como PM)
            budget: Presupuesto opcional
            **kwargs: Campos adicionales del modelo
        
        Returns:
            Proyecto creado y completamente inicializado
        
        Raises:
            ValidationError: Si datos inválidos o proyecto duplicado
            PermissionError: Si usuario no puede crear proyectos
        """
        # 1. Validaciones de negocio
        if not created_by.has_perm('projects.add_project'):
            raise PermissionError("Usuario sin permisos para crear proyectos")
        
        if Project.objects.filter(name=name, client=client).exists():
            raise ValidationError(f"Proyecto '{name}' ya existe para '{client}'")
        
        # 2. Crear entidad principal
        project = Project.objects.create(
            name=name,
            client=client,
            methodology=methodology,
            created_by=created_by,
            budget=budget,
            **kwargs
        )
        
        # 3. Side effects - inicialización relacionada
        ProjectMember.objects.create(
            project=project,
            user=created_by,
            role='project_manager',
            allocation_percentage=100
        )
        
        # 4. Eventos asíncronos
        send_project_created_notification.delay(project.id)
        
        # 5. Auditoría
        logger.info(
            f"Proyecto creado: {project.id} por {created_by.email}",
            extra={'project_id': project.id, 'user_id': created_by.id}
        )
        
        return project
```

### Patrón 2: Señales de Django (SECUNDARIO - 15% casos)

Para lógica desacoplada y basada en eventos:

```python
# ✅ CUÁNDO USAR SEÑALES
# - Logging/auditoría automática
# - Invalidación de cache
# - Notificaciones post-save
# - Efectos secundarios que NO afectan integridad de datos
# - Plugins/extensiones que deben reaccionar a eventos

# apps/projects/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Project

@receiver(post_save, sender=Project)
def project_post_save(sender, instance, created, **kwargs):
    """
    Hook post-save para auditoría y cache.
    NO DEBE contener lógica crítica de negocio.
    """
    if created:
        # Auditoría
        logger.info(f"Proyecto creado: {instance.id}")
        
        # Invalidar cache relacionado
        cache.delete(f'user_projects_{instance.created_by_id}')
        
        # Notificación asíncrona (no crítica)
        notify_team_new_project.delay(instance.id)

# apps/projects/apps.py
class ProjectsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.projects'

    def ready(self):
        """Registrar señales al inicio."""
        import apps.projects.signals  # noqa
```

#### ⚠️ CUIDADO con Señales

- No usar para lógica crítica (usar services)
- Pueden hacer flujo difícil de seguir
- Debugging más complejo
- Side effects ocultos
- Úsar solo cuando desacoplamiento sea beneficioso

### Patrón 3: Importación Directa de Modelos (5% casos)

Solo para:

- Relaciones ForeignKey/ManyToMany obligatorias
- Operaciones de solo lectura muy simples
- Dentro del mismo bounded context

```python
# ✅ ACEPTABLE - Relación ForeignKey
# apps/projects/models.py
from apps.accounts.models import User  # OK para FK

class Project(models.Model):
    created_by = models.ForeignKey(User, ...)  # Necesario

# ✅ ACEPTABLE - Lectura simple en selector
# apps/documents/selectors.py
from apps.users.models import User

def get_documents_for_user(*, user_id: int):
    user = User.objects.get(id=user_id)  # Solo lectura
    return Document.objects.filter(owner=user)

# ❌ EVITAR - Escritura o lógica compleja
# apps/documents/views.py
from apps.users.models import User

def create_document(request):
    user = User.objects.get(id=request.user.id)
    user.document_count += 1  # NO! Usar UserService
    user.save()
```

## 🔮 PREPARACIÓN PARA FUTURO ASÍNCRONO

### Celery para Tareas Pesadas

La arquitectura de service layer facilita migrar a async:

```python
# Fase 1: Síncrono
class ProjectService:
    @staticmethod
    def generate_report(project_id: int):
        # Lógica pesada...
        return report

# Fase 2: Asíncrono (sin cambiar interfaz)
class ProjectService:
    @staticmethod
    def generate_report(project_id: int):
        # Delegar a Celery
        task = generate_report_task.delay(project_id)
        return {'task_id': task.id}

# tasks.py
@shared_task
def generate_report_task(project_id: int):
    # Misma lógica, ahora async
    project = Project.objects.get(id=project_id)
    # ... generar report
```

### Django Channels para Real-Time

En el futuro, Channels puede añadirse sin refactorizar:

```python
# Mantener service layer
class TaskService:
    @staticmethod
    def update_task_status(task_id: int, status: str):
        task = Task.objects.get(id=task_id)
        task.status = status
        task.save()
        
        # Emitir evento WebSocket (opcional)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'project_{task.project_id}',
            {'type': 'task.updated', 'task_id': task_id}
        )
        
        return task
```

## 📊 MATRIZ DE COMUNICACIÓN ENTRE APPS

| Patrón                  | Acoplamiento | Complejidad | Caso de Uso Principal                    |
|------------------------|--------------|-------------|------------------------------------------|
| **Service Layer**      | Medio        | Media       | Comandos y lógica de negocio (80%)       |
| **Señales**            | Bajo         | Alta        | Eventos y side effects opcionales (15%)  |
| **Importación Modelo** | Alto         | Baja        | Relaciones FK y lecturas simples (5%)    |
| **Celery**             | Muy Bajo     | Alta        | Tareas pesadas y procesamiento async     |
| **Channels**           | Muy Bajo     | Muy Alta    | Comunicación real-time (futuro)          |

## 🎯 REGLAS DE DECISIÓN

### ¿Qué Patrón Usar?

```txt
┌─────────────────────────────────────┐
│ ¿Es lógica de negocio compleja?     │
│         (validaciones, orchestración)│
└────────────┬────────────────────────┘
             │ SÍ
             ▼
    ┌────────────────────┐
    │   SERVICE LAYER    │ ← 80% casos
    └────────────────────┘

┌─────────────────────────────────────┐
│ ¿Es side effect no crítico?         │
│         (logging, cache, analytics)  │
└────────────┬────────────────────────┘
             │ SÍ
             ▼
    ┌────────────────────┐
    │     SEÑALES        │ ← 15% casos
    └────────────────────┘

┌─────────────────────────────────────┐
│ ¿Es solo relación FK o lectura?     │
│         (sin lógica de negocio)      │
└────────────┬────────────────────────┘
             │ SÍ
             ▼
    ┌────────────────────┐
    │  IMPORTACIÓN       │ ← 5% casos
    │    DIRECTA         │
    └────────────────────┘

┌─────────────────────────────────────┐
│ ¿Tarea pesada (>1s) o background?   │
└────────────┬────────────────────────┘
             │ SÍ
             ▼
    ┌────────────────────┐
    │      CELERY        │ ← Futuro/avanzado
    └────────────────────┘
```

## 📐 DISEÑO DE INTERFACES ENTRE MÓDULOS

### Principios

1. **Contratos Explícitos**: Type hints + docstrings
2. **Stable Interfaces**: No cambiar firmas sin deprecation
3. **Versioning**: Considerar versiones si interfaz pública
4. **Backward Compatibility**: Mantener compatibilidad
5. **Documentation**: Documentar todas las interfaces públicas

### Template de Interface

```python
# apps/projects/services.py

class ProjectService:
    """
    Service para gestión de proyectos.
    
    Interfaz pública para operaciones sobre proyectos.
    Todas las funciones están transaccionalmente protegidas.
    """
    
    # --- WRITE OPERATIONS ---
    
    @staticmethod
    @transaction.atomic
    def create_project(...) -> Project:
        """Crear proyecto nuevo."""
        pass
    
    @staticmethod
    @transaction.atomic
    def update_project(...) -> Project:
        """Actualizar proyecto existente."""
        pass
    
    @staticmethod
    @transaction.atomic
    def delete_project(...) -> None:
        """Eliminar proyecto (soft delete)."""
        pass
    
    @staticmethod
    @transaction.atomic
    def assign_member(...) -> ProjectMember:
        """Asignar miembro al proyecto."""
        pass
    
    # --- BUSINESS LOGIC ---
    
    @staticmethod
    def calculate_project_cost(...) -> Decimal:
        """Calcular coste total del proyecto."""
        pass
    
    @staticmethod
    def calculate_progress(...) -> float:
        """Calcular % de progreso del proyecto."""
        pass
```

## 🧩 INTEGRACIÓN CON SISTEMAS EXTERNOS

### Apps de Integración Dedicadas

```python
# apps/integrations/
├── __init__.py
├── github/
│   ├── client.py       # Cliente API GitHub
│   ├── services.py     # Lógica de integración
│   └── webhooks.py     # Handlers de webhooks
├── discord/
│   ├── client.py
│   ├── services.py
│   └── webhooks.py
└── figma/
    ├── client.py
    └── services.py
```

### Patrón de Integración

```python
# apps/integrations/github/services.py

class GitHubIntegrationService:
    """Service para integración con GitHub."""
    
    @staticmethod
    def sync_project_repository(
        *,
        project_id: int,
        repo_url: str
    ) -> dict:
        """
        Sincronizar proyecto con repositorio GitHub.
        
        Esta función coordina entre múltiples dominios:
        - projects: Obtener/actualizar proyecto
        - integrations: Comunicarse con GitHub API
        - tasks: Crear tasks desde issues
        """
        from apps.projects.services import ProjectService
        
        # 1. Obtener proyecto
        project = ProjectService.get_project(project_id=project_id)
        
        # 2. Conectar con GitHub
        client = GitHubClient(repo_url)
        issues = client.get_issues()
        
        # 3. Sincronizar con tareas
        for issue in issues:
            TaskService.create_or_update_from_github(
                project_id=project.id,
                github_issue=issue
            )
        
        return {'synced_issues': len(issues)}
```

## 🔍 INSPECCIÓN Y DEBUGGING

### Herramientas Recomendadas

1. **Django Debug Toolbar**: Ver queries, cache, signals
2. **django-extensions**: shell_plus, graph_models
3. **Sentry**: Error tracking en producción
4. **Logging estructurado**: JSON logs con contexto

### Logging de Comunicación Entre Apps

```python
import structlog

logger = structlog.get_logger(__name__)

class ProjectService:
    @staticmethod
    @transaction.atomic
    def create_project(...):
        logger.info(
            "project.create.started",
            user_id=created_by.id,
            project_name=name,
            client=client
        )
        
        # ... lógica ...
        
        # Log de llamadas entre apps
        logger.info(
            "project.create.assigning_member",
            project_id=project.id,
            user_id=created_by.id
        )
        
        member = ProjectMemberService.assign(...) 
        
        logger.info(
            "project.create.completed",
            project_id=project.id,
            duration_ms=...
        )
```

---

**RECUERDA**: La arquitectura modular es una inversión en mantenibilidad a largo plazo. Respeta los boundaries entre módulos para mantener el sistema escalable y comprensible.
