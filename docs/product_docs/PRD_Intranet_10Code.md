# PRD - Intranet 10Code: Sistema Integral de Gestión Empresarial

**Versión:** 1.0  
**Fecha:** Noviembre 2024  
**Tipo de Documento:** Product Requirements Document (PRD)  
**Estado:** Definitivo  

---

## 1. Visión y Objetivos del Producto

### 1.1 Visión General

La **Intranet 10Code** es una plataforma monolítica integral que unifica la gestión completa del ciclo de vida operativo de 10Code como empresa tecnológica, desde la captación comercial hasta la entrega de proyectos, pasando por la gestión de recursos humanos, control horario, planificación de proyectos y análisis de rendimiento.

### 1.2 Problema que Resuelve

10Code enfrenta actualmente:

- **Dispersión de herramientas**: Uso de múltiples sistemas desconectados (Jira, hojas de cálculo, herramientas manuales)
- **Falta de visibilidad**: Imposibilidad de visualizar carga de trabajo, disponibilidad de recursos y rentabilidad en tiempo real
- **Ineficiencias operativas**: Procesos manuales para seguimiento de horas, estimaciones y gestión comercial
- **Pérdida de información**: Documentación y conocimiento disperso sin centralización
- **Dificultad de planificación**: Sin herramientas para gestionar múltiples proyectos y recursos compartidos

### 1.3 Objetivos Principales

1. **Centralizar operaciones**: Única plataforma para todas las operaciones internas de 10Code
2. **Visibilidad total**: Dashboards en tiempo real de recursos, proyectos, finanzas y rendimiento
3. **Cumplimiento normativo**: Sistema de control horario conforme a normativa española de fichaje digital 2025
4. **Optimización de recursos**: Gestión eficiente de asignaciones y capacidad entre múltiples proyectos
5. **Trazabilidad completa**: Desde oportunidad comercial hasta cierre de proyecto con documentación centralizada
6. **Base para escalabilidad**: Fundamento sólido para futuras capacidades avanzadas (ML, automatizaciones, etc.)

### 1.4 Propuesta de Valor

- **Para Dirección**: Visión estratégica consolidada con KPIs de rentabilidad, recursos y productividad
- **Para Operaciones**: Control total de capacidad, asignaciones y planificación de recursos
- **Para Comerciales**: Pipeline unificado desde contacto hasta proyecto con estimaciones robustas
- **Para Gestores de Proyecto**: Herramientas ágiles de seguimiento, backlog y comunicación con equipos
- **Para Desarrolladores**: Plataforma simple para fichaje, imputación de horas y gestión de tareas diarias
- **Para RR.HH.**: Sistema completo de gestión de personal, ausencias, vacaciones y cumplimiento normativo

---

## 2. Contexto y Alcance

### 2.1 Alcance del MVP

El MVP de la Intranet 10Code incluye los siguientes módulos prioritarios:

#### Módulos Críticos (MVP - Fase 1)

1. **Autenticación y Usuarios** - SSO con Google Workspace (@10code.es)
2. **RR.HH. y Control Horario** - Fichaje digital, gestión de ausencias, cumplimiento normativo
3. **Comercial + CRM Básico** - Pipeline desde contactos hasta oportunidades y ofertas
4. **Producción (Gestión de Proyectos)** - Backlog, tableros Kanban, seguimiento básico
5. **Planificación y Disponibilidad** - Visualización de recursos y capacidad
6. **Documentación** - Gestión documental básica con Google Drive
7. **Admin y Dirección** - Dashboards ejecutivos con KPIs clave

#### Funcionalidades Posteriores (Post-MVP)

- Sistema de estimación con Machine Learning (Fase 2+)
- Módulo de Formación y Noticias
- Módulo de Captación de Talento
- Integraciones avanzadas (Figma, herramientas adicionales)
- Capacidades de IA generativa avanzadas

### 2.2 Fuera de Alcance (Explícitamente)

- **No es un ERP completo**: Se integra con ODOO para contabilidad y nóminas
- **No reemplaza Git/GitHub**: Se integra pero no sustituye control de versiones
- **No es CRM comercial externo**: Enfoque en proceso interno de ventas de 10Code
- **No es herramienta de diseño**: Se integra con Figma pero no sustituye herramientas de diseño
- **No es sistema de correo**: Envía notificaciones pero no reemplaza Gmail/correo corporativo

### 2.3 Principios Guía del Producto

1. **Monolito Modular**: Arquitectura unificada pero con separación clara de responsabilidades
2. **Simplicidad sobre sofisticación**: Priorizar usabilidad y adopción sobre features complejas
3. **Desktop-first, mobile-friendly**: Optimizado para uso de escritorio con soporte móvil
4. **Integración sobre duplicación**: Conectar con herramientas existentes antes que replicarlas
5. **Datos centralizados**: Única fuente de verdad para información crítica de la empresa
6. **Progresivo y evolutivo**: Construcción incremental con valor entregable en cada fase

---

## 3. Usuarios y Roles del Sistema

### 3.1 Roles Principales

| Rol | Responsabilidades Clave | Necesidades Principales |
|-----|-------------------------|-------------------------|
| **Dirección (CEO/COO/CTO)** | Visión estratégica, decisiones de alto nivel, rentabilidad global | KPIs consolidados, visión financiera, análisis de rendimiento |
| **Director de Operaciones** | Optimización de recursos, gestión de capacidad, planificación | Disponibilidad de recursos, detección de cuellos de botella, simulación de escenarios |
| **RR.HH.** | Gestión de personal, vacaciones, ausencias, onboarding | Control horario, gestión de ausencias, cumplimiento normativo |
| **Comercial** | Captación de leads, gestión de oportunidades, generación de ofertas | Pipeline visual, seguimiento de contactos, conversión a proyectos |
| **Gestor de Proyecto/Scrum Master** | Planificación, seguimiento de progreso, gestión de equipos | Tableros Kanban, burndown charts, comunicación con equipo |
| **Product Manager** | Gestión de backlog, priorización, definición de requisitos | Épicas/historias, priorización drag & drop, roadmap |
| **Technical Lead** | Asignación técnica, seguimiento de desarrollo, arquitectura | Asignación de tareas, revisión de código (vía GitHub), deuda técnica |
| **Desarrollador/Diseñador** | Ejecución de tareas, desarrollo, entrega | Tareas claras, registro de tiempo simple, visualización de carga |
| **Administrador del Sistema** | Configuración, usuarios, permisos, integraciones | Panel de administración, gestión de roles, logs de auditoría |

### 3.2 Permisos y Niveles de Acceso

**Sistema RBAC (Role-Based Access Control)** con permisos granulares por módulo:

- **Nivel 1 - Lectura**: Visualizar información sin capacidad de modificación
- **Nivel 2 - Escritura**: Crear y editar dentro de su ámbito de responsabilidad
- **Nivel 3 - Gestión**: Administrar procesos y aprobar cambios
- **Nivel 4 - Administración**: Configuración global y gestión de sistema

Los permisos se asignan por combinación de **Rol + Módulo + Acción**, permitiendo control fino de accesos.

---

## 4. Módulos del Sistema

### 4.1 Módulo: Autenticación y Usuarios

#### 4.1.1 Propósito

Gestión de acceso seguro al sistema mediante Single Sign-On con Google Workspace, control de sesiones y administración de usuarios de la organización.

#### 4.1.2 Valor de Negocio

- **Seguridad centralizada**: Autenticación corporativa sin gestión de contraseñas
- **Auditoría completa**: Trazabilidad de accesos y acciones en el sistema
- **Simplicidad**: Los usuarios utilizan sus credenciales corporativas existentes

#### 4.1.3 Funcionalidades Principales

- Login exclusivo con cuentas @10code.es mediante OAuth de Google
- Gestión de perfiles de usuario con información profesional
- Sistema RBAC con roles predefinidos y personalizables
- Registro de auditoría de accesos y acciones críticas
- Gestión de sesiones y políticas de timeout
- Panel de administración de usuarios y permisos

#### 4.1.4 Consideraciones Especiales

- Restricción de dominio: Solo cuentas @10code.es pueden acceder
- No hay registro público ni autenticación local (solo Google OAuth)
- Permisos heredables: Los roles pueden heredar permisos de roles base

**Referencia técnica**: Ver FSD correspondiente para detalles de implementación OAuth y gestión de tokens.

---

### 4.2 Módulo: RR.HH. y Control Horario

#### 4.2.1 Propósito

Sistema integral de gestión de recursos humanos con énfasis en control horario digital cumpliendo la normativa española de fichaje digital 2025, gestión de ausencias, vacaciones y capacidad del equipo.

#### 4.2.2 Valor de Negocio

- **Cumplimiento legal**: Sistema de fichaje conforme a normativa española (4 años de retención, trazabilidad)
- **Optimización de planificación**: Conocimiento preciso de capacidad disponible del equipo
- **Transparencia**: Visibilidad clara de horas trabajadas para empleados y gestores
- **Base para facturación**: Datos de horas trabajadas alimentan módulo financiero

#### 4.2.3 Funcionalidades Principales

##### Fichaje Digital y Jornada Laboral

- **Fichaje entrada/salida**: Cronómetro con registro de fecha-hora exacta
- **Autocierre automático**: Cierre de jornada al final del día con 30min de gracia
- **Gestión de incidencias**: Sistema de alertas por olvidos de fichaje
- **SLA de imputación**: Regla de imputación antes de las 10:00 del día siguiente
- **Edición justificada**: Modificaciones con motivo y aprobaciones según política
- **Log histórico completo**: Registro inmutable de todos los fichajes para auditoría

##### Gestión de Ausencias y Vacaciones

- **Solicitud de vacaciones**: Workflow de solicitud-aprobación con validación de disponibilidad
- **Gestión de bajas**: Registro de bajas laborales con impacto en planificación
- **Permisos y ausencias**: Sistema flexible para diferentes tipos de ausencias
- **Carry-over**: Gestión de vacaciones no disfrutadas según normativa
- **Calendario de equipo**: Visualización de ausencias previstas

##### Capacidad y Disponibilidad

- **Cálculo de capacidad**: Horas disponibles por persona considerando ausencias
- **KPIs de disponibilidad**: Métricas de capacidad por equipo y departamento
- **Alertas proactivas**: Notificaciones de baja capacidad o sobreasignación

##### Onboarding (Básico en MVP)

- Checklist de incorporación con documentación de normativas de sala
- Control de lectura y "firma digital" de documentos corporativos

##### Comunicaciones Internas

- Sistema de comunicados centralizados
- Integración con Discord para alertas importantes
- Gestión de peticiones de materiales/inventario

#### 4.2.4 Cumplimiento Normativo

**Normativa Española de Fichaje Digital 2025**:

- ✅ Registro obligatorio de jornada con trazabilidad completa
- ✅ Almacenamiento mínimo 4 años con acceso para Inspección de Trabajo
- ✅ Cumplimiento RGPD en gestión de datos personales
- ✅ Mínimo 6-7h imputación diaria según perfil (configurable)
- ✅ SLA de imputación y generación automática de incidencias

#### 4.2.5 Consideraciones Especiales

- **Datos sensibles**: Información de salud (bajas médicas) con protección especial RGPD
- **Inmutabilidad**: Los fichajes no pueden eliminarse, solo editarse con justificación
- **Acceso auditoría**: Sistema preparado para exportación de datos a Inspección de Trabajo
- **Integraciones futuras**: Preparado para conectar con ODOO para nóminas

**Referencia técnica**: Ver FSD de Control Horario para detalles de validaciones, reglas de negocio y arquitectura de auditoría.

---

### 4.3 Módulo: Comercial + CRM Básico

#### 4.3.1 Propósito

Gestión del pipeline comercial completo desde la captación de leads hasta la conversión en proyectos, incluyendo seguimiento de oportunidades, generación de ofertas y cierre de ventas.

#### 4.3.2 Valor de Negocio

- **Visibilidad del pipeline**: Vista unificada de todas las oportunidades comerciales
- **Automatización de proceso**: Flujo estructurado desde contacto hasta proyecto
- **Trazabilidad comercial**: Historial completo de interacciones con clientes
- **Base para estimaciones**: Conexión directa con sistema de estimación de proyectos
- **Conversión eficiente**: Transformación ágil de ofertas aceptadas en proyectos activos

#### 4.3.3 Funcionalidades Principales

##### Gestión de Leads y Contactos

- **Captación de leads**: Entrada manual de contactos desde diferentes fuentes
- **Enriquecimiento**: Captura de información relevante del contacto y empresa
- **Segmentación básica**: Clasificación de contactos por tipo, sector, tamaño
- **Historial de interacciones**: Registro de llamadas, emails, reuniones
- **Asignación**: Vinculación de contactos a comerciales responsables

##### Pipeline de Oportunidades

- **Funnel de ventas**: Estados configurables (Prospecto → Cualificado → Propuesta → Negociación → Cerrado)
- **Oportunidades múltiples**: Un contacto puede generar múltiples oportunidades
- **Calificación**: Probabilidad de cierre, valor estimado, prioridad
- **Seguimiento temporal**: Fechas de última interacción, próximas acciones
- **Vista Kanban**: Arrastrar oportunidades entre etapas del funnel

##### Gestión de Requisitos Iniciales

- **Briefing del cliente**: Captura de necesidades y expectativas en reuniones
- **Documentación de requisitos**: Almacenamiento estructurado de requisitos técnicos y funcionales
- **Involucración técnica**: Posibilidad de añadir evaluaciones de perfiles técnicos
- **Vinculación con estimaciones**: Conexión directa con sistema de estimación

##### Generación de Ofertas

- **Tipos de oferta**: Fixed Price, SLA/Mantenimiento, Time & Materials, Bolsa de Horas
- **Plantillas configurables**: Templates por tipo de servicio
- **Generación de documentos**: Exportación de ofertas en formato presentable
- **Workflow de aprobación**: Flujo configurable para validación de ofertas (ej. Director Comercial)
- **Seguimiento de estado**: Enviada, Vista, En revisión, Aceptada, Rechazada

##### Cierre y Conversión

- **Conversión a proyecto**: Transformación automática de oferta aceptada en proyecto
- **Generación de contratos**: Vincular documentación legal (contratos firmados)
- **Handoff a Producción**: Traspaso fluido de información comercial a equipo de proyecto
- **Validación técnica**: Aprobación de jefe técnico antes de inicio

##### Envío Masivo y Comunicación (Básico)

- **Comunicaciones grupales**: Envío de newsletters o actualizaciones a segmentos
- **Integración email**: Registro de emails enviados desde Gmail corporativo

#### 4.3.4 Integraciones Clave

- **Google Drive**: Almacenamiento de ofertas, contratos y documentos comerciales
- **Gmail**: Trazabilidad de comunicaciones con clientes
- **Discord**: Notificaciones de oportunidades críticas o cierres

#### 4.3.5 Consideraciones Especiales

- **No es CRM completo**: Enfoque en proceso comercial interno de 10Code, no gestión masiva de clientes
- **Integración con estimación**: Diseñado para conectar con sistema de estimación (versión sin ML en MVP)
- **ML futuro**: Preparado para funcionalidades de cluster/etiquetado automático en fases posteriores
- **Asignación de Mayor Seller**: Campo preparado para asignar vendedor principal a oportunidades

**Referencia técnica**: Ver FSD de Módulo Comercial para detalles de estados del funnel, validaciones y conversión a proyectos.

---

### 4.4 Módulo: Producción (Gestión de Proyectos)

#### 4.4.1 Propósito

Sistema central de gestión de proyectos de desarrollo, que cubre desde la planificación inicial hasta la ejecución y seguimiento, con soporte para metodologías ágiles y tradicionales.

#### 4.4.2 Valor de Negocio

- **Gestión multi-equipo**: Coordinación eficiente de múltiples proyectos y equipos compartidos
- **Flexibilidad metodológica**: Adaptable a Scrum, Kanban, Waterfall o modelos híbridos
- **Visibilidad de progreso**: Dashboards en tiempo real del estado de proyectos
- **Trazabilidad completa**: Desde requisito inicial hasta entrega con historial de cambios
- **Base para rentabilidad**: Datos de ejecución alimentan análisis financiero

#### 4.4.3 Funcionalidades Principales

##### Planificación de Proyectos

- **Creación desde oferta**: Conversión automática de oportunidad cerrada a proyecto activo
- **Configuración flexible**: Selección de metodología (Scrum, Kanban, Waterfall, híbrido)
- **Definición de estructura**: Épicas, sprints, fases, hitos según metodología
- **Asignación de equipo**: Vinculación de personas y equipos con % de dedicación
- **Integración con GitHub**: Conexión con repositorios de código del proyecto
- **Documentación de proyecto**: Vinculación con carpeta de Google Drive del cliente

##### Gestión de Backlog

- **Épicas e Historias de Usuario**: Jerarquía de requisitos con descripción y criterios de aceptación
- **Tareas técnicas**: Desglose de historias en tareas implementables
- **Estimación en horas**: Rangos de esfuerzo por historia/tarea
- **Priorización visual**: Drag & drop para reordenar backlog por valor/urgencia
- **Estados**: Backlog → Ready → In Progress → Review → Done
- **Vinculación con diseño**: Adjuntar mockups, prototipos (integración Figma posterior)

##### Tableros Kanban

- **Tableros configurables**: Columnas personalizables según workflow del equipo
- **Gestión visual**: Arrastrar tareas entre estados
- **Filtros múltiples**: Por asignee, prioridad, tipo, etiquetas
- **Límites WIP**: (Work In Progress) configurables por columna
- **Vistas por equipo/persona**: Filtrado de tareas relevantes para cada rol

##### Seguimiento de Sprints (Scrum)

- **Planificación de sprint**: Selección de historias desde backlog con capacidad del equipo
- **Sprint activo**: Vista del sprint en curso con progreso diario
- **Burndown charts**: Visualización de trabajo restante vs. tiempo
- **Ceremonias**: Registro de daily stand-ups, retrospectivas, reviews
- **Velocity tracking**: Medición de capacidad histórica del equipo

##### Registro de Tiempo y Progreso

- **Imputación de horas a tareas**: Registro de tiempo trabajado vinculado a tareas específicas
- **Comentarios de progreso**: Descripción de trabajo realizado en cada sesión
- **Integración con commits**: Referencia a commits de GitHub vinculados a tareas
- **Reportes de sucesos**: Resúmenes de avances para comunicación con cliente
- **Autoaprobación básica**: Validación de horas imputadas por leads/gestores

##### Documentación de Proyecto

- **Actas de entrega**: Documentación de hitos completados
- **Certificaciones de avances**: Para proyectos con facturación por hitos
- **Base de conocimiento por proyecto**: Centralización de documentación técnica y funcional
- **Control de versiones**: Historial de cambios en documentos clave

##### Gestión Multi-Equipo

- **Asignación matricial**: Personas pueden trabajar en múltiples proyectos simultáneamente
- **Merge visual**: Iconos/colores diferenciando equipos en vistas consolidadas
- **Capacidad compartida**: Respeto de % de dedicación por proyecto
- **Priorización entre proyectos**: Coordinación de recursos compartidos

#### 4.4.4 Integraciones Clave

- **GitHub**:
  - Vinculación de repositorios a proyectos
  - Referencia de commits en tareas
  - Validación de commits diarios (norma 10Code)
- **Google Drive**: Carpetas de documentación por proyecto/cliente
- **Discord**: Notificaciones de cambios críticos, bloqueos, alertas

#### 4.4.5 Consideraciones Especiales

- **Versión simplificada de Jira**: Enfoque en lo esencial para equipos pequeños/medianos
- **No es herramienta de código**: Se integra con GitHub pero no reemplaza Git
- **Preparado para RAG futuro**: Estructura pensada para futuro chatbot de documentación de proyecto
- **Commits diarios obligatorios**: El sistema puede verificar cumplimiento de norma 10Code de commit diario

**Referencia técnica**: Ver FSD de Gestión de Proyectos para detalles de estados, transiciones, validaciones y arquitectura de backlog.

---

### 4.5 Módulo: Planificación y Disponibilidad de Recursos

#### 4.5.1 Propósito

Herramienta centralizada para visualizar, gestionar y optimizar la asignación de recursos humanos entre múltiples proyectos, con capacidad de simulación y detección proactiva de conflictos.

#### 4.5.2 Valor de Negocio

- **Visibilidad de carga**: Vista consolidada de ocupación de cada persona/equipo
- **Prevención de sobreasignación**: Alertas cuando recursos superan 100% de capacidad
- **Optimización de planificación**: Identificación de disponibilidad para nuevos proyectos
- **Simulación de escenarios**: Prueba de reasignaciones antes de confirmar cambios
- **Impacto en rentabilidad**: Maximización de utilización de recursos sin saturación

#### 4.5.3 Funcionalidades Principales

##### Visualización de Asignaciones

- **Vista de calendario (tipo Gantt)**: Timeline de asignaciones por persona y proyecto
- **Porcentajes de dedicación**: Visualización clara de % asignado a cada proyecto
- **Identificación visual de conflictos**: Código de colores para sobreasignación (>100%)
- **Filtros múltiples**: Por departamento, equipo, rol, proyecto, fechas
- **Vista consolidada empresa**: Ocupación global de toda la plantilla

##### Gestión de Capacidad

- **Cálculo automático**: Horas disponibles considerando jornada, ausencias, vacaciones
- **Capacidad por proyecto**: Distribución de horas disponibles entre asignaciones
- **Histórico de utilización**: Análisis de ocupación real vs. planificada
- **Alertas de baja utilización**: Detección de recursos infrautilizados
- **Proyección futura**: Visualización de disponibilidad en próximos meses

##### Reasignación de Recursos

- **Drag & drop**: Arrastrar personas entre proyectos de forma visual
- **Validación automática**: Verificación de disponibilidad antes de confirmar
- **Simulación de cambios**: "Qué pasaría si..." antes de aplicar reasignaciones
- **Flujo de aprobación**: Confirmación de director de operaciones para cambios significativos
- **Impacto en cascada**: Visualización de efecto en otros proyectos afectados

##### Planificación a Futuro

- **Contrataciones planificadas**: Proyección de necesidades de personal
- **Reservas de capacidad**: Bloqueo de disponibilidad para proyectos futuros
- **Análisis de tendencias**: Identificación de patrones de demanda de recursos
- **Ausencias previstas**: Consideración de vacaciones y ausencias planificadas

##### Herramienta de Calendario Centralizado

- **Calendario global**: Visualización de eventos, sprints, hitos, ausencias
- **Calendario por proyecto**: Vista filtrada de fechas relevantes del proyecto
- **Sincronización básica**: Integración con Google Calendar corporativo
- **Funcionalidad tipo Calendly (futuro)**: Reserva simplificada de disponibilidad

#### 4.5.4 Casos de Uso Clave

##### **Caso 1: Nuevo proyecto requiere recursos**

1. Director de Operaciones busca disponibilidad en vista de calendario
2. Identifica personas con capacidad libre en fechas requeridas
3. Simula asignación arrastrando recursos a nuevo proyecto
4. Valida que no genera conflictos en otros proyectos
5. Confirma asignación que se refleja en todos los módulos

##### **Caso 2: Sobreasignación detectada**

1. Sistema alerta que Desarrollador X está asignado al 120%
2. Gestor revisa proyectos afectados
3. Ajusta porcentajes de dedicación o reasigna tareas
4. Valida que nueva distribución no genera nuevos conflictos

##### **Caso 3: Planificación de vacaciones**

1. Empleado solicita vacaciones en módulo RR.HH.
2. Sistema detecta proyectos afectados por la ausencia
3. Alerta a gestores de proyecto correspondientes
4. Gestores ajustan planificación considerando la ausencia

#### 4.5.5 Integraciones Clave

- **Módulo RR.HH.**: Datos de capacidad, ausencias, vacaciones
- **Módulo Producción**: Asignaciones actuales de proyectos
- **Google Calendar**: Sincronización de eventos corporativos

#### 4.5.6 Consideraciones Especiales

- **No permite sobreasignación >100% sin autorización**: Validación estricta por defecto
- **Respeta pertenencia múltiple a equipos**: Un recurso puede estar en varios equipos con diferentes %
- **Preparado para machine learning futuro**: Estructura pensada para predicción de necesidades

**Referencia técnica**: Ver FSD de Planificación de Recursos para detalles de algoritmos de validación y arquitectura de simulación.

---

### 4.6 Módulo: Documentación (Gestión Documental)

#### 4.6.1 Propósito

Sistema centralizado de gestión documental para almacenar, organizar y acceder a toda la documentación generada en la empresa, con integración nativa con Google Drive corporativo.

#### 4.6.2 Valor de Negocio

- **Centralización**: Única fuente de verdad para documentación corporativa y de proyectos
- **Trazabilidad**: Vinculación directa entre documentos y elementos del sistema (proyectos, ofertas, etc.)
- **Eficiencia**: Templates reutilizables para documentos recurrentes
- **Cumplimiento**: Almacenamiento estructurado de contratos y documentos legales
- **Colaboración**: Aprovecha infraestructura existente de Google Workspace

#### 4.6.3 Funcionalidades Principales

##### Gestión de Carpetas en Google Drive

- **Estructura automática**: Creación de carpetas por proyecto/cliente en Google Drive
- **Permisos sincronizados**: Asignación automática de permisos según roles en el sistema
- **Navegación integrada**: Acceso a carpetas de Drive desde contexto del proyecto en la intranet
- **Vinculación bidireccional**: Referencias desde documentos de Drive a elementos del sistema

##### Editor Markdown Integrado (Básico en MVP)

- **Edición de documentos simples**: Markdown para documentación técnica ligera
- **Preview en tiempo real**: Vista previa mientras se edita
- **Sintaxis destacada**: Coloreado de sintaxis para legibilidad
- **Exportación**: Guardado en Drive o descarga local

##### Sistema de Templates

- **Plantillas reutilizables**: Templates para documentos comunes:
  - Ofertas comerciales por tipo de servicio
  - Contratos (Fixed Price, SLA, Time & Materials)
  - Actas de reunión
  - Informes de avance de proyecto
  - Documentación técnica estándar
- **Gestión de plantillas**: Creación, edición y versionado de templates
- **Variables dinámicas**: Campos que se rellenan automáticamente (cliente, fecha, proyecto, etc.)
- **Generación desde template**: Creación rápida de documentos pre-rellenados

##### Documentación por Proyecto

- **Repositorio de proyecto**: Centralización de todos los documentos relacionados
- **Categorización**: Organización por tipo (contratos, requisitos, técnica, entregas)
- **Búsqueda**: Localización rápida de documentos por nombre, contenido, fecha
- **Control de versiones básico**: Historial de versiones en Drive
- **Vinculación con backlog**: Adjuntar documentos a épicas, historias, tareas

##### Markdown → PDF (Investigación)

- **Conversión automática**: Transformación de documentos Markdown a PDF profesionales
- **Estilos corporativos**: Aplicación de identidad visual de 10Code
- **Generación bajo demanda**: Exportación PDF cuando se necesita compartir externamente

#### 4.6.4 Integraciones Clave

- **Google Drive**: Integración nativa y profunda con almacenamiento corporativo
- **Gmail**: Envío de documentos generados directamente desde el sistema

#### 4.6.5 Consideraciones Especiales

- **No reemplaza Drive**: Complementa y estructura el uso de Google Drive, no lo sustituye
- **Markdown como estándar interno**: Para documentación técnica y versionable
- **Preparado para RAG futuro**: Estructura pensada para chatbot que consulte documentación
- **Contratos firmados**: Integración futura con sistema de firma electrónica

**Referencia técnica**: Ver FSD de Gestión Documental para detalles de integración con Google Drive API y arquitectura de templates.

---

### 4.7 Módulo: Admin y Dirección (Dashboards)

#### 4.7.1 Propósito

Cuadros de mando ejecutivos que consolidan KPIs críticos de todos los módulos, proporcionando visibilidad en tiempo real para toma de decisiones estratégicas.

#### 4.7.2 Valor de Negocio

- **Visión consolidada**: Un solo lugar para todos los indicadores clave de la empresa
- **Decisiones informadas**: Datos en tiempo real para dirección y heads
- **Detección temprana**: Alertas proactivas de desviaciones y problemas
- **Transparencia**: Visibilidad de métricas relevantes para cada rol
- **Análisis de tendencias**: Comparación histórica y proyecciones

#### 4.7.3 Funcionalidades Principales

##### Dashboard Financiero y Tesorería

**Propósito**: Control de rentabilidad, facturación y costes

**KPIs principales**:

- Ingresos vs. Presupuesto (mensual, trimestral, anual)
- Rentabilidad por proyecto (margen bruto, costes vs. facturado)
- Proyección de facturación (pipeline + proyectos activos)
- Costes de personal (salarios, Seguridad Social)
- Tesorería proyectada (cobros esperados vs. gastos previstos)
- Facturas pendientes de cobro/pago
- Ratios financieros (ROI, margen neto)

**Integración**: ODOO para datos de facturas, gastos y nóminas

##### Dashboard Comercial

**Propósito**: Visibilidad del pipeline de ventas y conversión

**KPIs principales**:

- Pipeline por etapa (volumen y valor)
- Tasa de conversión por fase del funnel
- Tiempo medio de cierre
- Valor promedio de oportunidad
- Ofertas enviadas vs. aceptadas
- Proyección de ventas (weighted pipeline)
- Top clientes/oportunidades
- Performance por comercial

##### Dashboard de Productividad y Proyectos

**Propósito**: Seguimiento de ejecución y eficiencia operativa

**KPIs principales**:

- Proyectos activos vs. finalizados
- Horas facturables vs. no facturables (por proyecto y global)
- Utilización de recursos (% capacidad usada)
- Burndown agregado de sprints activos
- Velocidad promedio de equipos
- Tareas completadas vs. planificadas
- Bloqueos y impedimentos activos
- On-time delivery rate

##### Dashboard de RR.HH

**Propósito**: Gestión de personas y capacidad

**KPIs principales**:

- Plantilla actual vs. objetivo
- Ausencias y vacaciones (actuales y proyectadas)
- Tasa de incidencias de fichaje
- Horas trabajadas vs. esperadas
- Distribución de carga de trabajo
- Rotación de personal (si aplica)
- Capacidad disponible para nuevos proyectos
- Evaluaciones de desempeño (futuro)

##### Vistas Consolidadas por Departamento

- **Vista por equipo**: Métricas específicas de cada equipo vertical/horizontal
- **Vista por proyecto**: Dashboard individual por proyecto activo
- **Comparativas**: Benchmarks entre proyectos, equipos, períodos

##### Configuración de Dashboards

- **Dashboards personalizables**: Cada rol ve KPIs relevantes para su responsabilidad
- **Configuración de widgets**: Selección de métricas a visualizar
- **Filtros temporales**: Vista diaria, semanal, mensual, trimestral, anual
- **Alertas configurables**: Umbrales personalizados para notificaciones
- **Exportación**: Descarga de reportes en PDF/Excel

#### 4.7.4 Integraciones Clave

- **Todos los módulos internos**: Extracción de datos de cada módulo
- **ODOO**: Datos financieros, facturas, gastos, nóminas
- **GitHub**: Métricas de commits, actividad de desarrollo (futuro)

#### 4.7.5 Consideraciones Especiales

- **Actualización en tiempo real**: Datos refrescados continuamente
- **Histórico**: Capacidad de análisis de tendencias temporales
- **Permisos estrictos**: Información financiera sensible con acceso restringido
- **Performance**: Optimización de consultas para dashboards ágiles
- **Machine Learning futuro**: Preparado para analytics predictivo y detección de anomalías

**Referencia técnica**: Ver FSD de Dashboards para detalles de arquitectura de agregación de datos y optimización de queries.

---

### 4.8 Módulo: Sistema de Estimación de Proyectos

#### 4.8.1 Propósito

Herramienta para generar estimaciones de esfuerzo en proyectos de desarrollo, democratizando la capacidad de estimar y reduciendo dependencia de perfiles técnicos senior.

#### 4.8.2 Valor de Negocio

- **Democratización**: Equipos comerciales pueden generar estimaciones iniciales robustas
- **Consistencia**: Metodología estandarizada de estimación en toda la empresa
- **Velocidad**: Reducción de tiempo desde requisitos hasta oferta con estimación
- **Trazabilidad**: Historial completo de estimaciones vs. ejecución real
- **Base para mejora continua**: Datos para refinar precisión (ML futuro)

#### 4.8.3 Alcance en MVP: Versión Base sin Machine Learning

En la fase MVP, el sistema de estimación se implementa con una **versión simplificada basada en directrices y componentes estándares**, **sin algoritmos de Machine Learning**.

##### Biblioteca de Componentes Estándares

- **Catálogo de componentes**: Listado de elementos comunes en proyectos (login, CRUD, dashboard, API REST, etc.)
- **Valores de referencia**: Horas estimadas por componente basadas en experiencia histórica
- **Categorización**: Frontend, Backend, Diseño, Infraestructura, Testing
- **Factores de ajuste**: Multiplicadores por complejidad (simple, media, alta)
- **Gestión de biblioteca**: CRUD de componentes con valores actualizables

##### Proceso de Estimación Guiado

- **Wizard de estimación**: Flujo paso a paso para comerciales
  1. Selección de tipo de proyecto (web, móvil, SaaS, etc.)
  2. Selección de componentes necesarios desde biblioteca
  3. Ajuste de complejidad por componente
  4. Aplicación de factores contextuales (equipo nuevo, tecnología desconocida, cliente complejo)
  5. Generación de estimación agregada
- **Directrices de IA**: Uso de prompts a LLM para asistencia en clasificación
  - Análisis de descripción de requisitos
  - Sugerencia de componentes aplicables
  - Identificación de riesgos comunes
- **Refinamiento técnico**: Posibilidad de ajuste posterior por perfiles técnicos

##### Intervalos de Confianza Simples

- **Rangos por componente**: Mínimo-Esperado-Máximo
- **Agregación con buffer**: Suma con factores de contingencia configurables
- **Visualización clara**: Presentación de rango en ofertas (ej. 120-150h)

##### Vinculación con Módulo Comercial

- **Integración fluida**: Estimación directamente desde oportunidad
- **Generación de ofertas**: Transformación automática de estimación a oferta con precio
- **Feedback loop**: Registro de estimación vs. real cuando proyecto finaliza

#### 4.8.4 Futuro: Machine Learning (Fase 2+)

**Si se valida necesidad** tras uso de versión base, se implementará:

- Modelos de predicción de esfuerzo (Gradient Boosting)
- Cálculo de intervalos de confianza matemáticos (Quantile Regression)
- Clasificación automática de requisitos (BERT fine-tuned)
- Detección de anomalías en estimaciones
- Aprendizaje continuo con datos de ejecución real

#### 4.8.5 Consideraciones Especiales

- **No es herramienta de planificación**: Genera estimación de esfuerzo, no cronograma detallado
- **Requiere disciplina**: Valor depende de actualización continua de biblioteca de componentes
- **Mejora incremental**: Precisión aumenta con feedback de proyectos reales
- **Preparado para ML**: Arquitectura pensada para integración futura de modelos

**Referencia técnica**: Ver FSD de Sistema de Estimación para detalles de biblioteca de componentes, algoritmos de agregación y prompts de IA.

---

## 5. Requisitos No Funcionales

### 5.1 Rendimiento

- **Tiempo de respuesta**: < 2 segundos para operaciones comunes, < 5 segundos para dashboards complejos
- **Escalabilidad**: Soportar hasta 50 usuarios concurrentes sin degradación
- **Carga de datos**: Optimización de queries con select_related/prefetch_related en Django
- **Dashboards**: Cache de métricas agregadas con actualización cada 5 minutos (configurables)

### 5.2 Seguridad

- **Autenticación**: OAuth exclusivamente con Google Workspace (@10code.es)
- **Autorización**: RBAC granular con permisos por módulo y acción
- **HTTPS**: Comunicaciones cifradas en producción (TLS 1.2+)
- **Datos sensibles**: Encriptación de información confidencial (salarios, datos médicos)
- **Sesiones**: Timeout configurable (por defecto 8 horas inactividad)
- **Auditoría**: Logging de acciones críticas (fichajes, cambios financieros, modificaciones de permisos)
- **GDPR**: Cumplimiento de protección de datos, derecho al olvido, portabilidad

### 5.3 Usabilidad

- **Desktop-first, mobile-friendly**: Optimizado para escritorio, usable en móvil (especialmente fichaje)
- **Navegación contextual**: Acceso rápido a elementos relacionados entre módulos
- **Feedback inmediato**: Notificaciones claras de acciones completadas o errores
- **Accesos rápidos**: Shortcuts y favoritos basados en rol
- **Internacionalización**: Preparado para múltiples idiomas (inicialmente Español)
- **Accesibilidad**: Cumplimiento básico de WCAG 2.1 (contraste, navegación por teclado)

### 5.4 Mantenibilidad

- **Arquitectura monolítica modular**: Separación clara de responsabilidades por Django apps
- **Domain-Driven Design**: Apps organizadas por dominios de negocio
- **Service Layer Pattern**: Lógica de negocio en capa de servicios, no en views
- **Testing**: Cobertura mínima 70% en lógica crítica (pytest para backend)
- **Documentación**: Código autodocumentado, docstrings en funciones complejas
- **Estándares**: Adherencia a PEP8, linting con ruff, formateo con black

### 5.5 Disponibilidad

- **Objetivo uptime**: 99% (MVP), 99.9% (producción madura)
- **Backups**: Diarios automáticos de base de datos con retención 30 días
- **Recuperación**: RTO < 4 horas, RPO < 24 horas
- **Monitoreo**: Logs centralizados, alertas de errores críticos

### 5.6 Compatibilidad

- **Navegadores**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+ (últimas 2 versiones)
- **Resoluciones**: Mínimo 1366x768 (diseño responsive)
- **Móvil**: iOS 14+, Android 10+ para funciones críticas (fichaje)

---

## 6. Integraciones Clave

### 6.1 Integraciones Críticas (MVP)

#### GitHub

**Propósito**: Validación de commits diarios, vinculación de código a tareas

**Funcionalidades**:

- Vinculación de repositorios a proyectos
- Webhook para recepción de commits
- Validación de commit diario por desarrollador (norma 10Code)
- Referencia de commits en tareas del backlog
- Estadísticas básicas de actividad de desarrollo

**Tipo de integración**: Webhooks + GitHub API

#### ODOO

**Propósito**: Datos financieros, facturas, gastos, nóminas para dashboards

**Funcionalidades**:

- Importación de facturas emitidas/recibidas
- Datos de nóminas para cálculo de costes de personal
- Gastos por proyecto
- Sincronización periódica (diaria/semanal)

**Tipo de integración**: API REST de ODOO (lectura prioritaria)

#### Google Drive

**Propósito**: Almacenamiento estructurado de documentación

**Funcionalidades**:

- Creación automática de estructura de carpetas (proyecto/cliente)
- Gestión de permisos sincronizados con roles del sistema
- Navegación integrada desde intranet a Drive
- Listado de archivos en contexto de proyecto
- Subida/descarga de documentos

**Tipo de integración**: Google Drive API v3

#### Gmail (Google Workspace)

**Propósito**: Envío de notificaciones y comunicaciones

**Funcionalidades**:

- Envío de emails automáticos (alertas, notificaciones)
- Plantillas de email para comunicaciones estándar
- Registro de emails enviados desde el sistema

**Tipo de integración**: Gmail API / SMTP

### 6.2 Integraciones Secundarias (Post-MVP)

#### Discord

**Propósito**: Notificaciones automatizadas a canales de equipo

**Funcionalidades**:

- Webhooks para alertas críticas (bloqueos, fechas límite)
- Notificaciones de eventos de proyecto (deploy, PR merged)
- Comunicados generales de empresa

**Tipo de integración**: Discord Webhooks (simple y efectivo)

**Prioridad**: Antes que Figma, más sencillo de implementar

#### Figma (Futuro)

**Propósito**: Vinculación de diseños a historias de usuario

**Funcionalidades**:

- Embedding de prototipos en historias
- Sincronización de cambios en diseños
- Notificaciones de actualizaciones de diseño

**Tipo de integración**: Figma API / Webhooks

**Prioridad**: Posterior, evaluar necesidad real

### 6.3 Consideraciones de Integraciones

- **Resiliencia**: Fallos en integraciones externas no deben bloquear funcionalidad core
- **Reintentos**: Políticas de retry para APIs externas con exponential backoff
- **Logging**: Registro detallado de llamadas a APIs externas para debugging
- **Rate limiting**: Respeto de límites de APIs externas
- **Configurabilidad**: Integraciones activables/desactivables por configuración

---

## 7. Restricciones y Consideraciones

### 7.1 Restricciones Técnicas

- **Stack tecnológico fijo**: Django 5 + Inertia.js + React + PostgreSQL (decisión arquitectónica del SAD)
- **Autenticación exclusiva**: Solo Google OAuth con dominio @10code.es, sin otras opciones
- **Monolito**: No arquitectura de microservicios, al menos en MVP
- **Desarrollo solo**: Un único desarrollador (Juanje) en fase MVP
- **Sin equipo QA**: Testing debe estar embebido en proceso de desarrollo

### 7.2 Restricciones de Negocio

- **Uso interno**: Sistema para 10Code, no diseñado inicialmente como producto comercial
- **Presupuesto limitado**: Priorización estricta de features, evitar sobre-ingeniería
- **Time to market**: Necesidad de valor entregable rápido, iteraciones cortas
- **Datos sensibles**: Información financiera y personal requiere máxima protección

### 7.3 Dependencias Externas

- **Google Workspace**: Dependencia crítica para autenticación, email, almacenamiento
- **ODOO**: Datos financieros dependen de mantenimiento de integración
- **GitHub**: Asume uso de GitHub para control de versiones (no GitLab u otros)
- **Normativa legal**: Cumplimiento de legislación española de protección de datos y laboral

### 7.4 Asunciones

- **Conectividad**: Usuarios tienen acceso estable a internet
- **Infraestructura Google**: Google Workspace operativo y con licencias activas
- **Disciplina de equipo**: Cumplimiento de normas (fichaje, commits diarios, imputación)
- **Cultura de adopción**: Disposición del equipo a usar nueva herramienta

### 7.5 Riesgos Identificados

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| Baja adopción por equipo | Media | Alto | Training, involucración temprana, UX simple |
| Cambios en APIs externas (Google, GitHub) | Baja | Alto | Abstracciones, versionado de APIs, monitoreo |
| Sobrecarga del desarrollador único | Alta | Alto | Priorización estricta, uso de agentes IA, documentación clara |
| Problemas de rendimiento con crecimiento | Media | Medio | Optimización proactiva, monitoring, escalabilidad horizontal (futuro) |
| Cambios en normativa legal | Baja | Alto | Diseño flexible, seguimiento legislativo, auditorías |

---

## 8. Priorización y Roadmap de Desarrollo

### 8.1 Fases de Implementación

#### Fase 0: Fundamentos (Semanas 1-2)

- Configuración de proyecto Django + Inertia.js
- Estructura base de apps Django
- Autenticación SSO con Google
- Diseño de base de datos inicial
- Setup de Docker y entorno de desarrollo

#### Fase 1: MVP Core (Semanas 3-10)

**Prioridad 1 (Crítico)**:

1. **RR.HH. y Control Horario** (Semanas 3-5)
   - Fichaje digital con validaciones
   - Gestión de ausencias y vacaciones
   - Dashboard básico de capacidad

2. **Comercial + CRM Básico** (Semanas 6-7)
   - Pipeline de oportunidades
   - Gestión de ofertas
   - Conversión a proyectos

3. **Producción - Gestión de Proyectos** (Semanas 8-10)
   - Backlog de épicas/historias
   - Tableros Kanban
   - Registro básico de tiempo en tareas

**Prioridad 2 (Importante)**:

4. **Planificación de Recursos** (Semanas 11-12)
   - Vista de calendario de asignaciones
   - Detección de sobreasignación

5. **Documentación** (Semanas 13-14)
   - Integración con Google Drive
   - Sistema básico de templates

6. **Dashboards Admin** (Semanas 15-16)
   - Dashboard financiero básico
   - Dashboard de productividad

#### Fase 2: Refinamiento y Expansión (Post-MVP)

- Sistema de estimación con ML (si se valida necesidad)
- Integraciones avanzadas (Discord, Figma)
- Mejoras en dashboards (analytics predictivo)
- Optimizaciones de rendimiento
- Funcionalidades avanzadas de reportes

#### Fase 3: Módulos Futuros (Largo Plazo)

- Módulo de Formación y Noticias
- Módulo de Captación de Talento
- Gamificación y badges
- Chatbot RAG para documentación
- Capacidades de IA generativa

### 8.2 Criterios de Priorización

1. **Valor de negocio**: ¿Resuelve un dolor crítico actual?
2. **Dependencias**: ¿Bloquea desarrollo de otros módulos?
3. **Riesgo técnico**: ¿Validamos supuestos arquitectónicos tempranos?
4. **Complejidad**: ¿Podemos entregar valor rápido?
5. **Adopción**: ¿Facilita el uso del resto del sistema?

### 8.3 Definición de "Completado" por Fase

**Fase 1 MVP Completado cuando**:

- ✅ Control horario operativo con cumplimiento normativo
- ✅ Pipeline comercial funcional con conversión a proyectos
- ✅ Gestión básica de proyectos con backlog y tableros
- ✅ Visualización de asignaciones de recursos
- ✅ Integración con Google Drive operativa
- ✅ Dashboards con KPIs críticos visibles
- ✅ 10 usuarios piloto usando el sistema diariamente
- ✅ Documentación básica de usuario disponible

---

## 9. Métricas de Éxito

### 9.1 KPIs de Adopción (Fase MVP)

- **Tasa de adopción**: >80% del equipo usando el sistema activamente tras 2 meses
- **Fichajes diarios**: >95% de cumplimiento de fichaje sin incidencias
- **Imputación de tiempo**: >90% de horas imputadas dentro de SLA (10:00 día siguiente)
- **Proyectos activos**: 100% de proyectos nuevos gestionados en la plataforma

### 9.2 KPIs de Eficiencia Operativa

- **Reducción de tiempo en reporting**: -30% de horas dedicadas a generar reportes manuales
- **Visibilidad de recursos**: Tiempo para identificar disponibilidad <5 minutos (vs. horas antes)
- **Ciclo comercial**: -20% de tiempo desde oportunidad hasta oferta
- **Detección de problemas**: Identificación proactiva de sobreasignación antes de que genere retrasos

### 9.3 KPIs de Calidad de Datos

- **Integridad de datos**: <2% de registros incompletos o inconsistentes
- **Trazabilidad**: 100% de proyectos con documentación vinculada
- **Actualización de información**: Dashboards reflejando datos <15 minutos de antigüedad

### 9.4 KPIs Técnicos

- **Disponibilidad**: >99% uptime en horario laboral
- **Rendimiento**: <2s tiempo de respuesta p95 en operaciones comunes
- **Errores**: <0.5% tasa de error en operaciones críticas
- **Cobertura de tests**: >70% en lógica de negocio crítica

### 9.5 Evaluación de Éxito Post-6 Meses

El MVP se considerará exitoso si se cumplen:

1. ✅ >80% de adopción activa por el equipo
2. ✅ Cumplimiento normativo 100% en control horario
3. ✅ Reducción medible de tiempo en tareas administrativas
4. ✅ Mejora en visibilidad (encuesta de satisfacción >7/10)
5. ✅ Zero critical bugs en producción por >30 días
6. ✅ Decisión informada sobre implementar ML o mantener estimación base

---

## 10. Glosario y Terminología

### 10.1 Términos Específicos del Dominio

- **Épica**: Agrupación de alto nivel de funcionalidades relacionadas, típicamente con 20-80h de desarrollo
- **Historia de Usuario**: Requisito funcional desde perspectiva del usuario, implementable en 4-16h
- **Sprint**: Iteración de 1-2 semanas en metodología Scrum
- **Backlog**: Lista priorizada de épicas, historias y tareas pendientes
- **Burndown Chart**: Gráfico de trabajo restante vs. tiempo en un sprint
- **WIP (Work In Progress)**: Tareas en progreso, límite de cuántas pueden estar activas simultáneamente
- **Fichaje**: Registro de entrada/salida de jornada laboral
- **Imputación**: Asignación de horas trabajadas a tareas/proyectos específicos
- **Sobreasignación**: Cuando una persona tiene asignado >100% de su capacidad disponible
- **Pipeline**: Embudo de proceso comercial (leads → oportunidades → proyectos)
- **Funnel de ventas**: Visualización de oportunidades por etapa del proceso comercial
- **Fixed Price**: Modelo de proyecto con precio cerrado por alcance definido
- **Time & Materials**: Modelo de facturación por horas trabajadas
- **SLA (Service Level Agreement)**: Contrato de servicio con compromisos de respuesta/disponibilidad
- **Bolsa de Horas**: Paquete prepagado de horas de trabajo a consumir

### 10.2 Roles Específicos 10Code

- **Equipo Horizontal**: Equipo de ejecución de proyectos (desarrolladores, diseñadores)
- **Equipo Vertical**: Equipo de apoyo transversal (DevOps, QA, soporte)
- **Technical Lead**: Líder técnico de proyecto, responsable de arquitectura y calidad de código
- **Gestor de Proyecto**: Responsable de planificación, seguimiento y comunicación de proyecto

### 10.3 Términos Técnicos

- **Monolito Modular**: Arquitectura de aplicación única con separación lógica clara
- **Service Layer**: Capa de lógica de negocio separada de vistas y modelos
- **RBAC (Role-Based Access Control)**: Control de acceso basado en roles
- **SSO (Single Sign-On)**: Autenticación única corporativa
- **OAuth**: Protocolo de autenticación delegada (Google en nuestro caso)
- **Webhook**: Callback HTTP para notificaciones de eventos desde sistemas externos
- **ETL (Extract, Transform, Load)**: Proceso de extracción, transformación y carga de datos
- **RAG (Retrieval-Augmented Generation)**: Técnica de IA que combina búsqueda con generación

---

## 11. Referencias y Documentos Relacionados

### 11.1 Documentos de Diseño Técnico (A Desarrollar Post-PRD)

- **SAD (Solution Architecture Document)**: Arquitectura técnica detallada, decisiones de diseño, stack tecnológico, patrones implementados
- **FSDs (Feature Specification Documents)**: Especificaciones técnicas detalladas por módulo:
  - FSD - Módulo RR.HH. y Control Horario
  - FSD - Módulo Comercial + CRM
  - FSD - Módulo Gestión de Proyectos
  - FSD - Módulo Planificación de Recursos
  - FSD - Módulo Documentación
  - FSD - Módulo Dashboards
  - FSD - Sistema de Estimación
- **ADRs (Architecture Decision Records)**: Registro de decisiones arquitectónicas importantes tomadas durante el proyecto

### 11.2 Documentos de Referencia Existentes

- **Ideas_estructura_de_herramientas_de_intranet.md**: Boceto inicial de módulos (v1.0)
- **product-definition.md**: Definición de producto previa
- **epics-definition.md**: Épicas definidas en versión anterior
- **Guia_de_desarrollo_django_inertia.md**: Guía técnica de desarrollo
- **framework-metodologico-ogov.md**: Framework metodológico de trabajo

### 11.3 Normativas y Estándares

- **Normativa Española de Fichaje Digital 2025**: Real Decreto-ley 8/2019 sobre registro de jornada
- **RGPD (Reglamento General de Protección de Datos)**: UE 2016/679
- **WCAG 2.1**: Web Content Accessibility Guidelines
- **PEP 8**: Guía de estilo Python

### 11.4 Herramientas y Tecnologías

- **Django 5 Documentation**: <https://docs.djangoproject.com/>
- **Inertia.js Documentation**: <https://inertiajs.com/>
- **React Documentation**: <https://react.dev/>
- **PostgreSQL Documentation**: <https://www.postgresql.org/docs/>
- **Google Workspace API**: <https://developers.google.com/workspace>
- **GitHub API**: <https://docs.github.com/en/rest>

---

## 12. Control de Cambios del Documento

| Versión | Fecha | Autor | Cambios |
|---------|-------|-------|---------|
| 1.0 | 2024-11-14 | Juanje | Creación inicial del PRD definitivo |

---

## 13. Aprobaciones

Este documento requiere aprobación de:

- ✅ **Product Owner** (Juanje - 10Code): Aprobado para implementación
- 🔲 **Dirección Técnica**: Pendiente de validación arquitectónica (SAD)
- 🔲 **Dirección General**: Pendiente de aprobación de alcance y priorización

---

> **Fin del Documento PRD - Intranet 10Code v1.0**
>
> *Este PRD define el QUÉ y POR QUÉ del sistema. Los detalles de CÓMO se implementará técnicamente se desarrollarán en el SAD (Solution Architecture Document) y los FSDs (Feature Specification Documents) correspondientes.*
