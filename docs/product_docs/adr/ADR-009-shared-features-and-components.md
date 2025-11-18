# ADR-009: Patrón Arquitectónico para Componentes Transversales Compartidos

## Metadata

- **Status**: Accepted
- **Fecha**: 2025-11-18
- **Decisor(es)**: Juanje Márquez - 10Code
- **Tags**: arquitectura, ddd, modularidad, frontend, backend, patterns

---

## Contexto y Problema

En una arquitectura monolítica modular siguiendo principios de Domain-Driven Design (DDD), cada app Django debe ser un **bounded context autocontenido** con bajo acoplamiento y alta cohesión. Sin embargo, inevitablemente surgen funcionalidades **transversales** que necesitan ser utilizadas por múltiples módulos:

**Casos de uso identificados:**

1. **Editor de documentos (Tiptap) + Generación PDF (WeasyPrint)**: Necesario en:
   - `commercial`: Ofertas comerciales
   - `projects`: Informes de proyecto
   - `hr`: Certificados laborales
   - `financial`: Facturas y reportes financieros

2. **Futuros componentes transversales** (anticipados):
   - Sistema de notificaciones (emails, Discord, push)
   - Gestión de archivos adjuntos (uploads a Drive/S3)
   - Sistema de comentarios/actividad (audit trail)
   - Búsqueda full-text (búsqueda unificada cross-módulos)

**Problema arquitectónico:**

¿Cómo estructuramos componentes transversales manteniendo los principios de:
- **Bajo acoplamiento**: Módulos no deben conocer implementación interna de otros
- **Alta cohesión**: Cada módulo mantiene su dominio claro y autocontenido
- **Reusabilidad**: Evitar duplicación de código (DRY)
- **Testabilidad**: Cada módulo debe ser testeable independientemente
- **Evolución independiente**: Cambios en componentes shared no deben romper consumidores

**Restricciones técnicas:**
- Arquitectura: Monolito Modular Majestuoso (Django 5)
- Patrón de comunicación: Service Layer (80% comunicación entre módulos)
- Frontend: React 19 + Next.js + Inertia.js
- Team size: 1 desarrollador + agentes IA

---

## Factores de Decisión

1. **Cumplimiento DDD**: Mantener bounded contexts claros sin violaciones
2. **Bajo acoplamiento**: Módulos solo conocen interfaces públicas, no implementación
3. **Reusabilidad**: Código compartido sin duplicación innecesaria
4. **Testabilidad**: Facilidad para mockear dependencias en tests unitarios
5. **Developer Experience**: Claridad sobre dónde colocar código nuevo
6. **Mantenibilidad**: Facilidad para evolucionar componentes shared sin breaking changes
7. **Escalabilidad futura**: Preparado para extraer a microservicios si necesario
8. **Coherencia con stack**: Alineado con Django + React + Service Layer pattern

---

## Opciones Consideradas

### Opción 1: Shared Frontend Components + Dedicated Backend App (Elegida)

**Descripción Arquitectónica:**

**Frontend Layer:**
- Componentes UI compartidos en `frontend/components/shared/`
- Componentes presentacionales puros (sin lógica de negocio)
- Importables desde cualquier módulo vía `@/components/shared/ComponentName`

**Backend Layer:**
- App Django dedicada como bounded context (ej: `apps/documents/`)
- Service Layer expone **API pública** (`services.py`) para otros módulos
- Models internos **privados** (no importables directamente)
- Comunicación obligatoria vía Service Layer (80% pattern)

**Pros:**

- ✅ **Cumplimiento DDD estricto**: Cada app Django es un bounded context claro
- ✅ **Bajo acoplamiento extremo**: Consumidores solo conocen interface pública de services
- ✅ **Evolución independiente**: Cambios internos no afectan consumidores si API se mantiene
- ✅ **Testabilidad óptima**: Fácil mockear `DocumentService.create_document()` en tests
- ✅ **Separación Frontend/Backend clara**: Presentación (React) vs Lógica (Django)
- ✅ **Reusabilidad máxima**: Un componente/servicio, N consumidores
- ✅ **Escalabilidad futura**: `apps/documents/` puede extraerse como microservicio sin refactor masivo
- ✅ **Trazabilidad clara**: Metadata en documentos indica módulo de origen
- ✅ **Coherente con Service Layer**: 80% comunicación via services ya establecido

**Cons:**

- ❌ **Indirección adicional**: Llamadas `ModuleService → DocumentService` en lugar de acceso directo
- ❌ **Boilerplate inicial**: Crear service methods públicos requiere más código upfront
- ❌ **Curva de aprendizaje**: Developers deben entender dónde va cada tipo de código

**Implementación Estimada:** Patrón ya establecido, 0 overhead adicional

---

### Opción 2: Shared Django App (`apps/core/` o `apps/shared/`)

**Descripción:**
- Todo código compartido (models, services, utils) en app `apps/core/` o `apps/shared/`
- Otros módulos importan directamente desde core

```python
# Cualquier módulo puede hacer:
from apps.core.services import DocumentService
from apps.core.models import Document  # ❌ Problema
```

**Pros:**

- ✅ Simplicidad aparente: "Todo shared va en core"
- ✅ Menos apps Django (menos carpetas)

**Cons:**

- ❌ **Violación DDD**: `core` se convierte en "god app" sin dominio claro
- ❌ **Alto acoplamiento**: Módulos conocen models de core directamente
- ❌ **Testing difícil**: Difícil aislar tests cuando imports directos a models
- ❌ **Dios del código (God Object)**: `apps/core/` crece sin límite, todo "compartido" termina ahí
- ❌ **Dependencias circulares**: Core necesita de otros módulos y viceversa
- ❌ **Migración PostgreSQL compartida**: Cambios en core.models afectan toda la base de datos

**Razón de descarte:** Antipatrón conocido que lleva a monolitos acoplados y difíciles de mantener. Django documentation explícitamente advierte contra apps "core" monolíticas.

---

### Opción 3: Utilidades en `apps/core/utils/` + Apps Dedicadas

**Descripción:**
- Utilidades puras (helpers, decorators) en `apps/core/utils/`
- Lógica de negocio transversal en apps dedicadas (ej: `apps/documents/`)

```python
# Utils en core
from apps.core.utils import format_currency, slugify

# Lógica de negocio en app dedicada
from apps.documents.services import DocumentService
```

**Pros:**

- ✅ Separación clara: Utils (sin estado) vs Lógica de negocio (con estado)
- ✅ DDD compliance: Apps dedicadas mantienen bounded contexts
- ✅ Bajo acoplamiento para lógica de negocio

**Cons:**

- ❌ **Confusión sobre límites**: ¿Qué va en utils vs app dedicada?
- ❌ **Tentación de abuse**: Developers tienden a meter lógica de negocio en utils
- ❌ **Dos patrones simultáneos**: Inconsistencia (utils vs services)

**Razón de descarte:** Aunque mejor que Opción 2, introduce inconsistencia. Mejor tener una regla clara: apps dedicadas siempre, utils solo para helpers puros sin estado.

---

### Opción 4: Duplicación por Módulo (No Shared)

**Descripción:**
- Cada módulo implementa su propia versión de funcionalidad compartida
- Ej: `apps/commercial/pdf.py`, `apps/projects/pdf.py` (código duplicado)

```python
# Cada módulo tiene su propia implementación
# apps/commercial/pdf_generator.py
def generate_offer_pdf(...): pass

# apps/projects/pdf_generator.py  
def generate_report_pdf(...): pass  # Código duplicado!
```

**Pros:**

- ✅ **Autonomía total**: Cada módulo completamente independiente
- ✅ **No acoplamiento**: Cero dependencias entre módulos
- ✅ **Evolución independiente extrema**: Cambios no afectan a nadie

**Cons:**

- ❌ **Violación DRY masiva**: Código duplicado 3-5 veces
- ❌ **Bugs replicados**: Fix en un módulo no se propaga a otros
- ❌ **Mantenimiento pesadilla**: Actualizar WeasyPrint requiere cambios en 5 lugares
- ❌ **Inconsistencia inevitable**: Implementaciones divergen con el tiempo
- ❌ **Waste de desarrollo**: Implementar misma feature múltiples veces

**Razón de descarte:** Antipatrón clásico. DRY es un principio fundamental por buenas razones.

---

### Opción 5: Mixins Django

**Descripción:**
- Compartir funcionalidad via mixins en models/views

```python
# apps/core/mixins.py
class DocumentableMixin(models.Model):
    document = models.ForeignKey(Document, ...)
    
    class Meta:
        abstract = True

# apps/commercial/models.py
class Offer(DocumentableMixin):
    pass  # Hereda document field
```

**Pros:**

- ✅ Patrón Django estándar para compartir fields/methods
- ✅ Reusabilidad via herencia

**Cons:**

- ❌ **Solo para models/views**: No aplica a lógica de negocio compleja
- ❌ **Herencia vs composición**: Composición preferible para lógica de negocio (SOLID)
- ❌ **Acoplamiento de esquema**: Cambios en mixin afectan migrations múltiples
- ❌ **No resuelve services**: Mixins no ayudan con DocumentService

**Razón de descarte:** Útil para casos específicos (fields compartidos), pero no soluciona el problema arquitectónico principal de lógica de negocio transversal.

---

## Decisión

**Opción elegida**: **Shared Frontend Components + Dedicated Backend App**

### Justificación Detallada

Hemos decidido adoptar el patrón **"Componentes Compartidos Frontend + Apps Backend Dedicadas con Service Layer"** por las siguientes razones arquitectónicas fundamentadas:

#### 1. Coherencia con Arquitectura Monolítica Modular

**Principio del proyecto:**
> "Monolito físico, microservicios lógicos" - Cada app Django es un bounded context en DDD

**Esta decisión refuerza:**
- Cada app Django tiene su dominio claro (ej: `documents` = gestión de documentos)
- Comunicación entre apps **obligatoria** vía Service Layer (80% pattern ya establecido)
- Preparado para extraer apps como microservicios sin refactor masivo

**vs Opción 2 (shared app):** Que crea "god app" sin dominio específico, violando DDD.

#### 2. Bajo Acoplamiento mediante Interfaces Públicas

**Patrón implementado:**

```python
# ✅ PERMITIDO: Importar API pública
from apps.documents.services import DocumentService

# ❌ PROHIBIDO: Importar implementación interna
from apps.documents.models import Document
from apps.documents.tasks import generate_pdf_task
```

**Beneficios:**
- Consumidores no conocen implementación interna de `documents`
- Cambios en models/tasks no afectan a otros módulos
- Contract claro: si interface de `DocumentService` no cambia, consumidores no se rompen

**vs Opción 2:** Que permite imports directos a models, creando alto acoplamiento.

#### 3. Testabilidad Óptima con Mocking

**Tests unitarios con mocking:**

```python
# apps/commercial/tests/test_services.py
@pytest.mark.django_db
def test_create_offer(mocker):
    # Mock del servicio externo
    mock_create_doc = mocker.patch(
        'apps.documents.services.DocumentService.create_document',
        return_value=DocumentFactory()
    )
    
    offer = OfferService.create_offer(
        client=ClientFactory(),
        project_name="Test Project",
        created_by=UserFactory()
    )
    
    # Verificar llamada correcta sin dependencia real de documents app
    mock_create_doc.assert_called_once()
    assert offer.document is not None
```

**Ventaja:** Test de `commercial` no necesita DB de `documents`, se ejecuta aislado.

**vs Opción 4 (duplicación):** Que elimina necesidad de mocking pero introduce código duplicado.

#### 4. Reusabilidad Frontend Sin Duplicación

**Estructura de componentes:**

```typescript
// frontend/components/shared/TiptapEditor.tsx
export default function TiptapEditor({ onChange, ... }) {
  // Componente presentacional puro
}

// Uso desde Commercial
import TiptapEditor from '@/components/shared/TiptapEditor'
<TiptapEditor onChange={saveOfferDraft} />

// Uso desde Projects  
import TiptapEditor from '@/components/shared/TiptapEditor'
<TiptapEditor onChange={saveReportDraft} />

// Uso desde HR
import TiptapEditor from '@/components/shared/TiptapEditor'
<TiptapEditor onChange={saveCertificate} />
```

**Ventajas:**
- **Un componente, N consumidores**: Zero duplicación
- **Presentacional puro**: Sin lógica de negocio, solo UI
- **Fácil testeo**: Tests de componente independientes de módulos consumidores
- **Theming consistente**: Cambios visuales se propagan automáticamente

**vs Opción 4:** Que requeriría 3 implementaciones de TiptapEditor.

#### 5. Evolución Independiente con Versionado de API

**Ejemplo de evolución sin breaking changes:**

```python
# Versión 1.0 - DocumentService
def create_document(*, title, template_slug, markdown_content, created_by):
    pass

# Versión 1.1 - Añadir parámetro opcional (no breaking)
def create_document(
    *, 
    title, 
    template_slug, 
    markdown_content, 
    created_by,
    metadata: Optional[Dict] = None  # ✅ Nuevo parámetro opcional
):
    pass

# Módulos consumidores NO necesitan cambios
# Siguen funcionando con llamada antigua
```

**Estrategia de breaking changes:**

```python
# Si cambio es breaking:
# 1. Deprecar método antiguo
@deprecated(reason="Use create_document_v2", version="2.0")
def create_document(...): pass

# 2. Crear método nuevo
def create_document_v2(...): pass

# 3. Migrar consumidores gradualmente
# 4. Eliminar método deprecado en versión mayor
```

**vs Opción 2:** Donde cambios en models son siempre breaking (requieren migrations).

#### 6. Trazabilidad Cross-Módulo con Metadata

**Pattern de metadata:**

```python
# Desde commercial
document = DocumentService.create_document(
    title="Oferta ACME",
    template_slug='commercial-offer',
    markdown_content=content,
    metadata={
        'module': 'commercial',  # ⭐ Origen
        'offer_id': str(offer.id),
        'client_id': str(client.id),
    },
    created_by=user
)

# Desde projects
document = DocumentService.create_document(
    title="Informe Proyecto X",
    template_slug='project-report',
    markdown_content=content,
    metadata={
        'module': 'projects',  # ⭐ Origen
        'project_id': str(project.id),
    },
    created_by=user
)
```

**Beneficios:**
- Auditoría completa: sabemos qué módulo creó cada documento
- Queries específicas: filtrar documentos por módulo
- Analytics: métricas de uso por módulo
- Debugging: trazabilidad de origen

#### 7. Preparación para Microservicios Futuro

**Si escalamos a SaaS y necesitamos microservicios:**

```
Monolito actual:
┌─────────────────────────┐
│   Django Monolith       │
│  ┌─────────────────┐    │
│  │ apps/documents/ │    │ ← Bounded context bien definido
│  └─────────────────┘    │
│  ┌─────────────────┐    │
│  │ apps/commercial/│    │ ← Comunica vía DocumentService
│  └─────────────────┘    │
└─────────────────────────┘

Extracción a microservicio:
┌─────────────────────────┐
│  Documents Service      │ ← apps/documents/ extraído
│  (Django standalone)    │
└─────────┬───────────────┘
          │ REST API
          ↓
┌─────────────────────────┐
│   Commercial Service    │ ← Llama vía HTTP en lugar de import
│  (Django standalone)    │
└─────────────────────────┘
```

**Refactor mínimo:**

```python
# Antes (monolito)
from apps.documents.services import DocumentService
document = DocumentService.create_document(...)

# Después (microservicio)
import requests
response = requests.post('http://documents-service/api/documents/', data=...)
document = response.json()
```

Solo cambio en implementación de `DocumentService`, interface se mantiene.

**vs Opción 2/4:** Que requieren refactor masivo para extraer funcionalidad.

#### 8. Developer Experience y Claridad

**Reglas claras para developers y agentes IA:**

| Pregunta | Respuesta Clara |
|----------|----------------|
| ¿Dónde va componente React compartido? | `frontend/components/shared/` |
| ¿Dónde va lógica de negocio transversal? | App dedicada (ej: `apps/documents/`) |
| ¿Cómo consumo funcionalidad transversal? | Vía Service Layer (`DocumentService`) |
| ¿Puedo importar models de otros módulos? | ❌ NO - solo services públicos |
| ¿Cómo testeo mi módulo? | Mock de services externos |

**vs Opción 3:** Que tiene dos patrones (utils vs services), confusión.

---

## Consecuencias

### Positivas

- ✅ **DDD compliance perfecto**: Bounded contexts claros, bajo acoplamiento, alta cohesión
- ✅ **Service Layer reforzado**: 80% comunicación via services ahora incluye componentes shared
- ✅ **Testing independiente**: Cada módulo testeable sin dependencias reales de otros
- ✅ **Reusabilidad máxima**: Frontend shared components + Backend service API
- ✅ **Evolución sin breaking changes**: Interface stability permite cambios internos seguros
- ✅ **Preparado para microservicios**: Extracción futura con refactor mínimo
- ✅ **Trazabilidad completa**: Metadata indica origen de cada documento cross-módulo
- ✅ **Mantenibilidad superior**: Un lugar para cada tipo de código, sin ambigüedad
- ✅ **Developer Experience**: Reglas claras, fácil onboarding para nuevos developers/agentes
- ✅ **Consistencia arquitectónica**: Todos los módulos siguen mismo patrón

### Negativas

- ❌ **Indirección adicional**: Llamadas `ModuleService → SharedService` en lugar de acceso directo
- ❌ **Boilerplate inicial**: Crear services públicos requiere más código upfront vs imports directos
- ❌ **Curva de aprendizaje**: Developers deben entender patrón Service Layer y dónde va cada código
- ❌ **Overhead en tests**: Necesidad de crear mocks para services en tests unitarios
- ❌ **Más archivos**: Apps dedicadas añaden carpetas al proyecto vs un solo `apps/core/`

### Neutras

- ⚠️ **Necesidad de documentación clara**: Mantener reglas de imports en `.rules/ARCHITECTURE_RULES.md`
- ⚠️ **Enforcement via linting**: Considerar pre-commit hooks para validar imports prohibidos
- ⚠️ **Code review crítico**: Verificar que nuevos PRs siguen patrón establecido
- ⚠️ **Migración de código legacy**: Si hay código existente en `core/`, migrar a apps dedicadas
- ⚠️ **Monitorear performance**: Service Layer indirection añade microsegundos (negligible pero medible)

---

## Notas de Implementación

### Estructura de Directorios

```bash
10code-intranet/
├── apps/
│   ├── core/                      # Solo infraestructura técnica
│   │   ├── models.py              # Abstract base models
│   │   ├── middleware.py          # Django middleware
│   │   └── management/            # Django commands
│   │
│   ├── documents/                 # ✅ App dedicada transversal
│   │   ├── models.py              # Document, DocumentTemplate
│   │   ├── services.py            # ⭐ API PÚBLICA
│   │   ├── selectors.py           # Queries optimizadas
│   │   ├── tasks.py               # Celery tasks (privado)
│   │   └── templates/pdf/         # Templates PDF
│   │
│   ├── commercial/                # Módulo de dominio
│   │   ├── models.py              # Offer, Client
│   │   ├── services.py            # OfferService
│   │   └── views.py               # Inertia views
│   │
│   └── projects/                  # Módulo de dominio
│       ├── models.py              # Project, Task
│       ├── services.py            # ProjectService
│       └── views.py               # Inertia views
│
└── frontend/
    ├── components/
    │   ├── shared/                # ✅ Componentes compartidos
    │   │   ├── TiptapEditor.tsx
    │   │   ├── DocumentPreview.tsx
    │   │   └── TemplateSelector.tsx
    │   │
    │   ├── Commercial/            # Componentes específicos
    │   │   └── OfferForm.tsx      # Importa desde shared/
    │   │
    │   └── Projects/              # Componentes específicos
    │       └── ReportForm.tsx     # Importa desde shared/
    │
    └── lib/
        └── tiptap-config.ts       # Config compartida
```

### Template de Service Público (Backend)

```python
# apps/documents/services.py
from django.db import transaction
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class DocumentService:
    """
    API pública para gestión de documentos transversal.
    
    Esta es la ÚNICA interfaz que otros módulos deben usar.
    
    ❌ PROHIBIDO desde otros módulos:
        from apps.documents.models import Document
        from apps.documents.tasks import generate_pdf_task
    
    ✅ PERMITIDO desde otros módulos:
        from apps.documents.services import DocumentService
    """
    
    @staticmethod
    @transaction.atomic
    def create_document(
        *,
        title: str,
        template_slug: str,
        markdown_content: str,
        metadata: Dict[str, Any],
        created_by,
    ):
        """
        Crear documento desde cualquier módulo.
        
        Args:
            title: Título del documento
            template_slug: Slug de plantilla
            markdown_content: Contenido markdown
            metadata: Dict con module, entity_id, etc
            created_by: Usuario creador
            
        Returns:
            Document instance
            
        Example:
            document = DocumentService.create_document(
                title="Oferta ACME Corp",
                template_slug='commercial-offer',
                markdown_content=offer_markdown,
                metadata={
                    'module': 'commercial',
                    'offer_id': str(offer.id),
                },
                created_by=request.user
            )
        """
        from .models import DocumentTemplate, Document
        
        template = DocumentTemplate.objects.get(
            slug=template_slug,
            is_active=True
        )
        
        document = Document.objects.create(
            title=title,
            template=template,
            markdown_content=markdown_content,
            metadata=metadata,
            created_by=created_by
        )
        
        logger.info(
            f"Document created: {document.id} "
            f"by module={metadata.get('module')} "
            f"user={created_by.id}"
        )
        
        return document
    
    @staticmethod
    def generate_pdf_async(document_id: str) -> str:
        """
        Encolar generación de PDF.
        
        Returns:
            Celery task ID
        """
        from .tasks import generate_pdf_task
        
        task = generate_pdf_task.delay(document_id)
        logger.info(f"PDF generation queued: document={document_id} task={task.id}")
        return task.id
```

### Template de Consumo desde Otro Módulo

```python
# apps/commercial/services.py
from django.db import transaction
from apps.documents.services import DocumentService  # ✅ Solo service
import logging

logger = logging.getLogger(__name__)


class OfferService:
    """Servicio de negocio para ofertas comerciales."""
    
    @staticmethod
    @transaction.atomic
    def create_offer(
        *,
        client,
        project_name: str,
        estimated_hours: int,
        created_by,
        **kwargs
    ):
        # 1. Crear entidad de dominio (commercial)
        offer = Offer.objects.create(
            client=client,
            project_name=project_name,
            estimated_hours=estimated_hours,
            created_by=created_by,
            **kwargs
        )
        
        # 2. Generar markdown de oferta
        offer_markdown = OfferService._generate_offer_markdown(offer)
        
        # 3. Crear documento vía DocumentService ⭐
        document = DocumentService.create_document(
            title=f"Oferta {client.name} - {project_name}",
            template_slug='commercial-offer',
            markdown_content=offer_markdown,
            metadata={
                'module': 'commercial',      # ⭐ Origen
                'offer_id': str(offer.id),
                'client_id': str(client.id),
                'client_name': client.name,
            },
            created_by=created_by
        )
        
        # 4. Vincular documento a oferta
        offer.document = document
        offer.save()
        
        # 5. Generar PDF asíncrono
        task_id = DocumentService.generate_pdf_async(str(document.id))
        
        logger.info(
            f"Offer created: {offer.id} "
            f"with document={document.id} "
            f"pdf_task={task_id}"
        )
        
        return offer
    
    @staticmethod
    def _generate_offer_markdown(offer) -> str:
        """Generar markdown de oferta (lógica privada de commercial)."""
        return f"""
# Oferta Comercial: {offer.project_name}

**Cliente:** {offer.client.name}
**Fecha:** {offer.created_at.strftime('%Y-%m-%d')}

## Alcance
{offer.scope}

## Estimación
- Horas: {offer.estimated_hours}h
- Tarifa: €{offer.hourly_rate}/h
- **Total:** €{offer.total_price}
        """
```

### Template de Componente Compartido (Frontend)

```typescript
// frontend/components/shared/TiptapEditor.tsx
import { useEditor, EditorContent } from '@tiptap/react'
import StarterKit from '@tiptap/starter-kit'
import { Markdown } from 'tiptap-markdown'
import Table from '@tiptap/extension-table'
import { useCallback } from 'react'
import debounce from 'lodash/debounce'

interface TiptapEditorProps {
  initialContent?: string
  onChange: (markdown: string) => void
  placeholder?: string
  editable?: boolean
  className?: string
}

/**
 * Editor Tiptap compartido - componente presentacional puro.
 * 
 * ✅ Usado por: Commercial, Projects, HR, Financial
 * ❌ NO contiene lógica de negocio específica de módulos
 * 
 * @example
 * // En Commercial
 * <TiptapEditor onChange={saveOfferDraft} />
 * 
 * // En Projects
 * <TiptapEditor onChange={saveReportDraft} />
 */
export default function TiptapEditor({
  initialContent = '',
  onChange,
  placeholder = 'Empieza a escribir...',
  editable = true,
  className = ''
}: TiptapEditorProps) {
  
  const debouncedOnChange = useCallback(
    debounce((content: string) => onChange(content), 500),
    [onChange]
  )

  const editor = useEditor({
    extensions: [
      StarterKit,
      Markdown,
      Table.configure({ resizable: true }),
    ],
    content: initialContent,
    editable,
    onUpdate: ({ editor }) => {
      const markdown = editor.storage.markdown.getMarkdown()
      debouncedOnChange(markdown)
    },
    editorProps: {
      attributes: {
        class: 'prose prose-sm focus:outline-none min-h-[200px] p-4',
      },
    },
  })

  if (!editor) return null

  return (
    <div className={`border rounded-lg ${className}`}>
      {editable && (
        <div className="border-b p-2 flex gap-2 bg-gray-50">
          <button
            onClick={() => editor.chain().focus().toggleBold().run()}
            className={`px-2 py-1 rounded ${editor.isActive('bold') ? 'bg-gray-200' : ''}`}
          >
            Bold
          </button>
          <button
            onClick={() => editor.chain().focus().toggleItalic().run()}
            className={`px-2 py-1 rounded ${editor.isActive('italic') ? 'bg-gray-200' : ''}`}
          >
            Italic
          </button>
          <button
            onClick={() => editor.chain().focus().toggleHeading({ level: 2 }).run()}
            className={`px-2 py-1 rounded ${editor.isActive('heading', { level: 2 }) ? 'bg-gray-200' : ''}`}
          >
            H2
          </button>
        </div>
      )}
      
      <EditorContent editor={editor} />
    </div>
  )
}
```

### Testing con Mocking

```python
# apps/commercial/tests/test_services.py
import pytest
from apps.commercial.services import OfferService
from apps.commercial.tests.factories import ClientFactory, UserFactory

@pytest.mark.django_db
class TestOfferService:
    
    def test_create_offer_with_document(self, mocker):
        """Test que oferta se crea con documento sin dependencia real de documents app."""
        
        # Arrange: Mock del servicio externo
        mock_document = mocker.MagicMock(id='doc-123')
        mock_create_doc = mocker.patch(
            'apps.documents.services.DocumentService.create_document',
            return_value=mock_document
        )
        mock_generate_pdf = mocker.patch(
            'apps.documents.services.DocumentService.generate_pdf_async',
            return_value='task-456'
        )
        
        client = ClientFactory()
        user = UserFactory()
        
        # Act: Crear oferta
        offer = OfferService.create_offer(
            client=client,
            project_name="Test Project",
            estimated_hours=100,
            created_by=user
        )
        
        # Assert: Verificar llamadas correctas
        assert offer.document == mock_document
        
        mock_create_doc.assert_called_once_with(
            title=f"Oferta {client.name} - Test Project",
            template_slug='commercial-offer',
            markdown_content=mocker.ANY,  # Verificar que se pasó markdown
            metadata={
                'module': 'commercial',
                'offer_id': str(offer.id),
                'client_id': str(client.id),
                'client_name': client.name,
            },
            created_by=user
        )
        
        mock_generate_pdf.assert_called_once_with('doc-123')
```

### Reglas de Enforcement (Linting)

```python
# .rules/ARCHITECTURE_RULES.md
# Añadir sección:

## Componentes Transversales: Imports Permitidos

### ✅ PERMITIDO

```python
# Importar API pública de services
from apps.documents.services import DocumentService
from apps.documents.selectors import get_templates_list

# Importar componentes shared en frontend
import TiptapEditor from '@/components/shared/TiptapEditor'
```

### ❌ PROHIBIDO

```python
# NO importar models/tasks directamente
from apps.documents.models import Document  # ❌
from apps.documents.tasks import generate_pdf_task  # ❌

# NO duplicar componentes shared
# frontend/components/Commercial/TiptapEditor.tsx  # ❌ Ya existe en shared/
```

### Enforcement

```bash
# Pre-commit hook para validar imports
# .pre-commit-config.yaml
- repo: local
  hooks:
    - id: check-forbidden-imports
      name: Check forbidden cross-module imports
      entry: python scripts/check_imports.py
      language: python
      files: apps/.+\.py$
```

```python
# scripts/check_imports.py
import re
import sys

FORBIDDEN_PATTERNS = [
    r'from apps\.\w+\.models import',  # ❌ Cross-module model imports
    r'from apps\.\w+\.tasks import',   # ❌ Cross-module task imports
]

def check_file(filepath):
    with open(filepath) as f:
        content = f.read()
        for pattern in FORBIDDEN_PATTERNS:
            if re.search(pattern, content):
                # Exception: imports within same app
                app_name = filepath.split('/')[1]
                if f'from apps.{app_name}.' in content:
                    continue
                print(f"❌ Forbidden import in {filepath}: {pattern}")
                return False
    return True

# Uso en pre-commit
```

---

## Referencias

### Documentación Arquitectónica Interna

- **SAD Intranet 10Code**: `docs/product_docs/SAD_Intranet_10Code.md` - Sección 5.2 Service Layer Pattern
- **Architecture Rules**: `.rules/ARCHITECTURE_RULES.md` - Comunicación entre módulos
- **Django Patterns**: `.rules/DJANGO_PATTERNS.md` - Fat Services, Thin Models
- **ADR-008**: Service Layer Pattern - Decisión sobre 80% comunicación via services
- **ADR-005**: Tiptap + WeasyPrint - Decisión sobre stack de documentos

### Documentación Externa

- **Domain-Driven Design (Eric Evans)**: Blue Book - Bounded Contexts
- **Django Documentation**: https://docs.djangoproject.com/en/5.0/intro/reusable-apps/
- **Martin Fowler - Service Layer**: https://martinfowler.com/eaaCatalog/serviceLayer.html
- **Clean Architecture (Robert C. Martin)**: Dependency Inversion Principle
- **Django Anti-Patterns**: https://docs.quantifiedcode.com/python-anti-patterns/django/

### Artículos y Recursos

- **Packaging Django Apps**: https://docs.djangoproject.com/en/5.0/intro/reusable-apps/
- **Bounded Context Pattern**: https://martinfowler.com/bliki/BoundedContext.html
- **Service Layer in Django**: https://www.hacksoft.io/blog/service-layer-in-django
- **Testing with Mocks**: https://docs.python.org/3/library/unittest.mock.html

---

## Historial

| Fecha | Evento | Autor |
|-------|--------|-------|
| 2025-11-18 | ADR creado tras análisis arquitectónico de componentes transversales | Juanje Márquez |
| 2025-11-18 | Decisión aceptada y comunicada a equipo de desarrollo | Juanje Márquez |

---

**Firmado por:**

- **Juanje Márquez** - Arquitecto Principal & Tech Lead - 2025-11-18

---

> **Nota Crítica para Agentes IA de Codificación:**
>
> Este ADR define el **patrón arquitectónico fundamental** para componentes transversales.
>
> **REGLAS OBLIGATORIAS:**
>
> ✅ **HACER:**
> - Componentes React compartidos en `frontend/components/shared/`
> - Apps Django dedicadas para lógica transversal (ej: `apps/documents/`)
> - Comunicación entre módulos SOLO vía Service Layer
> - Importar solo API pública: `from apps.documents.services import DocumentService`
> - Metadata con `module` para trazabilidad
> - Tests con mocking de services externos
>
> ❌ **NO HACER:**
> - Importar models de otros módulos: `from apps.X.models import Y`
> - Importar tasks de otros módulos: `from apps.X.tasks import Y`
> - Crear app `apps/core/` o `apps/shared/` con lógica de negocio
> - Duplicar componentes shared en múltiples carpetas
> - Acceso directo a DB de otros módulos
>
> **Si necesitas crear funcionalidad transversal nueva:**
> 1. Pregúntate: ¿Es presentación (UI) o lógica de negocio?
> 2. Presentación → `frontend/components/shared/`
> 3. Lógica negocio → App Django dedicada con Service Layer
>
> **Si este patrón no aplica a tu caso:** Documentar justificación y crear nuevo ADR.
