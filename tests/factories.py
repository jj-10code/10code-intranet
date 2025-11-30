"""
Factories para testing del módulo accounts.

Proporciona factories con factory_boy para generar datos de prueba
consistentes y realistas para todos los modelos del módulo accounts.
"""

import factory
from factory.django import DjangoModelFactory

from apps.accounts.models import GoogleProfile, Permission, Role, User, UserRole


class UserFactory(DjangoModelFactory):
    """
    Factory para el modelo User.

    Crea usuarios con datos realistas usando Faker.
    Usa el UserManager.create_user para garantizar la correcta
    creación de usuarios con hash de contraseñas.

    Ejemplo:
        user = UserFactory()
        user_with_password = UserFactory(password='testpass123')
        admin_user = UserFactory(is_staff=True, is_superuser=True)
    """

    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user{n}@10code.es")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    is_active = True

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        return manager.create_user(*args, **kwargs)


class GoogleProfileFactory(DjangoModelFactory):
    """
    Factory para el modelo GoogleProfile.

    Crea perfiles OAuth de Google vinculados a usuarios.
    Automáticamente crea un usuario asociado si no se proporciona.
    """

    class Meta:
        model = GoogleProfile

    user = factory.SubFactory(UserFactory)
    google_id = factory.Sequence(lambda n: f"google_id_{n}")
    email = factory.SelfAttribute("user.email")


class RoleFactory(DjangoModelFactory):
    """
    Factory para el modelo Role.

    Crea roles básicos del sistema. Por defecto crea un rol 'employee'.
    Usa django_get_or_create para evitar duplicados al crear múltiples instancias.
    """

    class Meta:
        model = Role
        django_get_or_create = ("code",)

    code = factory.Sequence(lambda n: f"role_{n}")
    name = factory.Faker("job")
    description = factory.Faker("sentence")
    is_system = False


class UserRoleFactory(DjangoModelFactory):
    """
    Factory para el modelo UserRole.

    Crea relaciones entre usuarios y roles con metadata de auditoría.
    Por defecto, asigna un rol 'employee' a un usuario nuevo.
    """

    class Meta:
        model = UserRole

    user = factory.SubFactory(UserFactory)
    role = factory.SubFactory(RoleFactory)
    # assigned_at se asigna automáticamente con timezone.now
    assigned_by = factory.SubFactory(UserFactory)


class PermissionFactory(DjangoModelFactory):
    """
    Factory para el modelo Permission.

    Crea permisos granulares asociados a roles.
    El formato del permission_code sigue el patrón: app.action_model
    """

    class Meta:
        model = Permission

    role = factory.SubFactory(RoleFactory)
    permission_code = factory.Sequence(lambda n: f"app.action_model_{n}")
