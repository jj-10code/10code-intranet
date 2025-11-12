#!/usr/bin/env python
"""
Script de validación de configuración de secretos.
Verifica que los archivos de secretos existan y tengan el formato correcto.
NO requiere que Django esté instalado.
"""

import sys
from pathlib import Path


def validate_secrets():
    """Valida que los archivos de secretos existan y sean válidos."""
    # Como el script está en scripts/, subir un nivel para obtener project root
    base_dir = Path(__file__).resolve().parent.parent
    secrets_dir = base_dir / "secrets"

    print("🔐 Validando configuración de secretos...")
    print(f"📁 Directorio base: {base_dir}")
    print(f"📁 Directorio secrets: {secrets_dir}")
    print()

    errors = []
    warnings = []

    # 1. Verificar que existe la carpeta secrets/
    if not secrets_dir.exists():
        errors.append("❌ La carpeta 'secrets/' no existe")
        print("❌ La carpeta 'secrets/' no existe")
        print("   Créala con: mkdir secrets && chmod 700 secrets")
        return False

    print("✅ Carpeta 'secrets/' existe")

    # 2. Verificar permisos de la carpeta
    try:
        perms = oct(secrets_dir.stat().st_mode)[-3:]
        if perms != "700":
            warnings.append(f"⚠️  Permisos de secrets/ deberían ser 700 (actual: {perms})")
            print(f"⚠️  Permisos de secrets/ deberían ser 700 (actual: {perms})")
            print("   Arréglalo con: chmod 700 secrets/")
    except Exception as e:
        warnings.append(f"⚠️  No se pudieron verificar permisos: {e}")

    # 3. Verificar archivos de secretos
    required_secrets = {
        "secret_key.txt": {
            "description": "Django SECRET_KEY",
            "min_length": 30,
            "max_length": 100,
        },
        "db_password.txt": {
            "description": "PostgreSQL password",
            "min_length": 1,
            "max_length": 100,
        },
    }

    for filename, config in required_secrets.items():
        file_path = secrets_dir / filename
        print(f"\n📄 Verificando {filename} ({config['description']})...")

        if not file_path.exists():
            errors.append(f"❌ Falta el archivo: {filename}")
            print(f"   ❌ El archivo no existe")
            continue

        print(f"   ✅ Archivo existe")

        # Verificar permisos del archivo
        try:
            file_perms = oct(file_path.stat().st_mode)[-3:]
            if file_perms not in ("600", "400"):
                warnings.append(
                    f"⚠️  Permisos de {filename} deberían ser 600 o 400 (actual: {file_perms})"
                )
                print(f"   ⚠️  Permisos deberían ser 600 o 400 (actual: {file_perms})")
                print(f"   Arréglalo con: chmod 600 secrets/{filename}")
        except Exception as e:
            warnings.append(f"⚠️  No se pudieron verificar permisos de {filename}: {e}")

        # Verificar contenido
        try:
            content = file_path.read_text().strip()

            if not content:
                errors.append(f"❌ {filename} está vacío")
                print(f"   ❌ El archivo está vacío")
                continue

            print(f"   ✅ Archivo tiene contenido")

            # Verificar longitud
            if len(content) < config["min_length"]:
                errors.append(
                    f"❌ {filename} es demasiado corto "
                    f"(mín: {config['min_length']}, actual: {len(content)})"
                )
                print(
                    f"   ❌ Contenido demasiado corto "
                    f"(mín: {config['min_length']}, actual: {len(content)})"
                )
                continue

            if len(content) > config["max_length"]:
                warnings.append(
                    f"⚠️  {filename} es muy largo "
                    f"(máx recomendado: {config['max_length']}, actual: {len(content)})"
                )
                print(
                    f"   ⚠️  Contenido muy largo "
                    f"(máx: {config['max_length']}, actual: {len(content)})"
                )

            print(f"   ✅ Longitud adecuada: {len(content)} caracteres")

            # Validaciones específicas
            if filename == "secret_key.txt":
                # Detectar SECRET_KEYs inseguras
                insecure_patterns = [
                    "django-insecure-",
                    "change-me",
                    "changeme",
                    "your-secret-key",
                    "secret",
                    "password",
                ]
                content_lower = content.lower()
                for pattern in insecure_patterns:
                    if pattern in content_lower:
                        errors.append(f"❌ secret_key.txt contiene patrón inseguro: '{pattern}'")
                        print(f"   ❌ Contiene patrón inseguro: '{pattern}'")
                        break
                else:
                    print(f"   ✅ No contiene patrones inseguros")

        except Exception as e:
            errors.append(f"❌ Error leyendo {filename}: {e}")
            print(f"   ❌ Error leyendo archivo: {e}")

    # 4. Verificar .env
    print(f"\n📄 Verificando .env...")
    env_file = base_dir / ".env"
    if not env_file.exists():
        warnings.append("⚠️  El archivo .env no existe")
        print("   ⚠️  El archivo .env no existe (opcional pero recomendado)")
    else:
        print("   ✅ Archivo .env existe")

    # 5. Verificar .gitignore
    print(f"\n📄 Verificando .gitignore...")
    gitignore_file = base_dir / ".gitignore"
    if gitignore_file.exists():
        gitignore_content = gitignore_file.read_text()
        if "secrets/" in gitignore_content:
            print("   ✅ secrets/ está en .gitignore")
        else:
            errors.append("❌ secrets/ NO está en .gitignore - ¡PELIGRO DE LEAK!")
            print("   ❌ secrets/ NO está en .gitignore - ¡PELIGRO DE LEAK!")
    else:
        warnings.append("⚠️  No se encontró .gitignore")
        print("   ⚠️  No se encontró .gitignore")

    # Resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN")
    print("=" * 60)

    if errors:
        print(f"\n❌ ERRORES ({len(errors)}):")
        for error in errors:
            print(f"  {error}")

    if warnings:
        print(f"\n⚠️  ADVERTENCIAS ({len(warnings)}):")
        for warning in warnings:
            print(f"  {warning}")

    if not errors and not warnings:
        print("\n✅ ¡TODO CORRECTO! La configuración de secretos es válida.")
        return True
    elif not errors:
        print("\n✅ Configuración válida (con advertencias)")
        return True
    else:
        print(f"\n❌ Se encontraron {len(errors)} errores. Corrígelos antes de continuar.")
        return False


if __name__ == "__main__":
    success = validate_secrets()
    sys.exit(0 if success else 1)
