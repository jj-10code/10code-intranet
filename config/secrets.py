"""
Gestión de secretos para 10Code Intranet.

Filosofía KISS: Simple, seguro y funcional.

Prioridades de lectura:
1. /run/secrets/{nombre} - Docker Secrets (producción)
2. secrets/{nombre}.txt - Archivos locales (desarrollo)
3. Variable de entorno {nombre} - Fallback
4. Default (si se proporciona)
"""

import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)


def read_secret(
    secret_name: str,
    *,
    required: bool = True,
    default: str | None = None,
) -> str:
    """
    Lee un secreto desde archivos o variables de entorno.

    Args:
        secret_name: Nombre del secreto (ej: "SECRET_KEY", "DATABASE_PASSWORD")
        required: Si es True, lanza excepción si no se encuentra
        default: Valor por defecto si no se encuentra el secreto

    Returns:
        El valor del secreto como string

    Raises:
        ValueError: Si el secreto es requerido y no se encuentra

    Example:
        >>> secret_key = read_secret("SECRET_KEY", required=True)
        >>> db_password = read_secret("DATABASE_PASSWORD", default="postgres")
    """
    # Obtener el directorio base del proyecto
    base_dir = Path(__file__).resolve().parent.parent

    # 1. Intentar leer desde Docker Secrets (producción)
    docker_secret_path = Path("/run/secrets") / secret_name.lower()
    if docker_secret_path.exists():
        try:
            value = docker_secret_path.read_text().strip()
            logger.info(f"Secret '{secret_name}' cargado desde Docker Secrets")
            return value
        except Exception as e:
            logger.warning(f"Error leyendo Docker secret '{secret_name}': {e}")

    # 2. Intentar leer desde archivo local secrets/ (desarrollo)
    local_secret_path = base_dir / "secrets" / f"{secret_name.lower()}.txt"
    if local_secret_path.exists():
        try:
            value = local_secret_path.read_text().strip()
            logger.info(f"Secret '{secret_name}' cargado desde {local_secret_path}")
            return value
        except Exception as e:
            logger.warning(f"Error leyendo archivo local '{secret_name}': {e}")

    # 3. Intentar leer desde variable de entorno
    if secret_name in os.environ:
        value = os.environ[secret_name]
        logger.info(f"Secret '{secret_name}' cargado desde variable de entorno")
        return value

    # 4. Usar default si se proporciona
    if default is not None:
        logger.info(f"Usando valor por defecto para '{secret_name}'")
        return default

    # 5. Si es requerido y no se encontró, lanzar error
    if required:
        raise ValueError(
            f"Secret requerido '{secret_name}' no encontrado en:\n"
            f"  - Docker Secrets: {docker_secret_path}\n"
            f"  - Archivo local: {local_secret_path}\n"
            f"  - Variable de entorno: {secret_name}\n"
            f"Asegúrate de crear el archivo o definir la variable."
        )

    # 6. No requerido y no encontrado
    logger.warning(f"Secret '{secret_name}' no encontrado, retornando None")
    return None


def validate_secret_key(secret_key: str, *, environment: str = "production") -> bool:
    """
    Valida que SECRET_KEY cumpla requisitos mínimos de seguridad.

    Args:
        secret_key: La clave secreta a validar
        environment: Entorno ('development', 'production', 'staging')

    Returns:
        True si es válida, False si no lo es
    """
    if not secret_key or len(secret_key) == 0:
        return False

    # Longitud mínima según entorno
    min_length = 50 if environment == "production" else 30

    if len(secret_key) < min_length:
        logger.error(
            f"SECRET_KEY debe tener al menos {min_length} caracteres "
            f"en entorno '{environment}' (actual: {len(secret_key)})"
        )
        return False

    # Detectar claves inseguras obvias
    insecure_patterns = [
        "django-insecure-",
        "change-me",
        "changeme",
        "your-secret-key",
        "yoursecretkey",
        "secret",
        "password",
        "12345",
    ]

    secret_key_lower = secret_key.lower()
    for pattern in insecure_patterns:
        if pattern in secret_key_lower:
            logger.error(f"SECRET_KEY contiene patrón inseguro: '{pattern}'")
            return False

    return True


def get_environment() -> str:
    """
    Detecta el entorno actual basado en DJANGO_SETTINGS_MODULE.

    Returns:
        'development', 'production' o 'staging'
    """
    settings_module = os.getenv("DJANGO_SETTINGS_MODULE", "").lower()

    if "production" in settings_module:
        return "production"
    elif "staging" in settings_module:
        return "staging"
    elif "development" in settings_module or "dev" in settings_module:
        return "development"
    else:
        # Default seguro
        logger.warning(
            f"No se pudo detectar entorno desde DJANGO_SETTINGS_MODULE='{settings_module}', "
            "usando 'development'"
        )
        return "development"
