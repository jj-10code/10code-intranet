# AppLayout

El componente `AppLayout` es el layout principal de la aplicación 10Code Intranet. Proporciona una estructura consistente con Sidebar, Header y área de contenido principal, integrando funcionalidades de navegación y autenticación.

## Uso Básico

Para utilizar el layout en una página, importa `AppLayout` y envuelve tu contenido. Puedes proporcionar un título para la pestaña del navegador y breadcrumbs para la navegación.

```typescript
import { AppLayout } from '@/components/layout'

export default function MyPage() {
  return (
    <AppLayout 
      title="Mi Página"
      breadcrumbs={[
        { label: "Dashboard", href: "/dashboard/" },
        { label: "Mi Sección" }
      ]}
    >
      <div className="space-y-6">
        {/* Tu contenido aquí */}
        <h1 className="text-2xl font-bold">Bienvenido a mi sección</h1>
        <p>Este es el contenido principal de la página.</p>
      </div>
    </AppLayout>
  )
}
```

## Props

| Prop | Tipo | Descripción |
|------|------|-------------|
| `title` | `string` | Título de la página que se mostrará en la pestaña del navegador (vía `Head` de Inertia). Por defecto: '10Code Intranet'. |
| `breadcrumbs` | `BreadcrumbItem[]` | Array de objetos para generar las migas de pan en el header. Cada item puede tener `label` y `href` (opcional). |
| `children` | `ReactNode` | El contenido principal de la página. |

## Estructura del Sidebar

El Sidebar se genera dinámicamente a partir de la configuración en `frontend/src/components/layout/app-sidebar.tsx`. La estructura actual incluye:

### Menú Principal (`navMain`)
- **Dashboard**: Enlace directo al dashboard principal (`/dashboard/`).
- **Gestión de Usuarios**: Grupo desplegable con submenús:
  - Listado de Usuarios (`/users/`)
  - Roles y Permisos (`/users/roles/`)

### Menú Secundario (`navSecondary`)
- **Ayuda**: Enlace a la sección de ayuda (`/help/`).

### Footer
- **Usuario**: Muestra el avatar, nombre y email del usuario actual, con un menú desplegable para acciones de cuenta (Perfil, Facturación, Cerrar sesión, etc.).

## Agregar nuevos items al Sidebar

Para añadir nuevas secciones al menú lateral, edita el archivo `frontend/src/components/layout/app-sidebar.tsx` y actualiza el objeto `navigationData`.

```typescript
// En app-sidebar.tsx, actualizar navigationData
const navigationData = {
  navMain: [
    // Items existentes...
    {
      title: "Nuevo Módulo",
      url: "/nuevo-modulo/",
      icon: IconNuevoModulo, // Importar icono de @tabler/icons-react
      items: [  // Opcional: si tiene submenú
        { title: "Subitem 1", url: "/nuevo-modulo/subitem-1/" },
      ],
    },
  ],
  // ...
}
```

Asegúrate de importar el icono correspondiente desde `@tabler/icons-react`.

## Troubleshooting

### Problemas Comunes

- **Item activo no se resalta**:
  - Verifica que la URL definida en `navigationData` coincida exactamente con la URL actual.
  - El componente `NavMain` utiliza `usePage().url` para determinar el estado activo. Asegúrate de que Inertia esté manejando la navegación correctamente.

- **Sidebar no persiste estado (colapsado/expandido)**:
  - El estado del sidebar se gestiona mediante cookies (`sidebar:state`).
  - Verifica que las cookies estén habilitadas y que `SidebarProvider` en `app-layout.tsx` esté funcionando correctamente.

- **Breadcrumbs no se muestran**:
  - Asegúrate de pasar la prop `breadcrumbs` al componente `AppLayout`.
  - Verifica que el array de breadcrumbs tenga el formato correcto: `[{ label: "Inicio", href: "/" }, { label: "Página Actual" }]`.

## Capturas de Pantalla

*(Aquí se pueden incluir capturas de pantalla de los diferentes estados del layout)*

- **Desktop expandido**: Muestra el sidebar completo con textos e iconos.
- **Desktop colapsado**: Muestra solo los iconos del sidebar (modo "icon").
- **Móvil**: El sidebar se comporta como un drawer (offcanvas) que se desliza desde la izquierda.
