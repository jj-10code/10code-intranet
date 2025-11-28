import * as React from "react"
import defaultAvatar from '@/assets/default-avatar.svg'
import { usePage, Link } from '@inertiajs/react'
import { useEffect } from "react"
import {
  IconDashboard,
  IconHelp,
  IconUsers,
} from "@tabler/icons-react"

import { NavMain } from './nav-main'
import { NavSecondary } from './nav-secondary'
import { NavUser } from './nav-user'
import { ThemeToggle } from './theme-toggle'
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  useSidebar,
} from '@/components/ui/sidebar'

import Logo10Code from '@/assets/logo_10code.webp'

const navigationData = {
  navMain: [
    {
      title: "Dashboard",
      url: "/dashboard/",
      icon: IconDashboard,
    },
    {
      title: "Gestión de Usuarios",
      url: "#",
      icon: IconUsers,
      items: [
        { title: "Listado de Usuarios", url: "/users/" },
        { title: "Roles y Permisos", url: "/users/roles/" },
      ],
    },
  ],
  navSecondary: [
    {
      title: "Ayuda",
      url: "/help/",
      icon: IconHelp,
    },
  ],
}

export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
  const { auth } = usePage<{ auth: { user: { id: number; name: string; email: string; avatar: string | null } } }>().props
  const { setOpenMobile, isMobile } = useSidebar()
  const { url } = usePage()

  // Cerrar sidebar móvil al navegar
  useEffect(() => {
    if (isMobile) {
      setOpenMobile(false)
    }
  }, [url, isMobile, setOpenMobile])

  return (
    <Sidebar collapsible="icon" {...props} aria-label="Navegación principal">
      <SidebarHeader>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton
              asChild
              className="data-[slot=sidebar-menu-button]:!p-1.5"
            >
              <Link href="/dashboard/">
                <img src={Logo10Code} alt="10Code Logo" className="size-5 object-contain" />
                <span className="text-base font-semibold group-data-[collapsible=icon]:hidden">
                  10Code
                </span>
              </Link>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>
      <SidebarContent>
        <NavMain items={navigationData.navMain} />

        <NavSecondary items={navigationData.navSecondary} className="mt-auto">
          <SidebarMenuItem>
            <ThemeToggle asSidebarItem />
          </SidebarMenuItem>
        </NavSecondary>
      </SidebarContent>
      <SidebarFooter>
        <NavUser user={{
          name: auth.user.name,
          email: auth.user.email,
          avatar: auth.user.avatar || defaultAvatar,
        }} />
      </SidebarFooter>
    </Sidebar>
  )
}
