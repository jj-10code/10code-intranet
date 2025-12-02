import { useState } from 'react'
import { router } from '@inertiajs/react'
import { toast } from 'sonner'
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
} from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { Label } from '@/components/ui/label'
import type { User } from '@/types/models'

interface DeactivateUserModalProps {
    user: User
    open: boolean
    onOpenChange: (open: boolean) => void
}

export function DeactivateUserModal({ user, open, onOpenChange }: DeactivateUserModalProps) {
    const [reason, setReason] = useState('')
    const [isSubmitting, setIsSubmitting] = useState(false)

    function handleConfirm() {
        if (!reason.trim()) {
            return
        }

        setIsSubmitting(true)
        router.post(
            `/users/${user.id}/deactivate`,
            { reason },
            {
                onSuccess: () => {
                    toast.success('Usuario desactivado exitosamente')
                    onOpenChange(false)
                    setReason('')
                },
                onError: () => {
                    toast.error('Error al desactivar usuario')
                },
                onFinish: () => setIsSubmitting(false),
            }
        )
    }

    function handleCancel() {
        setReason('')
        onOpenChange(false)
    }

    return (
        <Dialog open={open} onOpenChange={onOpenChange}>
            <DialogContent className="sm:max-w-[500px]">
                <DialogHeader>
                    <DialogTitle>Desactivar Usuario</DialogTitle>
                    <DialogDescription>
                        ¿Estás seguro de que quieres desactivar a <strong>{user.first_name} {user.last_name}</strong> ({user.email})?
                        Esta acción bloqueará el acceso del usuario al sistema.
                    </DialogDescription>
                </DialogHeader>

                <div className="grid gap-4 py-4">
                    <div className="grid gap-2">
                        <Label htmlFor="reason">
                            Motivo de desactivación <span className="text-destructive">*</span>
                        </Label>
                        <Textarea
                            id="reason"
                            placeholder="Ej: Baja temporal por excedencia"
                            value={reason}
                            onChange={(e) => setReason(e.target.value)}
                            rows={4}
                            required
                            disabled={isSubmitting}
                        />
                        <p className="text-xs text-muted-foreground">
                            El motivo quedará registrado en el historial de auditoría.
                        </p>
                    </div>
                </div>

                <DialogFooter>
                    <Button
                        variant="outline"
                        onClick={handleCancel}
                        disabled={isSubmitting}
                    >
                        Cancelar
                    </Button>
                    <Button
                        variant="destructive"
                        onClick={handleConfirm}
                        disabled={!reason.trim() || isSubmitting}
                    >
                        {isSubmitting ? 'Desactivando...' : 'Confirmar Desactivación'}
                    </Button>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    )
}
