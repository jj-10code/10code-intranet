# Framework Metodológico para Product Analysis y Backlog Técnico

> Lo usaremos para el FSD de su módulo correspondiente de generación de ofertas y backlogs

**Versión:** 1.0  
**Fecha:** Diciembre 2024  
**Proyecto de referencia:** Módulo de Indicadores de Transparencia oGov

---

## 1. Proceso de Descubrimiento de Requisitos

### 1.1 Checklist de Preguntas Críticas

#### **Contexto Técnico**

- [ ] Stack tecnológico actual (versiones específicas)
- [ ] Arquitectura existente (monolito, microservicios, modular)
- [ ] Sistemas de autenticación/autorización en uso
- [ ] Framework CSS/UI establecido
- [ ] Infraestructura multi-tenant (si aplica)
- [ ] Sistemas de colas/jobs existentes
- [ ] CI/CD configurado

#### **Contexto de Negocio**

- [ ] Volumen actual vs proyectado (factor de crecimiento)
- [ ] Número de usuarios concurrentes esperados
- [ ] Frecuencia de uso/actualización de datos
- [ ] SLAs o requisitos de disponibilidad
- [ ] Presupuesto y timeline esperado
- [ ] ROI esperado y métricas de éxito

#### **Integraciones**

- [ ] Sistemas internos existentes a integrar
- [ ] APIs externas requeridas
- [ ] Dirección del flujo de datos (unidireccional/bidireccional)
- [ ] Servicios de terceros (email, storage, etc.)
- [ ] Formato de datos esperados (JSON, XML, etc.)

#### **Requisitos Funcionales Ocultos**

- [ ] Multi-idioma (cuáles idiomas específicamente)
- [ ] Sistema de notificaciones (email, push, SMS)
- [ ] Auditoría y logs (nivel de detalle requerido)
- [ ] Gestión de archivos adjuntos
- [ ] Versionado de datos
- [ ] Sistema de backups
- [ ] Workflows de aprobación
- [ ] Permisos granulares vs básicos

#### **Experiencia de Usuario**

- [ ] Dispositivos target (desktop, tablet, móvil)
- [ ] Navegadores soportados
- [ ] Requisitos de accesibilidad (WCAG)
- [ ] Necesidad de modo offline
- [ ] Diseño existente o referencia visual
- [ ] Componentes UI reutilizables disponibles

#### **Migración y Datos**

- [ ] Volumen de datos a migrar
- [ ] Formato de datos actuales (Excel, CSV, BD)
- [ ] Calidad de datos existentes
- [ ] Necesidad de limpieza/transformación
- [ ] Periodo de convivencia con sistema anterior
- [ ] Rollback plan

### 1.2 Detección de Requisitos Fantasma

**Patrones comunes de requisitos no mencionados:**

1. **Performance**: Caché, paginación, lazy loading
2. **Seguridad**: RGPD, auditoría, logs de acceso
3. **UX**: Autosave, confirmaciones, undo/redo
4. **Integraciones**: Webhooks, sincronización en tiempo real
5. **Reporting**: Exportaciones, dashboards, métricas
6. **Gestión**: Plantillas, configuraciones, personalizaciones
7. **Comunicaciones**: Notificaciones, alertas, recordatorios
8. **Validaciones**: Reglas de negocio complejas, dependencias

### 1.3 Clarificaciones Críticas

**Preguntas de clarificación esenciales:**

- "¿Esto significa que...?" - Confirmar entendimiento
- "¿El flujo es Portal → Indicadores o Indicadores → Portal?"
- "¿Qué pasa si...?" - Casos edge
- "¿Con qué frecuencia...?" - Volumetría
- "¿Quién es responsable de...?" - Ownership
- "¿Existe actualmente...?" - Reutilización

---

## 2. Estructura de Product Analysis

### 2.1 Jerarquía de Componentes

```markdown
Product Analysis
├── Resumen Ejecutivo (business-focused)
├── EPICs (60-160h cada uno)
│   ├── Valor de Negocio
│   ├── Beneficios Clave
│   ├── Consideraciones Técnicas
│   └── Estimación por Perfil
├── Requisitos No Funcionales
├── Arquitectura (decisiones, no implementación)
├── Plan de Desarrollo (fases con valor independiente)
├── Riesgos y Mitigación
└── Métricas de Éxito (KPIs medibles)
```

### 2.2 Principios de Definición de EPICs

**Un buen EPIC debe:**

1. **Aportar valor de negocio claro** (no ser solo técnico)
2. **Ser entregable independientemente** (aporta valor por sí solo)
3. **Tener entre 60-160 horas** de desarrollo
4. **Incluir 4-6 Historias de Usuario** relacionadas
5. **Ser testeable** end-to-end

**Estructura de EPIC:**

```markdown
#### EPIC N: [Nombre orientado a valor]
**Valor de negocio:**
- Problema específico que resuelve
- Beneficio cuantificable

**Beneficios clave:**
- 3-5 beneficios principales

**Funcionalidades del documento original:**
- Lo que pidió el cliente explícitamente

**Funcionalidades adicionales identificadas:**
- Lo que detectamos como necesario

**Consideraciones técnicas:**
- Complejidad: ALTA/MEDIA/BAJA
- Tecnologías principales involucradas
- Riesgos significativos

**Desglose por perfil:**
| Perfil | Horas Min | Horas Max |
|--------|-----------|-----------|
| Backend | XXh | XXh |
| Frontend | XXh | XXh |
| UX/UI | XXh | XXh |
| Architect | XXh | XXh |
```

### 2.3 Estimación por Perfiles

**Distribución típica en proyectos web:**

- **Backend**: 45-55% del total
- **Frontend**: 30-40% del total  
- **UX/UI**: 8-12% del total
- **Arquitecto**: 1-3% del total
- **QA**: 10-15% (si se incluye)

**Factors de ajuste:**

- +20% Backend si hay integraciones complejas
- +20% Frontend si es muy interactivo
- +10% UX si no hay diseño previo
- +5% Arquitecto si es greenfield

### 2.4 Marcado de Elementos

**Sistema de marcado para trazabilidad:**

- 🔴 **Requisito adicional** no explícito en documento original
- 🔄 **Actualización necesaria** detectada durante backlog
- ⚠️ **Riesgo identificado** que requiere mitigación
- 💡 **Optimización propuesta** para mejorar eficiencia
- 🔒 **Dependencia crítica** que puede bloquear

---

## 3. Estructura de Backlog Técnico

### 3.1 Jerarquía Completa

```markdown
EPIC (60-160h total)
└── Historia de Usuario (16-40h total)
    ├── Descripción (Como... Quiero... Para...)
    └── Criterios de Aceptación (testeables)
        └── Tareas (<8h cada una)
            ├── Backend (Laravel)
            ├── Frontend (React)
            └── UX/UI (Diseño)
```

### 3.2 Definición de Historia de Usuario

**Estructura estándar:**

```markdown
### HU-X.Y: [Nombre descriptivo] [Total horas] [Prioridad]

**Como** [rol específico],
**Quiero** [funcionalidad concreta],
**Para** [beneficio/objetivo].

#### Criterios de Aceptación

**CAX.Y-01: [Nombre del criterio] [Prioridad]**
- Descripción funcional clara
- Condiciones de éxito medibles
- Casos edge considerados

**Tareas:**
- BE: [Descripción específica] [Xh] [Prioridad]
- FE: [Descripción específica] [Xh] [Prioridad]
- UX: [Descripción específica] [Xh] [Prioridad]
```

### 3.3 Principios para Tareas

**Cada tarea debe:**

1. **Ser menor a 8 horas** (idealmente 4-6h)
2. **Ser atómica** (completable independientemente)
3. **Tener un entregable claro**
4. **Especificar el perfil** responsable
5. **Incluir prioridad** (P1, P2, P3)

**Descomposición si tarea > 8h:**

```markdown
Tarea original: "Implementar CRUD completo" [16h]
↓
Tarea 1: "API endpoints CREATE/READ" [6h]
Tarea 2: "API endpoints UPDATE/DELETE" [4h]
Tarea 3: "Validaciones y tests" [6h]
```

### 3.4 Sistema de Prioridades

#### **P1 - Crítica (Must Have)**

- Bloqueante para otras funcionalidades
- Core del MVP
- Requisito legal/normativo
- ~65% del proyecto

#### **P2 - Media (Should Have)**

- Mejora significativa de UX
- Optimización importante
- Requisito para go-live
- ~30% del proyecto

#### **P3 - Baja (Nice to Have)**

- Mejoras cosméticas
- Features adicionales
- Optimizaciones menores
- ~5% del proyecto

---

## 4. Patrones y Anti-patrones

### 4.1 Patrones Exitosos

✅ **DO's:**

1. **EPIC 0**: Siempre incluir setup y configuración base
2. **Análisis Excel/Datos**: Sprint 0 dedicado antes de desarrollo
3. **Importación primero**: Facilita testing con datos reales
4. **Componentes reutilizables**: Identificar y crear temprano
5. **Validación continua**: Demo al final de cada sprint
6. **Buffer realista**: 15-20% para imprevistos
7. **Fases con valor**: Cada fase debe ser usable independientemente

### 4.2 Anti-patrones a Evitar

❌ **DON'T's:**

1. **EPICs técnicos puros**: Sin valor de negocio claro
2. **Tareas genéricas**: "Implementar backend" sin especificar
3. **Dependencias circulares**: A necesita B, B necesita A
4. **Estimaciones optimistas**: Sin considerar integración y testing
5. **Requisitos implícitos**: Asumir sin preguntar
6. **All-or-nothing**: Fases que no aportan valor parcial
7. **Ignorar deuda técnica**: No planificar refactoring

---

## 5. Cálculo de Estimaciones

### 5.1 Fórmula Base

```markdown
Estimación Total = Desarrollo + Testing + Integración + Buffer

Donde:
- Desarrollo = Suma de tareas
- Testing = 15-20% del desarrollo
- Integración = 10-15% del desarrollo
- Buffer = 15-20% del subtotal
```

### 5.2 Factores de Complejidad

**Multiplicadores según complejidad:**

- **Simple** (CRUD básico): x1.0
- **Medio** (lógica de negocio): x1.3
- **Complejo** (integraciones, algoritmos): x1.6
- **Muy complejo** (tiempo real, ML): x2.0

### 5.3 Ajustes por Contexto

**Factores de ajuste:**

- **Primera vez con tecnología**: +30%
- **Sin diseño definido**: +25%
- **Integraciones externas**: +20%
- **Multi-idioma**: +15%
- **Requisitos cambiantes**: +20%
- **Cliente muy involucrado**: -10%
- **Reutilización alta**: -20%

---

## 6. Gestión de Riesgos

### 6.1 Riesgos Comunes en Proyectos SaaS

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| Datos mal estructurados | ALTA | ALTO | Sprint 0 análisis |
| Cambios de alcance | MEDIA | ALTO | Contrato change request |
| Integraciones complejas | MEDIA | ALTO | POC temprano |
| Performance con volumen | BAJA | ALTO | Tests de carga |
| Requisitos normativos | BAJA | MEDIO | Buffer compliance |

### 6.2 Estrategias de Mitigación

1. **Sprint 0 Técnico**: Validar supuestos técnicos
2. **POCs tempranos**: Para integraciones críticas
3. **Validación continua**: Demos frecuentes con stakeholders
4. **Documentación**: Decisiones y cambios documentados
5. **Tests automatizados**: Para regresiones

---

## 7. Documentación y Comunicación

### 7.1 Documentos Clave

1. **Product Analysis**: Para decisión de negocio
2. **Backlog Técnico**: Para equipo desarrollo
3. **Roadmap**: Para planificación y seguimiento
4. **Risk Register**: Para gestión proactiva
5. **Decision Log**: Para trazabilidad

### 7.2 Sincronización de Documentos

**Proceso de actualización:**

1. Detectar cambio durante desarrollo backlog
2. Marcar con 🔄 en backlog
3. Actualizar Product Analysis
4. Validar consistencia
5. Versionar ambos documentos

### 7.3 Comunicación con Stakeholders

**Niveles de detalle por audiencia:**

- **C-Level**: Resumen ejecutivo + ROI
- **Product Owner**: EPICs + Roadmap
- **Tech Lead**: Historias + Arquitectura
- **Developers**: Tareas + Criterios aceptación
- **QA**: Criterios aceptación + Casos edge

---

## 8. Herramientas y Plantillas

### 8.1 Plantilla Pregunta de Clarificación

```markdown
## 🔍 Clarificación Necesaria

**Contexto:** [Dónde surgió la duda]
**Pregunta:** [Pregunta específica]
**Supuesto actual:** [Lo que entendemos]
**Impacto si incorrecto:** [Qué afectaría]
**Opciones:**
- A) [Opción 1]
- B) [Opción 2]
**Recomendación:** [Nuestra sugerencia]
```

### 8.2 Plantilla Detección Requisito Fantasma

```markdown
## 👻 Posible Requisito No Especificado

**Funcionalidad:** [Qué detectamos]
**Por qué lo inferimos:** [Razón]
**Impacto si lo incluimos:** [Horas/complejidad]
**Impacto si NO lo incluimos:** [Riesgo]
**Recomendación:** [Incluir/Validar/Diferir]
```

### 8.3 Checklist Pre-Entrega

- [ ] Todos los EPICs tienen valor de negocio claro
- [ ] Todas las HUs siguen formato Como/Quiero/Para
- [ ] Todas las tareas son < 8h
- [ ] Estimaciones incluyen testing e integración
- [ ] Riesgos identificados y mitigados
- [ ] Dependencias claramente marcadas
- [ ] Métricas de éxito definidas
- [ ] ROI calculado y justificado

---

## 9. Lecciones Aprendidas del Proyecto

### 9.1 Qué Funcionó Bien

1. **Preguntas exhaustivas iniciales**: Ahorraron retrabajo
2. **Marcar requisitos adicionales con 🔴**: Clara trazabilidad
3. **Desglose por perfiles**: Mejor precisión en estimaciones
4. **EPICs con valor independiente**: Facilita priorización
5. **Sincronización de documentos**: Consistencia mantenida

### 9.2 Áreas de Mejora Identificadas

1. **Necesidad de ver el Excel antes**: Crítico para precisión
2. **Clarificar dirección de sincronización**: Portal→Indicadores
3. **Especificar versión de frameworks**: Laravel 11, no 10
4. **Confirmar si Inertia.js o no**: Impacta arquitectura
5. **Validar diseño Lovable**: Antes de estimar Frontend

### 9.3 Recomendaciones para Futuros Proyectos

1. **Siempre incluir EPIC 0**: Setup es crítico
2. **Sprint 0 obligatorio**: Para análisis de datos existentes
3. **POCs para integraciones**: Antes de estimar
4. **Cliente muy involucrado**: Reduce riesgo significativamente
5. **Buffer diferenciado**: Más para integraciones externas
6. **Versionado de documentos**: Desde el día 1

---

## 10. Métricas de Calidad

### 10.1 KPIs del Proceso

| Métrica | Target | Actual |
|---------|--------|--------|
| Cobertura de requisitos | >95% | ✓ |
| Tareas < 8h | 100% | ✓ |
| EPICs con valor claro | 100% | ✓ |
| Riesgos identificados | >10 | ✓ |
| Requisitos fantasma detectados | >5 | ✓ |

### 10.2 Señales de Éxito

✅ **Documento bien estructurado cuando:**

- Cliente entiende el valor sin explicación adicional
- Equipo técnico puede estimar sin dudas
- QA puede crear casos de prueba directamente
- No hay sorpresas en desarrollo
- ROI es claro y medible

---

## 11. Evolución del Framework

### 11.1 Versiones

- **v1.0** (Actual): Basado en proyecto Indicadores Transparencia
- **v1.1** (Futura): Incorporar feedback post-implementación
- **v2.0** (Futura): Incluir patrones de microservicios

### 11.2 Mejoras Propuestas

1. Incluir estimaciones de QA como perfil separado
2. Añadir checklist de accesibilidad WCAG
3. Plantillas para diferentes tipos de proyecto
4. Calculadora automática de estimaciones
5. Matriz de competencias por perfil

---

## Apéndice: Quick Reference

### Conversión Rápida Story Points → Horas

- 1 SP = 4-6h
- 2 SP = 8-12h  
- 3 SP = 16-24h
- 5 SP = 32-40h (1 semana)
- 8 SP = 60-80h (1 EPIC pequeño)

### Fórmula Rápida Estimación

```markdown
Backend = HUs * 20h (promedio)
Frontend = Backend * 0.7
UX = Frontend * 0.3
Total = (BE + FE + UX) * 1.15 (buffer)
```

### Red Flags en Requisitos

🚩 "Simple CRUD" → Nunca es simple
🚩 "Como en [competidor]" → Sin especificar
🚩 "Ya lo tenemos claro" → No está documentado
🚩 "Para ayer" → Sin prioridades reales
🚩 "Será fácil" → No han considerado edge cases

---

> *Framework v1.0 - Diciembre 2024*
