import { Head } from '@inertiajs/react'
import { AppLayout } from '@/components/layout/app-layout'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { UserFilters } from '@/components/shared/UserFilters'
import { UserTable } from '@/components/shared/UserTable'
import { UserPagination } from '@/components/shared/UserPagination'
import { IconPlus } from '@tabler/icons-react'
import type { User } from '@/types/models'

interface Props {
    users: User[]
    filters: Record<string, string>
    pagination: {
        current_page: number
        total_pages: number
        has_next: boolean
        has_previous: boolean
    }
    permissions: {
        can_create: boolean
    }
}

export default function UsersIndex({ users, filters, pagination, permissions }: Props) {
    return (
        <AppLayout
            title="Usuarios"
            breadcrumbs={[
                { label: 'Usuarios', href: '/users' },
            ]}
        >
            <Head title="Usuarios" />

            <div className="flex flex-col gap-6">
                {/* Header with create button */}
                <div className="flex items-center justify-between">
                    <div>
                        <h1 className="text-3xl font-bold tracking-tight">Usuarios</h1>
                        <p className="text-muted-foreground">
                            Gestiona los usuarios del sistema
                        </p>
                    </div>
                    {permissions.can_create && (
                        <Button asChild>
                            <a href="/users/create">
                                <IconPlus className="mr-2 h-4 w-4" />
                                Crear Usuario
                            </a>
                        </Button>
                    )}
                </div>

                {/* Filters */}
                <Card>
                    <CardHeader>
                        <CardTitle>Filtros</CardTitle>
                        <CardDescription>
                            Filtra los usuarios por estado, rol o búsqueda de texto
                        </CardDescription>
                    </CardHeader>
                    <CardContent>
                        <UserFilters filters={filters} />
                    </CardContent>
                </Card>

                {/* Table */}
                <Card>
                    <CardHeader>
                        <CardTitle>Lista de Usuarios</CardTitle>
                        <CardDescription>
                            {users.length} usuario{users.length !== 1 ? 's' : ''} encontrado{users.length !== 1 ? 's' : ''}
                        </CardDescription>
                    </CardHeader>
                    <CardContent>
                        <div className="space-y-4">
                            <UserTable users={users} />
                            <UserPagination pagination={pagination} filters={filters} />
                        </div>
                    </CardContent>
                </Card>
            </div>
        </AppLayout>
    )
}