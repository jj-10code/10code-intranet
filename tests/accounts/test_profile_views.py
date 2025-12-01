import pytest
from django.urls import reverse
from apps.accounts.models import User

@pytest.mark.integration
@pytest.mark.django_db
class TestProfileViews:
    """Tests para las vistas de perfil de usuario."""

    def test_profile_show_authenticated(self, client, user):
        """
        GET /profile/ autenticado debe retornar 200 y props correctos.
        """
        client.force_login(user)
        response = client.get(reverse("profile"), **{'HTTP_X_INERTIA': 'true', 'HTTP_X_INERTIA_VERSION': '1.0'})

        assert response.status_code == 200
        
        # Verificar props de Inertia
        data = response.json()
        props = data["props"]
        
        assert props["user"]["id"] == user.id
        assert props["user"]["email"] == user.email
        
        # Verificar permisos calculados
        # UserFactory no setea date_of_birth, así que debería ser True
        assert props["permissions"]["can_edit_avatar"] is True
        assert props["permissions"]["can_edit_birthday"] is True

    def test_profile_show_unauthenticated(self, client):
        """
        GET /profile/ sin autenticar debe redirigir al login.
        """
        response = client.get(reverse("profile"))
        assert response.status_code == 302
        # La URL de login configurada parece ser /login/
        assert "/login/" in response.url

    def test_profile_update_avatar(self, client, user):
        """
        POST /profile/ debe actualizar el avatar.
        """
        client.force_login(user)
        new_avatar = "https://example.com/avatar.jpg"
        
        # POST requests en Inertia también pueden ser interceptados, pero para redirects
        # el comportamiento estándar de Django 302 es lo que esperamos.
        response = client.post(reverse("profile"), {
            "avatar_url": new_avatar
        })

        assert response.status_code == 302
        assert response.url == reverse("profile")

        user.refresh_from_db()
        assert user.avatar_url == new_avatar

    def test_profile_update_avatar_file(self, client, user):
        """
        POST /profile/ con archivo debe actualizar el avatar.
        """
        client.force_login(user)
        
        # Crear imagen dummy
        from io import BytesIO
        from django.core.files.uploadedfile import SimpleUploadedFile
        from PIL import Image
        
        img_io = BytesIO()
        img = Image.new('RGB', (100, 100), color='red')
        img.save(img_io, format='JPEG')
        img_content = img_io.getvalue()
        
        avatar_file = SimpleUploadedFile("avatar.jpg", img_content, content_type="image/jpeg")
        
        response = client.post(reverse("profile"), {
            "avatar": avatar_file
        })

        assert response.status_code == 302
        assert response.url == reverse("profile")

        user.refresh_from_db()
        assert user.avatar
        assert "avatar.jpg" in user.avatar.name

    def test_can_edit_birthday_logic(self, client, user):
        """
        Verificar lógica de can_edit_birthday.
        """
        client.force_login(user)

        # Caso 1: Sin fecha de nacimiento -> True
        assert user.date_of_birth is None
        response = client.get(reverse("profile"), **{'HTTP_X_INERTIA': 'true', 'HTTP_X_INERTIA_VERSION': '1.0'})
        data = response.json()
        assert data["props"]["permissions"]["can_edit_birthday"] is True

        # Caso 2: Con fecha de nacimiento -> False
        from django.utils import timezone
        user.date_of_birth = timezone.now().date()
        user.save()
        
        response = client.get(reverse("profile"), **{'HTTP_X_INERTIA': 'true', 'HTTP_X_INERTIA_VERSION': '1.0'})
        data = response.json()
        assert data["props"]["permissions"]["can_edit_birthday"] is False
