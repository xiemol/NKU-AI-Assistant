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
  SystemMessage,
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
import { DownloadIcon } from '@radix-ui/react-icons'
import { useSelectedValue } from '@/components/chatbutton'






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

async function submitUserMessage(content: string, selectedValue: string, file?: FormData) {
  'use server';
  console.log("提交的", selectedValue)
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
        content: content
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
  let requestData
  let specialcontent = null;
  if (selectedValue === "File parser" && content.startsWith('发送了文件') && file) {
    const spinnerStream = createStreamableUI(<SpinnerMessage />);
    const messageStream = createStreamableUI(null);
    const textStream = createStreamableValue('');
    const uiStream = createStreamableUI();
    specialcontent = "文件已发送";
    // 发送文件到后端
    const response = await fetch('http://localhost:8000/file_analyze', {
      method: 'POST',
      body: file,  // 这里的 file 是之前创建的 FormData 对象
    });
    const answer = await response.json();  // 获取返回的JSON数据
    spinnerStream.done(null);

    specialcontent = answer.message

    aiState.update({
      ...aiState.get(),
      messages: [
        ...aiState.get().messages,
        {
          id: nanoid(),
          role: 'assistant',
          content: specialcontent
        }
      ]
    });
    messageStream.update(<BotMessage content={specialcontent} />);

    messageStream.done();
    uiStream.done();
    textStream.done();
    aiState.done({
      ...aiState.get(),
      messages: [
        ...aiState.get().messages
      ]
    })
    return {
      id: nanoid(),
      attachments: uiStream.value,
      spinner: spinnerStream.value,
      display: messageStream.value,
    };

  }
  else if (content.startsWith('发送了文件') && file) {
    const spinnerStream = createStreamableUI(<SpinnerMessage />);
    const messageStream = createStreamableUI(null);
    const textStream = createStreamableValue('');
    const uiStream = createStreamableUI();
    specialcontent = "文件已发送";
    try {
      // 发送文件到后端
      const response = await fetch('http://localhost:8000/translate', {
        method: 'POST',
        body: file,  // 这里的 file 是之前创建的 FormData 对象
      });
      if (response.ok) {
        // 解析响应的 JSON 数据
        const responseData = await response.json();

        // 获取 download_url
        const downloadUrl = responseData.download_url;

        // 使用 downloadUrl 创建 markdown 语法的下载链接
        specialcontent = `文件已翻译完毕，您可以[下载翻译后的文件](${downloadUrl})。`;

        // 在 BotMessage 组件中显示翻译完成的消息和下载链接
        // 将 specialcontent 传递给 BotMessage 组件
      } else {
        specialcontent = "文件翻译失败，请重试。";
      }
    } catch (e) {
      console.error('Error uploading file:', e);
      specialcontent = "文件上传出错，请重试。";
    }
    spinnerStream.done(null);
    messageStream.update(<BotMessage content={specialcontent} />);

    aiState.update({
      ...aiState.get(),
      messages: [
        ...aiState.get().messages,
        {
          id: nanoid(),
          role: 'assistant',
          content: specialcontent
        }
      ]
    });

    uiStream.done();
    textStream.done();
    messageStream.done();
    aiState.done({
      ...aiState.get(),
      messages: [
        ...aiState.get().messages
      ]
    });

    return {
      id: nanoid(),
      attachments: uiStream.value,
      spinner: spinnerStream.value,
      display: messageStream.value,
    };
  }
  else if (content.startsWith("请你显示")) {
    const spinnerStream = createStreamableUI(<SpinnerMessage />);
    const messageStream = createStreamableUI(null);
    const textStream = createStreamableValue('');
    const uiStream = createStreamableUI();
    let picture = " "
    if (content.includes("校历")) {
      picture = "![校历](../calendar.jpg)"
    }
    else if (content.includes("八里台") && content.includes("地图")) {
      picture = "![八里台地图](../map1.jpg)"
    }
    else if (content.includes("津南") && content.includes("地图")) {
      picture = "![津南地图](../map2.jpg)"
    }
    if (picture === " ") {
      specialcontent = "目前仅支持显示班车，地图，校历等信息哦"
    }
    specialcontent = "请查看 " + picture + "\n还可以显示班车，地图等信息哦";

    spinnerStream.done(null);
    messageStream.update(<BotMessage content={specialcontent} />);

    aiState.update({
      ...aiState.get(),
      messages: [
        ...aiState.get().messages,
        {
          id: nanoid(),
          role: 'assistant',
          content: specialcontent
        }
      ]
    });

    uiStream.done();
    textStream.done();
    messageStream.done();
    aiState.done({
      ...aiState.get(),
      messages: [
        ...aiState.get().messages
      ]
    });


    return {
      id: nanoid(),
      attachments: uiStream.value,
      spinner: spinnerStream.value,
      display: messageStream.value,
    };
  }
  else if ((content.includes('提供') || content.includes('显示')) && (content.includes('最新') || content.includes('最近'))) {
    const spinnerStream = createStreamableUI(<SpinnerMessage />);
    const messageStream = createStreamableUI(null);
    const textStream = createStreamableValue('');
    const uiStream = createStreamableUI();
    const requestData = {
      url: content
    };
    // 发送文件到后端
    (async () => {
      try {
        const response = await fetch('http://localhost:8000/nk_news_get', {
          method: 'POST',
          headers: {
            'accept': 'application/json',
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(requestData), // 这里的 file 是之前创建的 FormData 对象
        });
        const datas = await response.json();  // 获取返回的JSON数据
        spinnerStream.done(null);
        let currentcontxt = ""
        for (const data of datas) {
          currentcontxt += data.title + "\n\n"
          currentcontxt += "日期 " + data.date + "\n\n"
          currentcontxt += "链接 " + data.link + "\n\n"
          messageStream.update(<BotMessage content={currentcontxt} />);
        }

        aiState.update({
          ...aiState.get(),
          messages: [
            ...aiState.get().messages,
            {
              id: nanoid(),
              role: 'assistant',
              content: currentcontxt
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
      }
      catch (e) {
        console.error('Error uploading file:', e);
        specialcontent = "您的提示词有误，请重试。";
      }
    })()

    return {
      id: nanoid(),
      attachments: uiStream.value,
      spinner: spinnerStream.value,
      display: messageStream.value,
    };
  }
  else if (content === '你可以帮我翻译英文文献吗？') {
    const spinnerStream = createStreamableUI(<SpinnerMessage />);
    const messageStream = createStreamableUI(null);
    const textStream = createStreamableValue('');
    const uiStream = createStreamableUI();

    specialcontent = "当然可以！\n\n请点击输入框左边的加号上传文件呢！！\n\n目前支持txt，pdf，docx文件\n\n也可以切换到文件分析，上传文件后我帮你分析呢";
    aiState.update({
      ...aiState.get(),
      messages: [
        ...aiState.get().messages,
        {
          id: nanoid(),
          role: 'assistant',
          content: specialcontent
        }
      ]
    });

    spinnerStream.done(null);
    messageStream.update(<BotMessage content={specialcontent} />);

    uiStream.done();
    textStream.done();
    messageStream.done();
    aiState.done({
      ...aiState.get(),
      messages: [
        ...aiState.get().messages
      ]
    });


    return {
      id: nanoid(),
      attachments: uiStream.value,
      spinner: spinnerStream.value,
      display: messageStream.value,
    };

  }
  else if (selectedValue === "Video parser" && content.startsWith('https://www')) {
    const spinnerStream = createStreamableUI(<SpinnerMessage />);
    const messageStream = createStreamableUI(null);
    const textStream = createStreamableValue('');
    const uiStream = createStreamableUI();
    const requestData = {
      url: content
    };
    // 发送文件到后端
    (async () => {
      try {
        const response = await fetch('http://localhost:8000/videoinfo_analyze', {
          method: 'POST',
          headers: {
            'accept': 'application/json',
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(requestData), // 这里的 file 是之前创建的 FormData 对象
        });
        const answer = await response.json();  // 获取返回的JSON数据
        spinnerStream.done(null);
        console.log(answer)
        specialcontent = answer.message

        aiState.update({
          ...aiState.get(),
          messages: [
            ...aiState.get().messages,
            {
              id: nanoid(),
              role: 'assistant',
              content: specialcontent
            }
          ]
        });
        messageStream.update(<BotMessage content={specialcontent} />);


        messageStream.done();
        uiStream.done();
        textStream.done();
        aiState.done({
          ...aiState.get(),
          messages: [
            ...aiState.get().messages
          ]
        })
      }
      catch (e) {
        console.error('Error uploading file:', e);
        specialcontent = "您的提示词有误，请重试。";
      }
    })()

    return {
      id: nanoid(),
      attachments: uiStream.value,
      spinner: spinnerStream.value,
      display: messageStream.value,
    };

  }
  else if (selectedValue === "Web parser" && content.startsWith('https')) {
    const spinnerStream = createStreamableUI(<SpinnerMessage />);
    const messageStream = createStreamableUI(null);
    const textStream = createStreamableValue('');
    const uiStream = createStreamableUI();
    const requestData = {
      url: content
    };
    // 发送文件到后端
    (async () => {
      try {
        const response = await fetch('http://localhost:8000/webscrap_analyze', {
          method: 'POST',
          headers: {
            'accept': 'application/json',
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(requestData), // 这里的 file 是之前创建的 FormData 对象
        });
        const answer = await response.json();  // 获取返回的JSON数据
        spinnerStream.done(null);
        console.log(answer)
        specialcontent = answer.message

        aiState.update({
          ...aiState.get(),
          messages: [
            ...aiState.get().messages,
            {
              id: nanoid(),
              role: 'assistant',
              content: specialcontent
            }
          ]
        });
        messageStream.update(<BotMessage content={specialcontent} />);


        messageStream.done();
        uiStream.done();
        textStream.done();
        aiState.done({
          ...aiState.get(),
          messages: [
            ...aiState.get().messages
          ]
        })
      }
      catch (e) {
        console.error('Error uploading file:', e);
        specialcontent = "您的提示词有误，请重试。";
      }
    })()

    return {
      id: nanoid(),
      attachments: uiStream.value,
      spinner: spinnerStream.value,
      display: messageStream.value,
    };

  }


  // 获取完整的消息历史记录，包括最新的用户消息
  const spinnerStream = createStreamableUI(<SpinnerMessage />);
  const textStream = createStreamableValue('');
  const messageStream = createStreamableUI(null);
  const uiStream = createStreamableUI();
  let flag = false;
  let chat_url = "chat_stream"
  let headers = {
    'accept': 'text/event-stream',
    'Content-Type': 'application/json'
  }
  requestData = {
    chat_history: formattedMessages,
    input: content,
  };
  if (selectedValue === "Video parser") {
    chat_url = "videoinfo_chat";
    headers = {
      'accept': 'application/json',
      'Content-Type': 'application/json'
    }
  }
  else if (selectedValue === "Web parser") {
    chat_url = "webscrap_chat";
    headers = {
      'accept': 'application/json',
      'Content-Type': 'application/json'
    }
  }
  else if (selectedValue === "File parser") {
    {
      chat_url = "file_chat";
      headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
      }
    }
  }
  else if (selectedValue === "MetaAgent") {
    chat_url = "chat_graph";
    requestData = {
      input: content
    };
  } else if (selectedValue === "NeoGraph") {
    chat_url = "chat_GraphRAG";
  }



  (async () => {
    try {
      // 调用流式 API
      const URL = "http://localhost:8000/" + chat_url

      const response = await fetch(URL, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(requestData)
      });

      if (!response.body) {
        // 处理 `response.body` 为 null 的情况
        throw new Error('Failed to receive stream data');
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder('utf-8');

      let currentContent = ""; // 存储当前消息内容
      // 读取流并更新消息内容
      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        const chunk = decoder.decode(value, { stream: true });
        const lines = chunk.split('\n');

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
    } catch (e) {
      console.error(e)

      const error = new Error(
        'The AI got rate limited, please try again later.'
      )
      uiStream.error(error)
      textStream.error(error)
      messageStream.error(error)
    }
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