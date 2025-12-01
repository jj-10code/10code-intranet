import { render, screen } from "@testing-library/react"
import ProfileShow from "@/pages/profile/Show"
import { vi } from "vitest"

// Mock components
vi.mock("@/components/layout/app-layout", () => ({
    AppLayout: ({ children }: { children: React.ReactNode }) => <div data-testid="app-layout">{children}</div>,
}))
vi.mock("@/components/shared/AvatarUpload", () => ({
    AvatarUpload: () => <div data-testid="avatar-upload">Avatar Upload Component</div>,
}))

describe("ProfileShow", () => {
    const defaultUser = {
        id: 1,
        email: "test@10code.es",
        first_name: "Test",
        last_name: "User",
        avatar_url: "https://example.com/avatar.jpg",
        is_active: true,
        date_of_birth: "1990-01-01",
        roles: ["employee"],
    }

    const defaultProps = {
        user: defaultUser,
        permissions: {
            can_edit_avatar: true,
            can_edit_birthday: true,
        },
        google_data: {},
        title: "Mi Perfil",
    }

    it("renders user information correctly", () => {
        render(<ProfileShow {...defaultProps} />)

        expect(screen.getByText("Test User")).toBeInTheDocument()
        expect(screen.getByDisplayValue("test@10code.es")).toBeInTheDocument()
        expect(screen.getByDisplayValue("Test")).toBeInTheDocument()
        expect(screen.getByDisplayValue("User")).toBeInTheDocument()
        expect(screen.getByDisplayValue("1990-01-01")).toBeInTheDocument()
    })

    it("renders AvatarUpload when permission is granted", () => {
        render(<ProfileShow {...defaultProps} />)
        expect(screen.getByTestId("avatar-upload")).toBeInTheDocument()
    })

    it("renders read-only avatar when permission is denied", () => {
        render(<ProfileShow {...defaultProps} permissions={{ ...defaultProps.permissions, can_edit_avatar: false }} />)

        expect(screen.queryByTestId("avatar-upload")).not.toBeInTheDocument()
        // Should show initials fallback
        expect(screen.getByText("T")).toBeInTheDocument()
    })

    it("renders date of birth input as editable when permission is granted", () => {
        render(<ProfileShow {...defaultProps} />)
        const dobInput = screen.getByLabelText("Fecha de Nacimiento")
        expect(dobInput).not.toBeDisabled()
        expect(dobInput).not.toHaveAttribute("readonly")
        expect(dobInput).toHaveAttribute("type", "date")
    })

    it("renders date of birth input as read-only when permission is denied", () => {
        render(<ProfileShow {...defaultProps} permissions={{ ...defaultProps.permissions, can_edit_birthday: false }} />)
        const dobInput = screen.getByLabelText("Fecha de Nacimiento")
        expect(dobInput).toBeDisabled()
        expect(dobInput).toHaveAttribute("readonly")
        expect(dobInput).toHaveAttribute("type", "text")
    })

    it("renders google data when present", () => {
        const googleData = { sub: "123456789" }
        render(<ProfileShow {...defaultProps} google_data={googleData} />)

        expect(screen.getByText("Vinculado con Google")).toBeInTheDocument()
        expect(screen.getByText("ID: 123456789")).toBeInTheDocument()
    })
})
