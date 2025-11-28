import { AppLayout } from '@/components/layout'

interface User {
    id: number
    name: string
    email: string
}

interface UsersProps {
    users: User[]
}

export default function UsersIndex({ users }: UsersProps) {
    return (
        <AppLayout
            title="Usuarios"
            breadcrumbs={[
                { label: "Gestión de Usuarios", href: "#" },
                { label: "Usuarios" }
            ]}
        >
            <div className="space-y-6">
                <div className="flex items-center justify-between">
                    <h1 className="text-3xl font-bold tracking-tight">
                        Listado de Usuarios
                    </h1>
                </div>

                <div className="rounded-md border">
                    <table className="w-full">
                        <thead className="border-b bg-muted/50">
                            <tr>
                                <th className="p-4 text-left font-medium">Nombre</th>
                                <th className="p-4 text-left font-medium">Email</th>
                            </tr>
                        </thead>
                        <tbody>
                            {users.map((user) => (
                                <tr key={user.id} className="border-b last:border-0">
                                    <td className="p-4">{user.name}</td>
                                    <td className="p-4 text-muted-foreground">{user.email}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </AppLayout>
    )
}
