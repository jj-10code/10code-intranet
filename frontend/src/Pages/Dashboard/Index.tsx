import { Head, Link, usePage } from "@inertiajs/react"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Button } from "@/components/ui/button"
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuLabel,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Separator } from "@/components/ui/separator"
import { Home, User, LogOut, Menu } from "lucide-react"

interface User {
    id: number
    email: string
    full_name: string
    first_name: string
    last_name: string
    avatar_url: string
    is_staff: boolean
    is_superuser: boolean
    roles: string[]
}

interface DashboardProps {
    user: User
    title: string
}

export default function Dashboard({ user, title }: DashboardProps) {
    const csrf_token = (usePage().props as any).csrf_token

    return (
        <div className="min-h-screen bg-background">
            <Head title={title} />

            {/* Header */}
            <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
                <div className="container flex h-16 items-center px-4">
                    {/* Mobile menu button */}
                    <Button variant="ghost" size="icon" className="md:hidden">
                        <Menu className="h-5 w-5" />
                        <span className="sr-only">Toggle navigation menu</span>
                    </Button>

                    {/* Logo and title */}
                    <div className="mr-4 flex items-center space-x-2">
                        <div className="flex items-center justify-center w-8 h-8 bg-primary rounded-md">
                            <span className="text-primary-foreground text-sm font-bold">10</span>
                        </div>
                        <span className="hidden font-bold sm:inline-block text-xl">
                            10Code
                        </span>
                    </div>

                    <div className="flex flex-1 items-center justify-end space-x-2">
                        {/* Navigation - hidden on mobile */}
                        <nav className="hidden md:flex items-center space-x-6 text-sm font-medium">
                            <Link
                                href="/dashboard/"
                                className="transition-colors hover:text-foreground/80 text-foreground"
                            >
                                Inicio
                            </Link>
                        </nav>

                        {/* User menu */}
                        <div className="flex items-center space-x-2">
                            <form action="/logout/" method="post">
                                <input type="hidden" name="csrfmiddlewaretoken" value={csrf_token} />
                                <Button variant="ghost" size="icon" type="submit" title="Cerrar Sesión">
                                    <LogOut className="h-5 w-5" />
                                    <span className="sr-only">Cerrar Sesión</span>
                                </Button>
                            </form>
                            <DropdownMenu>
                                <DropdownMenuTrigger asChild>
                                    <Button variant="ghost" className="relative h-10 w-10 rounded-full">
                                        <Avatar className="h-10 w-10">
                                            <AvatarImage src={user.avatar_url} alt={user.full_name} />
                                            <AvatarFallback>
                                                {user.first_name ? user.first_name.charAt(0) : user.email.charAt(0).toUpperCase()}
                                            </AvatarFallback>
                                        </Avatar>
                                    </Button>
                                </DropdownMenuTrigger>
                                <DropdownMenuContent className="w-56" align="end" forceMount>
                                    <DropdownMenuLabel className="font-normal">
                                        <div className="flex flex-col space-y-1">
                                            <p className="text-sm font-medium leading-none">{user.full_name}</p>
                                            <p className="text-xs leading-none text-muted-foreground">
                                                {user.email}
                                            </p>
                                        </div>
                                    </DropdownMenuLabel>
                                    <DropdownMenuSeparator />
                                    <DropdownMenuItem asChild>
                                        <Link href="/accounts/profile/" className="cursor-pointer">
                                            <User className="mr-2 h-4 w-4" />
                                            Mi Perfil
                                        </Link>
                                    </DropdownMenuItem>
                                    <DropdownMenuSeparator />
                                    <DropdownMenuItem asChild>
                                        <form action="/logout/" method="post" className="w-full">
                                            <input type="hidden" name="csrfmiddlewaretoken" value={csrf_token} />
                                            <button
                                                type="submit"
                                                className="flex w-full items-center px-2 py-1.5 text-sm cursor-pointer text-destructive hover:bg-accent hover:text-accent-foreground rounded-md transition-colors"
                                            >
                                                <LogOut className="mr-2 h-4 w-4" />
                                                Cerrar Sesión
                                            </button>
                                        </form>
                                    </DropdownMenuItem>
                                </DropdownMenuContent>
                            </DropdownMenu>
                        </div>
                    </div>
                </div>
            </header>

            {/* Main Content */}
            <main className="flex-1 space-y-6 p-6 md:p-8">
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
                                        <AvatarImage src={user.avatar_url} alt={user.full_name} />
                                        <AvatarFallback className="text-lg">
                                            {user.first_name ? user.first_name.charAt(0) : user.email.charAt(0).toUpperCase()}
                                        </AvatarFallback>
                                    </Avatar>
                                    <div className="space-y-1">
                                        <h2 className="text-2xl font-semibold leading-none tracking-tight">
                                            ¡Bienvenido, {user.first_name || user.full_name}!
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
                                    <User className="mr-2 h-4 w-4" />
                                    Ver mi perfil
                                </Link>
                            </Button>
                        </div>
                    </div>

                    <div className="rounded-lg border bg-card text-card-foreground shadow-sm p-6">
                        <div className="flex items-center gap-2 mb-4">
                            <User className="h-5 w-5 text-primary" />
                            <h3 className="text-lg font-semibold">Mi Cuenta</h3>
                        </div>
                        <p className="text-sm text-muted-foreground mb-4">
                            Gestiona tu información personal y configuraciones de cuenta.
                        </p>
                        <div className="space-y-2">
                            <Button variant="outline" size="sm" asChild className="w-full justify-start">
                                <Link href="/accounts/profile/">
                                    <User className="mr-2 h-4 w-4" />
                                    Editar perfil
                                </Link>
                            </Button>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    )
}
