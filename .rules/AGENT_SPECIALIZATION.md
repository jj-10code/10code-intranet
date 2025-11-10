# Arquitectura de Agentes Especializados

## Propósito del Documento

Este documento establece la arquitectura de múltiples agentes especializados para el desarrollo del Sistema de Gestión de Proyectos Integral de 10Code. Cada agente posee autonomía alta dentro de su dominio de especialización, operando bajo raíles arquitectónicos claramente definidos que garantizan coherencia y calidad en todo el proyecto.

La especialización por dominio permite que cada agente desarrolle expertise profundo en su área, mientras que los protocolos de coordinación aseguran que el sistema final sea cohesivo y mantenga integridad arquitectónica. Este enfoque maximiza la velocidad de desarrollo al permitir trabajo paralelo, minimiza conflictos al definir boundaries claros, y facilita la escalabilidad del equipo de desarrollo.

---

## Principios de Coordinación

### Autonomía con Raíles

Los agentes operan con alta autonomía para tomar decisiones técnicas dentro de su dominio, siempre que respeten los patrones arquitectónicos establecidos en los archivos de reglas del proyecto. Esta autonomía incluye decisiones sobre implementación de algoritmos, estructuración interna de código y optimizaciones específicas del dominio.

Los raíles arquitectónicos son no negociables. Incluyen el uso obligatorio del Service Layer Pattern, la separación entre Services y Selectors, la optimización de queries con select_related y prefetch_related, y el cumplimiento de los estándares de testing definidos. Estos raíles garantizan que el trabajo de múltiples agentes pueda integrarse sin fricción.

### Protocolo de Handoff

Cuando un agente necesita interactuar con código de otro dominio, debe hacerlo exclusivamente a través de las interfaces definidas en el Service Layer del dominio objetivo. Las importaciones directas de modelos entre dominios están prohibidas excepto para relaciones ForeignKey necesarias. Este protocolo previene acoplamiento fuerte y facilita la evolución independiente de cada módulo.

Los agentes deben documentar explícitamente todas las dependencias entre dominios. Cuando el Agente de Proyectos necesita funcionalidad del dominio de Recursos, debe documentar qué función del ResourceService está invocando y con qué parámetros. Esta trazabilidad es fundamental para debugging y mantenimiento futuro.

### Ownership y Responsabilidad

Cada agente es el único responsable de su dominio. El Agente de Control Horario es el único autorizado para modificar código en apps/timetracking/. Esta propiedad exclusiva previene conflictos y establece accountability clara. Cuando un bug aparece en control horario, sabemos exactamente qué agente debe investigarlo.

Los agentes deben mantener la calidad de su dominio. Esto incluye mantener cobertura de tests por encima del ochenta por ciento, documentar todas las funciones públicas del Service Layer, y refactorizar proactivamente cuando el código comience a mostrar síntomas de deuda técnica. La autonomía viene acompañada de responsabilidad.

---

## Especialización de Agentes

### Agente Core e Infraestructura

**Dominio**: apps/core/, config/, infraestructura compartida

**Responsabilidades Principales**

Este agente gestiona la columna vertebral técnica del proyecto. Desarrolla y mantiene los modelos abstractos base como TimestampedModel y SoftDeleteModel que todas las apps heredan. Implementa middleware personalizado para funcionalidades transversales como logging estructurado, manejo de excepciones globales y métricas de performance.

Configura y mantiene la infraestructura de Docker, incluyendo los archivos docker-compose para desarrollo y producción. Gestiona la configuración de Celery para tareas asíncronas y asegura que el sistema de caché con Redis esté correctamente configurado. Implementa comandos de gestión de Django que son útiles para múltiples dominios, como comandos de seed de base de datos para testing o scripts de migración de datos.

**Interfaces Expuestas**

Proporciona modelos abstractos que otros dominios heredan. Expone utilidades genéricas en apps/core/utils.py como funciones de formateo de fechas, helpers de validación reutilizables y decoradores comunes. Mantiene middleware que puede ser configurado por otros agentes según necesidades específicas.

**Handoffs Críticos**

Coordina con todos los agentes para asegurar que los modelos base satisfacen las necesidades de cada dominio. Cuando el Agente de Proyectos requiere auditoría automática de cambios, el Agente Core implementa un modelo abstracto AuditedModel que puede ser heredado. Esta coordinación bidireccional asegura que la infraestructura evoluciona según las necesidades reales del negocio.

---

### Agente de Autenticación y Usuarios

**Dominio**: apps/accounts/

**Responsabilidades Principales**

Gestiona todo el ciclo de vida de usuarios. Implementa la autenticación con Google OAuth restringida al dominio 10code.es mediante el CustomSocialAccountAdapter. Desarrolla el modelo User personalizado con campos específicos como employee_id, department, position y weekly_capacity que son fundamentales para la gestión de recursos.

Implementa el sistema de permisos a nivel de objeto. Desarrolla mixins y decoradores para verificación de permisos que otros agentes pueden reutilizar. Gestiona el perfil de usuario, incluyendo la carga y procesamiento de avatares, preferencias de notificación y configuración de dashboard personalizado.

**Interfaces Expuestas**

UserService expone funciones para operaciones sobre usuarios como create_user, update_profile, change_password y reset_password_request. UserSelector proporciona consultas optimizadas como get_users_by_department, get_available_team_members y search_users. Estos servicios son consumidos por prácticamente todos los demás dominios.

**Coordinación Especial**

Este agente trabaja estrechamente con el Agente de Recursos. Cuando un usuario es asignado a un proyecto, el UserService proporciona información de disponibilidad que el ResourceService utiliza para validar la asignación. Esta coordinación requiere contratos claros sobre qué información está disponible y en qué formato.

---

### Agente de Proyectos

**Dominio**: apps/projects/

**Responsabilidades Principales**

Implementa el núcleo de la gestión de proyectos. Desarrolla los modelos Project y ProjectMember con todas sus relaciones y validaciones. Implementa ProjectService con funciones complejas de creación de proyectos que incluyen validaciones de negocio, asignación automática del creador como Project Manager y disparo de notificaciones.

Gestiona el ciclo de vida completo de proyectos desde draft hasta completed o cancelled. Implementa lógica para cambios de estado con auditoría completa. Desarrolla funcionalidades de búsqueda y filtrado avanzado de proyectos con support para filtros por cliente, metodología, estado y búsqueda full-text en nombre y descripción.

**Interfaces Expuestas**

ProjectService expone create_project, update_project, change_project_status, assign_team_member, update_member_allocation y archive_project. ProjectSelector proporciona get_projects_list, get_project_detail, get_project_statistics y get_user_projects. Estas interfaces son consumidas intensivamente por los agentes de Backlog, Recursos y Reporting.

**Integraciones Clave**

Coordina con el Agente de Recursos para validar disponibilidad antes de asignar miembros. Se integra con el Agente de Backlog para proporcionar contexto de proyecto a épicas e historias. Trabaja con el Agente Financiero para cálculos de rentabilidad basados en horas tracked versus presupuesto.

---

### Agente de Backlog y Product Management

**Dominio**: apps/backlog/

**Responsabilidades Principales**

Implementa la gestión completa del backlog de producto. Desarrolla modelos Epic, UserStory y Task con su jerarquía y relaciones. Implementa funcionalidad de priorización mediante drag and drop con actualización de campo de orden. Gestiona criterios de aceptación, vinculación con diseños de Figma y estimación en horas.

Desarrolla tableros Kanban configurables con columnas personalizables por proyecto. Implementa lógica de transición de estados con validaciones. Gestiona sprints incluyendo capacidad del equipo, planning, y cálculo de velocity. Implementa burndown y burnup charts con datos en tiempo real.

**Interfaces Expuestas**

BacklogService expone create_epic, create_user_story, create_task, update_priority_order, move_to_column y assign_to_sprint. BacklogSelector proporciona get_project_backlog, get_sprint_tasks, get_epic_hierarchy y calculate_sprint_velocity. Estas funciones son consumidas principalmente por el Agente de Ejecución y Seguimiento.

**Reglas de Negocio Específicas**

El agente implementa validaciones como no permitir más de diez user stories en refinamiento simultáneo por proyecto, requerir criterios de aceptación antes de mover una historia a ready for development, y validar que la suma de estimaciones en un sprint no exceda la capacidad del equipo.

---

### Agente de Recursos y Capacidad

**Dominio**: apps/resources/

**Responsabilidades Principales**

Gestiona la asignación y optimización de recursos humanos. Implementa visualización de capacidad versus demanda con calendario tipo Gantt. Desarrolla algoritmos para detectar sobreasignaciones y subutilización. Implementa funcionalidad de reasignación mediante drag and drop con validaciones automáticas de disponibilidad.

Gestiona ausencias incluyendo vacaciones, bajas y días remotos. Implementa carry-over de vacaciones según normativa española. Calcula capacidad disponible considerando días festivos, ausencias planificadas y porcentajes de asignación a múltiples proyectos. Implementa simulación de escenarios antes de aplicar cambios de asignación.

**Interfaces Expuestas**

ResourceService expone assign_resource_to_project, update_allocation_percentage, request_vacation, approve_absence y simulate_assignment_impact. ResourceSelector proporciona get_resource_allocation_calendar, get_team_capacity, get_overallocated_resources y calculate_availability_percentage.

**Validaciones Críticas**

Este agente implementa la regla de negocio fundamental de no permitir asignaciones superiores al cien por ciento sin autorización especial. Valida que la suma de porcentajes de asignación de un usuario a múltiples proyectos no exceda su capacidad. Estas validaciones son críticas para la integridad de la planificación.

---

### Agente de Control Horario

**Dominio**: apps/timetracking/

**Responsabilidades Principales**

Implementa el sistema de fichaje digital cumpliendo la normativa española de 2025. Desarrolla funcionalidad de entrada y salida con cronómetro en tiempo real. Implementa autocierre automático al final de jornada con treinta minutos de gracia. Genera incidencias automáticas para fichajes olvidados o imputaciones faltantes.

Gestiona la imputación de tiempo a tareas con validaciones de mínimos diarios según perfil. Implementa el SLA de imputación antes de las diez de la mañana del día siguiente. Desarrolla flujos de aprobación para ediciones de fichajes con justificación obligatoria. Mantiene trazabilidad completa cumpliendo RGPD con almacenamiento de cuatro años.

**Interfaces Expuestas**

TimeTrackingService expone clock_in, clock_out, log_time_to_task, edit_entry_with_approval y generate_weekly_summary. TimeTrackingSelector proporciona get_user_daily_entries, get_pending_approvals, calculate_weekly_hours y get_missing_imputations.

**Motor de Reglas**

Este agente implementa un motor de reglas configurable que permite definir mínimos de horas por perfil, SLAs de imputación y configuraciones de autocierre. El motor es extensible para añadir nuevas reglas sin modificar código core. Esta flexibilidad es esencial dado que las regulaciones laborales pueden cambiar.

---

### Agente de Estimación y Machine Learning

**Dominio**: apps/estimation/

**Responsabilidades Principales**

Implementa el innovador sistema CEPF combinado con Machine Learning. Gestiona la biblioteca de componentes estándares con sus Puntos de Función asociados. Desarrolla algoritmos de ML incluyendo Gradient Boosting para predicción de esfuerzo, Quantile Regression Forests para intervalos de confianza y BERT fine-tuned para clasificación automática de requisitos.

Implementa el sistema de aprendizaje continuo que mejora los modelos con cada proyecto completado. Desarrolla detección de anomalías con Isolation Forest para identificar estimaciones atípicas. Gestiona intervalos de confianza matemáticamente fundamentados del ochenta, noventa y noventa y cinco por ciento.

**Interfaces Expuestas**

EstimationService expone create_estimation_from_components, run_ml_prediction, calculate_confidence_intervals, refine_estimation_with_technical_input y update_models_with_project_actuals. EstimationSelector proporciona get_component_library, get_historical_accuracy, get_similar_past_projects y analyze_estimation_risk.

**Democratización de Estimaciones**

Este agente implementa interfaces diferenciadas. El portal simplificado permite a comerciales crear estimaciones robustas sin conocimiento técnico profundo. La consola técnica permite a desarrolladores refinar estimaciones con detalles de implementación. Esta democratización es un valor diferencial clave del sistema.

---

### Agente Financiero

**Dominio**: apps/financial/

**Responsabilidades Principales**

Implementa el seguimiento financiero integral de proyectos. Gestiona presupuestos con comparación de planificado versus real en tiempo real. Calcula rentabilidad considerando horas tracked, tarifas horarias y costes de recursos. Implementa diferentes modelos de facturación incluyendo fixed price, time and materials, SLAs recurrentes y bolsas de horas.

Desarrolla alertas proactivas por desviaciones presupuestarias. Implementa control de bolsas de horas con notificaciones de agotamiento inminente. Gestiona hitos de facturación para proyectos fixed price. Genera reportes financieros con múltiples vistas según audiencia.

**Interfaces Expuestas**

FinancialService expone calculate_project_profitability, register_billing_event, update_budget, create_financial_alert y generate_invoice_data. FinancialSelector proporciona get_profitability_report, get_budget_utilization, get_billing_summary y analyze_cost_trends.

**Integraciones ERP**

Este agente implementa conectores para sistemas ERP como Odoo. Sincroniza datos de facturación, actualiza información de clientes y exporta datos para nóminas. Estas integraciones requieren coordinación estrecha con el Agente de Integraciones para mantener consistencia.

---

### Agente de Reporting y Business Intelligence

**Dominio**: apps/reporting/

**Responsabilidades Principales**

Implementa el sistema de dashboards personalizados y reportes avanzados. Desarrolla KPIs específicos por rol incluyendo métricas para directivos, gestores de proyecto, technical leads y miembros de equipo. Implementa visualizaciones interactivas con filtros dinámicos. Gestiona exportación de reportes en múltiples formatos.

Desarrolla capacidades de análisis predictivo utilizando datos históricos. Implementa detección de patrones y tendencias. Genera insights automáticos sobre utilización de recursos, precisión de estimaciones y riesgos de proyectos. Crea alertas inteligentes basadas en análisis de datos.

**Interfaces Expuestas**

ReportingService expone generate_dashboard_data, create_custom_report, schedule_recurring_report y calculate_predictive_metrics. ReportingSelector proporciona get_kpis_by_role, aggregate_cross_project_metrics, analyze_resource_utilization_trends y identify_at_risk_projects.

**Performance Crítico**

Este agente debe prestar especial atención a performance dado que maneja agregaciones sobre grandes volúmenes de datos. Implementa estrategias de cache agresivas, materialización de vistas para reportes frecuentes y procesamiento asíncrono con Celery para reportes pesados.

---

### Agente de Integraciones

**Dominio**: apps/integrations/

**Responsabilidades Principales**

Gestiona todas las integraciones con sistemas externos. Implementa conectores para Git, GitHub y GitLab con sincronización de commits, branches y pull requests. Desarrolla integración bidireccional con Discord para notificaciones y comandos. Implementa vinculación con Figma para asociar diseños a historias de usuario.

Gestiona webhooks tanto entrantes como salientes. Implementa colas de retry con backoff exponencial para robustez ante fallos temporales de servicios externos. Desarrolla logging exhaustivo de todas las interacciones con sistemas externos para troubleshooting. Implementa rate limiting para respetar límites de APIs externas.

**Interfaces Expuestas**

IntegrationService expone sync_repository_data, send_discord_notification, fetch_figma_design, register_webhook_handler y handle_incoming_webhook. IntegrationSelector proporciona get_integration_status, get_sync_history y analyze_integration_health.

**Manejo de Errores**

Este agente implementa estrategias sofisticadas de manejo de errores. Los fallos temporales disparan retries automáticos. Los fallos persistentes generan alertas. Los datos parcialmente sincronizados se marcan claramente para revisión manual. Esta robustez es crítica dado que el sistema opera con servicios externos impredecibles.

---

## Coordinación y Comunicación

### Reuniones de Sincronización

Los agentes participan en sincronizaciones periódicas para alinear trabajo y resolver dependencias. Estas sincronizaciones no son reuniones tradicionales sino protocolos de comunicación donde cada agente reporta su estado, identifica blockers y solicita información de otros dominios.

Cuando el Agente de Proyectos está desarrollando funcionalidad de asignación de equipo, solicita en sincronización que el Agente de Recursos exponga una función específica para validar disponibilidad. Esta solicitud es documentada y priorizada. El Agente de Recursos se compromete a entregar la interfaz en un plazo específico.

### Documentación de Contratos

Cada vez que un agente expone una nueva función pública en su Service Layer, debe documentar el contrato completo. Esto incluye parámetros esperados con sus tipos, valor de retorno, excepciones que puede lanzar y efectos secundarios que produce. Esta documentación es consumida por otros agentes y es crítica para evitar malentendidos.

Los cambios a contratos existentes requieren comunicación proactiva. Si el Agente de Usuarios necesita añadir un parámetro obligatorio a una función existente, debe notificar a todos los agentes consumidores. Idealmente, los cambios mantienen backward compatibility mediante parámetros opcionales con defaults razonables.

### Sistema de Issues y Tracking

Cuando un agente identifica un bug en el dominio de otro agente, crea un issue detallado. El issue incluye steps to reproduce, comportamiento esperado versus observado, y logs relevantes. El agente propietario del dominio afectado es responsable de investigar y resolver.

Los issues de coordinación entre dominios requieren participación de múltiples agentes. Un issue sobre sincronización de datos entre Proyectos y Recursos involucra a ambos agentes. Estos issues se resuelven mediante discusión colaborativa donde cada agente aporta contexto de su dominio.

---

## Estándares de Calidad

### Cobertura de Tests

Cada agente debe mantener mínimo ochenta por ciento de cobertura de tests en su dominio. Los tests incluyen unit tests de servicios y selectors, integration tests de views y end-to-end tests de flujos críticos. El CI/CD pipeline rechaza automáticamente código que reduzca la cobertura por debajo del umbral.

Los agentes escriben tests antes o simultáneamente con la implementación. Un service sin tests es código incompleto. Los tests documentan el comportamiento esperado y sirven como especificación ejecutable. Esta disciplina de testing es no negociable.

### Code Reviews

Aunque cada agente tiene ownership de su dominio, el código es revisado por otros agentes antes de merge. Las reviews verifican adherencia a patrones arquitectónicos, calidad de tests, claridad de documentación y ausencia de antipatrones. Esta revisión cruzada mantiene estándares consistentes en todo el proyecto.

Las reviews son constructivas y educativas. Cuando se identifica una oportunidad de mejora, se explica el por qué y se sugiere una alternativa. El objetivo es elevar la calidad colectiva del código y compartir conocimiento entre agentes.

### Refactoring Continuo

Los agentes son responsables de refactorizar proactivamente su dominio. Cuando el código comienza a mostrar code smells como funciones excesivamente largas, duplicación o complejidad ciclomática alta, el agente debe refactorizar antes de que el problema se agrave.

El refactoring no requiere aprobación especial siempre que mantenga los tests pasando y no cambie contratos públicos. Los refactorings que afectan interfaces requieren coordinación con agentes consumidores. Esta práctica de mejora continua previene acumulación de deuda técnica.

---

## Onboarding de Nuevos Agentes

### Proceso de Integración

Cuando un nuevo agente se incorpora al proyecto, inicia con un período de familiarización. Lee completamente los archivos de reglas del proyecto, incluyendo las reglas principales, arquitectura, patrones Django e Inertia. Estudia el código existente de su dominio asignado para entender el estado actual.

El nuevo agente recibe un dominio con complejidad moderada inicialmente. No se le asigna inmediatamente el dominio más crítico o complejo. Esta rampa de entrada gradual permite desarrollar expertise mientras minimiza riesgo. A medida que demuestra competencia, asume responsabilidades más complejas.

### Mentoring entre Agentes

El agente establecido en un dominio relacionado actúa como mentor del nuevo agente. Cuando un nuevo agente asume el dominio de Backlog, el Agente de Proyectos proporciona guidance sobre cómo interactuar efectivamente con ProjectService. Este mentoring acelera la curva de aprendizaje.

El mentoring incluye code reviews detallados en las primeras implementaciones. El mentor no solo señala problemas sino explica el razonamiento detrás de los patrones preferidos. Esta transferencia de conocimiento institucional es invaluable para mantener coherencia arquitectónica.

### Evolución de Expertise

Los agentes desarrollan expertise profundo en su dominio a lo largo del tiempo. Un agente que ha trabajado seis meses en el dominio de Estimación entiende sutilezas del sistema de ML que serían difíciles de documentar completamente. Esta expertise acumulada es un activo del proyecto.

La especialización no significa aislamiento. Los agentes rotan ocasionalmente entre dominios relacionados para mantener perspectiva amplia y prevenir silos de conocimiento. Esta rotación controlada balancea expertise profunda con comprensión sistémica.

---

## Escalabilidad del Modelo

### Añadir Nuevos Dominios

Cuando el proyecto crece y se identifican nuevos bounded contexts, se crean nuevos agentes especializados. El proceso incluye definir claramente el boundary del nuevo dominio, identificar sus interfaces con dominios existentes y asignar un agente responsable.

El nuevo dominio sigue exactamente la misma estructura que dominios existentes. Tiene su models, services, selectors, views y tests. Esta consistencia estructural facilita que cualquier agente pueda navegar y entender código de cualquier dominio cuando sea necesario.

### Subdivisión de Dominios

Si un dominio crece excesivamente en complejidad, puede subdividirse. El dominio original de Proyectos podría dividirse en ProjectCore y ProjectReporting si la carga de trabajo justifica dos agentes especializados. Esta subdivisión requiere coordinación cuidadosa para mantener coherencia.

### Equipos de Agentes

Para proyectos de gran escala, múltiples agentes pueden especializarse en subdominios de un área grande. El dominio de Reporting podría tener un agente enfocado en dashboards interactivos y otro en reportes exportables. Estos agentes colaboran estrechamente pero mantienen ownership claro de sus subespecializaciones.

---

## Resolución de Conflictos

### Principio de Ownership

Cuando hay desacuerdo sobre dónde debe residir cierta funcionalidad, el principio de ownership prevalece. La funcionalidad reside en el dominio que tiene más contexto y responsabilidad sobre esa área de negocio. La validación de disponibilidad de recursos reside en el dominio de Recursos, no en Proyectos.

### Arbitraje Arquitectónico

Para conflictos arquitectónicos significativos, existe un proceso de arbitraje. El conflicto se documenta con argumentos de ambas posiciones. Un arquitecto senior o tech lead revisa y toma una decisión fundamentada. Esta decisión se documenta para referencia futura y guía para situaciones similares.

### Precedentes y Consistencia

Las decisiones arquitectónicas pasadas crean precedentes. Cuando surge una situación similar a una previamente resuelta, se sigue el precedente por consistencia. Esto reduce tiempo de decisión y asegura que el código mantiene patterns consistentes a lo largo del tiempo.

---

Este modelo de agentes especializados con alta autonomía dentro de raíles arquitectónicos bien definidos maximiza la velocidad y calidad del desarrollo. Cada agente desarrolla expertise profundo en su dominio mientras los protocolos de coordinación aseguran que el sistema final es cohesivo, mantenible y escalable. La claridad en responsabilidades, interfaces y procesos de comunicación es fundamental para el éxito de esta arquitectura distribuida.
