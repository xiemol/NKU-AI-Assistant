import { auth } from '@/auth'
import LoginForm from '@/components/login-form'
import { Session } from '@/lib/types'
import { redirect } from 'next/navigation'
import { Header } from '@/components/header'
import { SelectedValueProvider } from '@/components/chatbutton';

export default async function LoginPage() {
  const session = (await auth()) as Session

  if (session) {
    redirect('/chat')
  }

  return (
    <div>
    <Header/>
    <main className="flex flex-col p-4">
      <LoginForm />
    </main>
    </div>
  )
}
