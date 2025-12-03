import { Head, usePage } from '@inertiajs/react'
import { SidebarProvider, SidebarInset } from '@/components/ui/sidebar'
import { AppSidebar } from './app-sidebar'
import { AppHeader } from './app-header'
import type { AppLayoutProps } from '@/types/layout'
import { useEffect } from 'react'
import { toast } from 'sonner'

interface FlashMessage {
    type: 'success' | 'error' | 'warning' | 'info'
    message: string
}

interface PageProps {
    flash: FlashMessage[]
    [key: string]: unknown
}

export function AppLayout({
    title = '10Code Intranet',
    breadcrumbs,
    children
}: AppLayoutProps) {
    const { flash } = usePage<PageProps>().props

    useEffect(() => {
        if (flash?.length) {
            flash.forEach(({ type, message }) => {
                if (type === 'success') toast.success(message)
                else if (type === 'error') toast.error(message)
                else if (type === 'warning') toast.warning(message)
                else toast.info(message)
            })
        }
    }, [flash])

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
                    <main
                        id="main-content"
                        className="flex flex-1 flex-col gap-4 p-4 pt-0 w-full overflow-x-hidden @container/main"
                    >
                        {children}
                    </main>
                </SidebarInset>
            </SidebarProvider>
        </>
    )
}