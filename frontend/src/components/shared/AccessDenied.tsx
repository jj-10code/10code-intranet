import { ShieldAlert } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { Link } from '@inertiajs/react'

interface AccessDeniedProps {
    permission?: string
    message?: string
}

export function AccessDenied({
    permission,
    message = "No tienes permisos para acceder a esta sección"
}: AccessDeniedProps) {
    return (
        <div className="min-h-screen flex items-center justify-center bg-muted/50">
            <Card className="w-full max-w-md">
                <CardContent className="pt-6">
                    <div className="flex flex-col items-center text-center">
                        <div className="rounded-full bg-destructive/10 p-6 mb-4">
                            <ShieldAlert className="h-12 w-12 text-destructive" />
                        </div>

                        <h2 className="text-2xl font-bold mb-2">Acceso Denegado</h2>
                        <p className="text-muted-foreground mb-6">
                            {message}
                        </p>

                        {permission && (
                            <p className="text-xs text-muted-foreground mb-6 font-mono bg-muted px-3 py-1 rounded">
                                Permiso requerido: {permission}
                            </p>
                        )}

                        <div className="flex gap-3">
                            <Button variant="outline" onClick={() => window.history.back()}>
                                Volver Atrás
                            </Button>
                            <Button asChild>
                                <Link href="/dashboard">Ir al Dashboard</Link>
                            </Button>
                        </div>
                    </div>
                </CardContent>
            </Card>
        </div>
    )
}
