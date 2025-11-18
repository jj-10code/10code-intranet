# ADR-005: Tiptap + WeasyPrint para Edición WYSIWYG y Generación de PDFs

## Metadata

- **Status**: Accepted
- **Fecha**: 2025-11-18
- **Decisor(es)**: Juanje Márquez - 10Code
- **Tags**: frontend, backend, documentos, pdf, arquitectura

---

## Contexto y Problema

El sistema Intranet 10Code requiere una funcionalidad transversal para crear, editar y exportar documentos profesionales (ofertas comerciales, contratos, informes de proyecto, certificados, facturas) con las siguientes necesidades:

**Requisitos Funcionales:**

- Editor WYSIWYG moderno para creación de contenido markdown
- Soporte de tablas, listas, headings, code blocks
- Sistema de plantillas configurables por tipo de documento (oferta, reporte, factura, certificado)
- Generación de PDFs profesionales con:
  - Portadas personalizadas con logo, título, cliente, fecha
  - Headers y footers con numeración de páginas
  - Estilos corporativos (colores, tipografías, tablas con diseño específico)
  - Soporte de fuentes custom
- Exportación a múltiples formatos (PDF primordial, markdown nativo)
- Versionado de documentos (futuro)
- Posible colaboración en tiempo real (v2.0)

**Requisitos No Funcionales:**

- Licencia open source gratuita (sin costes operativos recurrentes)
- Integración nativa con stack Django 5 + React/Next.js
- Performance: generación de PDF < 2 segundos para documentos típicos (5-10 páginas)
- Escalabilidad: soportar generación masiva mediante Celery
- Mantenibilidad: stack activamente mantenido, sin dependencias obsoletas
- Developer Experience: fácil de integrar y extender

**Restricciones Técnicas:**

- Backend: Django 5 (Python 3.14+)
- Frontend: React 19 + Next.js + TypeScript
- Deployment: Docker en VPS (OVH)
- Equipo: 1 desarrollador principal + agentes IA de codificación

---

## Factores de Decisión

Los criterios clave para evaluar las opciones son:

1. **Mantenimiento activo**: Proyecto con commits recientes, comunidad activa, roadmap claro
2. **Integración con stack**: Compatibilidad nativa con Django + React/Next.js sin fricciones
3. **Calidad de PDFs generados**: Soporte CSS completo, headers/footers, fuentes custom, control tipográfico
4. **Performance**: Velocidad de generación de PDFs, consumo de memoria, escalabilidad
5. **Flexibilidad de plantillas**: Facilidad para crear y customizar múltiples plantillas de documentos
6. **Licencia y costes**: Open source sin costes ocultos, sin vendor lock-in
7. **Curva de aprendizaje**: Facilidad de integración para desarrollador + agentes IA
8. **Ecosistema**: Disponibilidad de extensiones, plugins, documentación, ejemplos

---

## Opciones Consideradas

### Opción 1: Tiptap (Editor) + WeasyPrint (PDF)

**Descripción Técnica:**

- **Tiptap**: Editor headless basado en ProseMirror, arquitectura extensible con sistema de extensiones modular
- **WeasyPrint**: Motor de renderizado HTML/CSS a PDF escrito en Python, compatible con CSS Paged Media Level 3

**Pros:**

- ✅ **Mantenimiento activo**: Tiptap tiene releases frecuentes, comunidad creciente (25k+ stars GitHub), WeasyPrint activamente mantenido (8k+ stars)
- ✅ **Arquitectura moderna**: Tiptap headless permite control total de UI, WeasyPrint motor Python puro (sin Node.js)
- ✅ **Integración perfecta**: Tiptap diseñado para React, WeasyPrint nativo en Django
- ✅ **Performance superior**: WeasyPrint 3x más rápido que navegadores headless (1-2s vs 3-5s), 50-100MB RAM vs 200-400MB
- ✅ **Calidad PDF profesional**: CSS Paged Media completo (@page, headers, footers, page breaks, custom fonts)
- ✅ **Licencias open source**: Tiptap MIT, WeasyPrint BSD - ambos gratuitos, sin restricciones
- ✅ **Extensibilidad**: Tiptap 100+ extensiones oficiales, custom extensions fáciles; WeasyPrint permite hooks Python
- ✅ **Stack unificado**: Sin necesidad de microservicio Node.js separado
- ✅ **Markdown nativo**: Tiptap exporta/importa markdown limpio, ideal para versionado Git
- ✅ **Futuro-proof**: Tiptap recién liberó extensiones Pro como open source (junio 2025), compromiso con comunidad

**Cons:**

- ❌ **Colaboración real-time no nativa**: Requiere extensión custom con Yjs + WebSockets (implementable pero complejo)
- ❌ **WeasyPrint limitaciones CSS**: No soporta CSS Grid avanzado, algunas features CSS modernas ausentes
- ❌ **Curva de aprendizaje inicial**: ProseMirror concepts requieren familiarización (nodes, marks, commands)

**Implementación Estimada:** 2-3 semanas para MVP funcional

---

### Opción 2: TOAST UI Editor + WeasyPrint

**Descripción Técnica:**

- **TOAST UI Editor**: Editor WYSIWYG basado en CodeMirror, incluye modo markdown y modo WYSIWYG switchable
- **WeasyPrint**: Mismo que Opción 1

**Pros:**

- ✅ **Editor todo-en-uno**: UI pre-construida, plugins built-in (chart, UML, syntax highlighting)
- ✅ **Dual mode**: Markdown raw + WYSIWYG switchable sin configuración
- ✅ **WeasyPrint ventajas**: Iguales que Opción 1
- ✅ **Licencia MIT**: Open source gratuito

**Cons:**

- ❌ **Proyecto estancado**: Último commit hace 2 años (febrero 2024), actividad reducida drásticamente
- ❌ **Repos deprecated**: Wrapper React movido a monorepo, señal de consolidación/abandono
- ❌ **Arquitectura antigua**: Basado en CodeMirror (vs ProseMirror moderno)
- ❌ **Menor control**: Editor monolítico, difícil customizar internals
- ❌ **Bundle size**: ~200KB+ con plugins incluidos (vs ~50-80KB Tiptap modular)
- ❌ **Integración Next.js**: Wrapper React menos maduro, fricciones con SSR/RSC
- ❌ **Output menos limpio**: HTML/markdown con metadatos específicos del editor

**Implementación Estimada:** 2 semanas para MVP funcional

**Razón de descarte:** Proyecto con señales de abandono relativo, arquitectura menos moderna, menor flexibilidad para nuestras necesidades de plantillas custom.

---

### Opción 3: MDXEditor + WeasyPrint

**Descripción Técnica:**

- **MDXEditor**: Editor WYSIWYG específico para MDX (Markdown + React components), basado en Lexical (framework de Facebook)
- **WeasyPrint**: Mismo que Opción 1

**Pros:**

- ✅ **MDX nativo**: Soporte de React components dentro de markdown
- ✅ **Lexical moderno**: Framework de edición de Facebook, arquitectura avanzada
- ✅ **UI Notion-style**: Experiencia de usuario pulida out-of-the-box
- ✅ **Mantenimiento activo**: 1.8k+ stars, actualizaciones frecuentes

**Cons:**

- ❌ **Complejidad MDX innecesaria**: No necesitamos React components en markdown, overhead no justificado
- ❌ **Menor madurez**: Proyecto más joven que Tiptap (menos battle-tested)
- ❌ **Bundle size mayor**: ~150-200KB vs ~50-80KB Tiptap
- ❌ **Menos extensiones**: Ecosistema de plugins más limitado

**Implementación Estimada:** 2-3 semanas

**Razón de descarte:** Complejidad MDX no necesaria para nuestro caso de uso, overhead no justificado, menos maduro que Tiptap.

---

### Opción 4: Tiptap (Editor) + Puppeteer/Playwright (PDF)

**Descripción Técnica:**

- **Tiptap**: Mismo que Opción 1
- **Puppeteer/Playwright**: Navegador headless (Chromium) para renderizar HTML a PDF

**Pros:**

- ✅ **Calidad pixel-perfect**: PDF idéntico a visualización en navegador
- ✅ **CSS completo**: Soporte de todas las features CSS modernas (Grid, Flexbox avanzado, custom properties)
- ✅ **JavaScript en PDFs**: Permite ejecutar JS antes de generar PDF

**Cons:**

- ❌ **Performance 3x peor**: 3-5s por PDF vs 1-2s WeasyPrint
- ❌ **Consumo memoria 4x mayor**: 200-400MB vs 50-100MB WeasyPrint
- ❌ **Complejidad infraestructura**: Requiere microservicio Node.js separado o instalación Chromium en contenedor Django
- ❌ **Dependencias pesadas**: Chromium binaries ~200MB, mantenimiento complejo
- ❌ **Escalabilidad limitada**: Múltiples instancias navegador consumen recursos exponencialmente

**Implementación Estimada:** 4-5 semanas (incluye setup microservicio)

**Razón de descarte:** Complejidad operativa no justificada, performance inferior, consumo de recursos excesivo para beneficio marginal en calidad PDF.

---

### Opción 5: Tiptap (Editor) + @react-pdf/renderer (PDF Cliente)

**Descripción Técnica:**

- **Tiptap**: Mismo que Opción 1
- **@react-pdf/renderer**: Generación de PDFs en el navegador usando React components

**Pros:**

- ✅ **Sin carga servidor**: PDFs generados en cliente, cero impacto backend
- ✅ **Preview instantáneo**: Usuario ve PDF antes de descargar
- ✅ **Componentes React**: Reutilización de componentes UI
- ✅ **Bundle razonable**: ~100KB

**Cons:**

- ❌ **No es HTML/CSS completo**: Subset limitado de propiedades CSS, sintaxis propia
- ❌ **Conversión manual**: Templates HTML existentes deben reescribirse como componentes React
- ❌ **No server-side**: Imposible generar PDFs en background con Celery
- ❌ **Limitaciones tipográficas**: Menor control sobre kerning, line-height, page breaks
- ❌ **No adecuado para batch**: Generación masiva requiere backend

**Implementación Estimada:** 3-4 semanas (incluye conversión templates)

**Razón de descarte:** No cumple requisito de generación server-side con Celery, sintaxis propietaria vs HTML/CSS estándar, limitaciones tipográficas.

---

## Decisión

**Opción elegida**: **Tiptap (Editor) + WeasyPrint (PDF Generation)**

### Justificación Detallada

Hemos decidido usar **Tiptap como editor WYSIWYG** y **WeasyPrint como motor de generación de PDFs** por las siguientes razones fundamentadas:

#### 1. Mantenimiento Activo y Futuro-Proof

**Tiptap:**

- Proyecto activamente desarrollado (último release noviembre 2025)
- Comunidad creciente (25k+ stars GitHub, 3M+ editores en producción)
- Recientemente (junio 2025) liberaron 10 extensiones Pro como open source, demostrando compromiso con la comunidad
- Roadmap público con features planeadas
- Utilizado por empresas tier-1 (GitLab, Axios, Substack)

**WeasyPrint:**

- Mantenimiento profesional por CourtBouillon
- 8k+ stars GitHub, 596k descargas semanales PyPI
- Releases regulares con fixes y mejoras
- Compliance con estándares W3C (CSS Paged Media Level 3)

**vs TOAST UI** (último commit febrero 2024, repos deprecated, actividad reducida)

#### 2. Arquitectura Técnica Superior

**Tiptap:**

- **Headless architecture**: Control total sobre UI, no dependencia de estilos pre-definidos
- **ProseMirror foundation**: Framework de edición moderno con document model inmutable, collaborative editing ready
- **Sistema de extensiones modular**: Solo cargar funcionalidad necesaria (~50-80KB vs 200KB+ monolitos)
- **React-first design**: Hooks nativos, server components compatible, TypeScript-friendly

**WeasyPrint:**

- **Python puro**: Sin dependencias Node.js, integración nativa en Django
- **CSS engine pagination-aware**: Diseñado específicamente para documentos paginados
- **Lightweight**: 50-100MB RAM vs 200-400MB navegadores headless

#### 3. Performance y Escalabilidad

**Benchmarks clave:**

- WeasyPrint: 1-2 segundos por PDF de 10 páginas
- Puppeteer: 3-5 segundos por PDF equivalente
- WeasyPrint: 50-100MB RAM por proceso
- Puppeteer: 200-400MB RAM por instancia navegador

**Implicación para Celery:** Con WeasyPrint podemos ejecutar 4-5 workers de generación de PDFs en el mismo hardware que ejecutaría 1 worker Puppeteer.

#### 4. Flexibilidad de Plantillas

**Tiptap:**

- Exporta/importa markdown limpio sin metadatos propietarios
- Output HTML completamente controlable vía custom rendering
- Extensiones custom para bloques específicos (ej: portadas, variables `{{cliente}}`)
- Integración con Design Tokens y CSS Custom Properties para theming

**WeasyPrint:**

- HTML/CSS estándar para plantillas (reutilizable, familiar para developers)
- CSS Paged Media permite:
  - `@page` rules para márgenes, tamaño página, headers/footers
  - `page-break-*` properties para control de paginación
  - Counters (`counter(page)`) para numeración
- Fuentes custom via `@font-face` con WOFF2/TTF

**Ejemplo de plantilla:**

```css
@page {
    size: A4;
    margin: 2cm;
    @top-center {
        content: "{{ company_name }}";
        font-family: var(--font-heading);
    }
    @bottom-right {
        content: "Página " counter(page) " de " counter(pages);
    }
}
```

#### 5. Integración con Stack Existente

**Django + React + Inertia.js:**

- Tiptap: Componente React nativo, se integra sin adaptadores
- WeasyPrint: Django helper library `django-weasyprint`, vistas basadas en clases ready-to-use
- No requiere microservicios adicionales ni infraestructura compleja
- Service Layer Pattern compatible: `DocumentService.generate_pdf()` encapsula lógica

**Celery Ready:**

```python
@shared_task
def generate_pdf_task(document_id):
    document = Document.objects.get(id=document_id)
    html = render_markdown_with_template(document.content, document.template)
    pdf_bytes = HTML(string=html).write_pdf()
    document.pdf_file.save(f'{document.id}.pdf', ContentFile(pdf_bytes))
```

#### 6. Costes y Licencias

- **Tiptap**: MIT License - uso comercial libre, sin restricciones
- **WeasyPrint**: BSD License - uso comercial libre, sin restricciones
- **Coste operativo**: €0/mes (vs servicios SaaS tipo DocRaptor $29-149/mes)
- **Sin vendor lock-in**: Control total del código, no dependencia de APIs externas

#### 7. Developer Experience (DX)

**Para desarrollador humano:**

- Tiptap: Documentación excelente, ejemplos abundantes, TypeScript-first
- WeasyPrint: API Python simple, debugging directo (no blackbox navegador)

**Para agentes IA:**

- Tiptap: Patterns claros, estructura predecible de extensiones
- WeasyPrint: HTML/CSS estándar (vs sintaxis propietaria de @react-pdf/renderer)
- Stack unificado Python simplifica context window de agentes

#### 8. Evolución Futura

**Roadmap v2.0:**

- **Colaboración real-time**: Tiptap + Yjs + WebSockets (implementable, extensión oficial disponible)
- **Versionado de documentos**: Markdown en Git + diffs nativos
- **Plantillas avanzadas**: Variables, bloques condicionales, loops (Jinja2 + WeasyPrint)
- **Exportación DOCX**: Tiptap → markdown → pandoc → DOCX (pipeline estándar)

**Escalado a SaaS:**

- Tiptap escala horizontalmente sin problemas
- WeasyPrint + Celery permite batch processing de miles de PDFs/hora
- Redis cache para templates renderizados (hit rate >80%)

---

## Consecuencias

### Positivas

- ✅ **Zero vendor lock-in**: Control total sobre generación de documentos, sin dependencia de servicios externos
- ✅ **Performance óptima**: 1-2s generación PDF permite UX responsive, usuarios no esperan
- ✅ **Coste operativo cero**: Sin gastos recurrentes en licencias, APIs o servicios SaaS
- ✅ **Stack unificado**: Python + React, sin microservicios Node.js adicionales, menor complejidad operativa
- ✅ **Escalabilidad horizontal**: WeasyPrint + Celery permite procesamiento batch masivo
- ✅ **Calidad profesional**: PDFs con tipografía correcta, headers/footers, numeración automática
- ✅ **Markdown como source of truth**: Versionado en Git, diffs legibles, portabilidad
- ✅ **Extensibilidad probada**: Tiptap 100+ extensiones, WeasyPrint hooks Python para customización
- ✅ **Developer Experience superior**: Debugging directo Python, no blackbox navegador headless
- ✅ **Comunidad activa**: Soporte, ejemplos, plugins disponibles de ambos proyectos

### Negativas

- ❌ **Colaboración real-time no nativa**: Requiere implementación custom con Yjs (~1-2 sprints adicionales si se necesita)
- ❌ **WeasyPrint limitaciones CSS modernas**: No soporta CSS Grid avanzado, Flexbox limitado, algunas propiedades CSS3 ausentes
- ❌ **Curva de aprendizaje ProseMirror**: Concepts de nodes/marks/transforms requieren familiarización inicial
- ❌ **WeasyPrint lento con PDFs >50 páginas**: Requiere optimización o chunking para documentos muy largos
- ❌ **Debugging PDFs no visual**: Iterar sobre estilos CSS require regenerar PDF, no hay preview instantáneo (mitigable con html preview en navegador)

### Neutras

- ⚠️ **Monitorear performance WeasyPrint en producción**: Establecer baselines, alertas si generación >3s
- ⚠️ **Tiptap evoluciona rápido**: Posibles breaking changes en updates (mitigar: version pinning en package.json)
- ⚠️ **Necesidad futura de Puppeteer para PDFs pixel-perfect**: Si marketing requiere PDFs idénticos a diseño web, evaluar híbrido WeasyPrint (mayoría) + Puppeteer (casos específicos)
- ⚠️ **Gestión de fuentes custom**: Requiere proceso de upload/validación de archivos WOFF2/TTF, licencias de fuentes a verificar

---

## Notas de Implementación

### Setup Inicial

**Frontend (Tiptap):**

```bash
npm install @tiptap/react @tiptap/starter-kit @tiptap/extension-table tiptap-markdown
```

**Backend (WeasyPrint):**

```bash
# En pyproject.toml
dependencies = [
    "weasyprint>=61.0",
    "django-weasyprint>=3.0",
]

# Instalar con uv
uv pip install -e .

# Verificar dependencias sistema (Ubuntu/Debian)
sudo apt-get install libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0 \
    libffi-dev libjpeg-dev libopenjp2-7-dev
```

### Arquitectura de Implementación

**Estructura de módulo:**

```markdown
apps/documents/
├── models.py           # Document, DocumentTemplate, DocumentVersion
├── services.py         # DocumentService (create, update, generate_pdf)
├── selectors.py        # get_documents_list, get_templates_list
├── tasks.py            # Celery tasks: generate_pdf_task
├── templates/
│   └── pdf/
│       ├── base.html           # Template HTML base
│       ├── offer.html          # Template oferta comercial
│       └── report.html         # Template informe
└── static/
    └── css/
        ├── pdf_base.css        # Estilos comunes
        └── templates/
            ├── offer.css       # Estilos oferta
            └── report.css      # Estilos informe
```

**Service Layer Pattern:**

```python
# apps/documents/services.py
from django.db import transaction
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
import markdown2

class DocumentService:
    @staticmethod
    @transaction.atomic
    def create_document(*, title: str, template_id: int, created_by: User) -> Document:
        template = DocumentTemplate.objects.get(id=template_id)
        document = Document.objects.create(
            title=title,
            template=template,
            markdown_content="",
            created_by=created_by
        )
        return document

    @staticmethod
    def generate_pdf(document: Document) -> bytes:
        """Generar PDF desde markdown con template."""
        # 1. Renderizar markdown a HTML
        html_content = markdown2.markdown(
            document.markdown_content,
            extras=['tables', 'fenced-code-blocks', 'header-ids']
        )

        # 2. Cargar template y estilos
        template_html = render_to_string('pdf/base.html', {
            'content': html_content,
            'config': document.template.configuration,
            'metadata': document.metadata,
        })

        # 3. Generar PDF con WeasyPrint
        font_config = FontConfiguration()
        css = CSS(string=document.template.css_content, font_config=font_config)

        pdf_bytes = HTML(string=template_html).write_pdf(
            stylesheets=[css],
            font_config=font_config
        )

        return pdf_bytes
```

**Celery Task para generación asíncrona:**

```python
# apps/documents/tasks.py
from celery import shared_task
from django.core.files.base import ContentFile
from django.core.cache import cache

@shared_task(bind=True, max_retries=3)
def generate_pdf_task(self, document_id: int):
    try:
        document = Document.objects.get(id=document_id)

        # Generar PDF
        pdf_bytes = DocumentService.generate_pdf(document)

        # Guardar archivo
        filename = f'doc_{document.id}.pdf'
        document.pdf_file.save(filename, ContentFile(pdf_bytes))
        document.pdf_generated_at = timezone.now()
        document.save()

        # Cachear URL 24h
        cache.set(f'pdf_url_{document.id}', document.pdf_file.url, 86400)

        return {'status': 'success', 'pdf_url': document.pdf_file.url}

    except Exception as exc:
        logger.error(f"Error generating PDF for document {document_id}: {exc}")
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))
```

**Frontend React Component:**

```typescript
// frontend/components/TiptapEditor.tsx
import { useEditor, EditorContent } from '@tiptap/react'
import StarterKit from '@tiptap/starter-kit'
import { Markdown } from 'tiptap-markdown'
import Table from '@tiptap/extension-table'

export default function TiptapEditor({ initialContent, onChange }) {
  const editor = useEditor({
    extensions: [
      StarterKit,
      Markdown,
      Table.configure({ resizable: true }),
    ],
    content: initialContent,
    onUpdate: ({ editor }) => {
      const markdown = editor.storage.markdown.getMarkdown()
      onChange(markdown)
    },
  })

  return <EditorContent editor={editor} />
}
```

### Sistema de Plantillas

**Modelo Django:**

```python
# apps/documents/models.py
class DocumentTemplate(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    template_type = models.CharField(max_length=50, choices=[
        ('offer', 'Oferta Comercial'),
        ('report', 'Informe'),
        ('invoice', 'Factura'),
        ('certificate', 'Certificado')
    ])

    # Configuración JSON flexible
    configuration = models.JSONField(default=dict, help_text="""
    {
        "page_size": "A4",
        "margins": {"top": "2cm", "bottom": "2cm"},
        "theme": {
            "primary_color": "#003366",
            "font_heading": "Helvetica-Bold",
            "font_body": "Arial"
        },
        "cover_page": {
            "enabled": true,
            "logo_position": "center"
        }
    }
    """)

    # CSS personalizado
    css_content = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
```

**CSS Paged Media Template:**

```css
/* static/css/templates/offer.css */
@page {
    size: A4;
    margin: 2cm;

    @top-center {
        content: "{{ company_name }}";
        font-family: var(--font-heading);
        color: var(--primary-color);
    }

    @bottom-right {
        content: "Página " counter(page) " de " counter(pages);
        font-size: 9pt;
    }
}

/* Evitar cortes incorrectos */
h1, h2, h3 {
    page-break-after: avoid;
}

table {
    page-break-inside: avoid;
}

/* Estilos tabla corporativa */
table {
    width: 100%;
    border-collapse: collapse;
}

thead {
    background-color: var(--primary-color);
    color: white;
}

th, td {
    padding: 12px;
    border: 1px solid #ddd;
}
```

### Caché Estratégico

**Multi-layer caching:**

```python
# Cache layer 1: PDFs generados (24h)
cache.set(f'pdf_{document_id}', pdf_url, 86400)

# Cache layer 2: HTML renderizado (1h, por hash contenido)
content_hash = hashlib.sha256(markdown.encode()).hexdigest()
cache.set(f'html_{content_hash}', rendered_html, 3600)

# Cache layer 3: Templates (15min)
@cache_page(60 * 15)
def template_list(request):
    return Template.objects.filter(is_active=True)
```

### Testing Strategy

**Unit tests Service:**

```python
@pytest.mark.django_db
class TestDocumentService:
    def test_generate_pdf_success(self):
        document = DocumentFactory(
            markdown_content="# Test\n\nContent"
        )

        pdf_bytes = DocumentService.generate_pdf(document)

        assert len(pdf_bytes) > 0
        assert pdf_bytes.startswith(b'%PDF-')  # PDF header
```

**Integration test:**

```python
@pytest.mark.django_db
def test_document_create_and_generate_pdf(client, authenticated_user):
    template = TemplateFactory(template_type='offer')

    # Crear documento
    response = client.post('/documents/create/', {
        'title': 'Test Offer',
        'template_id': template.id,
        'markdown_content': '# Oferta\n\nContenido'
    })

    document = Document.objects.get(title='Test Offer')

    # Generar PDF
    response = client.post(f'/documents/{document.id}/generate-pdf/')

    assert response.status_code == 202  # Accepted (async task)
    assert 'task_id' in response.json()
```

### Performance Benchmarks Objetivo

| Métrica | Target MVP | Target Producción |
|---------|-----------|-------------------|
| Generación PDF 5 páginas | < 1.5s | < 1s |
| Generación PDF 20 páginas | < 3s | < 2s |
| Throughput PDFs/hora (1 worker) | 1200 | 1800 |
| Memoria por worker | < 100MB | < 80MB |
| Cache hit rate | > 70% | > 85% |

---

## Referencias

### Documentación Oficial

- **Tiptap Documentation**: <https://tiptap.dev/>
- **Tiptap React Guide**: <https://tiptap.dev/docs/editor/getting-started/install/react>
- **Tiptap Markdown Extension**: <https://tiptap.dev/docs/editor/extensions/functionality/markdown>
- **WeasyPrint Documentation**: <https://doc.courtbouillon.org/weasyprint/>
- **WeasyPrint API Reference**: <https://doc.courtbouillon.org/weasyprint/stable/api_reference.html>
- **django-weasyprint**: <https://github.com/fdemmer/django-weasyprint>
- **CSS Paged Media Spec**: <https://www.w3.org/TR/css-page-3/>

### Artículos y Comparativas

- **Tiptap vs TOAST UI Analysis**: Conversación técnica 2025-11-18
- **WeasyPrint vs Puppeteer Benchmark**: <https://doc.courtbouillon.org/weasyprint/stable/going_further.html#performance>
- **ProseMirror Guide**: <https://prosemirror.net/docs/guide/>

### GitHub Repositories

- **Tiptap Core**: <https://github.com/ueberdosis/tiptap> (25k+ stars)
- **WeasyPrint**: <https://github.com/Kozea/WeasyPrint> (8k+ stars)
- **TOAST UI Editor**: <https://github.com/nhn/tui.editor> (17k+ stars, último commit 2 años)

### Proyectos de Referencia

- **GitLab**: Usa Tiptap para editor de issues/comments
- **Axiom**: Usa Tiptap para documentación colaborativa
- **CourtBouillon clients**: Múltiples empresas usando WeasyPrint para facturación automática

### Internal Documentation

- **PRD Intranet 10Code**: `docs/product_docs/PRD_Intranet_10Code.md`
- **SAD Intranet 10Code**: `docs/product_docs/SAD_Intranet_10Code.md`
- **FSD Documents Module**: `docs/product_docs/modules/documents/FSD-Documents.md` (pending)
- **Django Patterns**: `.rules/DJANGO_PATTERNS.md`
- **Frontend Patterns**: `.rules/INERTIA_FRONTEND.md`

---

## Historial

| Fecha | Evento | Autor |
|-------|--------|-------|
| 2025-11-18 | ADR creado y aceptado tras análisis técnico exhaustivo | Juanje Márquez |
| 2025-11-18 | Decisión comunicada a equipo de desarrollo (agentes IA) | Juanje Márquez |

---

**Firmado por:**

- **Juanje Márquez** - Arquitecto Principal & Tech Lead - 2025-11-18

---

> **Nota para Agentes IA de Codificación:**
>
> Esta decisión arquitectónica es **vinculante** y debe seguirse en toda implementación relacionada con edición de documentos y generación de PDFs.
>
> **Implementación obligatoria:**
>
> - Editor WYSIWYG: Tiptap con extensiones StarterKit + Markdown + Table
> - Generación PDFs: WeasyPrint con django-weasyprint
> - Generación asíncrona: Celery tasks
> - Caché: Redis multi-layer (PDFs, HTML, Templates)
>
> **Prohibido:**
>
> - TOAST UI Editor (proyecto estancado)
> - Puppeteer/Playwright para PDFs (excepto casos pixel-perfect justificados explícitamente)
> - @react-pdf/renderer (no cumple requisitos server-side)
> - Cualquier solución SaaS de terceros sin aprobación explícita
>
> **Si se propone desviación:** Documentar justificación técnica completa y crear nuevo ADR superseding este.
