# 🤖 Machine Learning - Guía de Desarrollo

Esta guía es para desarrolladores que trabajan con el módulo de estimaciones CEPF y Machine Learning.

## 📦 Dependencias de ML

El proyecto incluye las siguientes dependencias de ML (grupo opcional `[ml]`):

| Librería | Tamaño | Uso |
|----------|--------|-----|
| **TensorFlow** | ~2.5GB | Framework principal de ML |
| **PyTorch** | ~2GB | Framework alternativo de ML |
| **scikit-learn** | ~200MB | Algoritmos clásicos de ML |
| **pandas** | ~100MB | Manipulación de datos |
| **numpy** | ~50MB | Cálculo numérico |
| **spacy** | ~500MB | Procesamiento de lenguaje natural |
| **transformers** | ~300MB | Modelos preentrenados NLP |
| **nltk** | ~50MB | Toolkit de NLP |

**Total:** ~6GB de dependencias adicionales

## 🚀 Quick Start con ML

### Opción 1: Setup Completo (Recomendado)

```bash
# Setup inicial con ML (incluye migraciones)
make ml-setup

# Crear superusuario
make createsuperuser
```

### Opción 2: Agregar ML a Proyecto Existente

```bash
# Si ya tienes el proyecto corriendo sin ML

# 1. Detener servicios actuales
make down

# 2. Build con ML
make ml-build

# 3. Levantar con ML
make ml-up
```

## 🛠️ Comandos Disponibles

### Gestión de Servicios con ML

```bash
make ml-build      # Build de imágenes con ML (tarda ~10-15 min)
make ml-up         # Levantar servicios con ML
make ml-down       # Detener servicios con ML
make ml-logs       # Ver logs de servicios con ML
make ml-setup      # Setup completo desde cero
```

### Desarrollo Normal (Sin ML)

```bash
make build         # Build sin ML (~2-3 min)
make up            # Levantar sin ML
make down          # Detener servicios
```

## 💡 Cuándo Usar ML

**✅ Usa `make ml-*` cuando:**
- Desarrollas el módulo de estimaciones CEPF
- Entrenas o pruebas modelos de ML
- Trabajas con procesamiento de lenguaje natural
- Necesitas TensorFlow o PyTorch

**❌ NO necesitas ML para:**
- Desarrollo de frontend
- Trabajo en módulos de proyectos, recursos, timetracking
- Testing general de la aplicación
- Desarrollo de APIs

## ⏱️ Tiempos de Build

| Configuración | Primera Build | Rebuilds |
|--------------|---------------|----------|
| **Sin ML** (dev) | 2-3 min | 30-60 seg |
| **Con ML** | 10-15 min | 5-10 min |

💡 **Tip:** Los rebuilds son más rápidos gracias al cache de Docker y uv.

## 📊 Uso de Recursos

### Requisitos Mínimos para ML

- **RAM:** 8GB (16GB recomendado)
- **Disco:** 10GB libres para imágenes Docker
- **CPU:** 4 cores (8 cores recomendado)

### Configurar Memoria de Docker

Si usas Docker Desktop, aumenta la memoria asignada:

1. Docker Desktop → Settings → Resources → Memory
2. Aumentar a mínimo 6GB (8GB recomendado)
3. Apply & Restart

## 🔄 Workflow de Desarrollo

### Desarrollo Sin ML (Mayoría del Tiempo)

```bash
# Día a día sin ML
make up
make logs-web
make test
```

### Cuando Necesites ML

```bash
# Cambiar a modo ML
make down
make ml-up

# Tu código de ML aquí...

# Volver a modo normal
make down
make up
```

## 🐍 Verificar Instalación de ML

```bash
# Acceder al contenedor
make bash-web

# Verificar que ML está instalado
python -c "import tensorflow as tf; print(f'TensorFlow {tf.__version__}')"
python -c "import torch; print(f'PyTorch {torch.__version__}')"
python -c "import sklearn; print(f'scikit-learn {sklearn.__version__}')"

# Salir
exit
```

## 📝 Notas Importantes

### GPU Support

Por defecto, las imágenes usan **CPU only**. Para usar GPU:

1. Instalar [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html)
2. Modificar `compose.ml.yml` para agregar soporte GPU:

```yaml
services:
  web:
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
```

### Modelos Preentrenados

Los modelos de spacy y transformers se descargan la primera vez:

```bash
# Dentro del contenedor
python -m spacy download es_core_news_sm  # Modelo español
python -m spacy download en_core_web_sm   # Modelo inglés
```

### Cache de uv

El cache de uv acelera rebuilds. Para limpiar si hay problemas:

```bash
docker builder prune --filter type=exec.cachemount
```

## 🔧 Troubleshooting

### Build Muy Lento

- **Causa:** Descarga de TensorFlow/PyTorch
- **Solución:** Usar cache de Docker, esperar primera vez
- **Tip:** Compilar en horarios de buena conexión

### Error de Memoria

- **Causa:** Docker con poca RAM
- **Solución:** Aumentar memoria en Docker Desktop a 8GB

### Módulo No Encontrado

```bash
# Verificar que construiste con ML
docker compose -f compose.yml -f compose.override.yml -f compose.ml.yml ps

# Si dice que no tiene ML, rebuild
make ml-build
```

## 📚 Referencias

- [TensorFlow Docs](https://www.tensorflow.org/)
- [PyTorch Docs](https://pytorch.org/)
- [scikit-learn Docs](https://scikit-learn.org/)
- [spaCy Docs](https://spacy.io/)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers/)

---

**Desarrollado con 💙 por 10Code Team**
