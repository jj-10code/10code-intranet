# Historias de Usuario y Criterios de Aceptación

## Épica: Gestión de Estructura Organizativa

### Historia de Usuario #1: Configuración de Departamentos y Equipos

**Como** Administrador del sistema  
**Quiero** poder crear, editar y gestionar departamentos y equipos  
**Para** representar fielmente la estructura organizativa de la empresa en la plataforma

#### Criterios de Aceptación #1

1. **Creación de Departamentos**
   - Puedo crear nuevos departamentos especificando nombre, descripción y departamento padre (si aplica)
   - Puedo asignar un responsable principal a cada departamento
   - Puedo definir un código único para cada departamento
   - Puedo establecer jerarquías entre departamentos (departamentos y subdepartamentos)

2. **Creación de Equipos**
   - Puedo crear equipos indicando nombre, descripción y tipo (horizontal/vertical)
   - Puedo asociar equipos a uno o varios departamentos
   - Puedo definir un responsable principal para cada equipo
   - Puedo especificar el propósito principal del equipo

3. **Clasificación y Categorización**
   - Puedo clasificar equipos como "horizontales" (ejecución) o "verticales" (estructura/apoyo)
   - Puedo etiquetar equipos con categorías personalizadas (ej: desarrollo, diseño, producto)
   - Puedo filtrar equipos por tipo, departamento o categoría en la vista de administración

4. **Gestión y Mantenimiento**
   - Puedo editar la información de departamentos y equipos existentes
   - Puedo desactivar departamentos o equipos sin eliminarlos permanentemente
   - Puedo fusionar equipos manteniendo sus miembros e historial
   - Puedo visualizar todos los departamentos y equipos en una vista jerárquica

5. **Visualización Organizativa**
   - Puedo ver un organigrama visual de la estructura departamental
   - Puedo visualizar la composición de cada equipo con sus miembros
   - Puedo exportar la estructura organizativa en diferentes formatos (PDF, CSV)

---

### Historia de Usuario #2: Asignación de Colaboradores a Equipos

**Como** Administrador o Responsable de departamento  
**Quiero** poder asignar colaboradores a múltiples equipos simultáneamente  
**Para** reflejar la naturaleza multidisciplinar de nuestra estructura y la pertenencia de personas a equipos horizontales y verticales

#### Criterios de Aceptación #2

1. **Asignación Múltiple**
   - Puedo asignar un colaborador a varios equipos simultáneamente
   - Puedo especificar un porcentaje de dedicación para cada asignación equipo-colaborador
   - Puedo definir fechas de inicio y fin para asignaciones temporales a equipos
   - El sistema permite y gestiona correctamente la pertenencia simultánea a equipos horizontales y verticales

2. **Roles en Equipos**
   - Puedo definir un rol específico para cada colaborador dentro de cada equipo
   - Puedo asignar múltiples roles a un mismo colaborador en un equipo si es necesario
   - Puedo configurar los roles disponibles por tipo de equipo

3. **Gestión de Asignaciones**
   - Puedo visualizar todas las asignaciones de un colaborador en una vista centralizada
   - Puedo filtrar colaboradores por equipo, rol o departamento
   - Puedo realizar asignaciones masivas de colaboradores a equipos
   - Puedo modificar o finalizar asignaciones existentes

4. **Notificaciones y Comunicación**
   - El sistema notifica a los colaboradores cuando son asignados o removidos de un equipo
   - Los responsables de equipo reciben notificaciones cuando hay cambios en la composición de su equipo
   - Los colaboradores pueden ver todos los equipos a los que pertenecen en su perfil

5. **Validación y Controles**
   - El sistema alerta sobre posibles sobreasignaciones (suma de dedicaciones > 100%)
   - Tengo posibilidad de sobrepasar los límites de asignación con autorización especial
   - Existe validación para roles obligatorios en ciertos tipos de equipos
   - Se registra historial de cambios en las asignaciones para auditoría

---

### Historia de Usuario #3: Gestión de Perfiles de Colaboradores

**Como** Administrador de RRHH  
**Quiero** mantener perfiles detallados de cada colaborador con sus datos profesionales y habilidades  
**Para** facilitar la identificación de talento adecuado para proyectos y gestionar eficientemente los recursos humanos

#### Criterios de Aceptación #3

1. **Creación y Mantenimiento de Perfiles**
   - Puedo crear perfiles de colaboradores con información personal básica (nombre, contacto, etc.)
   - Puedo registrar información profesional (cargo, nivel, fecha de incorporación)
   - Puedo mantener historial laboral interno (proyectos anteriores, roles desempeñados)
   - Puedo cargar colaboradores masivamente mediante importación CSV/Excel

2. **Habilidades y Competencias**
   - Puedo definir catálogos de habilidades técnicas y blandas para la organización
   - Puedo asignar habilidades a colaboradores con niveles de competencia (1-5)
   - Los colaboradores pueden actualizar sus propias habilidades (sujeto a aprobación)
   - Puedo buscar colaboradores por habilidades específicas con filtros avanzados

3. **Información Contractual**
   - Puedo registrar tipo de contrato y condiciones laborales básicas
   - Puedo definir coste/hora del colaborador para cálculos de rentabilidad
   - Puedo establecer calendarios laborales específicos por colaborador
   - La información sensible está protegida con permisos especiales

4. **Seguimiento de Desarrollo**
   - Puedo registrar titulaciones, certificaciones y formación completada
   - Puedo establecer planes de desarrollo individuales con objetivos
   - Puedo realizar seguimiento de evaluaciones de desempeño
   - Puedo visualizar la progresión profesional a lo largo del tiempo

5. **Integraciones**
   - Los perfiles se sincronizan con el sistema de usuarios para autenticación
   - Puedo vincular perfiles con cuentas de herramientas externas (GitHub, Discord, etc.)
   - Los datos no sensibles del perfil son visibles para otros miembros del equipo
   - Los cambios clave en el perfil generan actualizaciones en sistemas integrados (RRHH)

---

### Historia de Usuario #4: Configuración de Capacidad y Disponibilidad

**Como** Director de Operaciones  
**Quiero** configurar y visualizar la capacidad y disponibilidad de los recursos humanos  
**Para** optimizar la asignación a proyectos y evitar sobreasignaciones

#### Criterios de Aceptación #4

1. **Configuración de Capacidad Base**
   - Puedo definir la jornada laboral estándar de la organización (horas/día)
   - Puedo configurar capacidad base personalizada por colaborador si difiere del estándar
   - Puedo establecer reducción de jornada para ciertos perfiles con porcentajes específicos
   - Puedo definir los días laborables por semana para cada colaborador

2. **Gestión de Calendarios**
   - Puedo configurar calendarios laborales con festivos por ubicación
   - Puedo gestionar ausencias planificadas (vacaciones, permisos, formación)
   - Puedo registrar ausencias no planificadas (bajas médicas, etc.)
   - Los colaboradores pueden solicitar vacaciones y permisos a través del sistema

3. **Cálculo de Disponibilidad**
   - El sistema calcula automáticamente las horas disponibles por colaborador en cualquier período
   - Puedo ver la disponibilidad real teniendo en cuenta asignaciones a proyectos
   - Recibo alertas de sobreasignación cuando la demanda supera la capacidad
   - Puedo visualizar la disponibilidad futura para planificación a medio plazo

4. **Visualización de Capacidad**
   - Puedo ver gráficos de capacidad vs asignación por colaborador
   - Puedo ver la disponibilidad agregada por equipo o departamento
   - Puedo filtrar la vista de capacidad por períodos específicos (semana, mes, trimestre)
   - Puedo exportar informes de capacidad y disponibilidad para análisis externo

5. **Aprobación de Ausencias**
   - Existe un flujo de aprobación configurable para solicitudes de ausencia
   - Los responsables reciben notificaciones de solicitudes pendientes de aprobación
   - Se visualiza el impacto de las ausencias en los proyectos asignados
   - Se sincroniza el calendario de ausencias con herramientas externas (Google Calendar, etc.)

---

### Historia de Usuario #5: Gestión de Roles y Permisos

**Como** Administrador del Sistema  
**Quiero** definir y gestionar roles con permisos granulares  
**Para** controlar el acceso a la información y funcionalidades según las responsabilidades de cada usuario

#### Criterios de Aceptación #5

1. **Creación y Configuración de Roles**
   - Puedo crear roles personalizados con nombres descriptivos
   - Puedo duplicar roles existentes para crear variaciones
   - Puedo establecer descripciones detalladas para cada rol
   - Puedo activar/desactivar roles sin eliminarlos definitivamente

2. **Asignación de Permisos Granulares**
   - Puedo asignar permisos específicos por módulo funcional (proyectos, usuarios, facturación)
   - Puedo definir niveles de acceso (sin acceso, lectura, escritura, administración)
   - Puedo configurar permisos sobre acciones específicas (crear proyecto, aprobar tiempo)
   - Puedo establecer permisos sobre datos específicos (ver costes, editar presupuestos)

3. **Asignación de Roles a Usuarios**
   - Puedo asignar múltiples roles a un usuario
   - Puedo asignar roles con alcance específico (global, departamento, proyecto)
   - Puedo establecer jerarquías de roles (un rol puede incluir permisos de otros)
   - Puedo realizar asignaciones masivas de roles a grupos de usuarios

4. **Gestión de Roles por Contexto**
   - Puedo definir roles específicos para contextos (proyectos, departamentos, etc.)
   - El sistema aplica automáticamente roles contextuales cuando un usuario está en ese contexto
   - Puedo establecer roles temporales con fecha de expiración
   - Los permisos se calculan correctamente considerando todos los roles aplicables

5. **Auditoría y Seguridad**
   - Puedo ver un registro de cambios en roles y permisos
   - Puedo comparar permisos entre diferentes roles
   - El sistema impide que un usuario pueda eliminar su propio acceso administrativo
   - Existe al menos un rol administrativo que no puede ser eliminado

---

### Historia de Usuario #6: Visualización de Estructura Organizativa

**Como** Usuario de la plataforma  
**Quiero** visualizar la estructura organizativa de manera clara e interactiva  
**Para** entender las relaciones entre departamentos, equipos y personas

#### Criterios de Aceptación #6

1. **Vista de Organigrama**
   - Puedo ver un organigrama interactivo de la estructura departamental
   - Puedo expandir/colapsar niveles del organigrama para ver más o menos detalle
   - Puedo buscar departamentos o personas específicas en el organigrama
   - Puedo ver información básica de cada entidad al seleccionarla en el organigrama

2. **Vista de Equipos**
   - Puedo ver una lista de todos los equipos clasificados por tipo (horizontal/vertical)
   - Puedo filtrar equipos por departamento, categoría o responsable
   - Puedo ver la composición detallada de cada equipo
   - Puedo identificar visualmente la intersección entre diferentes equipos

3. **Vista de Miembros**
   - Puedo ver un directorio de todos los colaboradores con información básica
   - Puedo filtrar colaboradores por equipo, rol o habilidades
   - Puedo ordenar la lista por diferentes criterios (antigüedad, cargo, etc.)
   - Puedo exportar listas de miembros filtradas en diferentes formatos

4. **Vista de Matriz**
   - Puedo ver una matriz que relaciona departamentos con equipos
   - Puedo ver una matriz que relaciona personas con equipos y sus roles
   - Las matrices son interactivas permitiendo filtrar y ordenar
   - Puedo exportar las vistas de matriz para análisis externos

5. **Personalización de Vistas**
   - Puedo guardar configuraciones personalizadas de visualización
   - Puedo seleccionar los campos visibles en cada tipo de vista
   - Puedo cambiar entre diferentes modos de visualización (lista, tarjetas, gráfico)
   - Mis preferencias de visualización se mantienen entre sesiones

---

### Historia de Usuario #7: Gestión de Movimientos Organizativos

**Como** Responsable de RRHH o Administrador  
**Quiero** gestionar cambios organizativos como promociones, traslados o reorganizaciones  
**Para** mantener actualizada la estructura organizativa y preservar el historial de cambios

#### Criterios de Aceptación #7

1. **Registro de Promociones y Cambios de Rol**
   - Puedo registrar promociones de colaboradores con fecha efectiva
   - Puedo especificar cambios en cargo, nivel y condiciones
   - El sistema mantiene historial de roles anteriores
   - Los cambios en rol actualizan automáticamente permisos y accesos

2. **Traslados entre Departamentos o Equipos**
   - Puedo registrar traslados de colaboradores entre departamentos
   - Puedo programar traslados con fecha futura
   - Puedo especificar períodos de transición donde el colaborador pertenece a ambos equipos
   - El sistema notifica a los responsables afectados por el traslado

3. **Gestión de Reorganizaciones**
   - Puedo fusionar departamentos o equipos preservando sus miembros
   - Puedo dividir un departamento o equipo en varios nuevos
   - Puedo recategorizar equipos (de horizontal a vertical o viceversa)
   - Puedo mover grupos de colaboradores masivamente durante reorganizaciones

4. **Planificación de Cambios**
   - Puedo simular cambios organizativos antes de aplicarlos
   - Puedo ver el impacto de los cambios en proyectos y asignaciones
   - Puedo programar cambios organizativos con fecha futura
   - Los cambios planificados se aplican automáticamente en la fecha especificada

5. **Historial y Auditoría**
   - Puedo ver el historial completo de cambios organizativos
   - Puedo reconstruir la estructura organizativa en cualquier fecha pasada
   - Puedo generar informes comparativos entre diferentes puntos temporales
   - El sistema mantiene trazabilidad completa de quién realizó cada cambio y cuándo
