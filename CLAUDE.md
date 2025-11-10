# 10Code Intranet - Reglas de Desarrollo para Agentes IA
# Sistema de Gestión de Proyectos Integral
# Stack: Django 5 + Inertia.js + React + PostgreSQL + ML

## 🎯 FILOSOFÍA ARQUITECTÓNICA CENTRAL

### Monolito Modular Majestuoso
Este proyecto implementa un monolito modular donde:
- Una sola base de código con módulos claramente separados por dominio (DDD)
- Inertia.js como puente entre Django y React (SPA sin API REST tradicional)
- Cada módulo (app Django) es autocontenido y representa un dominio de negocio
- Evitamos microservicios prematuros en favor de velocidad de desarrollo

### Principios No Negociables
1. **Service Layer Pattern**: Toda lógica de negocio va en services.py, NO en views ni models
2. **Thin Views, Fat Services**: Views solo routing HTTP, Services orchestan lógica
3. **Domain-Driven Design**: Apps organizadas por dominio de negocio (projects, resources, timetracking, etc.)
4. **Separation of Concerns**: Backend (Django) y Frontend (React) físicamente separados
5. **Testing Obligatorio**: No merge sin tests (unit + integration + e2e cuando aplique)

## 📁 ESTRUCTURA DE PROYECTO MANDATORIA

```
10code-intranet/
├── apps/                    # Todas las apps Django
│   ├── core/               # Utilidades compartidas SOLO
│   ├── accounts/           # Usuarios, autenticación
│   ├── projects/           # Gestión de proyectos
│   ├── resources/          # Gestión de recursos
│   ├── financial/          # Seguimiento financiero
│   ├── timetracking/       # Control horario
│   ├── estimation/         # Sistema CEPF + ML
│   ├── backlog/            # Gestión de backlog
│   ├── reporting/          # Reporting y BI
│   └── integrations/       # Integraciones externas
├── config/                 # Configuración proyecto
│   └── settings/           # Split settings (base, dev, prod)
├── frontend/               # React + Inertia + Vite
│   └── src/
│       ├── components/     # Componentes UI
│       ├── pages/          # Páginas Inertia
│       └── lib/            # Utilidades
└── templates/              # Solo base.html para Inertia
```

## 🏗️ ESTRUCTURA INTERNA DE CADA APP

Cada app Django DEBE seguir esta estructura exacta:

```
apps/[nombre_app]/
├── models.py           # Solo estructura de datos + métodos simples
├── services.py         # ✅ WRITE operations - Lógica de negocio
├── selectors.py        # ✅ READ operations - Consultas optimizadas
├── views.py            # Solo routing y props para Inertia
├── urls.py             # URLs de la app
├── admin.py            # Admin de Django
├── managers.py         # Custom QuerySet managers
├── enums.py            # Enumerations (choices)
├── validators.py       # Validaciones custom
├── signals.py          # Señales (usar con MODERACIÓN)
├── tasks.py            # Celery tasks
└── tests/              # Tests completos
    ├── factories.py    # Factory Boy
    ├── test_models.py
    ├── test_services.py
    ├── test_selectors.py
    └── test_views.py
```

## 🚫 ANTI-PATRONES - NUNCA HACER

1. ❌ Lógica de negocio en views.py
2. ❌ Lógica de negocio compleja en models.py
3. ❌ QuerySets directamente en templates
4. ❌ Queries en loops (N+1 problem)
5. ❌ Hardcodear configuración
6. ❌ `.objects.all()` sin filtros ni paginación
7. ❌ Skip migrations
8. ❌ Deploy sin CI green
9. ❌ Secretos en código
10. ❌ Operaciones blocking en views
11. ❌ Copiar-pegar código
12. ❌ Importaciones directas de modelos entre apps (usar services)

## ✅ PATRONES OBLIGATORIOS

### Service Layer Pattern (CRÍTICO)
```python
# apps/projects/services.py
from django.db import transaction

class ProjectService:
    @staticmethod
    @transaction.atomic
    def create_project(*, name: str, client: str, created_by: User, **kwargs):
        """
        Crear proyecto con validaciones y side effects.
        Nota: Type hints obligatorios, keyword-only args (*)
        """
        # Validaciones de negocio
        if Project.objects.filter(name=name, client=client).exists():
            raise ValidationError("Proyecto ya existe")
        
        # Crear proyecto
        project = Project.objects.create(...)
        
        # Side effects (asignar creador, enviar notificaciones)
        ProjectMember.objects.create(...)
        send_notification_task.delay(project.id)
        
        return project
```

### Selectors Pattern (CRÍTICO)
```python
# apps/projects/selectors.py
def get_projects_list(*, user: User, filters: dict = None):
    """
    READ-only operations con optimizaciones.
    Siempre usar select_related/prefetch_related.
    """
    qs = Project.objects.select_related(
        'created_by', 'client'
    ).prefetch_related(
        Prefetch('members', queryset=ProjectMember.objects.select_related('user'))
    )
    
    # Aplicar permisos
    if not user.is_staff:
        qs = qs.filter(Q(created_by=user) | Q(members__user=user)).distinct()
    
    # Aplicar filtros
    if filters:
        if 'status' in filters:
            qs = qs.filter(status=filters['status'])
    
    return qs.order_by('-created_at')
```

### Views con Inertia (Thin Views)
```python
# apps/projects/views.py
from inertia import render
from .selectors import get_projects_list
from .services import ProjectService

@login_required
def projects_index(request):
    """View solo hace routing y prepara props."""
    projects = get_projects_list(user=request.user, filters=request.GET.dict())
    
    return render(request, 'Projects/Index', props={
        'projects': [serialize_project(p) for p in projects],
        'filters': request.GET.dict(),
        'permissions': {
            'can_create': request.user.has_perm('projects.add_project')
        }
    })

@login_required
def projects_store(request):
    """POST solo valida y delega a service."""
    if request.method == 'POST':
        data = request.POST.dict()
        project = ProjectService.create_project(data=data, created_by=request.user)
        return redirect(route('projects.show', args=[project.id]))
```

## 🔧 OPTIMIZACIÓN DE QUERIES (OBLIGATORIO)

### Siempre Usar select_related / prefetch_related
```python
# ❌ MAL - N+1 queries
projects = Project.objects.all()
for project in projects:
    print(project.created_by.email)  # Query por cada proyecto!

# ✅ BIEN - 1 query
projects = Project.objects.select_related('created_by')
for project in projects:
    print(project.created_by.email)  # Sin queries adicionales
```

### Prefetch para relaciones inversas y M2M
```python
# ✅ EXCELENTE
projects = Project.objects.select_related(
    'created_by'
).prefetch_related(
    Prefetch('members', queryset=ProjectMember.objects.select_related('user')),
    'tasks',
    'sprints'
)
```

## 🧪 TESTING (NO NEGOCIABLE)

### Pirámide de Tests
1. **Unit Tests**: Services, selectors, models, utils (70%)
2. **Integration Tests**: Views completas con DB (20%)
3. **E2E Tests**: Flujos críticos con Playwright (10%)

### Cobertura Mínima: 80%

### Ejemplo Test de Service
```python
# apps/projects/tests/test_services.py
import pytest
from apps.projects.services import ProjectService

@pytest.mark.django_db
class TestProjectService:
    def test_create_project_success(self, user_factory):
        user = user_factory()
        
        project = ProjectService.create_project(
            name="Test Project",
            client="Test Client",
            methodology="scrum",
            created_by=user
        )
        
        assert project.id is not None
        assert project.name == "Test Project"
        assert project.members.filter(user=user).exists()
```

## 🎨 FRONTEND CON INERTIA

### Componentes de Página React
```typescript
// frontend/src/pages/Projects/Index.tsx
import { Head, Link } from '@inertiajs/react'
import Layout from '@/components/layout/Layout'

interface Props {
  projects: Project[]
  permissions: { can_create: boolean }
}

export default function ProjectsIndex({ projects, permissions }: Props) {
  return (
    <Layout>
      <Head title="Proyectos" />
      
      <div className="container">
        <h1>Proyectos</h1>
        
        {permissions.can_create && (
          <Link href="/projects/create" className="btn-primary">
            Nuevo Proyecto
          </Link>
        )}
        
        {projects.map(project => (
          <ProjectCard key={project.id} project={project} />
        ))}
      </div>
    </Layout>
  )
}
```

### Formularios con Inertia
```typescript
import { useForm } from '@inertiajs/react'

export default function ProjectCreate() {
  const { data, setData, post, processing, errors } = useForm({
    name: '',
    client: '',
    methodology: 'scrum'
  })
  
  const handleSubmit = (e) => {
    e.preventDefault()
    post('/projects')
  }
  
  return (
    <form onSubmit={handleSubmit}>
      <input 
        value={data.name}
        onChange={e => setData('name', e.target.value)}
      />
      {errors.name && <span>{errors.name}</span>}
      
      <button type="submit" disabled={processing}>
        Crear Proyecto
      </button>
    </form>
  )
}
```

## 🔐 SEGURIDAD Y PERMISOS

### Permisos a Nivel de Objeto
```python
# Patrón "Props como Permisos"
def document_detail(request, pk):
    document = get_object_or_404(Document, pk=pk)
    
    permissions = {
        'can_edit': request.user == document.owner,
        'can_delete': request.user == document.owner,
        'can_share': request.user.is_staff,
    }
    
    return render(request, 'Documents/Show', props={
        'document': serialize_document(document),
        'permissions': permissions  # Para UI
    })
```

### Aplicación en Backend (Seguridad Real)
```python
def document_update(request, pk):
    document = get_object_or_404(Document, pk=pk)
    
    # ✅ Verificación OBLIGATORIA en backend
    if request.user != document.owner:
        raise PermissionDenied("No tienes permisos")
    
    # Procesar actualización...
```

## 🚀 COMANDOS FRECUENTES

### Desarrollo
```bash
# Iniciar proyecto
docker-compose up

# Crear migración
python manage.py makemigrations [app_name] --name descriptive_name

# Aplicar migraciones
python manage.py migrate

# Tests
pytest apps/[app_name]/tests/

# Cobertura
pytest --cov=apps --cov-report=html

# Linters
black apps/
flake8 apps/
isort apps/
```

### Frontend
```bash
cd frontend
npm run dev        # Desarrollo con HMR
npm run build      # Build producción
npm run type-check # Verificar TypeScript
```

## 📝 CONFIGURACIÓN DE ENTORNO

### Variables Obligatorias (.env)
```bash
# Django
DEBUG=True
SECRET_KEY=your-secret-key
DJANGO_SETTINGS_MODULE=config.settings.development

# Database
DB_NAME=10code_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

# Redis
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/1

# OAuth Google (solo @10code.es)
GOOGLE_CLIENT_ID=xxx
GOOGLE_CLIENT_SECRET=xxx
ALLOWED_EMAIL_DOMAIN=10code.es
```

## 🎯 REGLAS DE NEGOCIO ESPECÍFICAS DEL PROYECTO

### Control Horario (Normativa Española 2025)
- Fichaje digital obligatorio con trazabilidad completa
- Mínimo 6-7h imputación diaria según perfil
- SLA imputación: antes 10:00 día siguiente
- Autocierre automático + 30min gracia
- Generación automática de incidencias
- Cumplimiento RGPD, almacenamiento 4 años

### Gestión de Recursos
- No permitir asignaciones >100% sin autorización especial
- Pertenencia múltiple a equipos horizontales/verticales
- Validación automática de disponibilidad antes de asignar
- Carry-over vacaciones según normativa española

### Sistema CEPF + ML
- Componentes estándares con Puntos de Función
- Intervalos confianza 80%, 90%, 95%
- Aprendizaje continuo con datos históricos
- Democratización: comerciales pueden estimar sin dependencia técnica
- Detección automática de anomalías en estimaciones

## 🎨 EXPERIENCIA DE USUARIO

### Principios de Diseño
- **Mobile-first responsive design**
- **Drag & drop** para operaciones comunes
- **Navegación contextual** entre módulos
- **Accesos rápidos** basados en rol
- **Notificaciones inteligentes** sin saturar

### Performance
- Tiempos respuesta <300ms p95 vistas principales
- Separación ETL mediante jobs/queues
- Cache estratégico para dashboards
- Optimización consultas mandatory

## 📚 CUANDO GENERES CÓDIGO

### Siempre Incluir
1. Type hints en Python
2. Docstrings descriptivos
3. Tests correspondientes
4. Validaciones de negocio
5. Manejo de errores explícito
6. Logging apropiado
7. Transacciones atómicas cuando sea necesario

### Patrones de Naming
- Models: Singular, PascalCase (`Project`, `User`)
- Services: `[Noun]Service` (`ProjectService`)
- Selectors: `get_[resource]_[action]` (`get_projects_list`)
- Views: `[resource]_[action]` (`projects_index`, `projects_store`)
- URLs: kebab-case (`/projects/`, `/time-tracking/`)

### Documentación de Código
```python
def create_project(
    *,
    name: str,
    client: str,
    methodology: str,
    created_by: User,
    **kwargs
) -> Project:
    """
    Crear un nuevo proyecto con validaciones completas.
    
    Args:
        name: Nombre del proyecto
        client: Cliente asociado
        methodology: Metodología (scrum, kanban, waterfall, hybrid)
        created_by: Usuario que crea el proyecto
        **kwargs: Campos adicionales opcionales
    
    Returns:
        Proyecto creado con su creador asignado como PM
        
    Raises:
        ValidationError: Si el proyecto ya existe o datos inválidos
    """
```

## 🔄 GIT WORKFLOW

### Commits
- Mensajes descriptivos en español
- Formato: `[TIPO] Descripción breve`
- Tipos: `feat`, `fix`, `refactor`, `test`, `docs`, `style`, `perf`

### Branches
- `main` - Producción
- `develop` - Desarrollo
- `feature/[nombre]` - Nuevas features
- `fix/[nombre]` - Correcciones

### CI/CD
- Tests automáticos en cada push
- Linters y formatters obligatorios
- No merge sin CI green
- Deploy automático a staging desde develop
- Deploy manual a producción desde main

## 📖 RECURSOS Y REFERENCIAS

- Django 5 Docs: https://docs.djangoproject.com/en/5.0/
- Inertia.js: https://inertiajs.com/
- Two Scoops of Django: Mejores prácticas
- DDD: Domain-Driven Design patterns

---

**RECUERDA**: Estas reglas son OBLIGATORIAS y no opcionales. Garantizan consistencia, calidad y mantenibilidad del proyecto a largo plazo.
