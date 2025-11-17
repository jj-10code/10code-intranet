# Anotaciones para implementar en las demás plantillas

---

## 0) Principios

1) **CA ⇒ Test**: cada **Criterio de Aceptación** debe mapear a **≥1 test** (Pest/Playwright).  
2) **Hu < 1 jornada y por perfil** (PT mantiene esta regla).  
3) **Simplicidad**: anti‑overengineering por defecto; triggers de escalado claros.  
4) **Trazabilidad mínima**: HU lista CA y **TEST‑ID**; PR checklist enlaza CA→TEST‑ID; CI reporta a Discord.  
5) **KPIs de entrega**: cycle time, throughput y % no facturable deben poder calcularse con los estados/etiquetas definidos.

---

## 1) Cambios en **Product Analysis** (PA)

> El PA sigue siendo **funcional/negocio** y prepara las **ÉPICAS**; no baja a backlog técnico. Añadimos 4 bloques nuevos opcionales, cortos.

### 1.1. **Testabilidad** por ÉPICA (nuevo)

- **CA críticos (títulos)**: 3–7 CA nucleares de la épica (solo enunciados).  
- **Tipo de prueba sugerido** por CA: `unit | feature/api | component | e2e`.  
- **Datos de prueba**: fixtures/factories imprescindibles (ej., usuario con rol X, catálogo Y con IVA Z).  
- **Riesgos de test**: dependencias externas, datos sensibles, entornos.

### 1.2. **Triggers de complejidad** (nuevo)

- Define cuándo **elevar** la solución: S3 si storage > 50GB; colas si > 200 jobs/min; estado global si patrones complejos; etc.  
- **Plan B**: decisión y señal de activación.

### 1.3. **Owner & Capitanes** (nuevo)

- **Owner de épica** (PM/PO).  
- **Capitán operativo** (3–5 devs): responsable de foco, desbloqueos y PR‑quality en su parcela.  
- **Stakeholders** (cliente/legales/ops si aplica).

### 1.4. **Métricas objetivo** (nuevo, breve)

- **Lead/Cycle time** esperados (orden de magnitud).  
- **Defectos post‑release** tolerables (p. ej. 0 críticos, ≤2 menores/sprint).  
- **% no facturable** esperado para la épica (p. ej. ≤ 20%).

---

## 2) Cambios en **Prompt Template** (PT)
>
> El PT baja de ÉPICA → **HU** → **CA** → **Tareas** por perfil. Conserva HU < 1 jornada.

### 2.1. Metadatos HU (ampliado)

- `HU-ID`, `EPIC-ID`, **Valor/Objetivo** (1–2 frases), **Riesgos**, **Dependencias**.  
- **Estados Kanban** (para métricas): `Backlog | Ready | In Dev | Ready for Review | In Review | Ready for QA (opc.) | Done`.

### 2.2. Criterios de Aceptación (ampliado)

- **Formato por defecto: prosa** (CA‑1, CA‑2…).  
- **Formato alternativo (cuando convenga)**: Gherkin `.feature` (solo en flujos transversales, reglas legales o integraciones).  
- Campo **`TEST-ID`** por cada CA (uno o varios).  
- Campo **`tipo_test`**: `unit | feature/api | component | e2e`.  
- Campo **`datos_prueba`**: fixtures o factories requeridas.

#### **Ejemplo HU (fragmento)**

```markdown
HU-ID: PC-81  
Objetivo: Como vendedor quiero crear un presupuesto para guardar un borrador con numeración correlativa.

CA-1: Guardar borrador válido con número correlativo  → TEST-ID: TEST-FEAT-412  → tipo_test: feature/api  → datos_prueba: factory Budget válida
CA-2: Validación de campos obligatorios            → TEST-ID: TEST-COMP-210  → tipo_test: component  → datos_prueba: formulario vacío
```

### 2.3. Tareas por perfil (sin cambiar la filosofía)

- **Backend**: controlador/servicio, validación, factory/seed, test Pest (unit/feature), migración.  
- **Frontend**: vista/estado mínimo, test component (Testing Library), **E2E** si el CA es de flujo.  
- **QA (si aplica)**: datos, criterios manuales complementarios.  
- **Infra** (si aplica): env vars, colas, storage (ver triggers PA 1.2).

### 2.4. Límites y checklists (añadido)

- **HU < 1 jornada** por perfil.  
- **PR < 300 LOC**, primera revisión ≤ 24h.  
- **IA traza**: pegar prompt útil y salida relevante en el ticket.  
- **DoR mínimo**: objetivo, CA, diseño/API acordado, datos de prueba.  
- **DoD mínimo**: tests verdes, revisión hecha, deployable, docs mínimas.

---

## 3) Trazabilidad y CI/Discord

- **En HU**: tabla CA ↔ `TEST-ID`.  
- **En PR**: checklist *CA‑n → TEST‑XYZ ✅*.  
- **CI**: reportar cobertura por capa y **TEST‑ID fallidos**.  
- **Discord**: enviar reportes de CI al hilo del proyecto en `#tests-global`; fallos mencionan a **capitán**; `/bloqueo` crea ticket con plantilla.

---

## 4) Métricas y lectura (cómo se calculan con PT/PA)

- **Cycle time (dev→merge)**: arranca cuando HU entra en `In Dev` y termina en `merged/Done`.  
- **Throughput**: HUs en `Done` con **CA testados**.  
- **% horas no facturables**: imputación por proyecto; tope y causas (deuda/I+D/on-call/formación).

### **Atribución por persona (para coaching)**

- HUs cerradas, **PR SLA**, participación en desbloqueos, defectos post‑release.

---

## 5) Roles y responsabilidades (ligero)

- **Owner de ÉPICA (PM/PO)**: valor, alcance, prioridades.  
- **Capitán operativo**: foco del grupo (3–5 devs), desbloqueos, calidad de PR, clima. Elegible a plus E1 si impacto sostenido.  
- **CTO/Leads**: estándares, decisiones técnicas, guardias.  
- **QA** (si aplica): pauta de pruebas y datos.  
- **Todos**: pedir/ayudar en bloqueos.

---

## 6) Plantillas para integrar YA (copiar/pegar)

### 6.1. Tabla CA en HU (PT)

| CA | Descripción | TEST‑ID | tipo_test | datos_prueba |
|---|---|---|---|---|
| CA‑1 | … | TEST‑FEAT‑412 | feature/api | factory Budget |
| CA‑2 | … | TEST‑COMP‑210 | component | form vacío |

### 6.2. Bloque Testabilidad en ÉPICA (PA)

- **CA críticos (títulos)**: …  
- **Tipo de prueba sugerido**: …  
- **Datos de prueba**: …  
- **Riesgos de test**: …

### 6.3. Checklist PR

- [ ] HU enlazada y **CA con TEST‑ID**  
- [ ] Tests verdes (Pest/Playwright)  
- [ ] Coberturas ≥ mínimos de la capa  
- [ ] Sin complejidad innecesaria (ver triggers PA)  
- [ ] ADR si hay decisión relevante

---

## 7) Convenciones y nomenclatura

- **TEST‑ID**: `TEST-UNIT-###`, `TEST-FEAT-###`, `TEST-COMP-###`, `TEST-E2E-###`.  
- **Estados**: `Backlog | Ready | In Dev | Ready for Review | In Review | Ready for QA | Done`.  
- **Etiquetas**: `in-dev`, `ready-for-review`, `merged`, `done` (para automatizar *cycle time*).
