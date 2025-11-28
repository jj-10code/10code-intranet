import * as React from "react"
import { usePage, Link } from '@inertiajs/react'
import { cn } from '@/lib/utils'

import {
  SidebarGroup,
  SidebarGroupContent,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from '@/components/ui/sidebar'
import type { MenuItem } from '@/types/layout'

export function NavSecondary({
  items,
  children,
  ...props
}: {
  items: MenuItem[]
  children?: React.ReactNode
} & React.ComponentPropsWithoutRef<typeof SidebarGroup>) {
  const { url } = usePage()

  const isActive = (path: string): boolean => {
    if (path === '#') return false
    return url.startsWith(path)
  }

  return (
    <SidebarGroup {...props}>
      <SidebarGroupContent>
        <SidebarMenu>
          {items.map((item) => (
            <SidebarMenuItem key={item.title}>
              <SidebarMenuButton
                asChild
                tooltip={item.title}
                className={cn(isActive(item.url) && "bg-accent text-accent-foreground")}
              >
                <Link href={item.url}>
                  {item.icon && <item.icon />}
                  <span>{item.title}</span>
                </Link>
              </SidebarMenuButton>
            </SidebarMenuItem>
          ))}
          {children}
        </SidebarMenu>
      </SidebarGroupContent>
    </SidebarGroup>
  )
}
