# API Reference: [Módulo]

## Autenticación

Todos los endpoints requieren autenticación OAuth 2.0.

**Header requerido:**

```bash

Authorization: Bearer {access_token}

```

---

## Endpoints

### GET /api/projects/

Lista proyectos del usuario con paginación.

**Query Parameters:**

- `page` (int, opcional): Número de página (default: 1)
- `per_page` (int, opcional): Items por página (default: 25, max: 100)
- `status` (string, opcional): Filtrar por status (`active`, `planning`, `completed`)
- `search` (string, opcional): Buscar en título/descripción

**Response 200:**

```json
{
  "count": 42,
  "next": "/api/projects/?page=2",
  "previous": null,
  "results": [
    {
      "id": "uuid",
      "title": "Proyecto X",
      "status": "active",
      "owner": { "id": "uuid", "name": "John Doe" },
      "created_at": "2025-01-15T10:30:00Z"
    }
  ]
}
```

**Errores:**

- `401 Unauthorized`: Token inválido o expirado
- `403 Forbidden`: Sin permisos para listar proyectos
- `400 Bad Request`: Parámetros inválidos

---

### POST /api/projects/

Crear proyecto nuevo.

**Request Body:**

```json
{
  "title": "Nuevo Proyecto",
  "description": "Descripción...",
  "team_members": ["uuid1", "uuid2"],
  "budget_hours": 200,
  "start_date": "2025-02-01"
}
```

**Response 201:**

```json
{
  "id": "uuid-created",
  "title": "Nuevo Proyecto",
  "status": "planning",
  "created_at": "2025-01-20T14:22:00Z"
}
```

> [Continuar con todos los endpoints...]
