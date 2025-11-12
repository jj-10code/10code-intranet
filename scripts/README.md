# Scripts Auxiliares - 10Code Intranet

Esta carpeta contiene scripts de utilidad para desarrollo, deployment y mantenimiento del proyecto.

## 📜 Scripts Disponibles

### `validate_secrets.py`

**Propósito:** Validar la configuración de secretos sin requerir Django instalado.

**Uso:**

```bash
python scripts/validate_secrets.py
```

**Verifica:**

- ✅ Existencia de carpeta `secrets/`
- ✅ Permisos de carpeta y archivos
- ✅ Existencia de archivos requeridos (`secret_key.txt`, `db_password.txt`)
- ✅ Longitud y formato de secretos
- ✅ Detección de patrones inseguros
- ✅ `.gitignore` incluye `secrets/`

**Salida exitosa:**

```txt
✅ ¡TODO CORRECTO! La configuración de secretos es válida.
```

---

## 🔮 Scripts Futuros

A medida que el proyecto crezca, esta carpeta contendrá scripts para:

### Deployment

- `deploy_staging.sh` - Desplegar a staging
- `deploy_production.sh` - Desplegar a producción
- `rollback.sh` - Rollback de deployment

### Base de Datos

- `backup_db.sh` - Backup de PostgreSQL
- `restore_db.sh` - Restaurar backup
- `seed_db.py` - Poblar BD con datos de prueba

### Maintenance

- `clean_media.py` - Limpiar archivos media huérfanos
- `check_migrations.py` - Verificar migraciones pendientes
- `rotate_secrets.py` - Rotación automática de secretos

### Development

- `setup_dev.sh` - Configuración inicial de desarrollo
- `generate_fake_data.py` - Generar datos de prueba
- `run_linters.sh` - Ejecutar todos los linters

---

## 📏 Convenciones

### Naming

- **Python scripts**: `snake_case.py`
- **Shell scripts**: `kebab-case.sh`
- Nombres descriptivos y auto-explicativos

### Shebang

```python
#!/usr/bin/env python
```

```bash
#!/usr/bin/env bash
```

### Documentación

Cada script debe tener:

- Docstring descriptivo al inicio
- Comentarios para lógica compleja
- Help/usage cuando sea aplicable

### Permisos

```bash
chmod +x scripts/*.py
chmod +x scripts/*.sh
```

---

## 🚀 Ejemplo: Crear Nuevo Script

```python
#!/usr/bin/env python
"""
Script de ejemplo para [descripción breve].

Usage:
    python scripts/ejemplo.py [opciones]

Example:
    python scripts/ejemplo.py --verbose
"""

import sys
from pathlib import Path

# Agregar project root al path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

def main():
    """Función principal."""
    print("✅ Script ejecutado correctamente")

if __name__ == "__main__":
    main()
```

---

**Última actualización:** 2025-11-12
