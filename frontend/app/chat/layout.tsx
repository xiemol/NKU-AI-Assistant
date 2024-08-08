import { SidebarDesktop } from '@/components/sidebar-desktop'
import { Header } from '@/components/header'
import { SelectedValueProvider } from '@/components/chatbutton';

interface ChatLayoutProps {
  children: React.ReactNode
}

export default async function ChatLayout({ children }: ChatLayoutProps) {
  return (
    <div>   
    <SelectedValueProvider>
    <Header/>
    <div className="relative flex h-[calc(100vh_-_theme(spacing.16))] overflow-hidden">
      <SidebarDesktop />
      {children}
    </div>
    </SelectedValueProvider>
    </div> 
  )
}
