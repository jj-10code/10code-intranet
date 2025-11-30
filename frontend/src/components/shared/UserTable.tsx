import { Badge } from '@/components/ui/badge'
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from '@/components/ui/table'
import type { User } from '@/types/models'

interface UserTableProps {
    users: User[]
}

export function UserTable({ users }: UserTableProps) {
    return (
        <div className="rounded-md border">
            <Table>
                <TableHeader>
                    <TableRow>
                        <TableHead>Usuario</TableHead>
                        <TableHead>Email</TableHead>
                        <TableHead>Estado</TableHead>
                        <TableHead>Roles</TableHead>
                        <TableHead className="hidden md:table-cell">Fecha de registro</TableHead>
                    </TableRow>
                </TableHeader>
                <TableBody>
                    {users.length === 0 ? (
                        <TableRow>
                            <TableCell colSpan={5} className="h-24 text-center">
                                No se encontraron usuarios.
                            </TableCell>
                        </TableRow>
                    ) : (
                        users.map((user) => (
                            <TableRow key={user.id}>
                                <TableCell className="font-medium">
                                    {user.first_name} {user.last_name}
                                </TableCell>
                                <TableCell>{user.email}</TableCell>
                                <TableCell>
                                    <Badge variant={user.is_active ? "default" : "secondary"}>
                                        {user.is_active ? "Activo" : "Inactivo"}
                                    </Badge>
                                </TableCell>
                                <TableCell>
                                    <div className="flex flex-wrap gap-1">
                                        {user.roles.map((role) => (
                                            <Badge key={role} variant="outline" className="text-xs">
                                                {role}
                                            </Badge>
                                        ))}
                                    </div>
                                </TableCell>
                                <TableCell className="hidden md:table-cell">
                                    {user.date_of_birth
                                        ? new Date(user.date_of_birth).toLocaleDateString('es-ES')
                                        : 'N/A'
                                    }
                                </TableCell>
                            </TableRow>
                        ))
                    )}
                </TableBody>
            </Table>
        </div>
    )
}