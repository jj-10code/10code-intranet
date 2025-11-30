from typing import Dict, List, Any, Optional

from apps.accounts.models import User, Role


def RoleSerializer(role: Role) -> Dict[str, Any]:
    """
    Serializa un objeto Role.
    """
    return {
        "id": role.id,
        "code": role.code,
        "name": role.name,
        "description": role.description,
        "is_system": role.is_system,
    }


def UserSerializer(user: User) -> Dict[str, Any]:
    """
    Serializa User para props de Inertia.
    
    Para evitar problemas de N+1, asegúrese de que el queryset de usuarios
    tenga prefetch_related('user_roles__role').
    """
    return {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "avatar_url": user.avatar_url,
        "is_active": user.is_active,
        "date_of_birth": user.date_of_birth.isoformat() if user.date_of_birth else None,
        "roles": [r.role.name for r in user.user_roles.all()],
    }
