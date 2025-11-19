import factory
from factory.django import DjangoModelFactory
from apps.accounts.models import User, GoogleProfile, Role

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user{n}@10code.es")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    is_active = True

class GoogleProfileFactory(DjangoModelFactory):
    class Meta:
        model = GoogleProfile

    user = factory.SubFactory(UserFactory)
    google_id = factory.Sequence(lambda n: f"google_id_{n}")
    email = factory.SelfAttribute("user.email")

class RoleFactory(DjangoModelFactory):
    class Meta:
        model = Role
        django_get_or_create = ("code",)

    code = "employee"
    name = "Employee"
