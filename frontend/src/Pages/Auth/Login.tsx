import { Head, router } from "@inertiajs/react"
import { Button } from "@/components/ui/button"
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from "@/components/ui/card"

import { Separator } from "@/components/ui/separator"
import { LogIn } from "lucide-react"
import logoBlack from "../../assets/logo_black.webp"

interface LoginProps {
    google_login_url: string
    title: string
}

export default function Login({ google_login_url, title }: LoginProps) {
    const handleGoogleLogin = () => {
        router.post(google_login_url)
    }

    return (
        <div className="min-h-screen w-full flex items-center justify-center bg-background p-4">
            <Head title={title} />
            <Card className="w-full max-w-md shadow-lg">
                <CardHeader className="space-y-4 text-center">
                    <img src={logoBlack} alt="10Code Logo" className="mx-auto h-12 w-auto object-contain" />
                    <div className="space-y-2">
                        <CardTitle className="text-2xl font-bold tracking-tight">
                            Bienvenido a 10Code
                        </CardTitle>
                        <CardDescription>
                            Accede a tu intranet corporativa
                        </CardDescription>
                    </div>
                </CardHeader>

                <CardContent className="space-y-6">
                    <div className="space-y-4">
                        <Button
                            className="w-full h-11 text-sm font-medium flex items-center justify-center gap-3"
                            size="lg"
                            onClick={handleGoogleLogin}
                            aria-label="Iniciar sesión con Google"
                        >
                            <LogIn className="h-5 w-5" />
                            Continuar con Google
                        </Button>
                    </div>

                    <div className="relative">
                        <div className="absolute inset-0 flex items-center">
                            <Separator className="w-full" />
                        </div>
                        <div className="relative flex justify-center text-xs uppercase">
                            <span className="bg-background px-2 text-muted-foreground">
                                Acceso exclusivo para empleados
                            </span>
                        </div>
                    </div>

                    <div className="text-center text-xs text-muted-foreground">
                        Al continuar, aceptas los términos de servicio y
                        la política de privacidad de 10Code.
                    </div>
                </CardContent>
            </Card>
        </div>
    )
}
