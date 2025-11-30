# Infraestructura de Testing - Módulo Accounts

Este documento describe la infraestructura de testing configurada para el módulo `apps/accounts`.

## 📋 Descripción General

Se ha implementado un sistema de testing completo con pytest, incluyendo:

- ✅ **pytest-django** configurado
- ✅ **Fixtures básicas** para usuarios, roles y permisos
- ✅ **Factory Boy** para generación de datos de prueba
- ✅ **Coverage** configurado con mínimo del 80%
- ✅ **66 tests** actualmente pasando
- ✅ **86.40% de cobertura** actual

## 🗂️ Estructura de Archivos

```
/
├── pytest.ini                          # Configuración principal de pytest
├── tests/
│   ├── conftest.py                     # Fixtures globales del proyecto
│   ├── factories.py                    # Factories globales (User, Role, etc.)
│   └── accounts/
│       ├── conftest.py                 # Fixtures específicas del módulo accounts
│       ├── test_factories.py           # Tests de verificación de factories
│       ├── test_adapters.py            # Tests de adaptadores OAuth
│       ├── test_middleware.py          # Tests de middleware
│       ├── test_selectors.py           # Tests de selectors
│       ├── test_services.py            # Tests de services
│       └── test_views.py               # Tests de views
```

## 🏭 Factories Disponibles

### UserFactory

Crea usuarios con datos realistas usando Faker.

```python
# Usuario básico
user = UserFactory()

# Usuario con contraseña
user = UserFactory(password='testpass123')

# Usuario administrador
admin_user = UserFactory(is_staff=True, is_superuser=True)

# Usuario inactivo
inactive_user = UserFactory(is_active=False)
```

### RoleFactory

Crea roles del sistema con o sin permisos heredados.

```python
# Rol básico
role = RoleFactory()

# Rol del sistema
admin_role = RoleFactory(
    code="admin",
    name="Administrator",
    is_system=True
)

# Rol con herencia
manager_role = RoleFactory(
    code="manager",
    parent_role=admin_role
)
```

### UserRoleFactory

Crea asignaciones de roles a usuarios con auditoría.

```python
# Asignación básica
user_role = UserRoleFactory()

# Asignación específica
user_role = UserRoleFactory(
    user=user,
    role=employee_role,
    assigned_by=admin_user
)
```

### PermissionFactory

Crea permisos granulares asociados a roles.

```python
# Permiso básico
permission = PermissionFactory()

# Permiso específico
permission = PermissionFactory(
    role=manager_role,
    permission_code="projects.add_project"
)
```

### GoogleProfileFactory

Crea perfiles OAuth de Google vinculados a usuarios.

```python
# Perfil básico (crea usuario automáticamente)
google_profile = GoogleProfileFactory()

# Perfil para usuario existente
google_profile = GoogleProfileFactory(user=existing_user)
```

## 🔧 Fixtures Disponibles

### Fixtures Globales (disponibles en todos los tests)

#### Factories como Fixtures

```python
def test_example(user_factory, role_factory):
    user = user_factory()
    role = role_factory(code="custom")
```

#### Instancias de Modelos

```python
def test_example(user, admin_user):
    # 'user' es un usuario regular
    # 'admin_user' es un superusuario
    assert user.is_staff is False
    assert admin_user.is_staff is True
```

#### Clientes HTTP

```python
def test_example(api_client, authenticated_client, admin_client):
    # api_client: sin autenticación
    # authenticated_client: autenticado como usuario regular
    # admin_client: autenticado como administrador
    
    response = authenticated_client.get("/api/users/")
```

### Fixtures Específicas del Módulo Accounts

#### Roles Predefinidos

```python
def test_example(employee_role, manager_role, admin_role):
    # Roles del sistema ya creados
    assert employee_role.code == "employee"
    assert manager_role.code == "manager"
    assert admin_role.code == "admin"
```

#### Usuarios con Roles

```python
def test_example(user_with_role):
    # Usuario con rol 'employee' ya asignado
    assert user_with_role.has_role("employee") is True
```

#### Requests HTTP con Usuarios

```python
def test_example(authenticated_request, admin_request, request_factory):
    # authenticated_request: request con usuario regular
    # admin_request: request con administrador
    # request_factory: factory para crear requests personalizados
    
    custom_request = request_factory.post("/api/users/", data={...})
```

## 🧪 Ejecutando Tests

### Ejecutar todos los tests del módulo accounts

```bash
uv run pytest tests/accounts/
```

### Ejecutar tests con coverage

```bash
uv run pytest tests/accounts/ --cov=apps/accounts
```

### Ejecutar un archivo específico

```bash
uv run pytest tests/accounts/test_services.py
```

### Ejecutar una clase de tests específica

```bash
uv run pytest tests/accounts/test_services.py::TestUserService
```

### Ejecutar un test específico

```bash
uv run pytest tests/accounts/test_services.py::TestUserService::test_create_user
```

### Ejecutar tests por marcador

```bash
# Solo tests unitarios
uv run pytest -m unit

# Solo tests de integración
uv run pytest -m integration

# Excluir tests lentos
uv run pytest -m "not slow"
```

### Ver cobertura HTML

```bash
uv run pytest tests/accounts/ --cov=apps/accounts --cov-report=html
# Abre htmlcov/index.html en el navegador
```

## 📊 Marcadores de Tests

Los tests pueden marcarse con los siguientes decoradores:

- `@pytest.mark.unit`: Tests unitarios
- `@pytest.mark.integration`: Tests de integración
- `@pytest.mark.slow`: Tests lentos
- `@pytest.mark.api`: Tests de API
- `@pytest.mark.ml`: Tests de machine learning

Ejemplo:

```python
@pytest.mark.unit
def test_user_creation():
    user = UserFactory()
    assert user.email
```

## 🔍 Coverage Requirements

- **Mínimo requerido**: 80%
- **Coverage actual**: 86.40%
- **Total de tests**: 66 tests pasando

### Archivos con coverage completo (100%)

- `apps/accounts/middleware.py`
- `apps/accounts/selectors.py`
- `apps/accounts/urls.py`
- `apps/accounts/views.py`
- `apps/core/middleware.py`
- `apps/core/services.py`

### Archivos con coverage >95%

- `apps/accounts/services.py`: 95.56%

## 📝 Buenas Prácticas

### 1. Usar Factories en lugar de crear objetos manualmente

❌ **Mal**:
```python
def test_user_creation():
    user = User.objects.create(
        email="test@10code.es",
        first_name="Test",
        last_name="User"
    )
```

✅ **Bien**:
```python
def test_user_creation():
    user = UserFactory(
        email="test@10code.es",
        first_name="Test"
    )
```

### 2. Usar fixtures para datos compartidos

❌ **Mal**:
```python
def test_user_role_assignment():
    user = UserFactory()
    role = RoleFactory(code="employee")
    # ...

def test_user_permissions():
    user = UserFactory()  # Duplicado
    role = RoleFactory(code="employee")  # Duplicado
    # ...
```

✅ **Bien**:
```python
def test_user_role_assignment(user, employee_role):
    # user y employee_role ya están creados
    UserRoleFactory(user=user, role=employee_role)

def test_user_permissions(user, employee_role):
    # Reutiliza las mismas fixtures
    PermissionFactory(role=employee_role)
```

### 3. Marcar apropiadamente los tests

```python
@pytest.mark.unit  # Test unitario rápido
def test_user_get_full_name():
    user = UserFactory(first_name="John", last_name="Doe")
    assert user.get_full_name() == "John Doe"

@pytest.mark.integration  # Test de integración
def test_user_login_flow(client):
    response = client.post("/login/", {...})
    assert response.status_code == 200
```

### 4. Usar nombres descriptivos

```python
# ✅ Nombres claros y descriptivos
def test_user_cannot_be_created_without_email():
    with pytest.raises(ValueError):
        UserFactory(email="")

# ❌ Nombres vagos
def test_user_error():
    with pytest.raises(ValueError):
        UserFactory(email="")
```

### 5. Organizar tests en clases por funcionalidad

```python
@pytest.mark.unit
class TestUserCreation:
    """Tests relacionados con la creación de usuarios."""
    
    def test_create_user_with_email(self):
        # ...
    
    def test_create_user_without_email_raises_error(self):
        # ...

@pytest.mark.unit
class TestUserPermissions:
    """Tests relacionados con permisos de usuarios."""
    
    def test_user_has_role(self):
        # ...
```

## 🐛 Debugging Tests

### Ver print statements

```bash
uv run pytest tests/accounts/ -s
```

### Debugger interactivo (ipdb)

```python
def test_example():
    user = UserFactory()
    import ipdb; ipdb.set_trace()  # Breakpoint
    assert user.email
```

### Ver traceback completo

```bash
uv run pytest tests/accounts/ --tb=long
```

### Ejecutar solo el último test fallido

```bash
uv run pytest --lf
```

## 📚 Recursos Adicionales

- [Documentación de pytest](https://docs.pytest.org/)
- [pytest-django](https://pytest-django.readthedocs.io/)
- [factory_boy](https://factoryboy.readthedocs.io/)
- [Django Testing Tools](https://docs.djangoproject.com/en/5.0/topics/testing/tools/)

---

**Última actualización**: 2025-11-30  
**Responsable**: Equipo de Desarrollo 10Code  
**Coverage actual**: 86.40% (66 tests)
