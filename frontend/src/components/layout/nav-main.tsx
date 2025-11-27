import { useState, useEffect } from 'react'
import { IconCirclePlusFilled, IconMail, IconChevronDown } from "@tabler/icons-react"
import { usePage, Link } from '@inertiajs/react'

import { Button } from '@/components/ui/button'
import {
  SidebarGroup,
  SidebarGroupContent,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from '@/components/ui/sidebar'
import { cn } from '@/lib/utils'
import type { MenuItem } from '@/types/layout'

export function NavMain({
  items,
}: {
  items: MenuItem[]
}) {
  const { url } = usePage()
  const [expandedItems, setExpandedItems] = useState<Set<string>>(new Set())

  const isActive = (path: string): boolean => {
    if (path === '#') return false
    return url.startsWith(path)
  }

  useEffect(() => {
    const itemsToExpand = items.filter(item =>
      item.items?.some(subItem => isActive(subItem.url))
    ).map(i => i.title)

    if (itemsToExpand.length > 0) {
      setExpandedItems(prev => {
        const next = new Set(prev)
        let changed = false
        itemsToExpand.forEach(title => {
          if (!next.has(title)) {
            next.add(title)
            changed = true
          }
        })
        return changed ? next : prev
      })
    }
  }, [url, items])

  const toggleItem = (title: string) => {
    setExpandedItems(prev => {
      const next = new Set(prev)
      if (next.has(title)) {
        next.delete(title)
      } else {
        next.add(title)
      }
      return next
    })
  }

  return (
    <SidebarGroup>
      <SidebarGroupContent className="flex flex-col gap-2">
        <SidebarMenu>
          <SidebarMenuItem className="flex items-center gap-2">
            <SidebarMenuButton
              tooltip="Quick Create"
              className="bg-primary text-primary-foreground hover:bg-primary/90 hover:text-primary-foreground active:bg-primary/90 active:text-primary-foreground min-w-8 duration-200 ease-linear"
            >
              <IconCirclePlusFilled />
              <span>Quick Create</span>
            </SidebarMenuButton>
            <Button
              size="icon"
              className="size-8 group-data-[collapsible=icon]:opacity-0"
              variant="outline"
            >
              <IconMail />
              <span className="sr-only">Inbox</span>
            </Button>
          </SidebarMenuItem>
        </SidebarMenu>
        <SidebarMenu>
          {items.map((item) => (
            <SidebarMenuItem key={item.title}>
              {item.items ? (
                // Item con submenú
                <div className="space-y-1">
                  <SidebarMenuButton
                    onClick={() => toggleItem(item.title)}
                    tooltip={item.title}
                    className={cn(
                      "w-full",
                      isActive(item.url) && "bg-accent text-accent-foreground"
                    )}
                  >
                    {item.icon && <item.icon />}
                    <span className="flex-1 text-left">{item.title}</span>
                    <IconChevronDown
                      className={cn(
                        "size-4 transition-transform duration-200",
                        expandedItems.has(item.title) && "rotate-180"
                      )}
                    />
                  </SidebarMenuButton>

                  {expandedItems.has(item.title) && (
                    <div className="ml-8 space-y-1 group-data-[collapsible=icon]:hidden">
                      {item.items.map((subItem) => (
                        <SidebarMenuButton
                          key={subItem.title}
                          asChild
                          className={cn(
                            isActive(subItem.url) && "bg-accent/50 text-accent-foreground"
                          )}
                        >
                          <Link href={subItem.url}>
                            <span>{subItem.title}</span>
                          </Link>
                        </SidebarMenuButton>
                      ))}
                    </div>
                  )}
                </div>
              ) : (
                // Item simple
                <SidebarMenuButton
                  tooltip={item.title}
                  asChild
                  className={cn(
                    isActive(item.url) && "bg-accent text-accent-foreground"
                  )}
                >
                  <Link href={item.url}>
                    {item.icon && <item.icon />}
                    <span>{item.title}</span>
                  </Link>
                </SidebarMenuButton>
              )}
            </SidebarMenuItem>
          ))}
        </SidebarMenu>
      </SidebarGroupContent>
    </SidebarGroup>
  )
}
