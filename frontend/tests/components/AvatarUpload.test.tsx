import { render, screen, fireEvent, waitFor } from "@testing-library/react"
import { AvatarUpload } from "@/components/shared/AvatarUpload"
import { vi } from "vitest"
import { router } from "@inertiajs/react"

// Mock inertia router
vi.mock("@inertiajs/react", async () => {
    const actual = await vi.importActual("@inertiajs/react")
    return {
        ...actual,
        router: {
            post: vi.fn(),
        },
    }
})

// Mock UI components
vi.mock("@/components/ui/avatar", () => ({
    Avatar: ({ children, onClick, "data-testid": testId }: any) => (
        <div onClick={onClick} data-testid={testId}>{children}</div>
    ),
    AvatarImage: ({ src, "data-testid": testId }: any) => <img src={src} data-testid={testId} />,
    AvatarFallback: ({ children }: any) => <div>{children}</div>,
}))

// Mock sonner
const toastErrorSpy = vi.fn()
const toastSuccessSpy = vi.fn()
vi.mock("sonner", () => ({
    toast: {
        error: (msg: string) => toastErrorSpy(msg),
        success: (msg: string) => toastSuccessSpy(msg),
    }
}))

describe("AvatarUpload", () => {
    const defaultProps = {
        currentAvatar: "https://example.com/avatar.jpg",
        fallback: "U",
    }

    beforeEach(() => {
        vi.clearAllMocks()
    })

    it("renders current avatar correctly", () => {
        render(<AvatarUpload {...defaultProps} />)
        const img = screen.getByTestId("avatar-image")
        expect(img).toHaveAttribute("src", defaultProps.currentAvatar)
    })

    it("renders fallback when no avatar provided", () => {
        render(<AvatarUpload {...defaultProps} currentAvatar={null} />)
        expect(screen.getByText("U")).toBeInTheDocument()
    })

    it("triggers file input click when avatar is clicked", () => {
        render(<AvatarUpload {...defaultProps} />)
        const fileInput = screen.getByTestId("avatar-upload-input")
        const clickSpy = vi.spyOn(fileInput, "click")

        const avatar = screen.getByTestId("avatar-upload-trigger")
        fireEvent.click(avatar)

        expect(clickSpy).toHaveBeenCalled()
    })

    it("handles file selection and triggers upload", async () => {
        render(<AvatarUpload {...defaultProps} />)
        const fileInput = screen.getByTestId("avatar-upload-input")

        const file = new File(["(⌐□_□)"], "chucknorris.png", { type: "image/png" })

        fireEvent.change(fileInput, { target: { files: [file] } })

        await waitFor(() => {
            expect(router.post).toHaveBeenCalledWith(
                "/profile/",
                expect.objectContaining({
                    _method: "post",
                    avatar: file,
                }),
                expect.objectContaining({
                    forceFormData: true,
                })
            )
        })
    })

    it("validates file type", async () => {
        render(<AvatarUpload {...defaultProps} />)
        const fileInput = screen.getByTestId("avatar-upload-input")

        const file = new File(["text"], "document.txt", { type: "text/plain" })

        fireEvent.change(fileInput, { target: { files: [file] } })

        // Should NOT call router.post
        expect(router.post).not.toHaveBeenCalled()
        // Should call toast.error
        expect(toastErrorSpy).toHaveBeenCalledWith("El archivo debe ser una imagen")
    })
})
