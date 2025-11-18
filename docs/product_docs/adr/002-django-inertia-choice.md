# ADR-002: Django + Inertia.js como Stack Principal

## Metadata

- **Status**: Accepted
- **Fecha**: 2025-11-18
- **Decisor(es)**: Juanje Márquez (Lead Developer, 10Code)
- **Tags**: arquitectura, backend, frontend, full-stack, spa

---

## Contexto y Problema

Necesitamos decidir la arquitectura de comunicación entre backend (Django) y frontend (React) para la Intranet 10Code. Los requisitos clave son:

- **Frontend moderno con React 19+**: Componentes reutilizables, estado reactivo, ecosistema rico (shadcn/ui)
- **Desarrollo rápido para 1 desarrollador + agentes IA**: Sin duplicación de lógica entre backend y frontend
- **Navegación SPA sin recargas de página**: Experiencia fluida, transiciones instantáneas
- **SEO no es prioridad**: Sistema interno, no necesita indexación
- **Autenticación server-side con Google OAuth**: Sin gestión de tokens JWT en cliente
- **Validaciones y lógica de negocio centralizadas**: Todo en Django, no duplicar en React
- **Testing simplificado**: Una sola codebase para testear, no API + Frontend separados

El problema principal es: **¿Cómo obtener los beneficios de una SPA moderna sin la complejidad de mantener una API REST separada?**

---

## Factores de Decisión

1. **Velocidad de desarrollo**: Tiempo para entregar MVP con 1 desarrollador
2. **Complejidad arquitectónica**: Overhead de mantener múltiples codebases
3. **Developer Experience (DX)**: Facilidad para desarrollar y depurar
4. **Compatibilidad con shadcn/ui**: Necesitamos usar componentes React modernos
5. **Gestión de estado**: Cómo sincronizar datos entre servidor y cliente
6. **Autenticación**: Complejidad de manejar sesiones y permisos
7. **Testing**: Facilidad para escribir y mantener tests
8. **Performance**: Tiempo de carga inicial y navegación

---

## Opciones Consideradas

### Opción 1: Django REST Framework + React SPA Separada

**Descripción:** Backend Django expone API REST, frontend React consume API con fetch/axios.

**Pros:**

- ✅ Separación clara backend/frontend
- ✅ Frontend puede ser PWA o mobile app futura
- ✅ Estándar de industria, mucha documentación

**Cons:**

- ❌ **Duplicación masiva de lógica**: Validaciones en DRF serializers + React forms
- ❌ **Gestión de estado compleja**: Redux/Zustand + cache + sincronización
- ❌ **Autenticación JWT compleja**: Refresh tokens, interceptors, storage seguro
- ❌ **Testing duplicado**: Tests de API + tests de frontend
- ❌ **CORS y configuración adicional**: Más puntos de fallo
- ❌ **Desarrollo más lento**: 2x código para CRUD básico

---

### Opción 2: Django Templates Tradicionales + HTMX

**Descripción:** Server-side rendering puro con Django templates, interactividad con HTMX.

**Pros:**

- ✅ Simplicidad máxima, todo en Django
- ✅ SEO perfecto (no necesario para nosotros)
- ✅ Sin JavaScript build process

**Cons:**

- ❌ **NO podemos usar shadcn/ui**: Componentes React imposibles
- ❌ **UX inferior**: Recargas parciales, no es verdadera SPA
- ❌ **Limitaciones de interactividad**: Estados complejos difíciles
- ❌ **Ecosistema limitado**: Menos librerías UI disponibles

---

### Opción 3: Django + Inertia.js (ELEGIDA ✅)

**Descripción:** Django sirve datos como props JSON, Inertia.js los pasa a componentes React sin API REST.

**Pros:**

- ✅ **Desarrollo 3x más rápido**: Sin serializers DRF, sin gestión de estado compleja
- ✅ **shadcn/ui funciona perfectamente**: React completo disponible
- ✅ **Navegación SPA real**: Sin recargas de página, transiciones fluidas
- ✅ **Autenticación simple**: Sesiones Django, sin JWT
- ✅ **Testing unificado**: Solo testear Django views + components
- ✅ **Sin CORS**: Todo en mismo dominio
- ✅ **Validaciones centralizadas**: Solo en Django services
- ✅ **Routing de Django**: No necesitas React Router

**Cons:**

- ❌ No es API REST pura (no reutilizable para mobile)
- ❌ Menos documentación que arquitecturas tradicionales
- ❌ Vendor lock-in con Inertia.js (mitigable con migración gradual)

---

## Decisión

**Opción elegida**: **Opción 3 - Django + Inertia.js**

**Justificación:**

Hemos decidido usar **Django + Inertia.js** porque:

1. **Velocidad de desarrollo crítica**: Como desarrollador único, Inertia elimina ~40% del código (no API REST, no serializers, no gestión estado)

2. **shadcn/ui es requisito obligatorio**: Necesitamos componentes React modernos para UI profesional rápida

3. **Complejidad innecesaria de API REST**: Para sistema interno monousuario, mantener API REST separada es overhead sin beneficio

4. **Ejemplo real de código simplificado**:

```python
# CON INERTIA (5 líneas) ✅
@inertia('Projects/Index')
def projects_list(request):
    projects = Project.objects.select_related('client').all()
    return {'projects': projects.values(), 'user': request.user.id}

# VS API REST (25+ líneas) ❌
class ProjectSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)
    class Meta: ...

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        # Más lógica de permisos, filtros, paginación...
```

5. **Testing 50% más simple**: Un test Inertia vs test API + test React

6. **Migración futura viable**: Si necesitamos API REST después, podemos añadirla gradualmente sin reescribir

---

## Consecuencias

### Positivas

- ✅ **MVP 2-3 meses antes**: Estimamos 40% menos código total
- ✅ **Menos bugs**: Sin sincronización frontend/backend, sin edge cases de estado
- ✅ **Developer experience superior**: Hot reload, props typesafe con TypeScript
- ✅ **Permisos simplificados**: `can_edit` como prop, no lógica duplicada
- ✅ **Formularios más simples**: Validación solo server-side, errores automáticos

### Negativas

- ❌ **Sin mobile app nativa fácil**: Necesitaría API REST adicional (no prioridad ahora)
- ❌ **Dependencia de Inertia.js**: Si proyecto muere, migración necesaria (bajo riesgo, comunidad activa)
- ❌ **Curva aprendizaje inicial**: 1-2 semanas para dominar patrón Inertia

### Neutras

- ⚠️ **Monitorear adopción de Inertia**: Verificar que comunidad sigue activa
- ⚠️ **Documentar patrones internos**: Crear guías para futuros desarrolladores
- ⚠️ **Performance en datasets grandes**: Paginar agresivamente (igual que con API REST)

---

## Notas de Implementación

### Setup Inicial

```bash
# Backend
pip install django inertia-django

# Frontend
npm install @inertiajs/react @vitejs/plugin-react
```

### Configuración Django

```python
# settings.py
INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'inertia',  # Añadir inertia
    # ...
]

INERTIA_LAYOUT = 'base.html'  # Template base

# urls.py
from inertia import render as inertia_render

urlpatterns = [
    path('', views.index, name='home'),
    path('projects/', views.projects_list, name='projects.index'),
    # Las rutas siguen siendo Django, no React Router
]
```

### Patrón de Views con Inertia

```python
# views.py
from inertia import inertia
from apps.projects.services import ProjectService

@login_required
@inertia('Projects/Create')  # Componente React a renderizar
def projects_create(request):
    """Vista Inertia que renderiza componente React con props."""
    if request.method == 'POST':
        # Procesar con Django service layer
        project = ProjectService.create_project(
            **request.POST.dict(),
            created_by=request.user
        )
        return redirect('projects.show', project.id)
    
    # Props para componente React
    return {
        'clients': Client.objects.values('id', 'name'),
        'methodologies': Project.METHODOLOGY_CHOICES,
        'can_create': request.user.has_perm('projects.add_project'),
    }
```

### Componente React Recibiendo Props

```jsx
// resources/js/Pages/Projects/Create.jsx
import { useForm } from '@inertiajs/react'
import { Card } from '@/components/ui/card'
import { Button } from '@/components/ui/button'

export default function ProjectCreate({ clients, methodologies, can_create }) {
    const { data, setData, post, errors } = useForm({
        name: '',
        client_id: '',
        methodology: 'scrum',
    })
    
    const handleSubmit = (e) => {
        e.preventDefault()
        post('/projects/create/')  // POST a Django, no API REST
    }
    
    if (!can_create) {
        return <div>Sin permisos para crear proyectos</div>
    }
    
    return (
        <Card>
            <form onSubmit={handleSubmit}>
                {/* Formulario con shadcn/ui components */}
                {errors.name && <span>{errors.name}</span>}
                <Button type="submit">Crear Proyecto</Button>
            </form>
        </Card>
    )
}
```

### Estructura de Carpetas Recomendada

```markdown
10code-intranet/
├── apps/                    # Django apps
│   └── projects/
│       ├── views.py        # Views con @inertia decorator
│       └── services.py     # Lógica de negocio
├── resources/              # Frontend React
│   └── js/
│       ├── Pages/          # Componentes página (1:1 con Django views)
│       │   └── Projects/
│       │       ├── Index.jsx
│       │       └── Create.jsx
│       └── components/     # Componentes reutilizables
│           └── ui/        # shadcn/ui components
└── templates/
    └── base.html          # Template HTML base para Inertia
```

---

## Referencias

- [Inertia.js Documentation](https://inertiajs.com/)
- [django-inertia Package](https://github.com/inertiajs/inertia-django)
- [Comparativa Inertia vs API REST](https://reinink.ca/articles/introducing-inertia-js)
- [shadcn/ui con Inertia ejemplo](https://github.com/shadcn-ui/ui/discussions/1834)
- [Discusión Slack: #arquitectura (2025-11-10)](https://10code.slack.com/archives/...)

---

## Historial

| Fecha | Evento |
|-------|--------|
| 2025-11-18 | ADR creado y aceptado |
| TBD | Revisión post-MVP para validar decisión |

---

**Firmado por:**

- Juanje Márquez - Lead Developer - 2025-11-18
