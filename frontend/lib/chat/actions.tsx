import 'server-only'
import {
  createAI,
  createStreamableUI,
  getMutableAIState,
  getAIState,
  createStreamableValue
} from 'ai/rsc'

import {
  spinner,
  BotCard,
  SystemMessage,
  Stock,
  Purchase
} from '@/components/stocks'

import {
  formatNumber,
  runAsyncFnWithoutBlocking,
  sleep,
  nanoid
} from '@/lib/utils'
import { saveChat } from '@/app/actions'
import { SpinnerMessage, UserMessage, BotMessage } from '@/components/stocks/message'
import { Chat, Message } from '@/lib/types'
import { auth } from '@/auth'


async function confirmPurchase(symbol: string, price: number, amount: number) {
  'use server'

  const aiState = getMutableAIState<typeof AI>()

  const purchasing = createStreamableUI(
    <div className="inline-flex items-start gap-1 md:items-center">
      {spinner}
      <p className="mb-2">
        Purchasing {amount} ${symbol}...
      </p>
    </div>
  )

  const systemMessage = createStreamableUI(null)

  runAsyncFnWithoutBlocking(async () => {
    await sleep(1000)

    purchasing.update(
      <div className="inline-flex items-start gap-1 md:items-center">
        {spinner}
        <p className="mb-2">
          Purchasing {amount} ${symbol}... working on it...
        </p>
      </div>
    )

    await sleep(1000)

    purchasing.done(
      <div>
        <p className="mb-2">
          You have successfully purchased {amount} ${symbol}. Total cost:{' '}
          {formatNumber(amount * price)}
        </p>
      </div>
    )

    systemMessage.done(
      <SystemMessage>
        You have purchased {amount} shares of {symbol} at ${price}. Total cost ={' '}
        {formatNumber(amount * price)}.
      </SystemMessage>
    )

    aiState.done({
      ...aiState.get(),
      messages: [
        ...aiState.get().messages,
        {
          id: nanoid(),
          role: 'system',
          content: `[User has purchased ${amount} shares of ${symbol} at ${price}. Total cost = ${amount * price
            }]`
        }
      ]
    })
  })

  return {
    purchasingUI: purchasing.value,
    newMessage: {
      id: nanoid(),
      display: systemMessage.value
    }
  }
}



// async function submitUserMessage(content: string) {
//   'use server'

//   const aiState = getMutableAIState<typeof AI>()

//   // 更新用户消息
//   aiState.update({
//     ...aiState.get(),
//     messages: [
//       ...aiState.get().messages,
//       {
//         id: nanoid(),
//         role: 'user',
//         content
//       }
//     ]
//   })

//   //let textStream: undefined | ReturnType<typeof createStreamableValue<string>>
//   let textNode: undefined | React.ReactNode

//   // 获取完整的消息历史记录，包括最新的用户消息
//   const allMessages = [
//     ...aiState.get().messages
//   ];

//   // 格式化消息，以匹配API期望的格式
//   const formattedMessages = allMessages.map((message) => ({
//     content: message.content,
//     type: message.role === 'user' ? 'human' : 'ai',
//   }));

//   // 构造请求数据
//   const requestData = {
//     chat_history: formattedMessages.map((message) => ({
//       type: message.type,
//       content: message.content,
//     })),
//     input: content,
//   };

//   // 调用你自己的 API
//   const response = await fetch('http://localhost:8000/chat', {
//     method: 'POST',
//     headers: {
//       'accept': 'application/json',
//       'Content-Type': 'application/json'
//     },
//     body: JSON.stringify(requestData)
//   });

//   const result = await response.json();

//   textNode = <BotMessage content={result.answer} />

//   aiState.done({
//     ...aiState.get(),
//     messages: [
//       ...aiState.get().messages,
//       {
//         id: nanoid(),
//         role: 'assistant',
//         content: result.answer
//       }
//     ]
//   })

//   return {
//     id: nanoid(),
//     display: textNode
//   }
// }

async function submitUserMessage(content: string) {
  'use server';

  const aiState = getMutableAIState<typeof AI>();

  // 更新用户消息
  const userMessageId = nanoid();
  // 更新 aiState，增加新消息
  aiState.update({
    ...aiState.get(),
    messages: [
      ...aiState.get().messages,
      {
        id: userMessageId,
        role: 'user',
        content
      }
    ]
  });

  // 获取完整的消息历史记录，包括最新的用户消息
  const updatedState = aiState.get(); // 确保获取最新的状态
  const allMessages = [...updatedState.messages];
  //console.log(allMessages)

  // 格式化消息，以匹配 API 期望的格式
  const formattedMessages = allMessages.map((message) => ({
    content: message.content,
    type: message.role === 'user' ? 'human' : 'ai',
  }));

  // 构造请求数据
  const requestData = {
    chat_history: formattedMessages,
    input: content,
  };
  console.log(formattedMessages)


  if (content == "发送了文件") {
    const spinnerStream = createStreamableUI(<SpinnerMessage />)
    const messageStream = createStreamableUI(null)
    const textStream = createStreamableValue('')
    const uiStream = createStreamableUI();
    spinnerStream.done(null)

    messageStream.update(<BotMessage content={"文件已添加"} />)
    uiStream.done()
    textStream.done()
    messageStream.done()

    return {
      id: nanoid(),
      attachments: uiStream.value,
      spinner: spinnerStream.value,
      display: messageStream.value
    };
  }

  // 获取完整的消息历史记录，包括最新的用户消息
  const textStream = createStreamableValue('');
  const spinnerStream = createStreamableUI(<SpinnerMessage />)
  console.log("spinnerStream 构建")
  const messageStream = createStreamableUI(null);
  const uiStream = createStreamableUI();
  let flag = false;


  (async () => {

    // 调用流式 API
    const response = await fetch('http://localhost:8000/chat_stream', {
      method: 'POST',
      headers: {
        'accept': 'text/event-stream',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(requestData)
    });

    if (!response.body) {
      // 处理 `response.body` 为 null 的情况
      throw new Error('Failed to receive stream data');
    }


    const reader = response.body.getReader();
    console.log(reader)
    console.log("++++++++++++++++++++++++++++++++++++++++++++++")
    const decoder = new TextDecoder('utf-8');

    let currentContent = ""; // 存储当前消息内容
    // 读取流并更新消息内容
    while (true) {
      const { value, done } = await reader.read();
      console.log(value)
      console.log("++++++++++++++++++++++++++++++++++++++++++++++")
      if (done) break;
      const chunk = decoder.decode(value, { stream: true });
      const lines = chunk.split('\n');
      console.log(lines)
      console.log("++++++++++++++++++++++++++++++++++++++++++++++")

      for (const line of lines) {
        if (line.startsWith("data: ")) {
          const data = JSON.parse(line.substring(6));
          if (data.code === '200' && data.msg === 'ok') {
            if (!flag) {
              spinnerStream.done(null);
              flag = true;
            }


            const answer = data.data;
            currentContent += answer;
            console.log(currentContent)
            messageStream.update(<BotMessage content={currentContent} />);
            // 更新消息内容

          }
        }
      }
    }

    aiState.update({
      ...aiState.get(),
      messages: [
        ...aiState.get().messages,
        {
          id: nanoid(),
          role: 'assistant',
          content: currentContent
        }
      ]
    });

    messageStream.done();
    uiStream.done();
    textStream.done();
    aiState.done({
      ...aiState.get(),
      messages: [
        ...aiState.get().messages
      ]
    })

  })()

  return {
    id: nanoid(),
    attachments: uiStream.value,
    spinner: spinnerStream.value,
    display: messageStream.value
  };
}


export type AIState = {
  chatId: string
  messages: Message[]
}

export type UIState = {
  id: string
  display: React.ReactNode
  spinner?: React.ReactNode
  attachments?: React.ReactNode
}[]

export const AI = createAI<AIState, UIState>({
  actions: {
    submitUserMessage,
    confirmPurchase
  },
  initialUIState: [],
  initialAIState: { chatId: nanoid(), messages: [] },
  onGetUIState: async () => {
    'use server'

    const session = await auth()

    if (session && session.user) {
      const aiState = getAIState() as Chat

      if (aiState) {
        const uiState = getUIStateFromAIState(aiState)
        return uiState
      }
    } else {
      return
    }
  },
  onSetAIState: async ({ state }) => {
    'use server'

    const session = await auth()

    if (session && session.user) {
      const { chatId, messages } = state

      const createdAt = new Date()
      const userId = session.user.id as string
      const path = `/chat/${chatId}`

      const firstMessageContent = messages[0].content as string
      const title = firstMessageContent.substring(0, 100)

      const chat: Chat = {
        id: chatId,
        title,
        userId,
        createdAt,
        messages,
        path
      }

      await saveChat(chat)
    } else {
      return
    }
  }
})

export const getUIStateFromAIState = (aiState: Chat) => {
  return aiState.messages
    .filter(message => message.role !== 'system')
    .map((message, index) => ({
      id: `${aiState.chatId}-${index}`,
      display:
        message.role === 'user' ? (
          <UserMessage>{message.content as string}</UserMessage>
        ) : message.role === 'assistant' &&
          typeof message.content === 'string' ? (
          <BotMessage content={message.content} />
        ) : null
    }))
}
