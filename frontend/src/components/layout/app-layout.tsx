import { Head } from '@inertiajs/react'
import { SidebarProvider } from '@/components/ui/sidebar'
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
                <main className="flex flex-1 flex-col w-full">
                    <AppHeader breadcrumbs={breadcrumbs} />
                    <div className="flex-1 p-4 lg:p-6 @container/main">
                        {children}
                    </div>
                </main>
            </SidebarProvider>
        </>
    )
}