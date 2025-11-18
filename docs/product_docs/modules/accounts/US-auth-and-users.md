# Historias de Usuario - Módulo de Autenticación y Usuarios

**Versión:** 1.0
**Fecha:** 2025-11-18
**Autor:** Juanje Márquez - 10Code
**Estado:** Ready for Implementation

Este documento contiene todas las Historias de Usuario (HU) del módulo de Autenticación y Usuarios, desarrolladas siguiendo la plantilla v2.1 simplificada. Cada HU está estructurada para facilitar su uso como contexto por agentes de IA especializados en desarrollo de software.

Las HU están organizadas por categorías funcionales y numeradas secuencialmente. Dependencias entre HU se indican explícitamente para optimizar el orden de desarrollo.

---

## 1. Autenticación

### HU-AUTH-001: Inicio de Sesión con Google OAuth

**HU-ID:** `HU-AUTH-001`  
**Módulo:** Autenticación  
**Prioridad:** P1-Critical  
**Estimación:** 8-12 horas  
**Estado:** Ready  

#### Descripción

**Como** empleado de 10Code  
**Quiero** iniciar sesión con mi cuenta de Google corporativa (@10code.es)  
**Para** acceder al sistema sin gestionar contraseñas adicionales  

**Contexto adicional:** Funcionalidad fundamental del sistema, elimina gestión manual de contraseñas y garantiza acceso exclusivo corporativo mediante SSO.

#### Dependencias

- [ ] Configuración Google OAuth en Google Cloud Console
- [ ] django-allauth instalado y configurado

#### Criterios de Aceptación

##### CA-01: Redirección a Google OAuth

**Prioridad:** P1

```gherkin
Escenario: Click en botón de login
  Dado que usuario visita /login
  Cuando hace click en "Login con Google"
  Entonces es redirigido a Google OAuth consent screen
  Y se solicitan scopes email y profile
```

**Testing:** TEST-E2E-001 (e2e) - `tests/e2e/auth.spec.ts`

##### CA-02: Creación automática de usuario

**Prioridad:** P1

```gherkin
Escenario: Primer login exitoso
  Dado que email es @10code.es válido
  Cuando OAuth callback retorna datos válidos
  Entonces se crea User + GoogleProfile automáticamente
  Y se asigna rol 'employee' por defecto
  Y se registra login en AuditLog
```

**Testing:** TEST-FEAT-001 (feature) - `tests/accounts/test_views.py`

#### Definition of Done

- [ ] Implementación OAuth flow con django-allauth
- [ ] Validación dominio @10code.es en callback
- [ ] Service Layer: `AuthService.authenticate_with_google()`
- [ ] Tests: 70% unit, 20% integration, 10% e2e
- [ ] Seguridad: HTTPS obligatorio, CSRF protection
- [ ] Auditoría: Login events logged

#### Notas Técnicas

**Implementación:** Usar django-allauth con provider Google. Service Layer maneja lógica de negocio. Cache de permisos en Redis.

**Referencias:**

- **FSD:** Sección 4.2 AuthService.authenticate_with_google()
- **SAD:** Sección 7.1 Integración Google OAuth

---

### HU-AUTH-002: Cierre de Sesión Seguro

**HU-ID:** `HU-AUTH-002`  
**Módulo:** Autenticación  
**Prioridad:** P1-Critical  
**Estimación:** 4-6 horas  
**Estado:** Ready  

#### Descripción

**Como** usuario autenticado  
**Quiero** cerrar sesión  
**Para** proteger mi cuenta cuando dejo mi equipo  

**Contexto adicional:** Seguridad básica, invalida sesión activa y registra logout para auditoría.

#### Dependencias

- [ ] HU-AUTH-001 completada

#### Criterios de Aceptación

##### CA-01: Logout exitoso

**Prioridad:** P1

```gherkin
Escenario: Usuario hace logout
  Dado que usuario está autenticado
  Cuando hace click en "Cerrar sesión"
  Entonces sesión se invalida
  Y es redirigido a /login
  Y se registra logout en AuditLog
```

**Testing:** TEST-E2E-002 (e2e) - `tests/e2e/auth.spec.ts`

#### Definition of Done

- [ ] POST /logout endpoint con CSRF
- [ ] AuthService.logout_user() implementation
- [ ] Session invalidation in Redis
- [ ] Tests coverage completa

---

### HU-AUTH-003: Rechazo de Emails No Corporativos

**HU-ID:** `HU-AUTH-003`  
**Módulo:** Autenticación  
**Prioridad:** P1-Critical  
**Estimación:** 3-5 horas  
**Estado:** Ready  

#### Descripción

**Como** sistema  
**Quiero** rechazar logins desde emails no @10code.es  
**Para** garantizar acceso exclusivo corporativo  

#### Criterios de Aceptación

##### CA-01: Validación de dominio

**Prioridad:** P1

```gherkin
Escenario: Email no corporativo
  Dado que usuario intenta login con gmail.com
  Cuando OAuth callback procesa email
  Entonces se rechaza con error claro
  Y se registra intento fallido en AuditLog
```

**Testing:** TEST-UNIT-001 (unit) - `tests/accounts/test_services.py`

#### Definition of Done

- [ ] Validación regex @10code.es en AuthService
- [ ] Error handling con mensaje claro
- [ ] Audit logging de rejected attempts

---

### HU-AUTH-004: Timeout de Sesión por Inactividad

**HU-ID:** `HU-AUTH-004`  
**Módulo:** Autenticación  
**Prioridad:** P2-High  
**Estimación:** 5-8 horas  
**Estado:** Ready  

#### Descripción

**Como** administrador  
**Quiero** que sesiones expiren tras 8 horas de inactividad  
**Para** proteger cuentas olvidadas abiertas  

#### Criterios de Aceptación

##### CA-01: Auto-logout tras 8 horas

**Prioridad:** P2

```gherkin
Escenario: Sesión inactiva 8+ horas
  Dado que usuario tiene sesión activa
  Cuando pasan 8 horas sin actividad
  Entonces es automáticamente logged out
  Y próxima request requiere re-login
```

**Testing:** TEST-FEAT-002 (feature) - `tests/accounts/test_middleware.py`

#### Definition of Done

- [ ] Django session config: SESSION_COOKIE_AGE = 28800
- [ ] Middleware para activity tracking
- [ ] Redis session backend

---

## 2. Gestión de Usuarios

### HU-USER-001: Creación Manual de Usuarios

**HU-ID:** `HU-USER-001`  
**Módulo:** Gestión de Usuarios  
**Prioridad:** P2-High  
**Estimación:** 10-15 horas  
**Estado:** Ready  

#### Descripción

**Como** administrador  
**Quiero** crear usuarios manualmente  
**Para** dar acceso anticipado antes del primer login Google  

#### Dependencias

- [ ] HU-AUTH-001 completada

#### Criterios de Aceptación

##### CA-01: Formulario de creación

**Prioridad:** P2

```gherkin
Escenario: Admin crea usuario
  Dado que admin tiene permisos
  Cuando llena formulario con email @10code.es
  Entonces se crea usuario inactivo
  Y puede hacer primer login con Google
```

**Testing:** TEST-E2E-003 (e2e) - `tests/e2e/users.spec.ts`

#### Definition of Done

- [ ] UserService.create_user_manually()
- [ ] Frontend: Users/Create.tsx
- [ ] Validación dominio email
- [ ] Audit logging

---

### HU-USER-002: Desactivación Temporal de Usuarios

**HU-ID:** `HU-USER-002`  
**Módulo:** Gestión de Usuarios  
**Prioridad:** P2-High  
**Estimación:** 6-10 horas  
**Estado:** Ready  

#### Descripción

**Como** administrador  
**Quiero** desactivar usuarios temporalmente  
**Para** gestionar ausencias prolongadas sin perder datos  

#### Criterios de Aceptación

##### CA-01: Soft delete funcional

**Prioridad:** P2

```gherkin
Escenario: Desactivar usuario
  Dado que usuario existe activo
  Cuando admin lo desactiva
  Entonces is_active = False
  Y no puede loguear
  Y datos preservados
```

**Testing:** TEST-FEAT-003 (feature) - `tests/accounts/test_services.py`

#### Definition of Done

- [ ] UserService.deactivate_user()
- [ ] Soft delete implementation
- [ ] Session invalidation

---

### HU-USER-003: Gestión de Perfil Personal

**HU-ID:** `HU-USER-003`  
**Módulo:** Gestión de Usuarios  
**Prioridad:** P3-Medium  
**Estimación:** 8-12 horas  
**Estado:** Ready  

#### Descripción

**Como** usuario  
**Quiero** ver y editar mi perfil (solo avatar)  
**Para** mantener información actualizada  

#### Criterios de Aceptación

##### CA-01: Edición de avatar

**Prioridad:** P3

```gherkin
Escenario: Usuario edita avatar
  Dado que usuario está en /profile
  Cuando sube nueva imagen
  Entonces avatar se actualiza
  Y se registra en AuditLog
```

**Testing:** TEST-E2E-004 (e2e) - `tests/e2e/profile.spec.ts`

#### Definition of Done

- [ ] Profile views y forms
- [ ] Avatar upload handling
- [ ] Audit logging

---

### HU-USER-004: Lista de Usuarios con Filtros

**HU-ID:** `HU-USER-004`  
**Módulo:** Gestión de Usuarios  
**Prioridad:** P2-High  
**Estimación:** 12-18 horas  
**Estado:** Ready  

#### Descripción

**Como** administrador  
**Quiero** visualizar lista completa de usuarios con filtros  
**Para** gestión eficiente  

#### Criterios de Aceptación

##### CA-01: Lista filtrable

**Prioridad:** P2

```gherkin
Escenario: Admin filtra usuarios
  Dado que hay múltiples usuarios
  Cuando aplica filtros (activo, rol, departamento)
  Entonces se muestra lista filtrada
  Y paginación funciona
```

**Testing:** TEST-FEAT-004 (feature) - `tests/accounts/test_views.py`

#### Definition of Done

- [ ] Users index view con filtros
- [ ] Selectors optimizados
- [ ] Frontend tabla con filtros

---

### HU-USER-005: Fecha de Nacimiento en Registro

**HU-ID:** `HU-USER-005`  
**Módulo:** Gestión de Usuarios  
**Prioridad:** P2-High  
**Estimación:** 6-10 horas  
**Estado:** Ready  

#### Descripción

**Como** usuario  
**Quiero** proporcionar fecha de nacimiento al registrarme  
**Para** cumplir requisitos de RR.HH.  

#### Dependencias

- [ ] HU-AUTH-001 completada

#### Criterios de Aceptación

##### CA-01: Onboarding con fecha nacimiento

**Prioridad:** P2

```gherkin
Escenario: Primer login requiere fecha nacimiento
  Dado que es primer login
  Cuando OAuth exitoso
  Entonces se muestra form de onboarding
  Y solicita fecha nacimiento obligatoria
```

**Testing:** TEST-E2E-005 (e2e) - `tests/e2e/auth.spec.ts`

#### Definition of Done

- [ ] Onboarding flow post-OAuth
- [ ] Validación fecha nacimiento
- [ ] RGPD compliance

---

### HU-USER-006: Actualización de Fecha de Nacimiento

**HU-ID:** `HU-USER-006`  
**Módulo:** Gestión de Usuarios  
**Prioridad:** P3-Medium  
**Estimación:** 8-12 horas  
**Estado:** Ready  

#### Descripción

**Como** usuario  
**Quiero** actualizar fecha de nacimiento máximo una vez al año  
**Para** corregir errores con auditoría completa  

#### Dependencias

- [ ] HU-USER-005 completada

#### Criterios de Aceptación

##### CA-01: Validación de frecuencia

**Prioridad:** P3

```gherkin
Escenario: Cambio de fecha nacimiento
  Dado que usuario quiere cambiar fecha
  Cuando intenta actualizar
  Entonces verifica último cambio < 1 año
  Y registra en AuditLog si permitido
```

**Testing:** TEST-UNIT-002 (unit) - `tests/accounts/test_services.py`

#### Definition of Done

- [ ] Validación temporal en UserService
- [ ] Audit logging completo
- [ ] RGPD compliance

---

## 3. Roles y Permisos

### HU-PERM-001: Asignación de Roles Múltiples

**HU-ID:** `HU-PERM-001`  
**Módulo:** Roles y Permisos  
**Prioridad:** P1-Critical  
**Estimación:** 10-15 horas  
**Estado:** Ready  

#### Descripción

**Como** administrador  
**Quiero** asignar múltiples roles a un usuario  
**Para** definir sus capacidades en el sistema  

#### Criterios de Aceptación

##### CA-01: Asignación múltiple

**Prioridad:** P1

```gherkin
Escenario: Asignar roles
  Dado que admin tiene permisos
  Cuando selecciona usuario y roles
  Entonces se asignan todos los roles
  Y permisos se unen (OR logic)
  Y se registra en AuditLog
```

**Testing:** TEST-FEAT-005 (feature) - `tests/accounts/test_services.py`

#### Definition of Done

- [ ] RoleService.assign_role_to_user()
- [ ] Frontend RoleSelector
- [ ] Cache invalidation

---

### HU-PERM-002: Creación de Roles Personalizados

**HU-ID:** `HU-PERM-002`  
**Módulo:** Roles y Permisos  
**Prioridad:** P2-High  
**Estimación:** 12-18 horas  
**Estado:** Ready  

#### Descripción

**Como** administrador  
**Quiero** crear roles personalizados  
**Para** adaptarme a necesidades organizativas  

#### Criterios de Aceptación

##### CA-01: Creación de rol

**Prioridad:** P2

```gherkin
Escenario: Crear rol personalizado
  Dado que admin tiene permisos
  Cuando crea rol con permisos específicos
  Entonces rol se guarda
  Y puede asignarse a usuarios
```

**Testing:** TEST-E2E-006 (e2e) - `tests/e2e/roles.spec.ts`

#### Definition of Done

- [ ] Role creation views
- [ ] Permission assignment UI
- [ ] Validation logic

---

### HU-PERM-003: Verificación de Permisos

**HU-ID:** `HU-PERM-003`  
**Módulo:** Roles y Permisos  
**Prioridad:** P1-Critical  
**Estimación:** 8-12 horas  
**Estado:** Ready  

#### Descripción

**Como** sistema  
**Quiero** verificar permisos antes de acciones críticas  
**Para** garantizar seguridad  

#### Criterios de Aceptación

##### CA-01: Check permission

**Prioridad:** P1

```gherkin
Escenario: Acción crítica
  Dado que usuario intenta acción
  Cuando sistema verifica permiso
  Entonces permite o deniega basado en roles
  Y cachea resultado
```

**Testing:** TEST-UNIT-003 (unit) - `tests/accounts/test_services.py`

#### Definition of Done

- [ ] AuthService.check_permission()
- [ ] Cache con Redis
- [ ] PermissionRequired decorators

---

### HU-PERM-004: Visualización de Capacidades

**HU-ID:** `HU-PERM-004`  
**Módulo:** Roles y Permisos  
**Prioridad:** P3-Medium  
**Estimación:** 6-10 horas  
**Estado:** Ready  

#### Descripción

**Como** usuario  
**Quiero** ver qué acciones puedo realizar  
**Para** comprender mis capacidades  

#### Criterios de Aceptación

##### CA-01: UI de permisos

**Prioridad:** P3

```gherkin
Escenario: Ver mis permisos
  Dado que usuario está logueado
  Cuando visita sección de permisos
  Entonces ve lista de acciones permitidas por módulo
```

**Testing:** TEST-COMP-001 (component) - `tests/frontend/components/PermissionGuard.test.tsx`

#### Definition of Done

- [ ] PermissionGuard component
- [ ] usePermissions hook
- [ ] UI indicators

---

## 4. Auditoría

### HU-AUDIT-001: Historial de Logins

**HU-ID:** `HU-AUDIT-001`  
**Módulo:** Auditoría  
**Prioridad:** P2-High  
**Estimación:** 10-15 horas  
**Estado:** Ready  

#### Descripción

**Como** administrador  
**Quiero** visualizar historial completo de logins  
**Para** detectar accesos sospechosos  

#### Criterios de Aceptación

##### CA-01: Vista de audit log

**Prioridad:** P2

```gherkin
Escenario: Ver logins
  Dado que admin tiene permisos
  Cuando accede a /audit
  Entonces ve tabla con logins exitosos/fallidos
  Y puede filtrar por usuario, fecha
```

**Testing:** TEST-FEAT-006 (feature) - `tests/accounts/test_views.py`

#### Definition of Done

- [ ] AuditLog model y queries
- [ ] Audit index view
- [ ] Frontend AuditLogViewer

---

### HU-AUDIT-002: Alertas de Intentos No Autorizados

**HU-ID:** `HU-AUDIT-002`  
**Módulo:** Auditoría  
**Prioridad:** P2-High  
**Estimación:** 8-12 horas  
**Estado:** Ready  

#### Descripción

**Como** responsable de seguridad  
**Quiero** recibir alertas de logins no autorizados  
**Para** respuesta rápida  

#### Criterios de Aceptación

##### CA-01: Alertas automáticas

**Prioridad:** P2

```gherkin
Escenario: Login rechazado
  Dado que email no @10code.es intenta login
  Cuando se registra en audit log
  Entonces se envía alerta a responsables
  Y se registra en sistema de alertas
```

**Testing:** TEST-UNIT-004 (unit) - `tests/accounts/test_services.py`

#### Definition of Done

- [ ] Alert system integration
- [ ] Email notifications
- [ ] Discord webhooks

---

### HU-AUDIT-003: Exportación de Logs

**HU-ID:** `HU-AUDIT-003`  
**Módulo:** Auditoría  
**Prioridad:** P3-Medium  
**Estimación:** 6-10 horas  
**Estado:** Ready  

#### Descripción

**Como** auditor  
**Quiero** exportar logs de acceso  
**Para** cumplimiento normativo  

#### Criterios de Aceptación

##### CA-01: Export CSV/JSON

**Prioridad:** P3

```gherkin
Escenario: Exportar logs
  Dado que auditor solicita export
  Cuando selecciona filtros y formato
  Entonces se genera archivo con datos
  Y se registra export en audit
```

**Testing:** TEST-FEAT-007 (feature) - `tests/accounts/test_services.py`

#### Definition of Done

- [ ] AuditService.export_audit_logs()
- [ ] CSV/JSON generation
- [ ] Background task con Celery

---

### HU-AUDIT-004: Registro de Cambios Críticos

**HU-ID:** `HU-AUDIT-004`  
**Módulo:** Auditoría  
**Prioridad:** P1-Critical  
**Estimación:** 5-8 horas  
**Estado:** Ready  

#### Descripción

**Como** sistema  
**Quiero** registrar cambios en permisos críticos  
**Para** trazabilidad completa  

#### Criterios de Aceptación

##### CA-01: Audit de cambios

**Prioridad:** P1

```gherkin
Escenario: Cambio de permisos
  Dado que se modifica rol/permiso
  Cuando se guarda cambio
  Entonces se registra en AuditLog
  Y incluye quién, qué, cuándo, IP
```

**Testing:** TEST-UNIT-005 (unit) - `tests/accounts/test_services.py`

#### Definition of Done

- [ ] AuditService.log_action()
- [ ] Signals para auto-logging
- [ ] IP address capture

---

### HU-AUDIT-005: Auditoría de Cambios de Fecha Nacimiento

**HU-ID:** `HU-AUDIT-005`  
**Módulo:** Auditoría  
**Prioridad:** P2-High  
**Estimación:** 4-6 horas  
**Estado:** Ready  

#### Descripción

**Como** auditor  
**Quiero** ver historial de cambios de fecha nacimiento  
**Para** detectar abusos relacionados con RR.HH.  

#### Dependencias

- [ ] HU-USER-006 completada

#### Criterios de Aceptación

##### CA-01: Historial específico

**Prioridad:** P2

```gherkin
Escenario: Ver cambios fecha nacimiento
  Dado que auditor busca usuario
  Cuando filtra por action='birthday_change'
  Entonces ve timeline de cambios
  Y detalles de cada modificación
```

**Testing:** TEST-FEAT-008 (feature) - `tests/accounts/test_selectors.py`

#### Definition of Done

- [ ] AuditLog filtering por action
- [ ] Frontend timeline component
- [ ] RGPD compliance

---

## Dependencias Generales entre HU

- **Fundacionales:** HU-AUTH-001 → HU-AUTH-002, HU-AUTH-003, HU-AUTH-004
- **Usuario Management:** HU-AUTH-001 → HU-USER-001 → HU-USER-002, HU-USER-003, HU-USER-004
- **Fecha Nacimiento:** HU-USER-005 → HU-USER-006 → HU-AUDIT-005
- **Roles:** HU-PERM-001, HU-PERM-002 → HU-PERM-003 → HU-PERM-004
- **Auditoría:** HU-AUDIT-004 → HU-AUDIT-001, HU-AUDIT-002, HU-AUDIT-003

## Consideraciones Técnicas Generales

**Stack Compliance:**

- Backend: Django 5 + Service Layer + PostgreSQL
- Frontend: React + Inertia.js + TypeScript
- Auth: Google OAuth + JWT-equivalent via sessions
- Cache: Redis para sesiones y permisos
- Async: Celery para tareas pesadas
- Security: HTTPS, CSRF, RBAC, Audit logging

**Patrones Arquitectónicos:**

- Service Layer para lógica de negocio (80% comunicación)
- Selectors para queries optimizadas
- Thin Models con lógica mínima
- Pydantic para validaciones de input
- Cache agresivo para performance

**Testing Strategy:**

- 70% Unit Tests en services
- 20% Integration/Feature tests
- 10% E2E con Playwright
- Cobertura mínima 80% en lógica crítica

**Referencias Cruzadas:**

- **PRD:** Sección 4.1 - Requisitos de autenticación
- **SAD:** Secciones 7 (Seguridad), 8 (Testing), 5.2 (Service Layer)
- **FSD:** Todo el documento fuente para reglas de negocio

---

> **Fin del documento de Historias de Usuario - Módulo de Autenticación y Usuarios**
>
> *Este documento está listo para ser usado como contexto principal por agentes de IA especializados en desarrollo de software Django + React.*
