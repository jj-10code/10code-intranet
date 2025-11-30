import { Link } from "@inertiajs/react"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Button } from "@/components/ui/button"
import { Separator } from "@/components/ui/separator"
import { Home, User as UserIcon } from "lucide-react"
import { AppLayout } from "@/components/layout"

import type { User } from "@/types/models"

interface DashboardProps {
    user: User
    title: string
}

export default function Dashboard({ user, title }: DashboardProps) {
    return (
        <AppLayout title={title}>
            <div className="space-y-6">
                <div className="flex items-center justify-between">
                    <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
                </div>

                <Separator />

                {/* Welcome Card */}
                <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
                    <div className="col-span-full">
                        <div className="rounded-lg border bg-card text-card-foreground shadow-sm">
                            <div className="flex flex-col space-y-1.5 p-6">
                                <div className="flex items-center gap-4">
                                    <Avatar className="h-16 w-16">
                                        <AvatarImage src={user.avatar_url || undefined} alt={`${user.first_name} ${user.last_name}`} />
                                        <AvatarFallback className="text-lg">
                                            {user.first_name ? user.first_name.charAt(0) : user.email.charAt(0).toUpperCase()}
                                        </AvatarFallback>
                                    </Avatar>
                                    <div className="space-y-1">
                                        <h2 className="text-2xl font-semibold leading-none tracking-tight">
                                            ¡Bienvenido, {user.first_name}!
                                        </h2>
                                        <p className="text-sm text-muted-foreground">
                                            Has iniciado sesión correctamente en la intranet de 10Code
                                        </p>
                                    </div>
                                </div>
                            </div>
                            <div className="p-6 pt-0">
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                    <div className="space-y-2">
                                        <p className="text-sm font-medium leading-none text-muted-foreground">
                                            Email
                                        </p>
                                        <p className="text-sm">
                                            {user.email}
                                        </p>
                                    </div>
                                    <div className="space-y-2">
                                        <p className="text-sm font-medium leading-none text-muted-foreground">
                                            Roles
                                        </p>
                                        <div className="flex flex-wrap gap-1">
                                            {user.roles.length > 0 ? (
                                                user.roles.map((role) => (
                                                    <span
                                                        key={role}
                                                        className="inline-flex items-center rounded-full bg-primary/10 px-2.5 py-0.5 text-xs font-medium text-primary"
                                                    >
                                                        {role}
                                                    </span>
                                                ))
                                            ) : (
                                                <span className="text-xs text-muted-foreground">
                                                    Sin roles asignados
                                                </span>
                                            )}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Quick Actions */}
                <div className="grid gap-6 md:grid-cols-2">
                    <div className="rounded-lg border bg-card text-card-foreground shadow-sm p-6">
                        <div className="flex items-center gap-2 mb-4">
                            <Home className="h-5 w-5 text-primary" />
                            <h3 className="text-lg font-semibold">Inicio</h3>
                        </div>
                        <p className="text-sm text-muted-foreground mb-4">
                            Desde aquí puedes acceder a todas las funcionalidades de la intranet.
                        </p>
                        <div className="space-y-2">
                            <Button variant="outline" size="sm" asChild className="w-full justify-start">
                                <Link href="/accounts/profile/">
                                    <UserIcon className="mr-2 h-4 w-4" />
                                    Ver mi perfil
                                </Link>
                            </Button>
                        </div>
                    </div>

                    <div className="rounded-lg border bg-card text-card-foreground shadow-sm p-6">
                        <div className="flex items-center gap-2 mb-4">
                            <UserIcon className="h-5 w-5 text-primary" />
                            <h3 className="text-lg font-semibold">Mi Cuenta</h3>
                        </div>
                        <p className="text-sm text-muted-foreground mb-4">
                            Gestiona tu información personal y configuraciones de cuenta.
                        </p>
                        <div className="space-y-2">
                            <Button variant="outline" size="sm" asChild className="w-full justify-start">
                                <Link href="/accounts/profile/">
                                    <UserIcon className="mr-2 h-4 w-4" />
                                    Editar perfil
                                </Link>
                            </Button>
                        </div>
                    </div>
                </div>
            </div>
        </AppLayout>
    )
}
