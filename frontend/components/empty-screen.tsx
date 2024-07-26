import { UseChatHelpers } from 'ai/react'

import { Button } from '@/components/ui/button'
import { ExternalLink } from '@/components/external-link'
import { IconArrowRight } from '@/components/ui/icons'

export function EmptyScreen() {
  return (
    <div className="mx-auto max-w-2xl px-4">
      <div className="flex flex-col gap-2 rounded-lg border bg-background p-8">
        <h1 className="text-lg font-semibold">
          欢迎使用南开大学智能小助手！
        </h1>
        <p className="leading-normal text-muted-foreground">
          南开大学智能小助手是你的校园生活好帮手。无论是学业上的问题，还是生活中的琐事，小助手都能为你提供贴心的帮助，就像是一位热心的学长或学姐。
        </p>
        <p className="leading-normal text-muted-foreground">
          小助手可以解答课程安排、学习资源、考试准备等学术问题；同时，也可以提供校园活动信息、社团介绍、生活服务等方面的帮助。无论你遇到什么问题，只需轻松询问，小助手将会为你提供详细且实用的解答。
        </p>
        
        <p className="leading-normal text-muted-foreground">
          无论你是新生还是老生，南开大学智能小助手都将成为你在校园生活中的得力助手，帮你解决各种问题，让你的大学生活更加轻松愉快！
        </p>
      </div>
    </div>
  )
}
