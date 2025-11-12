#!/usr/bin/env python
"""Script de debug para verificar carga de variables de entorno."""

import os
from pathlib import Path

print("=" * 60)
print("DEBUG: Verificando carga de .env")
print("=" * 60)

# 1. Estado ANTES de leer .env
print("\n1. ANTES de leer .env:")
print(f"   DJANGO_SETTINGS_MODULE = {os.getenv('DJANGO_SETTINGS_MODULE', 'NOT SET')}")
print(f"   DEBUG = {os.getenv('DEBUG', 'NOT SET')}")
print(f"   ALLOWED_HOSTS = {os.getenv('ALLOWED_HOSTS', 'NOT SET')}")

# 2. Leer .env manualmente (sin django-environ para debug)
BASE_DIR = Path(__file__).resolve().parent
env_file = BASE_DIR / ".env"

print(f"\n2. Buscando .env en: {env_file}")
print(f"   ¿Existe? {env_file.exists()}")

if env_file.exists():
    print("\n3. Contenido relevante del .env:")
    with open(env_file, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                if any(key in line for key in ["DJANGO_SETTINGS_MODULE", "DEBUG", "ALLOWED_HOSTS"]):
                    print(f"   {line}")

# 4. Ahora cargar con django-environ
try:
    import environ

    env = environ.Env()
    environ.Env.read_env(str(env_file))

    print("\n4. DESPUÉS de environ.Env.read_env():")
    print(f"   DJANGO_SETTINGS_MODULE = {os.getenv('DJANGO_SETTINGS_MODULE', 'NOT SET')}")
    print(f"   DEBUG = {os.getenv('DEBUG', 'NOT SET')}")
    print(f"   ALLOWED_HOSTS = {os.getenv('ALLOWED_HOSTS', 'NOT SET')}")

except ImportError:
    print("\n4. [SKIP] django-environ no disponible, continuando sin él")

# 5. Verificar qué pasaría con setdefault (SIMULACIÓN)
print("\n5. SIMULACIÓN de setdefault en manage.py:")
print(
    f"   Valor actual de DJANGO_SETTINGS_MODULE: {os.getenv('DJANGO_SETTINGS_MODULE', 'NOT SET')}"
)
print(
    f"   Si ahora ejecutamos setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development'):"
)

# Hacer una copia para simular
original_value = os.getenv("DJANGO_SETTINGS_MODULE")
if original_value:
    print(f"   → setdefault NO cambia nada, porque ya existe: '{original_value}'")
else:
    print(f"   → setdefault ESTABLECE 'config.settings.development'")

print("\n" + "=" * 60)
print("DIAGNÓSTICO DEL PROBLEMA:")
print("=" * 60)
print("""
El problema es el ORDEN de ejecución en manage.py:

1. manage.py ejecuta PRIMERO:
   os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
   ↓
2. Django carga el módulo de settings especificado
   ↓
3. config/settings/base.py RECIÉN AHORA lee el .env
   ↓
4. ¡Pero ya es tarde! Django ya eligió qué settings usar

SOLUCIÓN: Leer el .env ANTES del setdefault en manage.py
""")
print("=" * 60)
