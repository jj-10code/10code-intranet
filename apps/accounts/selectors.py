"""
Selectors del módulo de Autenticación y Usuarios.

Contienen queries optimizadas de solo lectura (READ operations).
Siguen el patrón Selector para separación de responsabilidades.
"""

from typing import Optional

from django.db.models import QuerySet

from apps.accounts.models import User


def get_user_by_email(*, email: str) -> Optional[User]:
    """
    Obtiene un usuario por su email.

    Args:
        email: Email del usuario a buscar

    Returns:
        Usuario si existe, None si no

    Example:
        >>> user = get_user_by_email(email="jmarquez@10code.es")
    """
    try:
        return User.objects.get(email=email, is_active=True)
    except User.DoesNotExist:
        return None


def get_user_by_id(*, user_id: int) -> Optional[User]:
    """
    Obtiene un usuario por su ID.

    Args:
        user_id: ID del usuario

    Returns:
        Usuario si existe, None si no
    """
    try:
        return User.objects.get(id=user_id, is_active=True)
    except User.DoesNotExist:
        return None


def get_active_users() -> QuerySet[User]:
    """
    Obtiene todos los usuarios activos.

    Returns:
        QuerySet de usuarios activos
    """
    return User.objects.filter(is_active=True).select_related("google_profile").order_by("email")


def user_has_role(*, user: User, role_code: str) -> bool:
    """
    Verifica si un usuario tiene un rol específico.

    Args:
        user: Usuario a verificar
        role_code: Código del rol (ej: 'superadmin', 'employee')

    Returns:
        True si el usuario tiene el rol, False si no
    """
    return user.user_roles.filter(role__code=role_code).exists()


def user_has_any_role(*, user: User, role_codes: list[str]) -> bool:
    """
    Verifica si un usuario tiene al menos uno de los roles especificados.

    Args:
        user: Usuario a verificar
        role_codes: Lista de códigos de roles

    Returns:
        True si tiene al menos uno, False si no
    """
    return user.user_roles.filter(role__code__in=role_codes).exists()
