import type { Icon } from '@tabler/icons-react'
import type { ReactNode } from 'react'

/**
 * Elemento de navegación para las migas de pan (breadcrumbs).
 */
export interface BreadcrumbItem {
    /** Texto a mostrar en el breadcrumb */
    label: string
    /** URL opcional. Si no se provee, se considera el elemento actual/activo */
    href?: string
}

/**
 * Propiedades principales para el componente AppLayout.
 */
export interface AppLayoutProps {
    /** Título de la página actual */
    title?: string
    /** Lista de elementos para las migas de pan */
    breadcrumbs?: BreadcrumbItem[]
    /** Contenido principal de la página */
    children: ReactNode
}

/**
 * Elemento de submenú dentro de un menú principal.
 */
export interface SubMenuItem {
    /** Título del submenú */
    title: string
    /** URL de destino */
    url: string
}

/**
 * Elemento principal del menú lateral.
 */
export interface MenuItem {
    /** Título del menú */
    title: string
    /** URL de destino principal */
    url: string
    /** Icono opcional de Tabler Icons */
    icon?: Icon
    /** Lista opcional de submenús */
    items?: SubMenuItem[]
}

/**
 * Datos del usuario autenticado.
 */
export interface UserData {
    /** Nombre completo del usuario */
    name: string
    /** Correo electrónico del usuario */
    email: string
    /** URL del avatar del usuario */
    avatar: string
}
