# ADR-{número}: {Título Corto de la Decisión}

## Metadata

- **Status**: [Proposed / Accepted / Deprecated / Superseded by ADR-XXX]
- **Fecha**: YYYY-MM-DD
- **Decisor(es)**: [Nombre(s)]
- **Tags**: [arquitectura, backend, frontend, infraestructura, etc.]

---

## Contexto y Problema

[Describe el contexto técnico o de negocio que motiva esta decisión. ¿Qué problema estamos tratando de resolver? ¿Qué fuerzas están en juego?]

**Ejemplo:**
> Necesitamos decidir cómo gestionar la creación y exportación de documentos técnicos (ofertas, contratos, reportes) en la intranet. Los requisitos son:
>
> - Edición WYSIWYG moderna (no textarea plano)
> - Generación de PDFs profesionales con plantillas
> - Exportación a múltiples formatos (PDF, DOCX, Markdown)
> - Versionado de documentos
> - Colaboración eventual (futuro v2.0)

---

## Factores de Decisión

[Lista de criterios importantes para evaluar las opciones]

- **Factor 1**: Facilidad de integración con Django + React
- **Factor 2**: Calidad de PDFs generados
- **Factor 3**: Curva de aprendizaje para developers
- **Factor 4**: Costo (licencias, mantenimiento)
- **Factor 5**: Soporte de plantillas customizables
- **Factor 6**: Performance en generación de PDFs

---

## Opciones Consideradas

### Opción 1: [Nombre de la Opción]

**Descripción:** [Breve explicación técnica]

**Pros:**

- ✅ [Ventaja 1]
- ✅ [Ventaja 2]

**Cons:**

- ❌ [Desventaja 1]
- ❌ [Desventaja 2]

---

### Opción 2: [Nombre de la Opción]

[Repetir estructura...]

---

### Opción 3: [Nombre de la Opción]

[Repetir estructura...]

---

## Decisión

**Opción elegida**: {Opción X} - {Nombre}

**Justificación:**

[Explicación de por qué se eligió esta opción sobre las otras, basándose en los factores de decisión]

**Ejemplo:**
> Hemos decidido usar **Tiptap (editor) + WeasyPrint (PDF)** porque:
>
> 1. **Mejor DX para developers**: Tiptap es React-friendly, WeasyPrint es Python puro
> 2. **Sin vendor lock-in**: Ambos son open-source, no dependemos de SaaS
> 3. **Calidad PDF superior**: WeasyPrint produce PDFs profesionales con CSS moderno
> 4. **Costo cero**: No requiere licencias, vs Google Docs API ($$$)
> 5. **Plantillas flexibles**: HTML/CSS para PDFs permite customización total
>
> Aunque CKEditor tiene más features out-of-box, Tiptap es más moderno y mantenible a largo plazo. La integración Tiptap + WeasyPrint ya está validada en otros proyectos Django.

---

## Consecuencias

### Positivas

- ✅ [Beneficio 1 esperado]
- ✅ [Beneficio 2 esperado]

### Negativas

- ❌ [Trade-off 1 aceptado]
- ❌ [Trade-off 2 aceptado]

### Neutras

- ⚠️ [Implicación 1 a monitorear]

**Ejemplo:**

> ### Positivas (ej)
>
> - ✅ Developers no necesitan aprender herramientas nuevas (React + Python)
> - ✅ PDFs con calidad profesional desde día 1
> - ✅ No hay límites de API calls o costos ocultos
>
> ### Negativas (ej)
>
> - ❌ Tiptap no tiene colaboración real-time nativa (requiere extensión custom)
> - ❌ WeasyPrint puede ser lento con PDFs >50 páginas (mitigable con Celery)
>
> ### Neutras (ej)
>
> - ⚠️ Necesitamos monitorear performance de WeasyPrint en producción
> - ⚠️ Tiptap evoluciona rápido, posibles breaking changes en updates

---

## Notas de Implementación

[Lineamientos técnicos breves para implementar esta decisión]

**Ejemplo:**
>
> - **Tiptap**: Instalar `@tiptap/react`, `@tiptap/starter-kit`
> - **WeasyPrint**: `pip install weasyprint`, verificar dependencias sistema (Cairo, Pango)
> - **Plantillas PDF**: Crear carpeta `templates/pdf/` con plantillas base HTML/CSS
> - **Service layer**: `apps/documents/services.py::generate_pdf_from_html()`
> - **Celery task**: Para PDFs grandes, encolar generación asíncrona

---

## Referencias

- [Link a documentación técnica relevante]
- [Link a benchmark o comparativa]
- [Link a discusión en GitHub/Slack]

**Ejemplo:**

- [Tiptap Documentation](https://tiptap.dev/)
- [WeasyPrint Documentation](https://doc.courtbouillon.org/weasyprint/)
- [Comparativa editores WYSIWYG 2024](https://ejemplo.com/wysiwyg-comparison)
- [Discusión Slack: #arquitectura (2025-01-10)](https://10code.slack.com/archives/...)

---

## Historial

| Fecha | Evento |
|-------|--------|
| 2025-01-15 | ADR creado y aceptado |
| 2025-03-20 | Status cambiado a "Deprecated" - Ver ADR-012 |

---

**Firmado por:**

- [Nombre] - [Rol] - [Fecha]
