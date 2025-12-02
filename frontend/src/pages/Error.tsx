import { AccessDenied } from '@/components/shared/AccessDenied'
import { Head } from '@inertiajs/react'

interface Props {
    status: number
}

export default function ErrorPage({ status }: Props) {
    const title = {
        503: '503: Servicio no disponible',
        500: '500: Error del servidor',
        404: '404: Página no encontrada',
        403: '403: Acceso denegado',
    }[status]

    const description = {
        503: 'Lo sentimos, estamos realizando tareas de mantenimiento. Por favor, inténtelo de nuevo más tarde.',
        500: 'Vaya, algo ha ido mal en nuestros servidores.',
        404: 'Lo sentimos, la página que busca no se encuentra.',
        403: 'Lo sentimos, no tiene permiso para acceder a esta página.',
    }[status]

    if (status === 403) {
        return (
            <>
                <Head title={title} />
                <AccessDenied />
            </>
        )
    }

    return (
        <div className="flex items-center justify-center min-h-screen p-5 text-indigo-100 bg-indigo-800">
            <Head title={title} />
            <div className="w-full max-w-md">
                <h1 className="text-3xl font-medium">{status}</h1>
                <p className="mt-3 text-xl leading-tight">{title}</p>
                <p className="mt-4 text-lg text-indigo-300">{description}</p>
            </div>
        </div>
    )
}
