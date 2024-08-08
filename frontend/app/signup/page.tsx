import { auth } from '@/auth'
import SignupForm from '@/components/signup-form'
import { Session } from '@/lib/types'
import { redirect } from 'next/navigation'
import { Header } from '@/components/header'
import { SelectedValueProvider } from '@/components/chatbutton';

export default async function SignupPage() {
  const session = (await auth()) as Session

  if (session) {
    redirect('/chat')
  }

  return (
    <div>
    <Header/>
    <main className="flex flex-col p-4">
      <SignupForm />
    </main>
    </div>
  )
}
