import { AppLayout } from '@/components/layout'
import { SectionCards } from '@/components/dashboard/section-cards'

export default function Dashboard() {
  return (
    <AppLayout 
      title="Dashboard" 
      breadcrumbs={[{ label: "Dashboard" }]}
    >
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-bold tracking-tight">
            Dashboard
          </h1>
        </div>
        
        <SectionCards />
      </div>
    </AppLayout>
  )
}