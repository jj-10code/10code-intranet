import { useState, useRef } from "react"
import { router } from "@inertiajs/react"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Input } from "@/components/ui/input"
import { Camera, Loader2 } from "lucide-react"
import { toast } from "sonner"

interface Props {
    currentAvatar: string | null
    fallback: string
    className?: string
}

export function AvatarUpload({ currentAvatar, fallback, className }: Props) {
    const [isLoading, setIsLoading] = useState(false)
    const fileInputRef = useRef<HTMLInputElement>(null)

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0]
        if (!file) return

        // Validar tamaño (max 2MB)
        if (file.size > 2 * 1024 * 1024) {
            toast.error("La imagen no debe superar los 2MB")
            return
        }

        // Validar tipo
        if (!file.type.startsWith("image/")) {
            toast.error("El archivo debe ser una imagen")
            return
        }

        setIsLoading(true)

        router.post("/profile", {
            _method: "post",
            avatar: file,
        }, {
            forceFormData: true,
            onSuccess: () => {
                toast.success("Avatar actualizado correctamente")
                setIsLoading(false)
            },
            onError: (errors) => {
                toast.error("Error al actualizar avatar")
                console.error(errors)
                setIsLoading(false)
            },
            onFinish: () => setIsLoading(false)
        })
    }

    const triggerClick = () => {
        fileInputRef.current?.click()
    }

    return (
        <div className={`relative inline-block ${className}`}>
            <Avatar className="h-32 w-32 cursor-pointer transition-opacity hover:opacity-90" onClick={triggerClick} data-testid="avatar-upload-trigger">
                <AvatarImage src={currentAvatar || ""} alt="Avatar" className="object-cover" data-testid="avatar-image" />
                <AvatarFallback className="text-4xl">{fallback}</AvatarFallback>

                {isLoading && (
                    <div className="absolute inset-0 flex items-center justify-center bg-black/50 rounded-full">
                        <Loader2 className="h-8 w-8 animate-spin text-white" />
                    </div>
                )}

                {!isLoading && (
                    <div className="absolute inset-0 flex items-center justify-center bg-black/30 opacity-0 transition-opacity hover:opacity-100 rounded-full">
                        <Camera className="h-8 w-8 text-white" />
                    </div>
                )}
            </Avatar>

            <Input
                ref={fileInputRef}
                type="file"
                className="hidden"
                accept="image/*"
                onChange={handleFileChange}
                disabled={isLoading}
                data-testid="avatar-upload-input"
            />
        </div>
    )
}

