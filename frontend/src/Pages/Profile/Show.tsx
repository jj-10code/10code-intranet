import { Head, Link } from "@inertiajs/react"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Button } from "@/components/ui/button"
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from "@/components/ui/card"
import { ArrowLeft } from "lucide-react"

interface Role {
    code: string
    name: string
    assigned_at: string
}

interface UserProfile {
    id: number
    email: string
    full_name: string
    first_name: string
    last_name: string
    avatar_url: string
    date_joined: string
    last_login: string | null
    is_staff: boolean
    roles: Role[]
}

interface ProfileProps {
    user: UserProfile
    google_data: any
    title: string
}

export default function Profile({ user, google_data, title }: ProfileProps) {
    return (
        <div className="min-h-screen bg-gray-50 p-8">
            <Head title={title} />
            <div className="mx-auto max-w-3xl space-y-6">
                <Button variant="ghost" asChild className="mb-4">
                    <Link href="/dashboard/">
                        <ArrowLeft className="mr-2 h-4 w-4" />
                        Volver al Dashboard
                    </Link>
                </Button>

                <Card>
                    <CardHeader>
                        <div className="flex items-center gap-4">
                            <Avatar className="h-20 w-20">
                                <AvatarImage src={user.avatar_url} alt={user.full_name} />
                                <AvatarFallback>{user.full_name.charAt(0)}</AvatarFallback>
                            </Avatar>
                            <div>
                                <CardTitle className="text-2xl">{user.full_name}</CardTitle>
                                <CardDescription>{user.email}</CardDescription>
                            </div>
                        </div>
                    </CardHeader>
                    <CardContent className="space-y-6">
                        <div className="grid gap-4 md:grid-cols-2">
                            <div>
                                <h3 className="mb-2 font-semibold">Información Personal</h3>
                                <dl className="space-y-1 text-sm">
                                    <div className="flex justify-between">
                                        <dt className="text-muted-foreground">Nombre:</dt>
                                        <dd>{user.first_name}</dd>
                                    </div>
                                    <div className="flex justify-between">
                                        <dt className="text-muted-foreground">Apellidos:</dt>
                                        <dd>{user.last_name}</dd>
                                    </div>
                                    <div className="flex justify-between">
                                        <dt className="text-muted-foreground">Miembro desde:</dt>
                                        <dd>{new Date(user.date_joined).toLocaleDateString()}</dd>
                                    </div>
                                    <div className="flex justify-between">
                                        <dt className="text-muted-foreground">Último acceso:</dt>
                                        <dd>
                                            {user.last_login
                                                ? new Date(user.last_login).toLocaleString()
                                                : "Nunca"}
                                        </dd>
                                    </div>
                                </dl>
                            </div>

                            <div>
                                <h3 className="mb-2 font-semibold">Roles y Permisos</h3>
                                <div className="space-y-2">
                                    {user.roles.map((role) => (
                                        <div
                                            key={role.code}
                                            className="rounded-md border p-2 text-sm"
                                        >
                                            <div className="font-medium">{role.name}</div>
                                            <div className="text-xs text-muted-foreground">
                                                Asignado: {new Date(role.assigned_at).toLocaleDateString()}
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </div>

                        {Object.keys(google_data).length > 0 && (
                            <div>
                                <h3 className="mb-2 font-semibold">Datos de Google</h3>
                                <pre className="overflow-auto rounded-md bg-muted p-4 text-xs">
                                    {JSON.stringify(google_data, null, 2)}
                                </pre>
                            </div>
                        )}
                    </CardContent>
                </Card>
            </div>
        </div>
    )
}
