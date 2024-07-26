<a href="https://chat.vercel.ai/">
  <img alt="Next.js 14 and App Router-ready AI chatbot." src="https://chat.vercel.ai/opengraph-image.png">
  <h1 align="center">Next.js AI Chatbot</h1>
</a>

<p align="center">
  An open-source AI chatbot app template built with Next.js, the Vercel AI SDK, OpenAI, and Vercel KV.
</p>

<p align="center">
  <a href="#features"><strong>Features</strong></a> ·
  <a href="#model-providers"><strong>Model Providers</strong></a> ·
  <a href="#deploy-your-own"><strong>Deploy Your Own</strong></a> ·
  <a href="#running-locally"><strong>Running locally</strong></a> ·
  <a href="#authors"><strong>Authors</strong></a>
</p>
<br/>

## Features

- [Next.js](https://nextjs.org) App Router
- React Server Components (RSCs), Suspense, and Server Actions
- [Vercel AI SDK](https://sdk.vercel.ai/docs) for streaming chat UI
- Support for OpenAI (default), Anthropic, Cohere, Hugging Face, or custom AI chat models and/or LangChain
- [shadcn/ui](https://ui.shadcn.com)
  - Styling with [Tailwind CSS](https://tailwindcss.com)
  - [Radix UI](https://radix-ui.com) for headless component primitives
  - Icons from [Phosphor Icons](https://phosphoricons.com)
- Chat History, rate limiting, and session storage with [Vercel KV](https://vercel.com/storage/kv)
- [NextAuth.js](https://github.com/nextauthjs/next-auth) for authentication

## Model Providers

This template ships with OpenAI `gpt-3.5-turbo` as the default. However, thanks to the [Vercel AI SDK](https://sdk.vercel.ai/docs), you can switch LLM providers to [Anthropic](https://anthropic.com), [Cohere](https://cohere.com/), [Hugging Face](https://huggingface.co), or using [LangChain](https://js.langchain.com) with just a few lines of code.

## Deploy Your Own

You can deploy your own version of the Next.js AI Chatbot to Vercel with one click:

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?demo-title=Next.js+Chat&demo-description=A+full-featured%2C+hackable+Next.js+AI+chatbot+built+by+Vercel+Labs&demo-url=https%3A%2F%2Fchat.vercel.ai%2F&demo-image=%2F%2Fimages.ctfassets.net%2Fe5382hct74si%2F4aVPvWuTmBvzM5cEdRdqeW%2F4234f9baf160f68ffb385a43c3527645%2FCleanShot_2023-06-16_at_17.09.21.png&project-name=Next.js+Chat&repository-name=nextjs-chat&repository-url=https%3A%2F%2Fgithub.com%2Fvercel-labs%2Fai-chatbot&from=templates&skippable-integrations=1&env=OPENAI_API_KEY%2CAUTH_SECRET&envDescription=How+to+get+these+env+vars&envLink=https%3A%2F%2Fgithub.com%2Fvercel-labs%2Fai-chatbot%2Fblob%2Fmain%2F.env.example&teamCreateStatus=hidden&stores=[{"type":"kv"}])

## Creating a KV Database Instance

Follow the steps outlined in the [quick start guide](https://vercel.com/docs/storage/vercel-kv/quickstart#create-a-kv-database) provided by Vercel. This guide will assist you in creating and configuring your KV database instance on Vercel, enabling your application to interact with it.

Remember to update your environment variables (`KV_URL`, `KV_REST_API_URL`, `KV_REST_API_TOKEN`, `KV_REST_API_READ_ONLY_TOKEN`) in the `.env` file with the appropriate credentials provided during the KV database setup.

## Running locally

You will need to use the environment variables [defined in `.env.example`](.env.example) to run Next.js AI Chatbot. It's recommended you use [Vercel Environment Variables](https://vercel.com/docs/projects/environment-variables) for this, but a `.env` file is all that is necessary.

> Note: You should not commit your `.env` file or it will expose secrets that will allow others to control access to your various OpenAI and authentication provider accounts.

1. Install Vercel CLI: `npm i -g vercel`
2. Link local instance with Vercel and GitHub accounts (creates `.vercel` directory): `vercel link`
3. Download your environment variables: `vercel env pull`

```bash
pnpm install
pnpm dev
```

Your app template should now be running on [localhost:3000](http://localhost:3000/).

## Authors

This library is created by [Vercel](https://vercel.com) and [Next.js](https://nextjs.org) team members, with contributions from:

- Jared Palmer ([@jaredpalmer](https://twitter.com/jaredpalmer)) - [Vercel](https://vercel.com)
- Shu Ding ([@shuding\_](https://twitter.com/shuding_)) - [Vercel](https://vercel.com)
- shadcn ([@shadcn](https://twitter.com/shadcn)) - [Vercel](https://vercel.com)

```
ai-chatbot
├─ .eslintrc.json
├─ app
│  ├─ (chat)
│  │  ├─ chat
│  │  │  └─ [id]
│  │  │     └─ page.tsx
│  │  ├─ layout.tsx
│  │  └─ page.tsx
│  ├─ actions.ts
│  ├─ globals.css
│  ├─ layout.tsx
│  ├─ login
│  │  ├─ actions.ts
│  │  └─ page.tsx
│  ├─ new
│  │  └─ page.tsx
│  ├─ opengraph-image.png
│  ├─ share
│  │  └─ [id]
│  │     └─ page.tsx
│  ├─ signup
│  │  ├─ actions.ts
│  │  └─ page.tsx
│  └─ twitter-image.png
├─ auth.config.ts
├─ auth.ts
├─ components
│  ├─ button-scroll-to-bottom.tsx
│  ├─ chat-history.tsx
│  ├─ chat-list.tsx
│  ├─ chat-message-actions.tsx
│  ├─ chat-message.tsx
│  ├─ chat-panel.tsx
│  ├─ chat-share-dialog.tsx
│  ├─ chat.tsx
│  ├─ clear-history.tsx
│  ├─ empty-screen.tsx
│  ├─ external-link.tsx
│  ├─ footer.tsx
│  ├─ header.tsx
│  ├─ login-button.tsx
│  ├─ login-form.tsx
│  ├─ markdown.tsx
│  ├─ prompt-form.tsx
│  ├─ providers.tsx
│  ├─ sidebar-actions.tsx
│  ├─ sidebar-desktop.tsx
│  ├─ sidebar-footer.tsx
│  ├─ sidebar-item.tsx
│  ├─ sidebar-items.tsx
│  ├─ sidebar-list.tsx
│  ├─ sidebar-mobile.tsx
│  ├─ sidebar-toggle.tsx
│  ├─ sidebar.tsx
│  ├─ signup-form.tsx
│  ├─ stocks
│  │  ├─ events-skeleton.tsx
│  │  ├─ events.tsx
│  │  ├─ index.tsx
│  │  ├─ message.tsx
│  │  ├─ spinner.tsx
│  │  ├─ stock-purchase.tsx
│  │  ├─ stock-skeleton.tsx
│  │  ├─ stock.tsx
│  │  ├─ stocks-skeleton.tsx
│  │  └─ stocks.tsx
│  ├─ tailwind-indicator.tsx
│  ├─ theme-toggle.tsx
│  ├─ ui
│  │  ├─ alert-dialog.tsx
│  │  ├─ badge.tsx
│  │  ├─ button.tsx
│  │  ├─ codeblock.tsx
│  │  ├─ dialog.tsx
│  │  ├─ dropdown-menu.tsx
│  │  ├─ icons.tsx
│  │  ├─ input.tsx
│  │  ├─ label.tsx
│  │  ├─ select.tsx
│  │  ├─ separator.tsx
│  │  ├─ sheet.tsx
│  │  ├─ sonner.tsx
│  │  ├─ switch.tsx
│  │  ├─ textarea.tsx
│  │  └─ tooltip.tsx
│  └─ user-menu.tsx
├─ components.json
├─ lib
│  ├─ chat
│  │  └─ actions.tsx
│  ├─ hooks
│  │  ├─ use-copy-to-clipboard.tsx
│  │  ├─ use-enter-submit.tsx
│  │  ├─ use-local-storage.ts
│  │  ├─ use-scroll-anchor.tsx
│  │  ├─ use-sidebar.tsx
│  │  └─ use-streamable-text.ts
│  ├─ types.ts
│  └─ utils.ts
├─ LICENSE
├─ middleware.ts
├─ next-env.d.ts
├─ next.config.js
├─ package.json
├─ pnpm-lock.yaml
├─ postcss.config.js
├─ prettier.config.cjs
├─ public
│  ├─ apple-touch-icon.png
│  ├─ favicon-16x16.png
│  ├─ favicon.ico
│  ├─ next.svg
│  ├─ thirteen.svg
│  └─ vercel.svg
├─ README.md
├─ tailwind.config.ts
└─ tsconfig.json

```