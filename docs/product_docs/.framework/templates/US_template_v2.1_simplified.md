# Historia de Usuario: [Título Descriptivo]

**HU-ID:** `HU-[MODULO]-[NUM]`  
**Módulo:** [Nombre del módulo/feature]  
**Prioridad:** [P1-Critical / P2-High / P3-Medium / P4-Low]  
**Estimación:** [XX-YY horas]  
**Estado:** [Backlog / Ready / In Dev / In Review / Done]

---

## Descripción

**Como** [rol específico del usuario]  
**Quiero** [funcionalidad concreta y accionable]  
**Para** [beneficio u objetivo de negocio claro]

**Contexto adicional:**  
[1-2 párrafos explicando el valor de negocio, casos de uso principales o información relevante para entender el alcance]

---

## Dependencias

- [ ] [HU-XX-XX o sistema/configuración requerida]
- [ ] [Otra dependencia si aplica]

---

## Criterios de Aceptación

### CA-01: [Nombre descriptivo del criterio]

**Prioridad:** [P1 / P2 / P3]

```gherkin
# Opcional: nombre de la característica
Característica: <nombre de la funcionalidad> y su CA

# Opcional: precondiciones comunes
Antecedentes:
  Dado <precondición común 1>
  Y <precondición común 2>

Escenario: <título del escenario>
  Dado <estado inicial específico>
  Y <otros supuestos necesarios>
  Cuando <acción del usuario o evento del sistema>
  Y <acciones adicionales si aplican>
  Entonces <resultado observable/verificable>
  Y <reglas de negocio/mensajes/efectos adicionales>

# Variante con ejemplos parametrizados
Esquema del escenario: <título>
  Dado <estado inicial con <variable>>
  Cuando <acción con <variable>>
  Entonces <resultado con <variable>>
Ejemplos:
  | variable | ... |
  | valor1   | ... |
  | valor2   | ... |
```

#### Ejemplo rápido

```gherkin
Característica: Recuperación de contraseña (o CA-02)

Escenario: Solicitud de restablecimiento válida
  Dado que el usuario está en la página "Olvidé mi contraseña"
  Y existe una cuenta asociada al correo "persona@ejemplo.com"
  Cuando envía el formulario con "persona@ejemplo.com"
  Entonces el sistema envía un correo con enlace de restablecimiento
  Y se muestra un mensaje de confirmación en pantalla

Escenario: Correo no registrado
  Dado que el usuario está en la página "Olvidé mi contraseña"
  Y no existe ninguna cuenta asociada al correo "nadie@ejemplo.com"
  Cuando envía el formulario con "nadie@ejemplo.com"
  Entonces se muestra un mensaje indicando que, si existe una cuenta, recibirá instrucciones
  Y por seguridad no se revela si el correo está registrado
```

**Casos edge:**

- [Caso edge 1: comportamiento en situación límite]
- [Validación o error específico a manejar]

**Testing:**

- **TEST-ID:** `TEST-[TIPO]-[NUM]` (ej: TEST-UNIT-412, TEST-FEAT-089, TEST-E2E-023)
- **Tipo:** [unit / feature / component / e2e]
- **Datos de prueba:** [Factory/fixture necesario]
- **Ubicación:** `tests/[modulo]/test_[funcionalidad].py`

---

### CA-02: [Nombre del siguiente criterio]

**Prioridad:** [P1 / P2 / P3]

```gherkin
Escenario: [Descripción del escenario]
  Dado que [precondición]
  Cuando [acción]
  Entonces [resultado esperado]
```

**Casos edge:**

- [Caso edge relevante]

**Testing:**

Cada CA debe tener al menos 1 test, pero puede estar involucrada en más de uno si es lo necesario.

- **TEST-ID:** `TEST-[TIPO]-[NUM]`
- **Tipo:** [unit / feature / component / e2e]
- **Datos de prueba:** [Factory/fixture necesario]
- **Ubicación:** `tests/[modulo]/test_[funcionalidad].py`

---

[Repetir estructura para cada criterio de aceptación]

---

## Estrategia de Testing

**Distribución objetivo:** 70% Unit | 20% Integration/Feature | 10% E2E

| CA | TEST-IDs | Tipo | Cobertura |
|----|----------|------|-----------|
| CA-01 | TEST-XXX-### | [tipo] | [capa afectada] |
| CA-02 | TEST-XXX-### | [tipo] | [capa afectada] |

---

## Notas Técnicas

**Consideraciones de implementación:**

- [Detalle técnico relevante]
- [Patrón de diseño sugerido]
- [Consideración de performance o seguridad]

**Integraciones:**

- [Sistema externo / API / Servicio a integrar]

**Referencias:**

- **PRD:** [Sección relevante del PRD]
- **SAD:** [Decisión arquitectónica aplicable]
- **FSD:** [Especificación funcional detallada]

---

## Mockups/Referencias

- **Figma:** [Link a diseños]
- **Flujo de usuario:** [Diagrama o descripción]
- **Documentación:** [Links relevantes]

---

## Definition of Ready

- [ ] Objetivo y valor de negocio claros
- [ ] Todos los CAs definidos con formato Gherkin
- [ ] Cada CA tiene al menos un TEST-ID asignado
- [ ] Dependencias identificadas
- [ ] Referencias a PRD/SAD/FSD incluidas

## Definition of Done

- [ ] Todos los CAs implementados y validados
- [ ] Tests verdes (70% unit, 20% feature, 10% e2e)
- [ ] Code review completado
- [ ] Documentación actualizada
- [ ] Deployable a staging

---

## Criterios de Éxito

**Métricas medibles:**

1. [Métrica cuantitativa específica]
2. [Comportamiento observable del usuario]
3. [KPI de negocio impactado]

---

## Convenciones

**TEST-IDs:**

- `TEST-UNIT-###`: Tests unitarios (models, services, utils)
- `TEST-FEAT-###`: Tests de API/integración con DB
- `TEST-COMP-###`: Tests de componentes React
- `TEST-E2E-###`: Tests end-to-end (Playwright)

**Estados:**

- **Backlog**: Identificada, no priorizada
- **Ready**: DoR cumplido, lista para desarrollo
- **In Dev**: En desarrollo activo
- **In Review**: En code review
- **Done**: DoD cumplido, completada

---

> _Versión: 2.1 - Simplificada para agentes IA_
