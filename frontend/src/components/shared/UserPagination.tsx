import { router } from '@inertiajs/react'
import { Button } from '@/components/ui/button'
import { IconChevronLeft, IconChevronRight } from '@tabler/icons-react'

interface UserPaginationProps {
    pagination: {
        current_page: number
        total_pages: number
        has_next: boolean
        has_previous: boolean
    }
    filters: Record<string, string>
}

export function UserPagination({ pagination, filters }: UserPaginationProps) {
    function handlePageChange(page: number) {
        router.get('/users', { ...filters, page: page.toString() }, {
            preserveState: true,
            preserveScroll: true,
        })
    }

    if (pagination.total_pages <= 1) {
        return null
    }

    return (
        <div className="flex items-center justify-between">
            <div className="text-sm text-muted-foreground">
                Página {pagination.current_page} de {pagination.total_pages}
            </div>
            <div className="flex items-center space-x-2">
                <Button
                    variant="outline"
                    size="sm"
                    onClick={() => handlePageChange(pagination.current_page - 1)}
                    disabled={!pagination.has_previous}
                >
                    <IconChevronLeft className="h-4 w-4" />
                    Anterior
                </Button>
                <Button
                    variant="outline"
                    size="sm"
                    onClick={() => handlePageChange(pagination.current_page + 1)}
                    disabled={!pagination.has_next}
                >
                    Siguiente
                    <IconChevronRight className="h-4 w-4" />
                </Button>
            </div>
        </div>
    )
}