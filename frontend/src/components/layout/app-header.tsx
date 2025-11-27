import { IconActivity, IconClock } from '@tabler/icons-react'
import { Button } from '@/components/ui/button'
import {
    Breadcrumb,
    BreadcrumbList,
    BreadcrumbItem,
    BreadcrumbLink,
    BreadcrumbPage,
    BreadcrumbSeparator,
} from '@/components/ui/breadcrumb'
import { Separator } from '@/components/ui/separator'
import { SidebarTrigger } from '@/components/ui/sidebar'
import type { BreadcrumbItem as BreadcrumbItemType } from '@/types/layout'

interface AppHeaderProps {
    breadcrumbs?: BreadcrumbItemType[]
}

export function AppHeader({ breadcrumbs }: AppHeaderProps) {
    const hasBreadcrumbs = breadcrumbs && breadcrumbs.length > 0

    return (
        <header className="flex h-14 shrink-0 items-center gap-2 border-b transition-[width,height] ease-linear">
            <div className="flex w-full items-center gap-2 px-4 lg:px-6">
                {/* Izquierda: Trigger del sidebar */}
                <SidebarTrigger className="-ml-1" />
                <Separator orientation="vertical" className="mx-2 h-4" />

                {/* Centro: Breadcrumbs dinámicos */}
                {hasBreadcrumbs && (
                    <Breadcrumb className="flex-1 hidden sm:block">
                        <BreadcrumbList>
                            {breadcrumbs.map((crumb, index) => {
                                const isLast = index === breadcrumbs.length - 1

                                return (
                                    <BreadcrumbItem key={`${crumb.label}-${index}`}>
                                        {!isLast && crumb.href ? (
                                            <>
                                                <BreadcrumbLink href={crumb.href}>
                                                    {crumb.label}
                                                </BreadcrumbLink>
                                                <BreadcrumbSeparator />
                                            </>
                                        ) : (
                                            <BreadcrumbPage>{crumb.label}</BreadcrumbPage>
                                        )}
                                    </BreadcrumbItem>
                                )
                            })}
                        </BreadcrumbList>
                    </Breadcrumb>
                )}

                {/* Espacio flexible si no hay breadcrumbs */}
                {!hasBreadcrumbs && <div className="flex-1" />}

                {/* Derecha: Botones de acción */}
                <div className="hidden items-center gap-2 md:flex">
                    <Button variant="ghost" size="sm" className="size-8 p-0">
                        <IconActivity className="size-4" />
                        <span className="sr-only">Estado</span>
                    </Button>
                    <Button variant="ghost" size="sm" className="size-8 p-0">
                        <IconClock className="size-4" />
                        <span className="sr-only">Tiempo</span>
                    </Button>
                </div>
            </div>
        </header>
    )
}
