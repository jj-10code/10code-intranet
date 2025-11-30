import { Head, useForm } from '@inertiajs/react'
import type { FormEvent } from 'react'
import { AppLayout } from '@/components/layout/app-layout'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Checkbox } from '@/components/ui/checkbox'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import type { Role } from '@/types/models'

interface Props {
    available_roles: Role[]
    permissions: {
        can_assign_roles: boolean
    }
}

export default function UserCreate({ available_roles, permissions }: Props) {
    const { data, setData, post, processing, errors } = useForm({
        email: '',
        first_name: '',
        last_name: '',
        date_of_birth: '',
        roles: [] as string[],
    })

    function handleSubmit(e: FormEvent) {
        e.preventDefault()
        post('/users/create')
    }

    const handleRoleChange = (roleCode: string, checked: boolean) => {
        if (checked) {
            setData('roles', [...data.roles, roleCode])
        } else {
            setData('roles', data.roles.filter((r) => r !== roleCode))
        }
    }

    return (
        <AppLayout
            title="Crear Usuario"
            breadcrumbs={[
                { label: 'Usuarios', href: '/users' },
                { label: 'Crear Usuario', href: '/users/create' },
            ]}
        >
            <Head title="Crear Usuario" />

            <div className="flex flex-col gap-6">
                <Card>
                    <CardHeader>
                        <CardTitle>Crear Nuevo Usuario</CardTitle>
                        <CardDescription>
                            Complete el formulario para registrar un nuevo usuario manualmente.
                        </CardDescription>
                    </CardHeader>
                    <CardContent>
                        <form onSubmit={handleSubmit} className="space-y-6">
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <div className="space-y-2">
                                    <Label htmlFor="email">Email Corporativo</Label>
                                    <Input
                                        id="email"
                                        type="email"
                                        placeholder="usuario@10code.es"
                                        value={data.email}
                                        onChange={(e) => setData('email', e.target.value)}
                                        required
                                    />
                                    {errors.email && (
                                        <p className="text-sm text-destructive">{errors.email}</p>
                                    )}
                                </div>

                                <div className="space-y-2">
                                    <Label htmlFor="date_of_birth">Fecha de Nacimiento</Label>
                                    <Input
                                        id="date_of_birth"
                                        type="date"
                                        value={data.date_of_birth}
                                        onChange={(e) => setData('date_of_birth', e.target.value)}
                                        required
                                    />
                                    {errors.date_of_birth && (
                                        <p className="text-sm text-destructive">
                                            {errors.date_of_birth}
                                        </p>
                                    )}
                                </div>

                                <div className="space-y-2">
                                    <Label htmlFor="first_name">Nombre</Label>
                                    <Input
                                        id="first_name"
                                        type="text"
                                        placeholder="Nombre"
                                        value={data.first_name}
                                        onChange={(e) => setData('first_name', e.target.value)}
                                        required
                                    />
                                    {errors.first_name && (
                                        <p className="text-sm text-destructive">
                                            {errors.first_name}
                                        </p>
                                    )}
                                </div>

                                <div className="space-y-2">
                                    <Label htmlFor="last_name">Apellidos</Label>
                                    <Input
                                        id="last_name"
                                        type="text"
                                        placeholder="Apellidos"
                                        value={data.last_name}
                                        onChange={(e) => setData('last_name', e.target.value)}
                                        required
                                    />
                                    {errors.last_name && (
                                        <p className="text-sm text-destructive">
                                            {errors.last_name}
                                        </p>
                                    )}
                                </div>
                            </div>

                            {permissions.can_assign_roles && (
                                <div className="space-y-3">
                                    <Label>Roles</Label>
                                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 border p-4 rounded-md">
                                        {available_roles.map((role) => (
                                            <div
                                                key={role.code}
                                                className="flex items-center space-x-2"
                                            >
                                                <Checkbox
                                                    id={`role-${role.code}`}
                                                    checked={data.roles.includes(role.code)}
                                                    onCheckedChange={(checked) =>
                                                        handleRoleChange(
                                                            role.code,
                                                            checked as boolean
                                                        )
                                                    }
                                                />
                                                <Label
                                                    htmlFor={`role-${role.code}`}
                                                    className="font-normal cursor-pointer"
                                                >
                                                    {role.name}
                                                </Label>
                                            </div>
                                        ))}
                                    </div>
                                    {errors.roles && (
                                        <p className="text-sm text-destructive">{errors.roles}</p>
                                    )}
                                </div>
                            )}

                            <div className="flex justify-end">
                                <Button type="submit" disabled={processing}>
                                    {processing ? 'Creando...' : 'Crear Usuario'}
                                </Button>
                            </div>
                        </form>
                    </CardContent>
                </Card>
            </div>
        </AppLayout>
    )
}
