# Sistema de Reglas para Frameworks Agénticos

## Sistema de Gestión de Proyectos Integral - 10Code

Este directorio contiene el conjunto completo de reglas, patrones y guías arquitectónicas para el desarrollo del Sistema de Gestión de Proyectos Integral de 10Code mediante frameworks agénticos como Droid, Claude Code o Cursor.

---

## 📚 Estructura de Documentación

El sistema de reglas está organizado en cuatro archivos especializados que deben consultarse según el contexto de trabajo:

### `CLAUDE.md` - Reglas Principales

**Cuándo consultar**: Siempre como punto de partida antes de generar cualquier código.

Este archivo contiene la filosofía arquitectónica central del proyecto, los principios no negociables y los patrones fundamentales que deben aplicarse en todo momento. Define el concepto de Monolito Modular Majestuoso, establece la estructura obligatoria del proyecto y enumera los antipatrones que nunca deben implementarse.

El archivo incluye ejemplos de código que ilustran los patrones correctos de implementación, desde la estructura del Service Layer hasta el manejo de formularios con Inertia. También define las reglas de negocio específicas del proyecto como los requisitos de control horario según normativa española y las validaciones del sistema CEPF con Machine Learning.

Cualquier agente o desarrollador debe leer este archivo completo antes de comenzar a trabajar en el proyecto. Las reglas aquí establecidas son obligatorias y no opcionales. Garantizan consistencia, calidad y mantenibilidad del código a largo plazo.

### `ARCHITECTURE_RULES.md` - Patrones Arquitectónicos

**Cuándo consultar**: Al diseñar comunicación entre módulos o implementar integraciones.

Este documento profundiza en la arquitectura modular del sistema. Explica cómo se estructuran las aplicaciones Django como bounded contexts siguiendo Domain-Driven Design. Define los tres patrones de comunicación entre aplicaciones: Service Layer como patrón primario, señales de Django como patrón secundario e importación directa de modelos como último recurso.

Incluye matrices de decisión que ayudan a determinar qué patrón usar en cada situación. Proporciona templates completos de código para interfaces entre módulos y explica cómo preparar el sistema para evolución futura hacia arquitecturas asíncronas con Celery o real-time con Django Channels.

Este archivo es especialmente relevante cuando se necesita que un módulo interactúe con otro. Por ejemplo, cuando el módulo de Proyectos necesita validar disponibilidad de recursos antes de asignar un miembro al equipo, este documento indica exactamente cómo debe estructurarse esa comunicación.

### `DJANGO_PATTERNS.md` - Patrones Backend

**Cuándo consultar**: Al implementar lógica de negocio, consultas a base de datos o APIs internas.

Este documento es la referencia técnica para todo código backend. Define con precisión quirúrgica cómo debe estructurarse el Service Layer, incluyendo reglas sobre transacciones atómicas, keyword-only arguments y type hints obligatorios. Explica el patrón de Selectors para operaciones de lectura optimizadas con ejemplos exhaustivos de uso de select_related y prefetch_related.

Proporciona guías detalladas sobre cómo mantener los models delgados, reservándolos exclusivamente para estructura de datos y métodos simples. Incluye secciones sobre optimización de queries con análisis del problema N+1 y estrategias para eliminarlo completamente. Define estándares de testing con ejemplos de tests de services y selectors.

Este archivo debe consultarse continuamente durante el desarrollo backend. Es la fuente de verdad para cualquier duda sobre cómo implementar lógica de negocio, estructurar consultas a la base de datos o escribir tests efectivos.

### `INERTIA_FRONTEND.md` - Patrones Frontend

**Cuándo consultar**: Al desarrollar componentes React, páginas Inertia o interfaces de usuario.

Este documento establece los estándares para todo el desarrollo frontend. Explica la filosofía de Inertia.js donde el servidor es la fuente de verdad y los props actúan como contrato entre backend y frontend. Define la estructura de dos niveles para componentes shadcn/ui, separando primitivos inmutables de componentes específicos de aplicación.

Incluye patrones completos para formularios usando el hook useForm, gestión de estado con la regla fundamental de que Inertia es el state manager para datos del servidor y Zustand solo para UI state efímero. Proporciona ejemplos de navegación con Links de Inertia, recargas parciales para optimización y custom hooks para funcionalidad reutilizable.

Este archivo es esencial para mantener consistencia en el frontend. Define cómo debe estructurarse cada página Inertia, cómo manejar permisos recibidos como props y cómo implementar responsive design mobile-first. También establece estándares de performance y seguridad.

### `AGENT_SPECIALIZATION.md` - Arquitectura de Agentes

**Cuándo consultar**: Para entender responsabilidades, coordinación entre agentes y ownership de dominios.

Este documento define el modelo de trabajo para múltiples agentes especializados operando con alta autonomía dentro de raíles arquitectónicos. Establece los principios de coordinación, explica el protocolo de handoff entre dominios y define claramente qué agente es responsable de cada módulo del sistema.

Detalla las responsabilidades de cada agente especializado, desde el Agente Core que gestiona infraestructura compartida hasta el Agente de Machine Learning que implementa el sistema CEPF de estimaciones. Describe las interfaces que cada agente expone a otros y las integraciones críticas que requieren coordinación estrecha.

Incluye secciones sobre procesos de comunicación entre agentes, estándares de calidad que todos deben mantener, procedimientos de onboarding para nuevos agentes y mecanismos de resolución de conflictos. Este documento es fundamental para que múltiples agentes trabajen de forma coordinada sin pisar territorio ajeno.

---

## 🎯 Cómo Usar Esta Documentación

### Para Frameworks Agénticos Autónomos

Los frameworks agénticos deben cargar y analizar todos estos archivos al inicio de cada sesión de trabajo. El archivo `CLAUDE.md` debe estar siempre en memoria como referencia constante. Los archivos específicos deben consultarse según el contexto del trabajo actual.

Cuando un agente recibe una tarea relacionada con backend, debe recargar DJANGO_PATTERNS.md en memoria. Si la tarea involucra frontend, debe consultar INERTIA_FRONTEND.md. Para tareas que cruzan múltiples dominios, ARCHITECTURE_RULES.md proporciona guía sobre cómo estructurar la comunicación.

Los frameworks deben aplicar estas reglas de forma estricta. No son sugerencias sino requerimientos. Cuando una regla parece entrar en conflicto con una decisión de diseño, el framework debe priorizar la regla establecida y solo desviarse si hay razón técnica fundamental y documentada.

### Para Desarrolladores Humanos

Los desarrolladores deben leer CLAUDE.md completo al unirse al proyecto. Este archivo proporciona el contexto esencial y los principios fundamentales. Posteriormente, deben consultar los archivos específicos según el área en que trabajen.

Un desarrollador implementando un nuevo módulo de gestión comercial consultaría ARCHITECTURE_RULES.md para entender cómo estructurar la app, DJANGO_PATTERNS.md para implementar services y selectors correctamente, e INERTIA_FRONTEND.md para crear las interfaces de usuario.

La documentación debe tratarse como living documentation. A medida que el proyecto evoluciona y se descubren mejores prácticas, estos archivos deben actualizarse. Cada actualización debe comunicarse al equipo para mantener a todos alineados.

### Principio de Consulta Frecuente

Estos archivos no son documentación que se lee una vez y se olvida. Deben consultarse frecuentemente durante el desarrollo. Ante cualquier duda sobre cómo implementar una funcionalidad, el primer paso es buscar en estos archivos si existe un patrón o guía aplicable.

Esta consulta frecuente tiene doble beneficio. Primero, asegura que el código generado cumple con estándares establecidos. Segundo, refuerza los patrones en la mente del desarrollador o modelo, creando coherencia natural en el código producido.

---

## 🚀 Flujo de Trabajo Recomendado

### 1. Análisis de Requisitos

Al recibir un nuevo requerimiento funcional, el primer paso es identificar qué dominio o dominios están involucrados. Un requerimiento para "añadir gestión de hitos en proyectos" afecta principalmente al dominio de Proyectos, posiblemente con interacción menor con el dominio de Backlog.

Consultar AGENT_SPECIALIZATION.md para confirmar ownership y verificar si la funcionalidad requiere coordinación entre múltiples agentes. Si es así, identificar las interfaces que necesitan exponerse o consumirse.

### 2. Diseño de Solución

Antes de escribir código, diseñar la solución consultando los archivos de reglas relevantes. Si la funcionalidad requiere nueva lógica de negocio, DJANGO_PATTERNS.md indica que debe ir en el Service Layer con transacciones atómicas. Si requiere nuevas consultas optimizadas, el mismo archivo muestra cómo estructurar selectors.

Para funcionalidad con interfaz de usuario, INERTIA_FRONTEND.md proporciona patrones sobre cómo estructurar las páginas, qué props pasar desde el backend y cómo manejar permisos. Esta fase de diseño previene refactorings costosos posteriores.

### 3. Implementación

Durante la implementación, mantener los archivos de reglas accesibles para consulta rápida. Cuando surja duda sobre cómo implementar algo, consultar primero la documentación antes de tomar decisión arbitraria. Esta disciplina asegura consistencia.

Seguir los templates de código proporcionados en los archivos. Los templates han sido diseñados cuidadosamente para balancear claridad, mantenibilidad y performance. Desviarse de ellos sin razón fuerte introduce inconsistencia.

### 4. Testing

DJANGO_PATTERNS.md establece que ningún código se considera completo sin tests. Implementar tests siguiendo los ejemplos proporcionados. La cobertura mínima del ochenta por ciento es no negociable. Los tests no solo verifican funcionalidad sino documentan comportamiento esperado.

### 5. Revisión

Antes de considerar el trabajo terminado, realizar auto-revisión contra los archivos de reglas. Verificar que se siguieron los patrones establecidos, que la documentación está completa y que no se introdujeron antipatrones listados en CLAUDE.md.

Esta auto-revisión rigurosa reduce dramáticamente el tiempo de code review por parte de otros desarrolladores o agentes, ya que el código llega ya conformado a estándares.

---

## 📋 Checklist de Conformidad

Antes de marcar cualquier tarea como completa, verificar:

### Arquitectura y Estructura

- El código reside en el dominio correcto según AGENT_SPECIALIZATION.md
- La estructura de archivos sigue la organización definida en CLAUDE.md
- La comunicación entre dominios usa Service Layer según ARCHITECTURE_RULES.md

### Backend Django

- Lógica de negocio está en Service Layer, no en views ni models
- Las write operations usan @transaction.atomic
- Los selectors tienen select_related/prefetch_related apropiados
- Los models son delgados con solo estructura de datos
- Type hints están presentes en todas las funciones

### Frontend Inertia

- Las páginas tienen interface Props completa con TypeScript
- Los formularios usan useForm de Inertia
- La navegación usa Links de Inertia, no <a> tags
- Los componentes siguen la estructura de dos niveles de shadcn/ui
- El responsive design es mobile-first

### Testing y Calidad

- Cobertura de tests es >= ochenta por ciento
- Existen unit tests de services y selectors
- Los tests de selectors verifican número de queries
- La documentación está completa con docstrings

### Coordinación

- Las interfaces públicas están documentadas
- Los cambios a contratos se han comunicado a agentes consumidores
- Los handoffs entre dominios están claros

---

## 🔄 Mantenimiento de la Documentación

Estos archivos de reglas son living documentation. Evolucionan con el proyecto a medida que se descubren mejores prácticas o cambian requisitos. El proceso de actualización es:

- **Propuesta de Cambio**: Cuando se identifica necesidad de añadir o modificar una regla, se documenta la propuesta con justificación técnica y ejemplos de código.
- **Revisión**: La propuesta se revisa por tech leads o arquitectos senior. Se evalúa impacto en código existente y esfuerzo de adopción.
- **Comunicación**: Si se aprueba el cambio, se actualiza el archivo correspondiente y se comunica explícitamente a todo el equipo de desarrollo y agentes.
- **Migración**: Se crea plan para actualizar código existente que no cumpla con la nueva regla. Esta migración puede ser gradual pero debe tener timeline claro.

La documentación desactualizada es peor que no tener documentación. Mantener estos archivos sincronizados con la realidad del proyecto es responsabilidad compartida de todo el equipo.

---

## 💡 Principios Finales

**Consistencia sobre Conveniencia**: Cuando hay tentación de tomar atajo que viola las reglas establecidas por conveniencia, resistir. La consistencia arquitectónica tiene valor compuesto que se multiplica con el tiempo.

**Documentación como Código**: Estos archivos de reglas tienen el mismo nivel de importancia que el código del proyecto. Deben versionarse, revisarse y mantenerse con el mismo rigor.

**Aprendizaje Continuo**: A medida que el equipo gana experiencia con el stack tecnológico y el dominio del negocio, las reglas pueden refinarse. Esta evolución es saludable siempre que sea deliberada y documentada.

**Pragmatismo Informado**: Las reglas existen por razones técnicas fundamentadas. Cuando ocasionalmente sea necesario desviarse, hacerlo conscientemente con documentación clara del por qué y con plan para eventual conformidad.

Este sistema de reglas representa la destilación de conocimiento arquitectónico y mejores prácticas para el stack Django + Inertia.js aplicado específicamente al dominio de gestión de proyectos tecnológicos. Su aplicación rigurosa es la diferencia entre un proyecto mantenible que escala ordenadamente y uno que degenera en complejidad inmanejable.

---

**Última Actualización**: Octubre 2025  
**Mantenedor**: Juan Jesús Márquez  
**Versión**: 1.0
