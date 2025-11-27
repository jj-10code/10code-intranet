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
        <header className="flex h-16 shrink-0 items-center gap-2 transition-[width,height] ease-linear group-has-data-[collapsible=icon]/sidebar-wrapper:h-12">
            <div className="flex w-full items-center gap-2 px-4">
                {/* Izquierda: Trigger del sidebar */}
                <SidebarTrigger className="-ml-1" />
                <Separator 
                    orientation="vertical" 
                    className="mr-2 data-[orientation=vertical]:h-4" 
                />

                {/* Centro: Breadcrumbs dinámicos */}
                {hasBreadcrumbs && (
                    <Breadcrumb className="flex-1">
                        <BreadcrumbList>
                            {breadcrumbs.map((crumb, index) => {
                                const isLast = index === breadcrumbs.length - 1

                                return (
                                    <BreadcrumbItem key={`${crumb.label}-${index}`} className={!isLast ? "hidden md:block" : ""}>
                                        {!isLast && crumb.href ? (
                                            <>
                                                <BreadcrumbLink href={crumb.href}>
                                                    {crumb.label}
                                                </BreadcrumbLink>
                                                <BreadcrumbSeparator className="hidden md:block" />
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