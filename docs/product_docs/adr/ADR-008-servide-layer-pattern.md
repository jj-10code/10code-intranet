# ADR-008: Service Layer Pattern como Arquitectura Principal de Lógica de Negocio

## Metadata

- **Status**: Accepted
- **Fecha**: 2025-11-17
- **Decisor(es)**: Juanje Márquez - 10Code
- **Tags**: arquitectura, backend, django, patrones, service-layer, ddd

---

## Contexto y Problema

En una aplicación Django monolítica modular, la lógica de negocio puede ubicarse en diferentes lugares:

- **Views (Fat Views)**: Toda la lógica en las vistas Django
- **Models (Fat Models)**: Lógica de negocio en métodos del modelo
- **Forms**: Validaciones y lógica en formularios Django
- **Service Layer**: Capa dedicada de servicios con lógica de negocio
- **Mixto sin patrón**: Lógica dispersa sin estructura clara

**Problemas a resolver:**

1. **Reutilización**: La misma operación de negocio se necesita desde views, APIs, Celery tasks, comandos management
2. **Testing**: Lógica acoplada a views/models es difícil de testear en aislamiento
3. **Transacciones**: Operaciones complejas requieren transacciones atómicas coordinadas
4. **Mantenibilidad**: Sin patrón claro, la lógica se dispersa y es difícil de localizar
5. **Evolución a async**: Migrar a Celery/async es complejo si la lógica está en views/models
6. **Comunicación entre módulos**: Apps Django necesitan invocar lógica de otros módulos de forma desacoplada

**Requerimientos del proyecto:**

- Desarrollo con un desarrollador principal + agentes IA (necesita patrones claros y consistentes)
- Módulos autocontenidos (bounded contexts en DDD)
- Bajo acoplamiento entre apps Django
- Preparado para tareas asíncronas (Celery)
- Testing obligatorio con 80% cobertura
- Evolución futura a SaaS multitenancy

---

## Factores de Decisión

| Factor | Peso | Descripción |
|--------|------|-------------|
| **Reutilización** | Alta | Lógica debe ser invocable desde views, APIs, Celery, CLI |
| **Testabilidad** | Alta | Testing en aislamiento sin HTTP/DB mocking complejo |
| **Mantenibilidad** | Alta | Código fácil de localizar y modificar por agentes IA |
| **Transacciones** | Media | Soporte para transacciones atómicas complejas |
| **Desacoplamiento** | Alta | Comunicación entre módulos sin dependencias circulares |
| **Curva de aprendizaje** | Media | Patrón debe ser comprensible para nuevos developers |
| **Django idiomatic** | Media | Alineado con filosofía Django cuando sea posible |
| **Async-ready** | Alta | Fácil migración a Celery/async en el futuro |

---

## Opciones Consideradas

### Opción 1: Fat Views (Lógica en Vistas Django)

**Descripción:** Toda la lógica de negocio reside en las funciones/clases de vista Django.

```python
# apps/projects/views.py
def create_project(request):
    # Validaciones
    if not request.user.has_perm('projects.add_project'):
        raise PermissionDenied()
    
    # Lógica de negocio
    project = Project.objects.create(
        name=request.POST['name'],
        client=request.POST['client'],
        created_by=request.user
    )
    
    # Side effects
    ProjectMember.objects.create(
        project=project,
        user=request.user,
        role='project_manager'
    )
    
    # Notificaciones
    send_notification(project.id)
    
    return redirect('projects.show', project.id)
```

**Pros:**

- ✅ Patrón tradicional Django, documentación abundante
- ✅ Sin abstracciones adicionales, código directo
- ✅ Curva de aprendizaje mínima para developers Django

**Cons:**

- ❌ **No reutilizable**: Para invocar desde Celery/CLI, duplicar código o importar view (anti-patrón)
- ❌ **Testing complejo**: Requiere request mocking, HTTP stack completo
- ❌ **Difícil evolución a async**: Lógica acoplada a request/response
- ❌ **Violación SRP**: Views manejan HTTP + lógica de negocio + side effects
- ❌ **No escalable**: Para comunicación entre módulos, importaciones directas entre views

---

### Opción 2: Fat Models (Lógica en Modelos Django)

**Descripción:** Métodos de instancia/manager en modelos contienen lógica de negocio.

```python
# apps/projects/models.py
class Project(models.Model):
    # ... campos ...
    
    def create_with_team(self, user):
        """Crear proyecto y asignar equipo."""
        # Lógica de negocio en el modelo
        self.save()
        
        ProjectMember.objects.create(
            project=self,
            user=user,
            role='project_manager'
        )
        
        send_notification(self.id)
        return self
```

**Pros:**

- ✅ Encapsulación: Lógica cerca de los datos
- ✅ Reutilizable: Invocar desde cualquier parte con `project.create_with_team()`
- ✅ OOP puro: Patrón Active Record familiar

**Cons:**

- ❌ **Violación SRP**: Model hace persistencia + lógica de negocio
- ❌ **Testing complejo**: Requiere instancia de modelo, dificulta mocking
- ❌ **Transacciones implícitas**: No hay punto claro para `@transaction.atomic`
- ❌ **Difícil desacoplamiento**: Models no pueden importar otros models fácilmente (circular imports)
- ❌ **No escalable**: Lógica compleja hace models inmanejables (1000+ líneas)
- ❌ **Mezcla concerns**: Persistencia + validación + lógica de negocio + side effects

---

### Opción 3: Forms + Class-Based Views

**Descripción:** Lógica en formularios Django + Class-Based Views para coordinación.

```python
# apps/projects/forms.py
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'client', 'methodology']
    
    def save(self, commit=True):
        project = super().save(commit=False)
        # Lógica de negocio en form.save()
        if commit:
            project.save()
            ProjectMember.objects.create(...)
        return project
```

**Pros:**

- ✅ Validación + lógica juntas (cohesión)
- ✅ Django idiomatic para formularios web

**Cons:**

- ❌ **No reutilizable**: Forms acoplados a contexto HTTP/request
- ❌ **Limitado**: No funciona para operaciones sin formulario (Celery, APIs)
- ❌ **Confuso**: Forms deben ser validación, no orquestación de negocio
- ❌ **Testing medio**: Mejor que views, pero requiere form context

---

### Opción 4: Service Layer + Thin Models + Selectors

**Descripción:** Capa dedicada de servicios con toda la lógica de negocio. Models solo estructura. Selectors para queries optimizadas.

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
        """Crear proyecto con validaciones completas."""
        # 1. Validaciones
        if not created_by.has_perm('projects.add_project'):
            raise PermissionDenied()
        
        # 2. Crear entidad
        project = Project.objects.create(
            name=name,
            client=client,
            methodology=methodology,
            created_by=created_by,
            **kwargs
        )
        
        # 3. Side effects
        ProjectMember.objects.create(
            project=project,
            user=created_by,
            role='project_manager'
        )
        
        # 4. Async tasks
        send_notification.delay(project.id)
        
        return project

# apps/projects/selectors.py
def get_projects_list(*, user: User) -> QuerySet[Project]:
    """Obtener proyectos con queries optimizadas."""
    return Project.objects.select_related(
        'created_by'
    ).prefetch_related(
        'members__user'
    ).filter(
        Q(created_by=user) | Q(members__user=user)
    ).distinct()

# apps/projects/models.py
class Project(TimestampedModel):
    """Thin model - solo estructura."""
    name = models.CharField(max_length=200)
    # ... campos ...
    
    def __str__(self):
        return self.name
    
    @property
    def is_active(self) -> bool:
        return self.status == self.Status.ACTIVE

# apps/projects/views.py
def create_project(request):
    """Thin view - delega a service."""
    project = ProjectService.create_project(
        name=request.POST['name'],
        client=request.POST['client'],
        methodology=request.POST['methodology'],
        created_by=request.user
    )
    return redirect('projects.show', project.id)
```

**Pros:**

- ✅ **Máxima reutilización**: Invocar desde views, Celery, CLI, otros módulos
- ✅ **Testing simple**: Testear services sin HTTP stack, con fixtures mínimos
- ✅ **Transacciones explícitas**: `@transaction.atomic` en cada operación
- ✅ **SRP**: Cada componente tiene responsabilidad única (view=HTTP, service=negocio, model=datos)
- ✅ **Desacoplamiento**: Módulos se comunican vía service layer (interfaz clara)
- ✅ **Async-ready**: Fácil mover lógica a Celery sin refactorizar
- ✅ **Type hints**: Interfaces explícitas con type hints para herramientas y agentes IA
- ✅ **Escalable**: Lógica compleja no contamina models/views
- ✅ **DDD-friendly**: Services = Application Layer en DDD

**Cons:**

- ❌ **Boilerplate adicional**: Más archivos/clases que Fat Models
- ❌ **Curva de aprendizaje**: No es patrón Django tradicional (aunque común en proyectos grandes)
- ❌ **Tentación de over-engineering**: Riesgo de servicios muy granulares

---

## Decisión

**Opción elegida**: **Service Layer + Thin Models + Selectors** (Opción 4)

### Justificación

Hemos decidido implementar el **Service Layer Pattern** como arquitectura principal para toda la lógica de negocio del proyecto por las siguientes razones técnicas y estratégicas:

#### 1. **Desarrollo con Agentes IA (Crítico)**

El proyecto se desarrolla con un desarrollador principal + agentes IA (Claude, Cursor, etc.). El Service Layer proporciona:

- **Contratos explícitos**: Type hints + docstrings claros = agentes comprenden interfaces
- **Código predecible**: Estructura consistente = agentes generan código correcto
- **Separación de concerns**: Agentes pueden modificar services sin romper views/models
- **Testing automático**: Agentes pueden generar tests unitarios fácilmente

**Sin Service Layer**, agentes IA tienden a mezclar concerns y generar código difícil de mantener.

#### 2. **Reutilización Máxima**

La misma operación se invoca desde:

- **Views Django**: `ProjectService.create_project(...)`
- **Celery tasks**: `ProjectService.create_project(...)`
- **Django management commands**: `ProjectService.create_project(...)`
- **Otros módulos**: `from apps.projects.services import ProjectService`

**Sin Service Layer**, duplicaríamos lógica o haríamos imports anti-patrón entre views.

#### 3. **Testing Simple y Rápido**

```python
# Test de service (sin HTTP stack)
def test_create_project():
    user = UserFactory()
    project = ProjectService.create_project(
        name="Test",
        client="Client",
        methodology="scrum",
        created_by=user
    )
    assert project.id is not None
```

vs testing Fat Views (requiere RequestFactory, middleware, etc.)

#### 4. **Transacciones Atómicas Explícitas**

Cada service method tiene `@transaction.atomic`, garantizando ACID en operaciones complejas:

```python
@transaction.atomic
def create_project(...):
    project = Project.objects.create(...)  # Se rollbackea si falla lo siguiente
    ProjectMember.objects.create(...)
    # Todo o nada
```

#### 5. **Comunicación Entre Módulos Desacoplada**

```python
# apps/backlog/services.py
from apps.projects.services import ProjectService

class BacklogService:
    @staticmethod
    def link_epic_to_project(epic_id: int, project_id: int):
        # Invocar lógica de projects sin importar models directamente
        project = ProjectService.get_project(project_id=project_id)
        # ...
```

**Sin Service Layer**, apps se acoplan vía imports directos de models = alto acoplamiento.

#### 6. **Evolución a Async Sin Refactorizar**

Fase actual (síncrono):

```python
class ProjectService:
    @staticmethod
    def create_project(...):
        # Lógica síncrona
        return project
```

Fase futura (async con Celery):

```python
class ProjectService:
    @staticmethod
    def create_project(...):
        # Delegar a Celery sin cambiar interfaz
        task = create_project_task.delay(...)
        return {'task_id': task.id}
```

**Views no cambian**, solo cambia implementación interna del service.

#### 7. **Escalabilidad a SaaS Multitenancy**

Services son el lugar ideal para añadir lógica de multitenancy:

```python
@transaction.atomic
def create_project(*, tenant_id: int, ...):
    # Validar tenant
    tenant = get_current_tenant(tenant_id)
    
    # Crear proyecto en tenant
    project = Project.objects.create(
        tenant=tenant,
        ...
    )
```

#### 8. **Alineado con DDD (Domain-Driven Design)**

El proyecto usa DDD con bounded contexts (apps Django). En DDD:

- **Service Layer = Application Layer**: Orquesta use cases
- **Models = Domain Layer**: Entidades y value objects
- **Views = Interface Layer**: Adaptadores HTTP

Service Layer es el patrón DDD estándar para este tipo de arquitectura.

---

## Consecuencias

### Positivas

- ✅ **Lógica centralizada**: Toda la lógica de negocio en un lugar predecible (`apps/<module>/services.py`)
- ✅ **Testing rápido**: Tests unitarios de services sin dependencias HTTP/DB pesadas
- ✅ **Reutilización total**: Una función, múltiples consumidores (views, Celery, CLI, otros módulos)
- ✅ **Transacciones garantizadas**: `@transaction.atomic` en cada operación crítica
- ✅ **Desacoplamiento entre módulos**: Comunicación vía service layer (interfaz estable)
- ✅ **Type safety**: Type hints obligatorios = mejor tooling y menos bugs
- ✅ **IA-friendly**: Código estructurado y predecible para agentes IA
- ✅ **Async-ready**: Preparado para Celery sin refactorizar views
- ✅ **Escalable**: Lógica compleja no contamina models (que permanecen thin)
- ✅ **Documentación viva**: Docstrings de services = contratos explícitos

### Negativas

- ❌ **Boilerplate inicial**: Requiere crear archivos `services.py`, `selectors.py` por app
- ❌ **Curva de aprendizaje**: Desarrolladores nuevos deben aprender el patrón (no es Django "vanilla")
- ❌ **Tentación over-engineering**: Riesgo de crear services muy granulares innecesarios
- ❌ **No es Django "tradicional"**: Documentación Django oficial no cubre Service Layer

### Neutras

- ⚠️ **Consistencia obligatoria**: TODO el equipo (incluidos agentes IA) debe seguir el patrón
- ⚠️ **Code reviews estrictos**: Verificar que lógica NO se filtre a views/models
- ⚠️ **Educación continua**: Nuevos developers deben leer `.rules/DJANGO_PATTERNS.md`

---

## Notas de Implementación

### Estructura de Archivos Obligatoria

```python
apps/<module>/
├── services.py       # WRITE operations + lógica de negocio
├── selectors.py      # READ operations optimizadas
├── models.py         # THIN models - solo estructura
├── views.py          # THIN views - delegan a services/selectors
├── urls.py
└── tests/
    ├── test_services.py   # Tests unitarios de services
    ├── test_selectors.py  # Tests de queries optimizadas
    └── factories.py       # Factory Boy fixtures
```

### Template de Service (Copiar y adaptar)

```python
# apps/<module>/services.py
from django.db import transaction
from django.core.exceptions import ValidationError, PermissionDenied
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class <Module>Service:
    """Service para gestión de <dominio>."""
    
    @staticmethod
    @transaction.atomic
    def create_<entity>(
        *,
        field1: str,
        field2: int,
        user: User,
        optional_field: Optional[str] = None,
        **kwargs
    ) -> <Entity>:
        """
        Crear <entidad> con validaciones completas.
        
        Args:
            field1: Descripción del campo
            field2: Descripción del campo
            user: Usuario que realiza la operación
            optional_field: Campo opcional
            **kwargs: Campos adicionales del modelo
        
        Returns:
            <Entity> creada
        
        Raises:
            ValidationError: Si datos inválidos
            PermissionDenied: Si usuario sin permisos
        """
        # 1. Validar permisos
        if not user.has_perm('<module>.add_<entity>'):
            raise PermissionDenied("Usuario sin permisos para crear <entity>")
        
        # 2. Validar negocio
        if <Entity>.objects.filter(field1=field1).exists():
            raise ValidationError(f"<Entity> con field1='{field1}' ya existe")
        
        # 3. Crear entidad principal
        entity = <Entity>.objects.create(
            field1=field1,
            field2=field2,
            created_by=user,
            **kwargs
        )
        
        # 4. Side effects (creación de entidades relacionadas)
        RelatedEntity.objects.create(
            entity=entity,
            ...
        )
        
        # 5. Tareas asíncronas (opcional)
        async_task.delay(entity.id)
        
        # 6. Logging
        logger.info(
            f"<Entity> creada: {entity.id} por {user.email}",
            extra={'entity_id': entity.id, 'user_id': user.id}
        )
        
        return entity
    
    @staticmethod
    @transaction.atomic
    def update_<entity>(
        *,
        entity_id: int,
        field1: Optional[str] = None,
        user: User,
        **kwargs
    ) -> <Entity>:
        """Actualizar <entidad>."""
        # Similar estructura...
        pass
    
    @staticmethod
    def calculate_<metric>(*, entity_id: int) -> float:
        """Calcular métrica de negocio (READ-ONLY, sin @transaction)."""
        entity = <Entity>.objects.get(id=entity_id)
        # Lógica de cálculo...
        return result
```

### Template de Selector (Copiar y adaptar)

```python
# apps/<module>/selectors.py
from typing import Optional, Dict
from django.db.models import QuerySet, Q, Prefetch

def get_<entities>_list(
    *,
    user: User,
    filters: Optional[Dict] = None
) -> QuerySet[<Entity>]:
    """
    Obtener lista de <entidades> optimizada.
    
    Args:
        user: Usuario para filtros de permisos
        filters: Filtros opcionales (status, date_from, etc.)
    
    Returns:
        QuerySet optimizado con select_related/prefetch_related
    """
    # Base query con optimizaciones
    qs = <Entity>.objects.select_related(
        'created_by',
        'related_entity'
    ).prefetch_related(
        Prefetch(
            'many_to_many_relation',
            queryset=RelatedModel.objects.select_related('nested_relation')
        )
    )
    
    # Permisos: staff ve todo, otros solo lo suyo
    if not user.is_staff:
        qs = qs.filter(
            Q(created_by=user) | Q(members__user=user)
        ).distinct()
    
    # Filtros opcionales
    if filters:
        if 'status' in filters:
            qs = qs.filter(status=filters['status'])
        
        if 'date_from' in filters:
            qs = qs.filter(created_at__gte=filters['date_from'])
    
    return qs.order_by('-created_at')

def get_<entity>_by_id(*, entity_id: int, user: User) -> <Entity>:
    """Obtener <entidad> por ID con permisos."""
    entity = <Entity>.objects.select_related(
        'created_by'
    ).get(id=entity_id)
    
    # Validar permisos de lectura
    if not user.is_staff and entity.created_by != user:
        raise PermissionDenied("No tienes permiso para ver esta entidad")
    
    return entity
```

### Template de Thin Model

```python
# apps/<module>/models.py
from django.db import models
from apps.core.models import TimestampedModel

class <Entity>(TimestampedModel):
    """Modelo <Entity> - THIN MODEL (solo estructura)."""
    
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Borrador'
        ACTIVE = 'active', 'Activo'
    
    # Campos
    field1 = models.CharField(max_length=200, db_index=True)
    field2 = models.IntegerField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT
    )
    created_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.PROTECT,
        related_name='created_<entities>'
    )
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'created_at']),
        ]
    
    def __str__(self):
        return self.field1
    
    # SOLO propiedades simples sin queries
    @property
    def is_active(self) -> bool:
        return self.status == self.Status.ACTIVE
```

### Template de Thin View

```python
# apps/<module>/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .services import <Module>Service
from .selectors import get_<entities>_list

@login_required
def <entities>_index(request):
    """Listar <entidades> - THIN VIEW."""
    <entities> = get_<entities>_list(
        user=request.user,
        filters=request.GET.dict()
    )
    
    return render(request, '<Module>/Index', props={
        '<entities>': serialize_<entities>(<entities>),
        'permissions': {
            'can_create': request.user.has_perm('<module>.add_<entity>'),
        }
    })

@login_required
def <entities>_create(request):
    """Crear <entidad> - THIN VIEW."""
    if request.method == 'POST':
        # View delega TODO a service
        <entity> = <Module>Service.create_<entity>(
            field1=request.POST['field1'],
            field2=int(request.POST['field2']),
            user=request.user
        )
        return redirect('<module>.<entities>.show', <entity>.id)
    
    return render(request, '<Module>/Create')
```

### Reglas de Oro para Implementación

1. ✅ **TODA lógica de negocio va en services.py**
2. ✅ **Selectors para TODAS las queries READ** (nunca queries en views)
3. ✅ **Models son thin** - solo estructura + propiedades simples
4. ✅ **Views son thin** - solo HTTP handling + delegación a services/selectors
5. ✅ **@transaction.atomic en TODAS las operaciones WRITE**
6. ✅ **Type hints OBLIGATORIOS en services y selectors**
7. ✅ **Keyword-only args** (`*,` después del primer parámetro)
8. ✅ **Docstrings completos** en todos los métodos públicos
9. ✅ **Logging estructurado** en operaciones críticas
10. ✅ **Un service por app Django** (no múltiples services pequeños en MVP)

### Comunicación Entre Módulos

```python
# ✅ CORRECTO - Importar service de otro módulo
# apps/backlog/services.py
from apps.projects.services import ProjectService

class BacklogService:
    @staticmethod
    def link_epic_to_project(epic_id: int, project_id: int):
        project = ProjectService.get_project(project_id=project_id)
        epic = Epic.objects.get(id=epic_id)
        epic.project = project
        epic.save()

# ❌ INCORRECTO - Importar model directamente
# apps/backlog/services.py
from apps.projects.models import Project  # NO!

class BacklogService:
    @staticmethod
    def link_epic_to_project(epic_id: int, project_id: int):
        project = Project.objects.get(id=project_id)  # Acoplamiento fuerte!
```

### Testing de Services

```python
# apps/<module>/tests/test_services.py
import pytest
from apps.<module>.services import <Module>Service
from apps.accounts.tests.factories import UserFactory

@pytest.mark.django_db
class Test<Module>Service:
    
    def test_create_<entity>_success(self):
        user = UserFactory(permissions=['<module>.add_<entity>'])
        
        <entity> = <Module>Service.create_<entity>(
            field1="Test",
            field2=123,
            user=user
        )
        
        assert <entity>.id is not None
        assert <entity>.field1 == "Test"
        assert <entity>.created_by == user
    
    def test_create_<entity>_without_permission(self):
        user = UserFactory()  # Sin permisos
        
        with pytest.raises(PermissionDenied):
            <Module>Service.create_<entity>(
                field1="Test",
                field2=123,
                user=user
            )
    
    def test_create_<entity>_duplicate(self):
        user = UserFactory(permissions=['<module>.add_<entity>'])
        <Module>Service.create_<entity>(field1="Test", field2=123, user=user)
        
        # Intentar duplicar
        with pytest.raises(ValidationError):
            <Module>Service.create_<entity>(
                field1="Test",  # Mismo field1
                field2=456,
                user=user
            )
```

---

## Referencias

- **Django Service Layer Pattern**: <https://www.dabapps.com/insights/django-models-and-encapsulation/>
- **Phalt's Styleguide**: <https://github.com/phalt/django-api-domains>
- **HackSoftware Django Styleguide**: <https://github.com/HackSoftware/Django-Styleguide>
- **Domain-Driven Design (Eric Evans)**: Libro fundacional de DDD
- **Clean Architecture (Robert C. Martin)**: Service Layer como Use Cases
- `.rules/DJANGO_PATTERNS.md`: Patrones obligatorios del proyecto
- `.rules/ARCHITECTURE_RULES.md`: Comunicación entre módulos
- `docs/product_docs/SAD_Intranet_10Code.md`: Sección 5 (Arquitectura Detallada)

---

## Historial

| Fecha | Evento |
|-------|--------|
| 2025-11-17 | ADR-008 creado y aceptado como patrón obligatorio |

---

**Firmado por:**

- Juanje Márquez - Arquitecto Principal y Lead Developer - 2025-11-17
