import { useState, useEffect } from 'react'
import { router } from '@inertiajs/react'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from '@/components/ui/select'

interface UserFiltersProps {
    filters: Record<string, string>
}

export function UserFilters({ filters }: UserFiltersProps) {
    const [searchValue, setSearchValue] = useState(filters.search || '')

    // Debounced search - wait 300ms after user stops typing
    useEffect(() => {
        const timer = setTimeout(() => {
            if (searchValue !== filters.search) {
                router.get('/users', { ...filters, search: searchValue }, {
                    preserveState: true,
                    preserveScroll: true,
                })
            }
        }, 300)

        return () => clearTimeout(timer)
    }, [searchValue, filters])

    function handleFilterChange(key: string, value: string) {
        router.get('/users', { ...filters, [key]: value }, {
            preserveState: true,
            preserveScroll: true,
        })
    }

    return (
        <div className="flex flex-col gap-4 md:flex-row md:items-end">
            <div className="flex-1 space-y-2">
                <Label htmlFor="search">Buscar usuarios</Label>
                <Input
                    id="search"
                    type="text"
                    placeholder="Buscar por email, nombre o apellidos..."
                    value={searchValue}
                    onChange={(e) => setSearchValue(e.target.value)}
                    className="max-w-sm"
                />
            </div>

            <div className="space-y-2">
                <Label htmlFor="is_active">Estado</Label>
                <Select
                    value={filters.is_active || 'all'}
                    onValueChange={(value) => handleFilterChange('is_active', value === 'all' ? '' : value)}
                >
                    <SelectTrigger className="w-40">
                        <SelectValue placeholder="Todos" />
                    </SelectTrigger>
                    <SelectContent>
                        <SelectItem value="all">Todos</SelectItem>
                        <SelectItem value="true">Activos</SelectItem>
                        <SelectItem value="false">Inactivos</SelectItem>
                    </SelectContent>
                </Select>
            </div>

            <div className="space-y-2">
                <Label htmlFor="role">Rol</Label>
                <Select
                    value={filters.role || 'all'}
                    onValueChange={(value) => handleFilterChange('role', value === 'all' ? '' : value)}
                >
                    <SelectTrigger className="w-40">
                        <SelectValue placeholder="Todos" />
                    </SelectTrigger>
                    <SelectContent>
                        <SelectItem value="all">Todos</SelectItem>
                        <SelectItem value="admin">Administrador</SelectItem>
                        <SelectItem value="manager">Manager</SelectItem>
                        <SelectItem value="employee">Empleado</SelectItem>
                    </SelectContent>
                </Select>
            </div>
        </div>
    )
}