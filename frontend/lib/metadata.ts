// metadata.ts
export const metadata = {
    metadataBase: process.env.VERCEL_URL
      ? new URL(`https://${process.env.VERCEL_URL}`)
      : undefined,
    title: {
      default: 'Next.js AI Chatbot',
      template: `%s - Next.js AI Chatbot`
    },
    description: 'An AI-powered chatbot template built with Next.js and Vercel.',
    icons: {
      icon: '/NKSC.ico',
      shortcut: '/NKSC.png',
      apple: '/NKSC.png'
    }
  };
  
  export const viewport = {
    themeColor: [
      { media: '(prefers-color-scheme: light)', color: 'white' },
      { media: '(prefers-color-scheme: dark)', color: 'black' }
    ]
  };
  