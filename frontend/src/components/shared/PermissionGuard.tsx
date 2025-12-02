import { usePermissions } from '@/hooks/usePermissions'
import { AccessDenied } from '@/components/shared/AccessDenied'

interface PermissionGuardProps {
    permission: string
    fallback?: React.ReactNode
    children: React.ReactNode
}

export function PermissionGuard({
    permission,
    fallback,
    children
}: PermissionGuardProps) {
    const { can } = usePermissions()

    if (!can(permission)) {
        return fallback || <AccessDenied permission={permission} />
    }

    return <>{children}</>
}
