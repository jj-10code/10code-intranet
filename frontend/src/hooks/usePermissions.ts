import { usePage } from '@inertiajs/react'

interface PageProps {
    permissions?: Record<string, boolean>
    [key: string]: unknown
}

export function usePermissions() {
    const { props } = usePage<PageProps>()

    const can = (permission: string): boolean => {
        return props.permissions?.[permission] ?? false
    }

    const canAny = (permissions: string[]): boolean => {
        return permissions.some(can)
    }

    const canAll = (permissions: string[]): boolean => {
        return permissions.every(can)
    }

    return { can, canAny, canAll }
}
