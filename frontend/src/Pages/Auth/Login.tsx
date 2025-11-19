import { Head } from "@inertiajs/react"
import { Button } from "@/components/ui/button"
import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "@/components/ui/card"
import { LogIn } from "lucide-react"

interface LoginProps {
    google_login_url: string
    title: string
}

export default function Login({ google_login_url, title }: LoginProps) {
    return (
        <div className="flex min-h-screen items-center justify-center bg-gray-50 p-4">
            <Head title={title} />
            <Card className="w-full max-w-md">
                <CardHeader className="text-center">
                    <CardTitle className="text-2xl font-bold">10Code Intranet</CardTitle>
                    <CardDescription>
                        Acceso exclusivo para empleados de 10Code
                    </CardDescription>
                </CardHeader>
                <CardContent className="grid gap-4">
                    <div className="text-center text-sm text-muted-foreground">
                        Inicia sesión con tu cuenta corporativa
                    </div>
                </CardContent>
                <CardFooter>
                    <Button className="w-full" asChild>
                        <a href={google_login_url}>
                            <LogIn className="mr-2 h-4 w-4" />
                            Login con Google
                        </a>
                    </Button>
                </CardFooter>
            </Card>
        </div>
    )
}
