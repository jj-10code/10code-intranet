import * as React from "react"
import {
  IconBuilding,
  IconDashboard,
  IconHelp,
  IconUsers,
} from "@tabler/icons-react"

import { NavMain } from './nav-main'
import { NavSecondary } from './nav-secondary'
import { NavUser } from './nav-user'
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from '@/components/ui/sidebar'

const navigationData = {
  user: {
    name: "Usuario Demo",
    email: "usuario@10code.es",
    avatar: "/avatars/default.jpg",
  },
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
  return (
    <Sidebar collapsible="offcanvas" {...props}>
      <SidebarHeader>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton
              asChild
              className="data-[slot=sidebar-menu-button]:!p-1.5"
            >
              <a href="#">
                <IconBuilding className="!size-5" />
                <span className="text-base font-semibold">10Code</span>
              </a>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>
      <SidebarContent>
        <NavMain items={navigationData.navMain} />

        <NavSecondary items={navigationData.navSecondary} className="mt-auto" />
      </SidebarContent>
      <SidebarFooter>
        <NavUser user={navigationData.user} />
      </SidebarFooter>
    </Sidebar>
  )
}
