export interface User {
    id: number
    email: string
    first_name: string
    last_name: string
    avatar_url: string | null
    is_active: boolean
    date_of_birth: string | null // ISO 8601
    roles: string[]
}

export interface Role {
    id: number
    code: string
    name: string
    description: string
    is_system: boolean
}

export interface AuditLog {
    id: number
    user: User | null
    action: string
    resource_type: string
    resource_id: number | null
    metadata: Record<string, any>
    ip_address: string | null
    timestamp: string // ISO 8601
}
