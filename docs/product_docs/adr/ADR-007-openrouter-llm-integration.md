# ADR-007: OpenRouter para Acceso Multi-Modelo a LLMs

## Metadata

- **Status**: Accepted
- **Fecha**: 2025-11-17
- **Decisor(es)**: Juanje Márquez (Arquitecto Principal)
- **Tags**: integraciones, ia, llm, estimaciones, arquitectura

---

## Contexto y Problema

El sistema de Intranet 10Code requiere capacidades de inteligencia artificial para múltiples funcionalidades, principalmente:

- **Estimaciones de proyectos**: Análisis de requisitos y sugerencia de componentes aplicables
- **Asistencia en clasificación**: Identificación de riesgos y categorización de proyectos
- **Generación de documentación**: Templates y contenido contextual
- **Análisis de texto**: Procesamiento de briefings de clientes y requisitos

**Requisitos técnicos:**

- Acceso a múltiples modelos LLM (Claude, GPT-4, etc.) sin reescribir código
- Flexibilidad para cambiar de modelo según caso de uso (coste vs. calidad)
- Sin vendor lock-in: poder migrar entre proveedores sin refactorización
- Cost-effective: optimizar costes vs. capacidades
- Simplicidad de integración: API única, no múltiples SDKs

**Restricciones:**

- Equipo de desarrollo reducido (1 developer + agentes IA)
- Presupuesto limitado para APIs externas
- No hay infraestructura propia para hosting de modelos
- Necesidad de producción-ready desde MVP

---

## Factores de Decisión

- **Factor 1**: Acceso multi-modelo vs. single-provider
- **Factor 2**: Coste total (requests, mantenimiento, complejidad)
- **Factor 3**: Flexibilidad para cambiar modelos según contexto
- **Factor 4**: Simplicidad de integración y DX (Developer Experience)
- **Factor 5**: Ausencia de vendor lock-in
- **Factor 6**: Calidad y variedad de modelos disponibles
- **Factor 7**: Rate limits y disponibilidad del servicio

---

## Opciones Consideradas

### Opción 1: OpenAI API Directamente

**Descripción:** Integración directa con OpenAI para usar GPT-4, GPT-3.5-turbo

**Pros:**

- ✅ API oficial y bien documentada
- ✅ Modelos de alta calidad (GPT-4, GPT-4-turbo)
- ✅ Rate limits generosos en tiers de pago
- ✅ SDKs oficiales en Python

**Cons:**

- ❌ Vendor lock-in total a OpenAI
- ❌ Sin acceso a Claude u otros modelos
- ❌ Cambiar a otro proveedor requiere refactorización completa
- ❌ Costes menos flexibles (pricing fijo por modelo)
- ❌ No permite comparar rendimiento entre modelos fácilmente

---

### Opción 2: Anthropic API Directamente

**Descripción:** Integración directa con Anthropic para Claude (Sonnet, Opus)

**Pros:**

- ✅ Acceso a Claude (mejor para tareas analíticas y razonamiento)
- ✅ API oficial y documentada
- ✅ Context window extenso (200k tokens en Claude 2.1)
- ✅ SDK oficial Python

**Cons:**

- ❌ Vendor lock-in a Anthropic
- ❌ Sin acceso a GPT-4 u otros modelos
- ❌ Cambiar proveedor requiere refactorización
- ❌ Costes fijos por modelo
- ❌ Menor variedad de modelos que OpenAI

---

### Opción 3: Azure OpenAI Service

**Descripción:** Usar OpenAI a través de Azure con SLA empresarial

**Pros:**

- ✅ SLA empresarial y soporte de Microsoft
- ✅ Integración con otros servicios Azure
- ✅ Data residency en Europa (si se requiere GDPR estricto)
- ✅ Rate limits más altos

**Cons:**

- ❌ Vendor lock-in a Microsoft/Azure
- ❌ Solo modelos OpenAI disponibles
- ❌ Complejidad de configuración (Azure Portal, IAM)
- ❌ Coste superior a OpenAI directo
- ❌ Overhead de gestión de infraestructura Azure

---

### Opción 4: OpenRouter (Unified API Gateway)

**Descripción:** Gateway unificado que proporciona acceso a múltiples proveedores LLM (OpenAI, Anthropic, Google, Meta, etc.) con una sola API

**Pros:**

- ✅ **Acceso multi-modelo**: Claude, GPT-4, Gemini, Llama, etc. con misma API
- ✅ **Sin vendor lock-in**: Cambiar modelo es cambiar un parámetro
- ✅ **Cost-effective**: Comparar precios y elegir modelo óptimo por tarea
- ✅ **Simplicidad**: API única estilo OpenAI, compatible con SDKs existentes
- ✅ **Fallback automático**: Si un modelo falla, puede intentar con otro
- ✅ **Rate limiting unificado**: Un solo servicio gestiona límites
- ✅ **Métricas centralizadas**: Dashboard único para monitorear uso

**Cons:**

- ❌ Dependencia de servicio third-party (aunque es solo un gateway)
- ❌ Ligero markup en costes vs. APIs directas (~3-5%)
- ❌ Latencia adicional mínima por proxy (10-50ms)
- ❌ No tiene SLA empresarial garantizado en tier gratuito

---

### Opción 5: Hosting Propio (Llama, Mistral open-source)

**Descripción:** Desplegar y gestionar modelos open-source en infraestructura propia

**Pros:**

- ✅ Coste marginal cero por request (después de setup)
- ✅ Control total sobre datos y privacidad
- ✅ Sin rate limits externos

**Cons:**

- ❌ Inversión inicial alta (GPUs, infraestructura)
- ❌ Complejidad operativa (mantenimiento, actualizaciones, scaling)
- ❌ Requiere expertise en ML Ops
- ❌ Modelos open-source inferiores a Claude/GPT-4 en calidad
- ❌ No viable para equipo pequeño sin infraestructura GPU

---

## Decisión

**Opción elegida**: **Opción 4 - OpenRouter (Unified API Gateway)**

**Justificación:**

Hemos decidido usar **OpenRouter** como gateway unificado para acceso a LLMs porque:

1. **Flexibilidad multi-modelo**: Permite usar Claude para análisis complejos, GPT-4 para generación de texto, y modelos más baratos (GPT-3.5) para tareas simples, todo desde la misma integración.

2. **Sin vendor lock-in**: Si Anthropic o OpenAI cambian precios o políticas, simplemente cambiamos el parámetro `model` en las requests. No hay refactorización de código.

3. **Cost-effective**: Podemos optimizar costes eligiendo el modelo correcto para cada tarea:
   - Claude Sonnet para estimaciones críticas (mejor razonamiento)
   - GPT-3.5-turbo para clasificación simple (más barato)
   - Comparar rendimiento/coste fácilmente con A/B testing

4. **DX superior**: API compatible con OpenAI SDK, lo que significa:
   - SDK Python oficial funciona sin cambios
   - Documentación familiar para cualquier developer
   - Compatibilidad con herramientas de desarrollo existentes

5. **Fallback y resiliencia**: Si Claude está saturado, OpenRouter puede automáticamente usar GPT-4 como fallback (configurable).

6. **Métricas centralizadas**: Dashboard único para monitorear:
   - Costes por modelo y por feature
   - Latencias y errores
   - Rate limiting agregado

**Trade-off aceptado**: El markup de ~3-5% sobre costes directos es marginal comparado con los beneficios de flexibilidad y el ahorro de tiempo de desarrollo que implica gestionar múltiples APIs.

**Comparativa de costes (ejemplo estimación de 500 tokens input, 1500 output):**

```markdown
OpenAI GPT-4 directo:     $0.03 + $0.06 = $0.09
OpenRouter GPT-4:         $0.09 + 5% markup = ~$0.095  (diferencia: $0.005)

Claude Sonnet directo:    $0.015 + $0.045 = $0.06
OpenRouter Claude Sonnet: $0.06 + 5% markup = ~$0.063 (diferencia: $0.003)
```

El markup es despreciable (~$0.003-0.005 por request) comparado con los beneficios.

---

## Consecuencias

### Positivas

- ✅ **Desarrollo ágil**: Un solo SDK para integrar, no múltiples integraciones
- ✅ **Optimización de costes**: Elegir modelo óptimo por caso de uso sin refactorizar
- ✅ **Future-proof**: Acceso inmediato a nuevos modelos que OpenRouter agregue
- ✅ **Experimentación fácil**: A/B testing entre modelos con cambios mínimos
- ✅ **Resiliencia**: Fallback automático si proveedor primario falla

### Negativas

- ❌ **Dependencia third-party**: Si OpenRouter tiene downtime, perdemos acceso a todos los modelos (mitigable con fallback a APIs directas si es crítico)
- ❌ **Markup en costes**: 3-5% adicional vs. APIs directas (aceptable por beneficios)
- ❌ **Latencia adicional**: 10-50ms por proxy (imperceptible en uso humano)

### Neutras

- ⚠️ **Monitoreo de costes**: Necesitamos dashboard interno para alertar si uso excede presupuesto
- ⚠️ **Rate limiting**: OpenRouter gestiona limits agregados; debemos monitorear para evitar sorpresas
- ⚠️ **Evolución de pricing**: Debemos revisar periódicamente si markup de OpenRouter sigue siendo competitivo

---

## Notas de Implementación

### Instalación

```bash
# SDK compatible OpenAI
uv add openai
```

### Configuración Base

```python
# apps/integrations_openrouter/client.py
from openai import OpenAI
import os

class OpenRouterClient:
    """Cliente para OpenRouter (compatible con OpenAI SDK)."""
    
    def __init__(self):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY"),
        )
    
    def chat_completion(
        self,
        model: str,
        messages: list[dict],
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ):
        """Wrapper para completions con OpenRouter."""
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            extra_headers={
                "HTTP-Referer": "https://10code.es",  # Opcional: para analytics
                "X-Title": "10Code Intranet",
            }
        )
        return response
```

### Uso en Services

```python
# apps/estimation/services.py
from apps.integrations_openrouter.client import OpenRouterClient

class EstimationService:
    """Service para estimaciones con LLM."""
    
    MODELS = {
        'analysis': 'anthropic/claude-sonnet-4',      # Para análisis profundo
        'classification': 'openai/gpt-3.5-turbo',     # Para clasificación simple
        'generation': 'openai/gpt-4-turbo-preview',   # Para generación de contenido
    }
    
    @staticmethod
    def analyze_requirements(requirements: str) -> dict:
        """Analizar requisitos con Claude (mejor razonamiento)."""
        client = OpenRouterClient()
        
        response = client.chat_completion(
            model=EstimationService.MODELS['analysis'],
            messages=[
                {
                    "role": "system",
                    "content": "Eres un experto en estimación de proyectos de software."
                },
                {
                    "role": "user",
                    "content": f"Analiza estos requisitos y sugiere componentes:\n{requirements}"
                }
            ],
            temperature=0.3,  # Más determinístico para estimaciones
            max_tokens=2000,
        )
        
        # Parse response...
        return parsed_result
```

### Modelos Disponibles Recomendados

```python
# apps/integrations_openrouter/constants.py
RECOMMENDED_MODELS = {
    # Anthropic Claude - Mejor para análisis y razonamiento
    'claude-sonnet': 'anthropic/claude-sonnet-4',
    'claude-opus': 'anthropic/claude-opus-4',
    
    # OpenAI - Mejor para generación y tareas generales
    'gpt-4-turbo': 'openai/gpt-4-turbo-preview',
    'gpt-4': 'openai/gpt-4',
    'gpt-3.5': 'openai/gpt-3.5-turbo',
    
    # Google - Bueno para tareas multimodales
    'gemini-pro': 'google/gemini-pro',
    
    # Open-source - Cost-effective para tareas simples
    'llama-70b': 'meta-llama/llama-2-70b-chat',
}
```

### Gestión de Secrets

```python
# config/secrets.py - Agregar OpenRouter API key
OPENROUTER_API_KEY = read_secret("openrouter_api_key", required=True)
```

```bash
# secrets/openrouter_api_key.txt
sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Monitoreo de Costes

```python
# apps/integrations_openrouter/monitoring.py
import logging

logger = logging.getLogger(__name__)

def log_llm_usage(model: str, prompt_tokens: int, completion_tokens: int, cost: float):
    """Log uso de LLM para monitoreo de costes."""
    logger.info(
        "llm_usage",
        model=model,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        total_tokens=prompt_tokens + completion_tokens,
        estimated_cost=cost,
    )
```

### Testing con Mocks

```python
# apps/estimation/tests/test_services.py
from unittest.mock import Mock, patch

@patch('apps.integrations_openrouter.client.OpenRouterClient.chat_completion')
def test_analyze_requirements(mock_completion):
    """Test análisis de requisitos sin llamar API real."""
    mock_completion.return_value = Mock(
        choices=[Mock(message=Mock(content='{"components": [...]}'))]
    )
    
    result = EstimationService.analyze_requirements("Crear CRUD de usuarios")
    
    assert "components" in result
    mock_completion.assert_called_once()
```

---

## Referencias

- [OpenRouter Documentation](https://openrouter.ai/docs)
- [OpenRouter Models & Pricing](https://openrouter.ai/models)
- [OpenAI SDK Python](https://github.com/openai/openai-python) - Compatible con OpenRouter
- [Comparativa de costes LLMs 2024](https://artificialanalysis.ai/)
- [Discusión interna: Slack #arquitectura (2024-11-15)](https://10code.slack.com/archives/...)

---

## Historial

| Fecha | Evento |
|-------|--------|
| 2025-11-17 | ADR creado y aceptado como parte del SAD v1.0 |

---

**Firmado por:**

- Juanje Márquez - Arquitecto Principal - 2025-11-17
