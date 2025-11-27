import { Head } from '@inertiajs/react'
import { SidebarProvider, SidebarInset } from '@/components/ui/sidebar'
import { AppSidebar } from './app-sidebar'
import { AppHeader } from './app-header'
import type { AppLayoutProps } from '@/types/layout'

export function AppLayout({
    title = '10Code Intranet',
    breadcrumbs,
    children
}: AppLayoutProps) {
    return (
        <>
            <Head title={title} />
            <a
                href="#main-content"
                className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 focus:bg-primary focus:text-primary-foreground focus:px-4 focus:py-2 focus:rounded focus:outline-none focus:ring-2 focus:ring-ring"
            >
                Saltar al contenido principal
            </a>
            <SidebarProvider>
                <AppSidebar />
                <SidebarInset>
                    <AppHeader breadcrumbs={breadcrumbs} />
                    <div
                        id="main-content"
                        role="main"
                        className="flex flex-1 flex-col gap-4 p-4 pt-0 @container/main"
                    >
                        {children}
                    </div>
                </SidebarInset>
            </SidebarProvider>
        </>
    )
}