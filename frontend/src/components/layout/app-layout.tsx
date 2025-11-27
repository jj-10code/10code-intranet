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
            <SidebarProvider>
                <AppSidebar />
                <SidebarInset>
                    <AppHeader breadcrumbs={breadcrumbs} />
                    <div className="flex flex-1 flex-col gap-4 p-4 pt-0 @container/main">
                        {children}
                    </div>
                </SidebarInset>
            </SidebarProvider>
        </>
    )
}