import { Head, Link, usePage } from "@inertiajs/react"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Button } from "@/components/ui/button"
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from "@/components/ui/card"
import { LogOut, User as UserIcon } from "lucide-react"

interface User {
    id: number
    email: string
    full_name: string
    avatar_url: string
    roles: string[]
}

interface DashboardProps {
    user: User
    title: string
}

export default function Dashboard({ user, title }: DashboardProps) {
    const { csrf_token } = usePage().props as any

    return (
        <div className="min-h-screen bg-gray-50 p-8">
            <Head title={title} />
            <div className="mx-auto max-w-4xl space-y-8">
                <div className="flex items-center justify-between">
                    <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
                    <div className="flex gap-2">
                        <Button variant="outline" asChild>
                            <Link href="/accounts/profile/">
                                <UserIcon className="mr-2 h-4 w-4" />
                                Mi Perfil
                            </Link>
                        </Button>
                        <form action="/accounts/logout/" method="post">
                            <input type="hidden" name="csrfmiddlewaretoken" value={csrf_token} />
                            <Button variant="destructive" type="submit">
                                <LogOut className="mr-2 h-4 w-4" />
                                Cerrar Sesión
                            </Button>
                        </form>
                    </div>
                </div>

                <Card>
                    <CardHeader>
                        <CardTitle>Bienvenido, {user.full_name}</CardTitle>
                        <CardDescription>{user.email}</CardDescription>
                    </CardHeader>
                    <CardContent className="flex items-center gap-6">
                        <Avatar className="h-24 w-24">
                            <AvatarImage src={user.avatar_url} alt={user.full_name} />
                            <AvatarFallback>{user.full_name.charAt(0)}</AvatarFallback>
                        </Avatar>
                        <div className="space-y-2">
                            <div className="text-sm font-medium text-muted-foreground">
                                Roles asignados:
                            </div>
                            <div className="flex flex-wrap gap-2">
                                {user.roles.map((role) => (
                                    <span
                                        key={role}
                                        className="inline-flex items-center rounded-full bg-blue-100 px-2.5 py-0.5 text-xs font-medium text-blue-800"
                                    >
                                        {role}
                                    </span>
                                ))}
                            </div>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    )
}
