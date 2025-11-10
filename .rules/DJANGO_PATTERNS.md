# Patrones Django - 10Code Intranet

## Service Layer, Selectors, Models y Optimización

## 🎯 RESUMEN EJECUTIVO

Este documento define los patrones obligatorios de Django para el proyecto:

- **Service Layer**: Lógica de negocio y WRITE operations
- **Selectors**: READ operations optimizadas
- **Thin Models**: Solo estructura de datos
- **Custom Managers**: QuerySets reutilizables
- **Optimización**: Eliminar N+1 queries

---

## 📋 REGLAS DE ORO

1. ✅ **Service Layer para toda lógica de negocio**
2. ✅ **Selectors para todas las consultas optimizadas**
3. ✅ **Models delgados - solo estructura**
4. ✅ **Transacciones atómicas en writes**
5. ✅ **Type hints obligatorios**
6. ✅ **select_related/prefetch_related siempre**
7. ❌ **NO lógica de negocio en views**
8. ❌ **NO lógica compleja en models**
9. ❌ **NO queries en loops (N+1)**

---

## 🎯 SERVICE LAYER

### Responsabilidades

- WRITE operations (Create, Update, Delete)
- Orquestación de lógica de negocio
- Validaciones complejas
- Coordinación de side effects
- Transacciones atómicas

### Template Estándar

```python
# apps/projects/services.py

from django.db import transaction
from typing import Optional, Dict
from decimal import Decimal

class ProjectService:
    """Service para gestión de proyectos."""
    
    @staticmethod
    @transaction.atomic
    def create_project(
        *,
        name: str,
        client: str,
        methodology: str,
        created_by: User,
        budget: Optional[Decimal] = None
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
        # 1. Validaciones
        if not created_by.has_perm('projects.add_project'):
            raise PermissionError("Usuario sin permisos")
        
        if Project.objects.filter(name=name, client=client).exists():
            raise ValidationError("Proyecto ya existe")
        
        # 2. Crear entidad
        project = Project.objects.create(
            name=name,
            client=client,
            methodology=methodology,
            created_by=created_by,
            budget=budget
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
```

---

## 📖 SELECTORS

### Responsabilidades de selectors

- READ operations únicamente
- Optimización con select_related/prefetch_related
- Filtros y búsquedas
- Sin side effects

### Template Estándar para selectors

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

## 📦 THIN MODELS

### Reglas

- Solo estructura de datos
- Métodos de instancia simples
- NO lógica de negocio
- Propiedades calculadas básicas

### Template Estándar para models

```python
# apps/projects/models.py

from django.db import models
from apps.core.models import TimestampedModel

class Project(TimestampedModel):
    """Modelo de Proyecto."""
    
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Borrador'
        ACTIVE = 'active', 'Activo'
        COMPLETED = 'completed', 'Completado'
    
    name = models.CharField(max_length=200, db_index=True)
    description = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT
    )
    
    created_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.PROTECT,
        related_name='created_projects'
    )
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'created_at']),
        ]
    
    def __str__(self):
        return self.name
    
    @property
    def is_active(self) -> bool:
        """Property simple sin queries."""
        return self.status == self.Status.ACTIVE
```

---

## ⚡ OPTIMIZACIÓN DE QUERIES

### Problema N+1

```python
# ❌ MAL
projects = Project.objects.all()
for p in projects:
    print(p.created_by.email)  # +N queries!

# ✅ BIEN
projects = Project.objects.select_related('created_by')
for p in projects:
    print(p.created_by.email)  # Sin queries extra
```

### select_related vs prefetch_related

```python
# select_related - ForeignKey / OneToOne
Project.objects.select_related('created_by', 'client')

# prefetch_related - ManyToMany / Reverse FK
Project.objects.prefetch_related('members', 'tasks')

# Combinado
Project.objects.select_related(
    'created_by'
).prefetch_related(
    'members__user',
    'tasks__assigned_to'
)
```

### Agregaciones en BD

```python
from django.db.models import Count, Sum, Avg

Project.objects.annotate(
    task_count=Count('tasks'),
    total_hours=Sum('tasks__hours_tracked'),
    avg_hours=Avg('tasks__hours_tracked')
)
```

---

## 🧪 TESTING

### Test de Service

```python
import pytest

@pytest.mark.django_db
class TestProjectService:
    
    def test_create_project_success(self, user):
        project = ProjectService.create_project(
            name="Test",
            client="Client",
            methodology="scrum",
            created_by=user
        )
        
        assert project.id is not None
        assert project.name == "Test"
        assert project.members.filter(user=user).exists()
```

### Test de Selector

```python
@pytest.mark.django_db
def test_get_projects_list_optimized(user):
    ProjectFactory.create_batch(5, created_by=user)
    
    with pytest.assertNumQueries(2):
        projects = list(get_projects_list(user=user))
        for p in projects:
            _ = p.created_by.email  # Sin queries extra
```

---

## 📝 CHECKLIST POR FEATURE

Al implementar una nueva feature:

- [ ] Crear/actualizar models en `models.py`
- [ ] Crear services en `services.py` con `@transaction.atomic`
- [ ] Crear selectors en `selectors.py` con optimizaciones
- [ ] Views delgadas que delegan a services/selectors
- [ ] Type hints en todas las funciones
- [ ] Docstrings completos
- [ ] Tests de services (unit)
- [ ] Tests de selectors (queries optimizadas)
- [ ] Verificar N+1 con Debug Toolbar

---

Este documento debe consultarse antes de escribir código Django para asegurar consistencia y calidad.
