# Historias de Usuario y Criterios de Aceptación

## Épica: Gestión de Recursos y Capacidad

### Historia de Usuario #1: Visualización Calendario de Asignaciones

**Como** Director de Operaciones  
**Quiero** visualizar en un calendario la asignación actual y planificada de cada colaborador  
**Para** tener una visión clara de la carga de trabajo y disponibilidad a nivel individual y de equipo

#### Criterios de Aceptación #1

1. **Vista de Calendario Principal**
   - Puedo ver un calendario tipo Gantt con todos los colaboradores y sus asignaciones
   - Las asignaciones se muestran como bloques de color según proyecto/cliente
   - Puedo ver el porcentaje de dedicación de cada asignación directamente en el bloque
   - La vista muestra por defecto la semana actual, pero puedo ajustar el rango temporal

2. **Filtros y Agrupaciones**
   - Puedo filtrar la vista por departamento, equipo, rol o colaborador específico
   - Puedo agrupar colaboradores por departamento, equipo o proyecto
   - Puedo buscar colaboradores por nombre, habilidad o proyecto asignado
   - Puedo guardar configuraciones de filtro para acceso rápido

3. **Visualización de Disponibilidad**
   - El calendario muestra claramente períodos de no disponibilidad (vacaciones, bajas)
   - Puedo ver gráficamente el porcentaje de asignación diaria de cada persona
   - El sistema resalta visualmente sobreasignaciones (>100%) o baja asignación (<50%)
   - Puedo ver la capacidad teórica versus asignación actual

4. **Interactividad**
   - Puedo hacer clic en cualquier asignación para ver detalles (proyecto, tareas, horas)
   - Al pasar el cursor sobre un bloque de asignación se muestra información adicional
   - Puedo hacer zoom para ver períodos más largos o más cortos (día, semana, mes, trimestre)
   - La vista se actualiza en tiempo real reflejando cambios hechos por otros usuarios

5. **Exportación y Compartición**
   - Puedo exportar la vista actual como PDF, imagen o datos (CSV/Excel)
   - Puedo compartir un enlace a una vista específica con otros usuarios
   - Puedo programar informes periódicos de asignación para ser enviados automáticamente
   - Puedo imprimir el calendario con formato optimizado

---

### Historia de Usuario #2: Gestión Visual de Capacidad vs. Demanda

**Como** Director de Operaciones  
**Quiero** visualizar gráficos que comparen capacidad disponible vs. demanda requerida  
**Para** identificar rápidamente períodos de sobrecarga o infrautilización de recursos

#### Criterios de Aceptación #2

1. **Gráficos de Capacidad Individual**
   - Para cada colaborador, puedo ver una gráfica que muestre capacidad vs. asignación
   - La gráfica muestra claramente períodos de sobreasignación con alertas visuales
   - Puedo ver la tendencia de asignación a lo largo del tiempo (próximas semanas/meses)
   - La capacidad se ajusta automáticamente considerando vacaciones y ausencias

2. **Gráficos de Capacidad por Equipo**
   - Puedo ver gráficos agregados por equipo que muestren capacidad total vs. asignación
   - Puedo desglosar la vista para ver contribución individual dentro del equipo
   - Puedo identificar equipos con alta carga o capacidad disponible
   - Puedo ver predicciones de capacidad futura basadas en asignaciones planificadas

3. **Gráficos por Rol o Especialidad**
   - Puedo visualizar la capacidad vs. demanda agrupada por roles específicos
   - Puedo identificar déficits o excedentes en roles críticos (ej: desarrolladores frontend)
   - Puedo comparar la carga de trabajo entre roles similares
   - Puedo proyectar necesidades futuras de contratación basadas en déficits persistentes

4. **Dashboards de Capacidad Global**
   - Puedo ver un dashboard consolidado con KPIs de capacidad a nivel empresa
   - El dashboard muestra porcentajes de utilización por departamento y equipo
   - Puedo visualizar tendencias de asignación a lo largo del tiempo
   - Puedo configurar alertas para umbrales específicos (ej: equipos >90% asignados)

5. **Análisis Predictivo**
   - Puedo ver proyecciones de capacidad vs. demanda para los próximos 3-6 meses
   - El sistema sugiere redistribuciones de carga basadas en habilidades compatibles
   - Puedo simular escenarios añadiendo o quitando proyectos potenciales
   - El sistema identifica cuellos de botella potenciales con anticipación

---

### Historia de Usuario #3: Reasignación de Recursos entre Proyectos

**Como** Director de Operaciones  
**Quiero** poder reasignar recursos entre proyectos de forma visual e intuitiva  
**Para** optimizar la utilización y responder rápidamente a cambios en prioridades o necesidades

#### Criterios de Aceptación #3

1. **Interfaz de Drag & Drop**
   - Puedo arrastrar y soltar bloques de asignación entre proyectos y colaboradores
   - Al arrastrar, veo previsualizaciones de cómo quedaría la nueva asignación
   - Puedo ajustar la duración y dedicación directamente en la interfaz visual
   - La interfaz muestra automáticamente sugerencias de personal disponible con habilidades adecuadas

2. **Validaciones Automáticas**
   - El sistema valida que no se generen sobreasignaciones al reasignar recursos
   - Recibo alertas si la persona no tiene las habilidades requeridas para el nuevo rol
   - El sistema verifica conflictos con vacaciones o ausencias planificadas
   - Se valida que se respeten las asignaciones mínimas comprometidas en contratos

3. **Gestión de Impacto**
   - Veo el impacto inmediato de los cambios en la capacidad de los equipos afectados
   - Recibo notificaciones sobre posibles riesgos en proyectos al quitar recursos
   - Puedo ver cómo afecta la reasignación a las fechas de entrega estimadas
   - Puedo añadir justificaciones para cada reasignación significativa

4. **Workflows de Aprobación**
   - Las reasignaciones mayores a cierto porcentaje requieren aprobación configurable
   - Los responsables de proyecto afectados reciben notificaciones y pueden aprobar/rechazar
   - Puedo ver el estado de todas las solicitudes de reasignación pendientes
   - El historial de aprobaciones queda registrado para auditoría

5. **Notificaciones y Comunicación**
   - Los colaboradores reasignados reciben notificaciones automáticas
   - Los responsables de proyectos afectados son informados de los cambios
   - Puedo enviar mensajes explicativos junto con la notificación de reasignación
   - El sistema genera automáticamente actas de reuniones de reasignación

---

### Historia de Usuario #4: Simulación de Escenarios de Asignación

**Como** Director de Operaciones  
**Quiero** poder simular diferentes escenarios de asignación de recursos  
**Para** evaluar impactos y tomar las mejores decisiones antes de aplicar cambios

#### Criterios de Aceptación #4

1. **Creación de Escenarios**
   - Puedo crear múltiples escenarios hipotéticos partiendo de la asignación actual
   - Puedo nombrar y describir cada escenario para identificarlo fácilmente
   - Puedo duplicar escenarios existentes para crear variaciones
   - Los escenarios se guardan para revisión posterior sin afectar asignaciones reales

2. **Manipulación de Escenarios**
   - Dentro de un escenario, puedo añadir/quitar proyectos hipotéticos
   - Puedo modificar asignaciones de recursos libremente
   - Puedo ajustar fechas de inicio/fin de proyectos para ver impactos
   - Puedo simular contrataciones o bajas de personal

3. **Análisis de Impacto**
   - Para cada escenario, puedo ver métricas de capacidad y utilización resultantes
   - Puedo comparar varios escenarios lado a lado en términos de KPIs clave
   - Puedo ver el impacto financiero estimado de cada escenario
   - El sistema identifica riesgos potenciales en cada configuración

4. **Optimización Asistida**
   - El sistema sugiere distribuciones óptimas basadas en restricciones definidas
   - Puedo establecer reglas de optimización (minimizar costes, maximizar velocidad, etc.)
   - Recibo sugerencias para resolver sobreasignaciones o subutilizaciones
   - Puedo bloquear asignaciones críticas que no deben modificarse en la optimización

5. **Aplicación de Escenarios**
   - Puedo convertir un escenario simulado en el plan real tras su aprobación
   - El sistema genera un plan detallado de transición entre la situación actual y el escenario elegido
   - Mantengo acceso al historial de escenarios aplicados
   - Los afectados reciben notificaciones escalonadas según el plan de transición

---

### Historia de Usuario #5: Gestión de Solicitudes de Recursos

**Como** Responsable de Proyecto  
**Quiero** poder solicitar recursos adicionales o específicos para mis proyectos  
**Para** cubrir necesidades puntuales o planificadas siguiendo un proceso formal

#### Criterios de Aceptación #5

1. **Creación de Solicitudes**
   - Puedo crear solicitudes detallando recursos necesarios (rol, habilidades, dedicación)
   - Puedo especificar el período durante el cual necesito los recursos
   - Puedo indicar si necesito personas específicas o solo el perfil
   - Puedo establecer prioridad y justificación de negocio para la solicitud

2. **Workflow de Aprobación**
   - Las solicitudes siguen un flujo configurable de aprobaciones
   - Los aprobadores reciben notificaciones de solicitudes pendientes
   - Cada aprobador puede añadir comentarios o condiciones
   - El solicitante puede hacer seguimiento del estado en tiempo real

3. **Matching de Recursos**
   - El sistema sugiere automáticamente candidatos disponibles que cumplen los requisitos
   - Puedo ver el porcentaje de coincidencia de cada candidato con el perfil solicitado
   - Puedo filtrar sugerencias por departamento, ubicación u otros criterios
   - Veo el impacto que tendría en otros proyectos asignar a cada candidato sugerido

4. **Resolución de Solicitudes**
   - El Director de Operaciones puede aprobar, rechazar o proponer alternativas
   - En caso de rechazo, se debe proporcionar justificación y alternativas si existen
   - Las asignaciones aprobadas se crean automáticamente en el calendario
   - Se notifica a todos los involucrados sobre la resolución final

5. **Análisis y Reporting**
   - Puedo ver estadísticas de solicitudes (tiempo de resolución, tasa de aprobación, etc.)
   - Puedo analizar patrones de demanda por tipo de perfil o departamento
   - Los datos de solicitudes alimentan previsiones de necesidades futuras
   - Puedo exportar informes de solicitudes para reuniones de planificación de capacidad

---

### Historia de Usuario #6: Planificación de Capacidad a Largo Plazo

**Como** Director de Operaciones  
**Quiero** planificar la capacidad de recursos a medio y largo plazo (6-18 meses)  
**Para** alinear la contratación y desarrollo de talento con las necesidades futuras del negocio

#### Criterios de Aceptación #6

1. **Previsión de Demanda**
   - Puedo registrar previsiones de proyectos futuros con probabilidades de materialización
   - Puedo definir necesidades aproximadas de recursos por rol y habilidad
   - Puedo importar previsiones desde el CRM u otras fuentes
   - El sistema ajusta automáticamente la demanda según probabilidades configurables

2. **Análisis de Oferta vs Demanda**
   - Puedo visualizar gráficos comparativos de capacidad proyectada vs demanda prevista
   - La proyección considera rotación histórica de personal
   - Puedo ver déficits o excedentes previstos por tipo de perfil y período
   - El sistema muestra tendencias y puntos críticos que requieren atención

3. **Planificación de Contrataciones**
   - Basado en el análisis, puedo crear planes de contratación por período
   - Puedo establecer tiempos estimados de incorporación y curva de aprendizaje
   - El plan considera presupuestos y restricciones de contratación
   - Los planes se integran con el departamento de RRHH para seguimiento

4. **Desarrollo de Capacidades**
   - Puedo identificar habilidades estratégicas con déficit proyectado
   - Puedo crear planes de formación para desarrollar esas capacidades internamente
   - El sistema sugiere candidatos internos para reconversión basados en perfil
   - Puedo realizar seguimiento de la evolución de capacidades en la organización

5. **Escenarios Estratégicos**
   - Puedo crear escenarios basados en diferentes hipótesis de crecimiento
   - Puedo simular el impacto de decisiones estratégicas (nueva línea de negocio, expansión)
   - Puedo comparar costes y beneficios de diferentes estrategias de capacidad
   - Los escenarios se pueden presentar en formato ejecutivo para toma de decisiones

---

### Historia de Usuario #7: Gestión de Disponibilidad y Ausencias

**Como** Colaborador y Responsable  
**Quiero** gestionar eficientemente vacaciones, permisos y otras ausencias  
**Para** garantizar transparencia en la disponibilidad real y su impacto en proyectos

#### Criterios de Aceptación #7

1. **Solicitud de Ausencias**
   - Como Colaborador, puedo solicitar vacaciones y permisos especificando fechas y tipo
   - El sistema muestra mi saldo disponible de días actualizados
   - Puedo ver el impacto de mi ausencia en proyectos asignados
   - Recibo recomendaciones de períodos con menor impacto en proyectos

2. **Aprobación de Solicitudes**
   - Como Responsable, recibo notificaciones de solicitudes pendientes
   - Puedo ver el impacto de la ausencia en proyectos y planificación
   - Puedo aprobar, rechazar o proponer fechas alternativas
   - El sistema notifica posibles conflictos con hitos críticos o solapamientos en equipo

3. **Visualización de Calendario de Ausencias**
   - Puedo ver un calendario de equipo con todas las ausencias programadas
   - Puedo filtrar por tipo de ausencia, equipo o período
   - El calendario distingue visualmente entre tipos de ausencia
   - Puedo exportar o compartir vistas del calendario

4. **Integración con Capacidad**
   - Las ausencias aprobadas reducen automáticamente la capacidad disponible
   - El sistema ajusta asignaciones durante períodos de ausencia
   - Se generan alertas para tareas sin cobertura durante ausencias
   - Los informes de capacidad reflejan con precisión ausencias planificadas

5. **Políticas y Cumplimiento**
   - El sistema implementa políticas configurables (límites, períodos bloqueados)
   - Se calculan automáticamente saldos de vacaciones según políticas de empresa
   - Se generan informes de cumplimiento normativo
   - El historial de ausencias se archiva para consulta y auditoría

---

### Historia de Usuario #8: Seguimiento de Tiempo Real de Asignaciones

**Como** Director de Operaciones y Responsable de Proyecto  
**Quiero** visualizar en tiempo real la actividad de los recursos y comparar con lo planificado  
**Para** detectar desviaciones, ajustar asignaciones y maximizar la productividad

#### Criterios de Aceptación #8

1. **Dashboard de Actividad Actual**
   - Puedo ver qué está haciendo cada recurso en tiempo real (en qué proyectos/tareas)
   - La vista se actualiza automáticamente sin necesidad de refrescar
   - Puedo filtrar por equipo, proyecto o departamento
   - Veo indicadores de estado (activo, en pausa, en reunión)

2. **Comparación con Planificación**
   - Puedo comparar la actividad real con lo que estaba planificado para cada recurso
   - Veo desviaciones significativas resaltadas visualmente
   - Puedo analizar tendencias de cumplimiento de planificación por persona o equipo
   - El sistema calcula métricas de adherencia a la planificación

3. **Seguimiento de Dedicación**
   - Puedo ver estadísticas de tiempo dedicado por proyecto en tiempo real
   - Comparo porcentajes de dedicación real vs. asignada
   - Identifico proyectos que están consumiendo más recursos de lo previsto
   - Puedo definir umbrales de alerta por desviación

4. **Ajustes Dinámicos**
   - Puedo realizar ajustes en asignaciones basados en la actividad real
   - Los ajustes pueden ser temporales o permanentes
   - El sistema sugiere reasignaciones basadas en patrones de actividad
   - Los cambios quedan registrados con justificación para análisis posterior

5. **Análisis de Productividad**
   - Puedo identificar patrones de productividad por hora del día o día de la semana
   - El sistema detecta posibles bloqueos basados en tiempo excesivo en tareas
   - Puedo comparar velocidad entre equipos similares
   - Los datos alimentan recomendaciones para optimización de asignaciones futuras
