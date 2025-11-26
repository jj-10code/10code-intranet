import { IconActivity, IconClock } from '@tabler/icons-react'
import { Button } from '@/components/ui/button'
import { Separator } from '@/components/ui/separator'
import { SidebarTrigger } from '@/components/ui/sidebar'
import type { BreadcrumbItem } from '@/types/layout'

interface AppHeaderProps {
    breadcrumbs?: BreadcrumbItem[]
}

export function AppHeader({ breadcrumbs: _breadcrumbs }: AppHeaderProps) {
    return (
        <header className="flex h-14 shrink-0 items-center gap-2 border-b transition-[width,height] ease-linear">
            <div className="flex w-full items-center gap-2 px-4 lg:px-6">
                {/* Izquierda: Trigger del sidebar */}
                <SidebarTrigger className="-ml-1" />
                <Separator orientation="vertical" className="mx-2 h-4" />

                {/* Centro: Breadcrumbs (implementar en siguiente tarea) */}
                <div className="flex-1">
                    {/* TODO: Implementar breadcrumbs */}
                    <div className="text-sm text-muted-foreground">
                        Breadcrumbs aquí
                    </div>
                </div>

                {/* Derecha: Botones de acción */}
                <div className="hidden items-center gap-2 md:flex">
                    <Button
                        variant="ghost"
                        size="sm"
                        className="size-8 p-0"
                    >
                        <IconActivity className="size-4" />
                        <span className="sr-only">Estado</span>
                    </Button>
                    <Button
                        variant="ghost"
                        size="sm"
                        className="size-8 p-0"
                    >
                        <IconClock className="size-4" />
                        <span className="sr-only">Tiempo</span>
                    </Button>
                </div>
            </div>
        </header>
    )
}
