# config/secrets.py
"""Service layer para gestión de secretos en 10Code Intranet."""

import json
import logging
import os
from enum import Enum
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

class Environment(str, Enum):
    """
    Enum para los diferentes entornos de despliegue.
    """
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    STAGING = "staging"

def get_environment(django_settings_module: str) -> Environment:
    """Detecta el entorno actual basado en la variable de entorno DJANGO_SETTINGS_MODULE."""
    settings_module = django_settings_module.lower()
    if "development" in settings_module:
        return Environment.DEVELOPMENT.value
    elif "staging" in settings_module:
        return Environment.STAGING.value
    elif "production" in settings_module:
        return Environment.PRODUCTION.value
    else:
        logger.warning("No se pudo detectar el entorno, usando 'development' por defecto.")
        return Environment.DEVELOPMENT.value


def read_secret(
    env_var: str,
    default: str | None = None,
    secret_type: str = "string",  # Configuración: tipo de parsing, no secreto  # noqa: S107
    required: bool = False,
    validation_func: callable | None = None,
) -> str | bool | int | list[str] | dict[str, Any] | None:
    """
    Lee un secreto desde múltiples fuentes con validación robusta.

    Args:
        env_var: Nombre de la variable de entorno
        default: Valor por defecto si no se encuentra
        secret_type: Tipo de dato ('string', 'bool', 'int', 'list', 'json')
        required: Si es True, falla si no se encuentra el secreto
        validation_func: Función de validación personalizada

    Returns:
        El secreto convertido al tipo especificado

    Raises:
        ValueError: Si el secreto es requerido pero no se encuentra
        ValueError: Si el tipo de dato es inválido
    """
    # 1. Docker Secrets (solo en producción)
    secret_file = Path("/run/secrets") / env_var.lower()
    if secret_file.exists():
        try:
            value = secret_file.read_text().strip()
            logger.info(f"Secret '{env_var}' loaded from Docker Secrets")
            return _parse_secret_value(value, secret_type, validation_func)
        except Exception as e:
            logger.warning(f"Failed to read Docker secret '{env_var}': {e}")
            if required:
                raise ValueError(f"Required Docker secret '{env_var}' could not be read") from e

    # 2. Archivo externo via {env_var}_FILE
    file_path_env = f"{env_var}_FILE"
    if file_path_env in os.environ:
        try:
            file_path = Path(os.environ[file_path_env])
            if file_path.exists():
                value = file_path.read_text().strip()
                logger.info(f"Secret '{env_var}' loaded from file: {file_path}")
                return _parse_secret_value(value, secret_type, validation_func)
        except Exception as e:
            logger.warning(f"Failed to read file secret '{env_var}': {e}")
            if required:
                raise ValueError(f"Required file secret '{env_var}' could not be read") from e

    # 3. Variable de entorno directa
    if env_var in os.environ:
        value = os.environ[env_var]
        logger.debug(f"Secret '{env_var}' loaded from environment variable")
        return _parse_secret_value(value, secret_type, validation_func)

    # 4. Default o error
    if default is not None:
        logger.debug(
            f"Using default value for '{env_var}': {'***' if secret_type == 'string' else default}"
        )
        return _parse_secret_value(str(default), secret_type, validation_func)

    if required:
        raise ValueError(f"Required secret '{env_var}' not found in any source")

    logger.warning(f"Secret '{env_var}' not found, returning None")
    return None


def _parse_secret_value(
    value: str,
    secret_type: str,
    validation_func: callable | None = None,
) -> str | bool | int | list[str] | dict[str, Any] | None:
    """
    Convierte el valor del secreto al tipo especificado con validación.
    """
    try:
        # Parsear según el tipo
        if secret_type == "string":
            result = value
        elif secret_type == "bool":
            result = value.lower() in ("true", "1", "yes", "on")
        elif secret_type == "int":
            result = int(value)
        elif secret_type == "list":
            # Comma-separated list
            result = [item.strip() for item in value.split(",") if item.strip()]
        elif secret_type == "json":
            result = json.loads(value)
        else:
            raise ValueError(f"Unsupported secret type: {secret_type}")

        # Aplicar validación personalizada
        if validation_func and not validation_func(result):
            raise ValueError(f"Secret validation failed for type {secret_type}")

        return result

    except (ValueError, json.JSONDecodeError) as e:
        raise ValueError(f"Failed to parse secret as {secret_type}: {e}") from e


def validate_secret_key(secret_key: str, environment: str = "production") -> bool:
    """
    Valida que el SECRET_KEY de Django cumpla con los requisitos mínimos.

    Args:
        secret_key: La clave secreta a validar
        environment: El entorno ('development', 'production')
    """
    if not secret_key:
        return False

    # Django requiere al menos 50 caracteres para SECRET_KEY
    if len(secret_key) < 50:
        if environment == "development":
            return len(secret_key) >= 20
        return False

    # Para desarrollo, ser más permisivo
    if environment == "development":
        insecure_patterns = [
            "your-secret-key",
            "CHANGE_ME",
        ]
        return not any(pattern in secret_key.upper() for pattern in insecure_patterns)

    # Para production, ser más estricto
    default_keys = ["django-insecure-", "insecure", "change-me", "your-secret-key"]

    return not any(default_key in secret_key.lower() for default_key in default_keys)


def validate_db_url(db_url: str) -> bool:
    """
    Valida que la URL de base de datos tenga el formato correcto.
    """
    if not db_url:
        return False

    # Debe empezar con postgresql://, postgres://, o sqlite://
    valid_prefixes = ["postgresql://", "postgres://", "sqlite://"]
    return any(db_url.startswith(prefix) for prefix in valid_prefixes)


def validate_redis_url(redis_url: str) -> bool:
    """
    Valida que la URL de Redis tenga el formato correcto.
    """
    if not redis_url:
        return False

    return redis_url.startswith("redis://") or redis_url.startswith("rediss://")
