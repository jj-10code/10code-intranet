import { AppLayout } from '@/components/layout'

export default function Help() {
    return (
        <AppLayout
            title="Ayuda"
            breadcrumbs={[{ label: "Ayuda" }]}
        >
            <div className="space-y-6">
                <div className="flex items-center justify-between">
                    <h1 className="text-3xl font-bold tracking-tight">
                        Ayuda
                    </h1>
                </div>
                <div className="p-4 rounded-lg border bg-card text-card-foreground shadow-sm">
                    <p>Página de prueba para verificar la navegación.</p>
                </div>
            </div>
        </AppLayout>
    )
}
