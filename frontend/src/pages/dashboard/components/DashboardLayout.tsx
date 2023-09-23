import { SidebarNav } from "./SidebarNav"

const sidebarNavItems = [
  {
    title: "Billing",
    href: "/dashboard/billing",
  },
  {
    title: "Access Token",
    href: "/dashboard/token",
  },
  
]

interface SettingsLayoutProps {
  children: React.ReactNode
}

export default function SettingsLayout({ children }: SettingsLayoutProps) {
  return (

      

      <div className="hidden space-y-6 p-10 pb-16 md:block">
        {/* <div className="space-y-0.5">
          <h2 className="text-2xl font-bold tracking-tight">Dashboard</h2>
          <p className="text-muted-foreground">
            Manage your account settings
          </p>
        </div> */}
        {/* <Separator className="my-6" /> */}
        <div className="flex flex-col space-y-8 lg:flex-row lg:space-x-12 lg:space-y-0">
          <aside className="-mx-4 lg:w-1/5">
            <SidebarNav items={sidebarNavItems} />
          </aside>
          <div className="flex-1 lg:max-w-2xl">{children}</div>
        </div>
      </div>

  )
}