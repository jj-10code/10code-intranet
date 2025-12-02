import { AlertCircle } from 'lucide-react'

interface AccessDeniedProps {
    permission?: string
    message?: string
}

export function AccessDenied({ permission, message = "No tienes permisos para acceder a esta sección." }: AccessDeniedProps) {
    return (
        <div className="flex flex-col items-center justify-center p-8 text-center border rounded-lg bg-muted/10 border-muted-foreground/20">
            <AlertCircle className="w-10 h-10 mb-4 text-destructive" />
            <h3 className="text-lg font-semibold text-foreground">Acceso Denegado</h3>
            <p className="text-sm text-muted-foreground mt-2">{message}</p>
            {permission && (
                <p className="text-xs text-muted-foreground mt-4 font-mono bg-muted px-2 py-1 rounded">
                    Permiso requerido: {permission}
                </p>
            )}
        </div>
    )
}
