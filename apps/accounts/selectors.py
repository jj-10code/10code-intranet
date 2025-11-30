"""
Selectors del módulo de Autenticación y Usuarios.

Contienen queries optimizadas de solo lectura (READ operations).
Siguen el patrón Selector para separación de responsabilidades.
"""


from django.db.models import Prefetch, Q, QuerySet

from apps.accounts.models import User, UserRole


def get_user_by_email(*, email: str) -> User | None:
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


def get_user_by_id(*, user_id: int) -> User | None:
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


class RoleSelector:
    """
    Selector para obtener roles disponibles.
    """

    @staticmethod
    def get_available_roles() -> list[dict]:
        """
        Obtiene lista de roles disponibles para asignar.

        Returns:
            Lista de diccionarios con 'code' y 'name'
        """
        from apps.accounts.models import Role

        return list(
            Role.objects.filter(is_system=False)
            .values("code", "name")
            .order_by("name")
        )


class UserSelector:
    """
    Selector para obtener usuarios con filtros y optimizaciones.
    """

    @staticmethod
    def get_users_list(
        *,
        user: User,  # noqa: ARG004  # For future permission checking
        filters: dict | None = None
    ) -> QuerySet[User]:
        """
        Obtener lista de usuarios con filtros y optimizaciones.

        Args:
            user: Usuario solicitante (para permisos)
            filters: Dict con is_active, role, department, search

        Returns:
            QuerySet optimizado con select_related/prefetch_related
        """
        qs = User.objects.select_related('google_profile').prefetch_related(
            Prefetch('user_roles', queryset=UserRole.objects.select_related('role'))
        )

        # Aplicar filtros
        if filters:
            if filters.get('is_active') is not None:
                qs = qs.filter(is_active=filters['is_active'])
            if filters.get('role'):
                qs = qs.filter(user_roles__role__code=filters['role'])
            if filters.get('search'):
                qs = qs.filter(
                    Q(email__icontains=filters['search']) |
                    Q(first_name__icontains=filters['search']) |
                    Q(last_name__icontains=filters['search'])
                )

        return qs.order_by('-date_joined')
