import { Head } from "@inertiajs/react"
import { AppLayout } from "@/components/layout/app-layout"
import { AvatarUpload } from "@/components/shared/AvatarUpload"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import type { User } from "@/types/models"

interface Props {
    user: User
    permissions: {
        can_edit_avatar: boolean
        can_edit_birthday: boolean
    }
    google_data: any
    title: string
}

export default function ProfileShow({ user, permissions, google_data, title }: Props) {
    const breadcrumbs = [
        { label: "Dashboard", href: "/dashboard" },
        { label: "Mi Perfil", href: "/profile" },
    ]

    return (
        <AppLayout title={title} breadcrumbs={breadcrumbs}>
            <Head title={title} />

            <div className="max-w-4xl mx-auto space-y-6 p-6">
                <Card>
                    <CardHeader>
                        <CardTitle>Información del Perfil</CardTitle>
                        <CardDescription>
                            Gestiona tu información personal y visualiza tus permisos.
                        </CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-8">
                        {/* Sección Avatar */}
                        <div className="flex flex-col items-center space-y-4 sm:flex-row sm:space-y-0 sm:space-x-6">
                            {permissions.can_edit_avatar ? (
                                <AvatarUpload
                                    currentAvatar={user.avatar_url}
                                    fallback={user.first_name.charAt(0)}
                                    className="h-24 w-24"
                                />
                            ) : (
                                <div className="h-24 w-24 rounded-full bg-muted flex items-center justify-center text-2xl font-bold">
                                    {user.first_name.charAt(0)}
                                </div>
                            )}

                            <div className="space-y-1 text-center sm:text-left">
                                <h3 className="text-lg font-medium">{user.first_name} {user.last_name}</h3>
                                <p className="text-sm text-muted-foreground">{user.email}</p>
                                <div className="flex flex-wrap gap-2 justify-center sm:justify-start mt-2">
                                    {user.roles.map((role) => (
                                        <span key={role} className="inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 border-transparent bg-secondary text-secondary-foreground hover:bg-secondary/80">
                                            {role}
                                        </span>
                                    ))}
                                </div>
                            </div>
                        </div>

                        <div className="grid gap-6 md:grid-cols-2">
                            {/* Datos Personales */}
                            <div className="space-y-4">
                                <h4 className="text-sm font-medium text-muted-foreground">Datos Personales</h4>
                                <div className="grid gap-2">
                                    <Label htmlFor="email">Email Corporativo</Label>
                                    <Input id="email" value={user.email} disabled readOnly />
                                </div>
                                <div className="grid grid-cols-2 gap-4">
                                    <div className="grid gap-2">
                                        <Label htmlFor="first_name">Nombre</Label>
                                        <Input id="first_name" value={user.first_name} disabled readOnly />
                                    </div>
                                    <div className="grid gap-2">
                                        <Label htmlFor="last_name">Apellidos</Label>
                                        <Input id="last_name" value={user.last_name} disabled readOnly />
                                    </div>
                                </div>
                                <div className="grid gap-2">
                                    <Label htmlFor="dob">Fecha de Nacimiento</Label>
                                    <Input
                                        id="dob"
                                        value={user.date_of_birth || "No definida"}
                                        disabled={!permissions.can_edit_birthday}
                                        readOnly={!permissions.can_edit_birthday}
                                        type={permissions.can_edit_birthday ? "date" : "text"}
                                    />
                                    {permissions.can_edit_birthday && (
                                        <p className="text-xs text-muted-foreground">
                                            Puedes establecer tu fecha de nacimiento una única vez.
                                        </p>
                                    )}
                                </div>
                            </div>

                            {/* Datos de Sistema */}
                            <div className="space-y-4">
                                <h4 className="text-sm font-medium text-muted-foreground">Información de Cuenta</h4>
                                <div className="rounded-lg border p-4 space-y-3 bg-muted/50">
                                    <div className="flex justify-between text-sm">
                                        <span className="text-muted-foreground">Estado</span>
                                        <span className={user.is_active ? "text-green-600 font-medium" : "text-red-600 font-medium"}>
                                            {user.is_active ? "Activo" : "Inactivo"}
                                        </span>
                                    </div>
                                    {/* Google Data Info */}
                                    {google_data && Object.keys(google_data).length > 0 && (
                                        <div className="pt-2 border-t mt-2">
                                            <p className="text-xs font-medium mb-2">Vinculado con Google</p>
                                            <div className="text-xs text-muted-foreground break-all">
                                                ID: {google_data.sub || "N/A"}
                                            </div>
                                        </div>
                                    )}
                                </div>
                            </div>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </AppLayout>
    )
}
