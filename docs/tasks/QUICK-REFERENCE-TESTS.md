# 🚀 Quick Reference - Testing Infrastructure

## Básicos

### Ejecutar tests
```bash
# Todos los tests del módulo accounts
uv run pytest tests/accounts/

# Con coverage
uv run pytest tests/accounts/ --cov=apps/accounts

# Ver reporte HTML
uv run pytest tests/accounts/ --cov-report=html
# Abre: htmlcov/index.html
```

## Factories

### Crear usuarios
```python
# Usuario básico
user = UserFactory()

# Usuario administrador
admin = UserFactory(is_staff=True, is_superuser=True)

# Usuario con email específico
user = UserFactory(email="custom@10code.es")
```

### Crear roles
```python
# Rol básico
role = RoleFactory()

# Rol específico
employee = RoleFactory(code="employee", name="Employee", is_system=True)
```

### Asignar roles
```python
# Asignar rol a usuario
UserRoleFactory(user=user, role=employee_role, assigned_by=admin)

# Verificar rol
assert user.has_role("employee")
```

### Crear permisos
```python
# Permiso básico
permission = PermissionFactory(
    role=manager_role,
    permission_code="projects.add_project"
)
```

## Fixtures

### Usar fixtures predefinidas
```python
def test_example(user, admin_user, employee_role):
    # user: usuario regular
    # admin_user: administrador
    # employee_role: rol de empleado
    UserRoleFactory(user=user, role=employee_role)
    assert user.has_role("employee")
```

### Fixtures HTTP
```python
def test_api(authenticated_client):
    # Cliente autenticado listo para usar
    response = authenticated_client.get("/api/users/")
    assert response.status_code == 200
```

## Marcadores

### Marcar tests
```python
@pytest.mark.unit
def test_user_creation():
    """Test unitario rápido"""
    user = UserFactory()
    assert user.email

@pytest.mark.integration
def test_user_login(client):
    """Test de integración"""
    response = client.post("/login/", {...})
    assert response.status_code == 200
```

### Ejecutar por marcador
```bash
# Solo unitarios
uv run pytest -m unit

# Solo integración
uv run pytest -m integration

# Excluir lentos
uv run pytest -m "not slow"
```

## Coverage

### Ver coverage específico
```bash
# Solo un archivo
uv run pytest tests/accounts/test_services.py --cov=apps/accounts/services.py

# Con detalles de líneas faltantes
uv run pytest --cov=apps/accounts --cov-report=term-missing
```

## Debugging

### Modo verbose
```bash
uv run pytest tests/accounts/ -v
```

### Ver prints
```bash
uv run pytest tests/accounts/ -s
```

### Breakpoint
```python
def test_debug():
    user = UserFactory()
    import ipdb; ipdb.set_trace()  # Pausar aquí
    assert user.email
```

### Último test fallido
```bash
uv run pytest --lf
```

## Tips Rápidos

✅ **HACER**:
- Usar factories para crear datos
- Reutilizar fixtures
- Marcar tests apropiadamente
- Mantener coverage >80%

❌ **EVITAR**:
- Crear objetos manualmente
- Duplicar código de setup
- Tests sin marcadores
- Bajar el coverage

## Recursos

- 📖 Documentación completa: `tests/accounts/README.md`
- 📋 Estado del proyecto: `docs/tasks/T1-configuracion-tests-COMPLETADO.md`
- 📊 Resumen visual: `docs/tasks/T1-RESUMEN-VISUAL.txt`

---

**Coverage actual**: 86.40% | **Tests**: 66 pasando | **DoD**: ✅ Completado
