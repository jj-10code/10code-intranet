# Patrones Inertia.js y Frontend - 10Code Intranet

## React + TypeScript + Vite + shadcn/ui

## 🎯 FILOSOFÍA INERTIA

Inertia.js transforma el desarrollo frontend al eliminar la necesidad de una API REST tradicional. El servidor envía componentes de React con sus props, creando una experiencia de aplicación de página única sin la complejidad de gestionar estado del servidor en el cliente.

### Principios Fundamentales

**El servidor es la fuente de verdad**: Todas las decisiones de autorización, validación de negocio y preparación de datos ocurren en el backend Django. El frontend React recibe datos preparados y listos para renderizar.

**Props como contrato**: La firma de props de un componente de página Inertia define su interfaz con el backend. Esta claridad facilita el desarrollo independiente de ambos equipos.

**Sin cliente HTTP adicional**: Inertia maneja todas las peticiones HTTP internamente. No es necesario configurar Axios o fetch para comunicarse con el backend.

---

## 🏗️ ARQUITECTURA FRONTEND

### Estructura de Directorios

```txt
frontend/
├── src/
│   ├── main.tsx              # Entry point
│   ├── components/
│   │   ├── ui/              # shadcn/ui primitivos (NO modificar)
│   │   │   ├── button.tsx
│   │   │   ├── card.tsx
│   │   │   └── input.tsx
│   │   ├── shared/          # Componentes aplicación
│   │   │   ├── ProjectCard.tsx
│   │   │   ├── TaskList.tsx
│   │   │   └── UserAvatar.tsx
│   │   └── layout/          # Layouts
│   │       ├── Layout.tsx
│   │       └── AuthLayout.tsx
│   ├── pages/               # Páginas Inertia
│   │   ├── Projects/
│   │   │   ├── Index.tsx
│   │   │   ├── Create.tsx
│   │   │   ├── Edit.tsx
│   │   │   └── Show.tsx
│   │   ├── Resources/
│   │   └── Dashboard/
│   ├── hooks/               # Custom hooks
│   │   ├── usePermissions.ts
│   │   └── useDebounce.ts
│   ├── lib/                 # Utilidades
│   │   └── utils.ts
│   ├── types/               # TypeScript types
│   │   ├── models.ts
│   │   └── index.ts
│   └── stores/              # Zustand stores (solo UI state)
│       └── uiStore.ts
├── package.json
├── tsconfig.json
└── vite.config.ts
```

---

## 📄 PÁGINAS INERTIA

### Template de Página

Cada página Inertia debe seguir esta estructura:

```typescript
// frontend/src/pages/Projects/Index.tsx

import { Head, Link } from '@inertiajs/react'
import Layout from '@/components/layout/Layout'
import { Project } from '@/types/models'
import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'

interface Props {
  projects: Project[]
  filters: Record<string, string>
  permissions: {
    can_create: boolean
    can_export: boolean
  }
}

export default function ProjectsIndex({ projects, filters, permissions }: Props) {
  return (
    <Layout>
      <Head title="Proyectos" />
      
      <div className="container mx-auto px-4 py-8">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold">Proyectos</h1>
          
          {permissions.can_create && (
            <Link href="/projects/create">
              <Button>Nuevo Proyecto</Button>
            </Link>
          )}
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {projects.map((project) => (
            <Card key={project.id}>
              <Link href={`/projects/${project.id}`}>
                <h3>{project.name}</h3>
                <p>{project.client}</p>
              </Link>
            </Card>
          ))}
        </div>
      </div>
    </Layout>
  )
}
```

### Reglas de Páginas

**Type safety total**: Definir interface Props con todos los datos esperados del backend.

**Layout wrapper**: Todas las páginas deben envolverse en un Layout para consistencia.

**Head component**: Usar el componente Head de Inertia para title y meta tags.

**Permisos en props**: Recibir permisos como props booleanos para mostrar/ocultar UI.

---

## 📝 FORMULARIOS CON INERTIA

### Hook useForm

El hook useForm de Inertia simplifica el manejo de formularios:

```typescript
// frontend/src/pages/Projects/Create.tsx

import { useForm } from '@inertiajs/react'
import { FormEvent } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'

export default function ProjectCreate() {
  const { data, setData, post, processing, errors } = useForm({
    name: '',
    client: '',
    methodology: 'scrum',
    budget: ''
  })
  
  const handleSubmit = (e: FormEvent) => {
    e.preventDefault()
    post('/projects')
  }
  
  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div>
        <Label htmlFor="name">Nombre del Proyecto</Label>
        <Input
          id="name"
          value={data.name}
          onChange={e => setData('name', e.target.value)}
          disabled={processing}
        />
        {errors.name && (
          <p className="text-sm text-red-600 mt-1">{errors.name}</p>
        )}
      </div>
      
      <div>
        <Label htmlFor="client">Cliente</Label>
        <Input
          id="client"
          value={data.client}
          onChange={e => setData('client', e.target.value)}
          disabled={processing}
        />
        {errors.client && (
          <p className="text-sm text-red-600 mt-1">{errors.client}</p>
        )}
      </div>
      
      <Button type="submit" disabled={processing}>
        {processing ? 'Creando...' : 'Crear Proyecto'}
      </Button>
    </form>
  )
}
```

### Validación de Formularios

El flujo de validación es transparente:

**Frontend envía**: El formulario se envía con useForm.post()

**Backend valida**: Django Form/Serializer valida los datos

**Errores retornan**: Si falla, Django flashea los errores a la sesión

**Inertia los captura**: El middleware de Inertia los añade automáticamente a props.errors

**Frontend los muestra**: useForm expone los errores en el objeto errors

---

## 🎨 INTEGRACIÓN SHADCN/UI

### Filosofía de Dos Niveles

shadcn/ui no es una librería tradicional. Los componentes se copian directamente al proyecto, otorgando control total sobre el código.

**Nivel 1 - Primitivos (ui/)**: Componentes base de shadcn/ui sin modificar. Estos definen el sistema de diseño.

**Nivel 2 - Aplicación (shared/)**: Componentes específicos del dominio que componen los primitivos.

### Instalación de Componentes

```bash
cd frontend
npx shadcn-ui@latest add button
npx shadcn-ui@latest add card
npx shadcn-ui@latest add input
npx shadcn-ui@latest add form
```

### Composición de Componentes

```typescript
// frontend/src/components/shared/ProjectCard.tsx

import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Project } from '@/types/models'

interface ProjectCardProps {
  project: Project
  onEdit?: () => void
}

export function ProjectCard({ project, onEdit }: ProjectCardProps) {
  return (
    <Card>
      <CardHeader>
        <div className="flex justify-between items-start">
          <CardTitle>{project.name}</CardTitle>
          <Badge variant={project.status === 'active' ? 'default' : 'secondary'}>
            {project.status}
          </Badge>
        </div>
        <CardDescription>{project.client}</CardDescription>
      </CardHeader>
      
      <CardContent>
        <p className="text-sm text-gray-600">{project.description}</p>
        
        {onEdit && (
          <div className="mt-4">
            <Button onClick={onEdit} size="sm">
              Editar
            </Button>
          </div>
        )}
      </CardContent>
    </Card>
  )
}
```

---

## 🔄 GESTIÓN DE ESTADO

### Regla de Oro: Inertia es el State Manager

Para datos del servidor, Inertia ES el gestor de estado. Los props de la página son el estado. No usar React Query, SWR o similar.

### Zustand Solo para UI State

Zustand se usa únicamente para estado de UI efímero que no está vinculado al servidor:

```typescript
// frontend/src/stores/uiStore.ts

import { create } from 'zustand'

interface UIStore {
  sidebarOpen: boolean
  toggleSidebar: () => void
  
  theme: 'light' | 'dark'
  setTheme: (theme: 'light' | 'dark') => void
  
  modalOpen: boolean
  openModal: () => void
  closeModal: () => void
}

export const useUIStore = create<UIStore>((set) => ({
  sidebarOpen: true,
  toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
  
  theme: 'light',
  setTheme: (theme) => set({ theme }),
  
  modalOpen: false,
  openModal: () => set({ modalOpen: true }),
  closeModal: () => set({ modalOpen: false })
}))
```

### Cuándo Usar Zustand

**SÍ usar para**:

- Estado de modales, sidebars, dropdowns
- Tema (dark/light mode)
- Preferencias de UI del usuario
- Estado de formularios multi-paso
- Filtros de tabla en memoria

**NO usar para**:

- Datos de proyectos, usuarios, tareas (usar Inertia)
- Caché de peticiones al servidor (Inertia lo hace)
- Estado que debe persistir entre recargas (usar localStorage + Inertia)

---

## 🔗 NAVEGACIÓN Y LINKS

### Links de Inertia

Siempre usar el componente Link de Inertia para navegación interna:

```typescript
import { Link } from '@inertiajs/react'

// ✅ BIEN
<Link href="/projects" className="nav-link">
  Proyectos
</Link>

// ❌ MAL - No usar <a> para rutas internas
<a href="/projects">Proyectos</a>
```

### Navegación Programática

```typescript
import { router } from '@inertiajs/react'

// Navegación simple
const goToProject = (id: number) => {
  router.visit(`/projects/${id}`)
}

// Con datos (POST)
const createProject = (data: ProjectData) => {
  router.post('/projects', data)
}

// Con confirmación
const deleteProject = (id: number) => {
  if (confirm('¿Eliminar proyecto?')) {
    router.delete(`/projects/${id}`)
  }
}
```

### Recargas Parciales

Optimización clave: recargar solo los datos necesarios:

```typescript
import { router } from '@inertiajs/react'

// Recargar solo el campo 'projects'
router.reload({
  only: ['projects'],
  preserveScroll: true
})

// Útil para actualizar listas sin recargar toda la página
const refreshProjects = () => {
  router.reload({ only: ['projects'] })
}
```

---

## 🪝 CUSTOM HOOKS

### Hook de Permisos

```typescript
// frontend/src/hooks/usePermissions.ts

import { usePage } from '@inertiajs/react'

interface PageProps {
  permissions?: Record<string, boolean>
}

export function usePermissions() {
  const { props } = usePage<PageProps>()
  
  const can = (permission: string): boolean => {
    return props.permissions?.[permission] ?? false
  }
  
  return { can }
}

// Uso en componente
import { usePermissions } from '@/hooks/usePermissions'

export default function ProjectsIndex() {
  const { can } = usePermissions()
  
  return (
    <div>
      {can('create_project') && (
        <Button>Nuevo Proyecto</Button>
      )}
    </div>
  )
}
```

### Hook de Usuario Actual

```typescript
// frontend/src/hooks/useAuth.ts

import { usePage } from '@inertiajs/react'
import { User } from '@/types/models'

interface AuthProps {
  auth: {
    user: User
  }
}

export function useAuth() {
  const { props } = usePage<AuthProps>()
  
  return {
    user: props.auth.user,
    isAuthenticated: !!props.auth.user
  }
}
```

---

## 📱 RESPONSIVE DESIGN

### Mobile-First Approach

Todos los componentes deben diseñarse mobile-first:

```typescript
export default function ProjectsGrid({ projects }: Props) {
  return (
    <div className="
      grid 
      grid-cols-1           /* Mobile: 1 columna */
      md:grid-cols-2        /* Tablet: 2 columnas */
      lg:grid-cols-3        /* Desktop: 3 columnas */
      xl:grid-cols-4        /* Large: 4 columnas */
      gap-4
    ">
      {projects.map(project => (
        <ProjectCard key={project.id} project={project} />
      ))}
    </div>
  )
}
```

---

## ⚡ PERFORMANCE

### Lazy Loading de Componentes

```typescript
import { lazy, Suspense } from 'react'

const HeavyChart = lazy(() => import('@/components/HeavyChart'))

export default function Dashboard() {
  return (
    <Suspense fallback={<div>Cargando gráfico...</div>}>
      <HeavyChart data={chartData} />
    </Suspense>
  )
}
```

### Memoización

```typescript
import { useMemo } from 'react'

export default function ProjectsList({ projects, filters }: Props) {
  const filteredProjects = useMemo(() => {
    return projects.filter(p => 
      p.status === filters.status &&
      p.name.includes(filters.search)
    )
  }, [projects, filters])
  
  return (
    <div>
      {filteredProjects.map(project => (
        <ProjectCard key={project.id} project={project} />
      ))}
    </div>
  )
}
```

---

## 🔒 SEGURIDAD

### XSS Protection

React escapa automáticamente todo el contenido renderizado. Solo usar dangerouslySetInnerHTML con datos sanitizados del servidor:

```typescript
// ❌ PELIGROSO
<div dangerouslySetInnerHTML={{ __html: userInput }} />

// ✅ SEGURO - Sanitizado en backend
<div dangerouslySetInnerHTML={{ __html: sanitizedContent }} />
```

### CSRF Protection

Inertia maneja CSRF automáticamente. No requiere configuración adicional en el frontend.

---

## 📝 CHECKLIST POR PÁGINA

Al crear una nueva página Inertia:

- [ ] Definir interface Props completa con TypeScript
- [ ] Usar componente Head para title
- [ ] Envolver en Layout apropiado
- [ ] Recibir permisos como props para UI condicional
- [ ] Usar componentes de shadcn/ui apropiados
- [ ] Implementar responsive design mobile-first
- [ ] Manejar estados loading y error
- [ ] Usar Links de Inertia para navegación
- [ ] Validar formularios con useForm
- [ ] Testing con React Testing Library

---

Este documento establece los estándares para todo desarrollo frontend en el proyecto. La consistencia en estos patrones garantiza mantenibilidad y calidad a largo plazo.
