import { nanoid } from '@/lib/utils'
import { Chat } from '@/components/chat'
import { AI } from '@/lib/chat/actions'
import { auth } from '@/auth'
import { Session } from '@/lib/types'

export const metadata = {
  title: 'NKU Smart assistant'
}

export default async function ChatHomePage() {
  const id = nanoid()
  const session = (await auth()) as Session

  return (
    <AI initialAIState={{ chatId: id, messages: [] }}>
      <Chat id={id} session={session} />
    </AI>
    

  )
}
