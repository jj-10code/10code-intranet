from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from apps.accounts.models import Role
from apps.accounts.services import AuthService


class UserCreationForm(forms.Form):
    """
    Formulario para creación manual de usuarios.
    """

    email = forms.EmailField(label="Email corporativo")
    first_name = forms.CharField(label="Nombre", max_length=150)
    last_name = forms.CharField(label="Apellidos", max_length=150)
    date_of_birth = forms.DateField(
        label="Fecha de nacimiento", widget=forms.DateInput(attrs={"type": "date"})
    )
    roles = forms.MultipleChoiceField(
        label="Roles", widget=forms.CheckboxSelectMultiple, required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Cargar opciones de roles dinámicamente
        self.fields["roles"].choices = [
            (role.code, role.name)
            for role in Role.objects.filter(is_system=False).order_by("name")
        ]

    def clean_email(self):
        email = self.cleaned_data["email"]
        if not AuthService.validate_email_domain(email):
            raise ValidationError("El email debe pertenecer al dominio @10code.es")
        return email

    def clean_date_of_birth(self):
        dob = self.cleaned_data["date_of_birth"]
        today = timezone.now().date()
        age = (
            today.year
            - dob.year
            - ((today.month, today.day) < (dob.month, dob.day))
        )
        if age < 16:
            raise ValidationError("El usuario debe tener al menos 16 años.")
        return dob
