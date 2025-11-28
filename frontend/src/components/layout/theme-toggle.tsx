import { IconMoon, IconSun, IconCheck } from '@tabler/icons-react'
import { Button } from '@/components/ui/button'
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import { SidebarMenuButton, useSidebar } from '@/components/ui/sidebar'
import { useTheme } from '@/hooks/use-theme'

export function ThemeToggle({ asSidebarItem }: { asSidebarItem?: boolean }) {
    const { theme, setTheme } = useTheme()
    const { isMobile } = useSidebar()

    if (asSidebarItem) {
        return (
            <DropdownMenu>
                <DropdownMenuTrigger asChild>
                    <SidebarMenuButton tooltip="Cambiar tema">
                        <IconSun className="size-4 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
                        <IconMoon className="absolute size-4 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
                        <span>Cambiar tema</span>
                    </SidebarMenuButton>
                </DropdownMenuTrigger>
                <DropdownMenuContent
                    side={isMobile ? "bottom" : "right"}
                    align="end"
                    sideOffset={4}
                >
                    <DropdownMenuItem onClick={() => setTheme('light')}>
                        <IconCheck className={`mr-2 size-4 ${theme === 'light' ? 'opacity-100' : 'opacity-0'}`} />
                        Claro
                    </DropdownMenuItem>
                    <DropdownMenuItem onClick={() => setTheme('dark')}>
                        <IconCheck className={`mr-2 size-4 ${theme === 'dark' ? 'opacity-100' : 'opacity-0'}`} />
                        Oscuro
                    </DropdownMenuItem>
                    <DropdownMenuItem onClick={() => setTheme('system')}>
                        <IconCheck className={`mr-2 size-4 ${theme === 'system' ? 'opacity-100' : 'opacity-0'}`} />
                        Sistema
                    </DropdownMenuItem>
                </DropdownMenuContent>
            </DropdownMenu>
        )
    }

    return (
        <DropdownMenu>
            <DropdownMenuTrigger asChild>
                <Button variant="ghost" size="sm" className="size-8 p-0">
                    <IconSun className="size-4 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
                    <IconMoon className="absolute size-4 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
                    <span className="sr-only">Cambiar tema</span>
                </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
                <DropdownMenuItem onClick={() => setTheme('light')}>
                    <IconCheck className={`mr-2 size-4 ${theme === 'light' ? 'opacity-100' : 'opacity-0'}`} />
                    Claro
                </DropdownMenuItem>
                <DropdownMenuItem onClick={() => setTheme('dark')}>
                    <IconCheck className={`mr-2 size-4 ${theme === 'dark' ? 'opacity-100' : 'opacity-0'}`} />
                    Oscuro
                </DropdownMenuItem>
                <DropdownMenuItem onClick={() => setTheme('system')}>
                    <IconCheck className={`mr-2 size-4 ${theme === 'system' ? 'opacity-100' : 'opacity-0'}`} />
                    Sistema
                </DropdownMenuItem>
            </DropdownMenuContent>
        </DropdownMenu>
    )
}
