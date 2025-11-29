export interface Role {
    code: string
    name: string
}

export interface User {
    id: number
    email: string
    first_name: string
    last_name: string
    full_name: string
    avatar_url?: string | null
    is_staff: boolean
    is_superuser: boolean
    roles?: string[]
}
