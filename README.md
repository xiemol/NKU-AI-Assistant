
<a href="https://chat.vercel.ai/">
  <img alt="Next.js 14 and App Router-ready AI chatbot." src="https://gemini-chatbot.vercel.rocks/og.png">
  <h1 align="center">Next.js AI Chatbot</h1>
</a>

<p align="center">
  An open-source AI chatbot app template built with Next.js, the Vercel AI SDK, Google Gemini, and Vercel KV.
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
- Support for Google Gemini (default), OpenAI, Anthropic, Cohere, Hugging Face, or custom AI chat models and/or LangChain
- [shadcn/ui](https://ui.shadcn.com)
  - Styling with [Tailwind CSS](https://tailwindcss.com)
  - [Radix UI](https://radix-ui.com) for headless component primitives
  - Icons from [Phosphor Icons](https://phosphoricons.com)
- Chat History, rate limiting, and session storage with [Vercel KV](https://vercel.com/storage/kv)
- [NextAuth.js](https://github.com/nextauthjs/next-auth) for authentication

## Model Providers

This template ships with Google Gemini `models/gemini-1.0-pro-001` as the default. However, thanks to the [Vercel AI SDK](https://sdk.vercel.ai/docs), you can switch LLM providers to [OpenAI](https://openai.com), [Anthropic](https://anthropic.com), [Cohere](https://cohere.com/), [Hugging Face](https://huggingface.co), or using [LangChain](https://js.langchain.com) with just a few lines of code.

## Deploy Your Own

You can deploy your own version of the Next.js AI Chatbot to Vercel with one click:

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?demo-title=Next.js+Chat&demo-description=A+full-featured%2C+hackable+Next.js+AI+chatbot+built+by+Vercel+Labs&demo-url=https%3A%2F%2Fchat.vercel.ai%2F&demo-image=%2F%2Fimages.ctfassets.net%2Fe5382hct74si%2F4aVPvWuTmBvzM5cEdRdqeW%2F4234f9baf160f68ffb385a43c3527645%2FCleanShot_2023-06-16_at_17.09.21.png&project-name=Next.js+Chat&repository-name=nextjs-chat&repository-url=https%3A%2F%2Fgithub.com%2Fvercel-labs%2Fgemini-chatbot&from=templates&skippable-integrations=1&env=GOOGLE_GENERATIVE_AI_API_KEY%2CAUTH_SECRET&envDescription=How+to+get+these+env+vars&envLink=https%3A%2F%2Fgithub.com%2Fvercel-labs%2Fgemini-chatbot%2Fblob%2Fmain%2F.env.example&teamCreateStatus=hidden&stores=[{%22type%22:%22kv%22}])

## Running locally

You will need to use the environment variables [defined in `.env.example`](.env.example) to run Next.js AI Chatbot. It's recommended you use [Vercel Environment Variables](https://vercel.com/docs/projects/environment-variables) for this, but a `.env` file is all that is necessary.

> Note: You should not commit your `.env` file or it will expose secrets that will allow others to control access to your various Google Cloud and authentication provider accounts.

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
- Jeremy Philemon ([@jrmyphlmn](https://twitter.com/jrmyphlmn)) - [Vercel](https://vercel.com)
```
Smart-Assistant-Lite
├─ .eslintrc.json
├─ .git
│  ├─ COMMIT_EDITMSG
│  ├─ config
│  ├─ description
│  ├─ HEAD
│  ├─ hooks
│  │  ├─ applypatch-msg.sample
│  │  ├─ commit-msg.sample
│  │  ├─ fsmonitor-watchman.sample
│  │  ├─ post-update.sample
│  │  ├─ pre-applypatch.sample
│  │  ├─ pre-commit.sample
│  │  ├─ pre-merge-commit.sample
│  │  ├─ pre-push.sample
│  │  ├─ pre-rebase.sample
│  │  ├─ pre-receive.sample
│  │  ├─ prepare-commit-msg.sample
│  │  ├─ push-to-checkout.sample
│  │  ├─ sendemail-validate.sample
│  │  └─ update.sample
│  ├─ index
│  ├─ info
│  │  └─ exclude
│  ├─ logs
│  │  ├─ HEAD
│  │  └─ refs
│  │     ├─ heads
│  │     │  └─ main
│  │     └─ remotes
│  │        └─ origin
│  │           ├─ HEAD
│  │           └─ main
│  ├─ objects
│  │  ├─ 01
│  │  │  └─ 8be513648d0741f79456bb904ba6d0d6e903cc
│  │  ├─ 02
│  │  │  ├─ 02362b5f0984235a9550f4f42bdf76854fc6bf
│  │  │  └─ b35815183d0fd95ecd71a61797ac4f4c3171d4
│  │  ├─ 08
│  │  │  └─ 2c5d67ff47398c3090b93f49f9612edf01e5e8
│  │  ├─ 0b
│  │  │  └─ 46ea13c87edb4efec8118b5e47b06c194eb49f
│  │  ├─ 0e
│  │  │  └─ b831fd3f83deadb29cb4fc846e9feb919a61c2
│  │  ├─ 10
│  │  │  ├─ 5f9fa2bcd621503be02c8c59a12ece36e66b46
│  │  │  └─ d6a5cf1cecb7752c5f9bfddac6cfc1cdfda2a7
│  │  ├─ 11
│  │  │  ├─ 0cdfaba03fb10e647988120c28f07976c8eab3
│  │  │  └─ cc7fc47c201fa66f84043010b010352f8470c3
│  │  ├─ 12
│  │  │  └─ d81c4a853472948b6dd2e85eff99b5d12fe60b
│  │  ├─ 13
│  │  │  └─ dedbe255ff9aa79b98a462055d2c9e95585361
│  │  ├─ 19
│  │  │  └─ f6b7e9676ece664f081b2739ac7254f7390e83
│  │  ├─ 1b
│  │  │  └─ de5acb5ca7a53f5395fb7a88c004b32c44bf9f
│  │  ├─ 1c
│  │  │  └─ 60a51d8a8341320cc1c11ae64462ac0abc1704
│  │  ├─ 1f
│  │  │  ├─ 6ba9105e1575f383e4853306a6413cdb0e8619
│  │  │  └─ ba27bea2d1874784e26eb8e28c48dc611ec769
│  │  ├─ 21
│  │  │  ├─ 254d9e5edfdc5f7d0bb6b7135c13469b8a25ba
│  │  │  └─ 63a7494b9f054158736a24e9ad9cdc382916d7
│  │  ├─ 23
│  │  │  ├─ e845d460c37ee8ae86740852088a021042768c
│  │  │  └─ ebf117dae4ad6f64acac94504c2e8ea40c5349
│  │  ├─ 25
│  │  │  └─ 944c922e95e1a2b8457ba0ad89a8280dc13fa2
│  │  ├─ 27
│  │  │  └─ b8709a3fec9990ef96e744315d98a51bd3e5d6
│  │  ├─ 28
│  │  │  └─ 25d593cec3b4aee45a2f9c91c65c1fea10d0a9
│  │  ├─ 2e
│  │  │  └─ 9bdfce60e3abbb17b8b66392a5b146f9adbbef
│  │  ├─ 2f
│  │  │  ├─ 0a839ba4c825a5d3af0c3455f00121fd2966db
│  │  │  └─ 53f6755754dca26e300c9768d817fbb74809f0
│  │  ├─ 30
│  │  │  └─ d71612b5862971d69a086eb1ff076975f2017c
│  │  ├─ 33
│  │  │  └─ ad091d26d8a9dc95ebdf616e217d985ec215b8
│  │  ├─ 36
│  │  │  └─ 4a56c1ce61f03c2667cee8e49b9975d8d30b25
│  │  ├─ 37
│  │  │  └─ d61e4bf77fb4a83fa03ffc6e6cd064e29c8ad6
│  │  ├─ 3a
│  │  │  └─ d28f0344ec9cea168c6aa0be331600d6fe46e9
│  │  ├─ 3d
│  │  │  └─ b547d273139f28f25bef10977c1c7ba580a2ac
│  │  ├─ 3e
│  │  │  └─ 700eb9913f8218a3e24c9029fed1ad5458676c
│  │  ├─ 45
│  │  │  ├─ 2b06c9247c68638e8e899dae49f05126ce6a1d
│  │  │  ├─ 2f4d9f0dde88611113632c1d759d60155fe4d3
│  │  │  └─ db9a818dee948f6aede661e3df192ea6b540d8
│  │  ├─ 47
│  │  │  └─ 4e00c0af05ac42cec3a118597379fb73926a07
│  │  ├─ 49
│  │  │  └─ 2586ae461c7f511bfd0927456df2e74fde4dd1
│  │  ├─ 4a
│  │  │  ├─ 52baf194d04dd2016ad8738c27d7c0b6774087
│  │  │  └─ f06a8ce813670edb5106f0b12df26a59bd3f16
│  │  ├─ 4f
│  │  │  ├─ 11a03dc6cc37f2b5105c08f2e7b24c603ab2f4
│  │  │  └─ 90f2d5da43c73bfe005bd12fdc9aeda0f1df86
│  │  ├─ 51
│  │  │  └─ 74b28c565c285e3e312ec5178be64fbeca8398
│  │  ├─ 52
│  │  │  └─ dc5bd76217e3db8a2aecb9e6dd87ff85a217bd
│  │  ├─ 53
│  │  │  ├─ 4182176bf87f9308355514adc884d2b69750a5
│  │  │  ├─ 46e98d3f035695a990adbfd61f12dbe2b10ea9
│  │  │  └─ 842a09d346ec67a9ab3bf6020fe8e6dd205b79
│  │  ├─ 55
│  │  │  └─ a7cb56281672bbc7893569172b4d82595feda5
│  │  ├─ 58
│  │  │  └─ b812d037d6d8c04547447d71847a2c12576ad3
│  │  ├─ 59
│  │  │  └─ 48a9e373b83351fd33cee2856df9598e4f4df2
│  │  ├─ 5c
│  │  │  └─ 2d31e2a020ab4b977a5bc1f68c72ebf24a61a7
│  │  ├─ 5e
│  │  │  └─ e834b02977d8428c50afde176fbef645bdca10
│  │  ├─ 60
│  │  │  ├─ 73a8fd4443dbddbd44d0a8d05f9c50266a27bf
│  │  │  └─ 8f8c673b1b0c6d099acd4d5e6682742938a7be
│  │  ├─ 62
│  │  │  ├─ 0c7d81f90b455bd9a8ee5a37d4d4f335443076
│  │  │  ├─ 230fde452674e111dd69747fd83da09759b7c3
│  │  │  └─ f7156dca246c46b213151af003a3a177977ccf
│  │  ├─ 65
│  │  │  └─ 76878dbd14f9920b883ca7ddeb6d7c6ad24692
│  │  ├─ 67
│  │  │  ├─ b63eeb8776d39453313ba48ba060679f9d29d4
│  │  │  └─ d3f1a2c163ccbeb52c40a7e42f107190237154
│  │  ├─ 68
│  │  │  └─ 31e3eebc1fec882f5bec7c8e21e70a063f0b1e
│  │  ├─ 69
│  │  │  └─ cf70ec39e421d68b2944a8d0072bf4af918f8c
│  │  ├─ 6a
│  │  │  └─ d48dcd84bc480dcabac3a3627cb1ebe267f9b7
│  │  ├─ 6b
│  │  │  └─ afe03d68f0e52ddc73b6de84bec73b39a7fd4f
│  │  ├─ 6c
│  │  │  ├─ 16c29f41168411dbf6e3ba3a063ce789c27334
│  │  │  └─ 750097405ff94e482b24fa9d8203f37cad2670
│  │  ├─ 6d
│  │  │  └─ b16bbdacdab6838766305d9c7e80f1c8489b15
│  │  ├─ 6e
│  │  │  └─ 74c18bbdaaa4d14fa84f15a05803a3f5893098
│  │  ├─ 71
│  │  │  └─ 9f693783e77925db05a633a43caa9da5ed256b
│  │  ├─ 73
│  │  │  ├─ d602350052b8a1cf9d23c41830163f0dd357eb
│  │  │  └─ f7148af524c9960b6dfafb4127effa43872da6
│  │  ├─ 74
│  │  │  ├─ 52b5dc69b2a634c86779ee4cd4c13319549b43
│  │  │  ├─ b28ef16573958588969b48e83204eedc90de58
│  │  │  └─ fc45290314819007be61b86f36784ccad38a43
│  │  ├─ 75
│  │  │  └─ 42992bdd02d92dbf3fdc44c0b0675072be5795
│  │  ├─ 7a
│  │  │  └─ 738cf5ec0cba1a901aefdb96dfdfd028828e97
│  │  ├─ 7b
│  │  │  └─ c0e19c19fbc8802928936eacdc9514ceb82681
│  │  ├─ 7c
│  │  │  └─ 7cf942be8bd5a7f2908c60ece4299fb332a523
│  │  ├─ 7e
│  │  │  └─ 9664c8df4e55bddaa1b02e855acd1f066c2784
│  │  ├─ 82
│  │  │  └─ f0aa5b7982a7302591b32091e22cf0648ee7c0
│  │  ├─ 83
│  │  │  ├─ 55d99dd30553ae9554864eaecb72bddc75cdff
│  │  │  └─ e60ace98b1357b5f2754d2e7129c6fd085c9ac
│  │  ├─ 84
│  │  │  ├─ 2ca6b5f46a88e8fdbf7506c73bf54caa6a9c1b
│  │  │  └─ 6faa96a23bb8300ff80ad2d534e5d9d8484dc8
│  │  ├─ 86
│  │  │  └─ 2523fe2dd44aed4c77638199a99cd7773d2b3c
│  │  ├─ 89
│  │  │  └─ 77c1bd123cbe4a9f7b32c63594921688275cdd
│  │  ├─ 8e
│  │  │  └─ ab1d31b5296b3527621415a3b6e0861c80cbb9
│  │  ├─ 91
│  │  │  └─ 5ec613412637f45fae4ecff1d995b7599acc95
│  │  ├─ 95
│  │  │  └─ ccf465f2a0466d0dfa20bd64fb45546a4d0a56
│  │  ├─ 9a
│  │  │  └─ c846a1a2ac765f20101e7309b2e9ec64e7a67b
│  │  ├─ 9b
│  │  │  └─ 7d60b3b262dbc59bf50b428b444ec795cb54f1
│  │  ├─ 9f
│  │  │  ├─ 04a97e74bff2fc76505b3764c5a4d14309e2aa
│  │  │  └─ 05d2e9a4c1d010fee4d75a5a4c190285f57f0c
│  │  ├─ a0
│  │  │  └─ a213fedf56e4797aed28e23225d8d0d11147d2
│  │  ├─ a1
│  │  │  ├─ 422aec3532f6ac323036508d7b4adb6b1a20de
│  │  │  └─ 6275cb38cd4e609688daf3a6dd4db6539caa52
│  │  ├─ a2
│  │  │  ├─ 5dfefd11d9cc00cf8350e1c1fdb6826903400d
│  │  │  ├─ a7246afd5c6350c9700d31251a605535b31d1f
│  │  │  └─ e18ea6649fa6a505b77cda0e53b6e6e240f0a2
│  │  ├─ a5
│  │  │  └─ 78ec04d8ee550f9cf516e1e2b63716267d5c55
│  │  ├─ a7
│  │  │  ├─ 14994c2a64508209da2a2c62fc7f2150404b1d
│  │  │  └─ 3375193a7cd5e0efbd255aee646c2dde1fd0e8
│  │  ├─ a8
│  │  │  └─ f3846e33fe115bac17f929b0be50370d1b04ef
│  │  ├─ a9
│  │  │  ├─ 7e0676fc82ba8842a29335ec90b7add549b81b
│  │  │  ├─ a5c0badaa9c68a3415a1a5e06534e82db85f0c
│  │  │  └─ da590f4d33998c2989c5cb88e08078c3a26304
│  │  ├─ ae
│  │  │  └─ 8f8427413f44f19db3f10993ce0fa9b19b5fec
│  │  ├─ af
│  │  │  └─ a0e1cd7efcd75de834221b7202b483113561d8
│  │  ├─ b3
│  │  │  └─ 1a358c94a2edf186a6753a3792f621fac35010
│  │  ├─ b6
│  │  │  └─ 5c9414836f9bc28ac0c6041fbddd1049ef6897
│  │  ├─ b7
│  │  │  └─ 0e01b25c7657ea3fa60f0170db2bc941dce13b
│  │  ├─ ba
│  │  │  └─ 6cc0161457e56c609c1a64ab458d573039d27d
│  │  ├─ bb
│  │  │  └─ be03cbca25e3335635477e12b03c0c0e7743ca
│  │  ├─ c0
│  │  │  └─ 30c780b9f7c0d9d5014b2ecc07f126f48388fd
│  │  ├─ c1
│  │  │  └─ 7b5320a8a70d3212b44ac7bb6f6635cd1d1a5a
│  │  ├─ c5
│  │  │  └─ adc235855f1372540136aad7ca25a89f60ed94
│  │  ├─ c8
│  │  │  └─ ef91ea21dbbf6060ff5251caa95ee279fb70cd
│  │  ├─ c9
│  │  │  └─ c22dc6a905ceb3709bb4fd3c35b595180a8109
│  │  ├─ cb
│  │  │  └─ 703219698cddc4d5e68c0a4a380d787ed5076f
│  │  ├─ cd
│  │  │  └─ a179cf15dd53b00acb570e827e330895c2c385
│  │  ├─ cf
│  │  │  └─ 9c54901f01e36df112421e53ae65746cd7990e
│  │  ├─ d2
│  │  │  ├─ 3589481372b24b64caabc41116a2275c03b4a7
│  │  │  └─ f84222734f27b623d1c80dda3561b04d1284af
│  │  ├─ d4
│  │  │  ├─ 491467a1f14d1d72e535caac9c40636054e5df
│  │  │  └─ e4b40a4d008e9b0f0d4414085793fe9bb03720
│  │  ├─ d6
│  │  │  └─ 6b2d3253baff164235d4ca791aae6d84721835
│  │  ├─ d8
│  │  │  ├─ 0f0c842e0af00ca13996cf726a641597d0e491
│  │  │  └─ e03c0bd741132f7652b5785bd411aa2123f0f9
│  │  ├─ d9
│  │  │  ├─ 1dfe5d04f988a8fa695e4201ed065eb6b8f8d7
│  │  │  ├─ 6447c6948a2e4ccf20a257bc408c50d25be3f7
│  │  │  └─ 6d1931dc5a1a2483950bfbf1b997f3267f159c
│  │  ├─ db
│  │  │  └─ ac96428e64945b4e18efb0b915cbaed40b91c1
│  │  ├─ dc
│  │  │  └─ 64b06aa49e64e07e356e1399efedd18d84bc05
│  │  ├─ dd
│  │  │  └─ 019e4039731b6a49b63c0fe6677fe1041d940f
│  │  ├─ de
│  │  │  └─ 1c55658057edb168a4e72992f759321c32de0e
│  │  ├─ e1
│  │  │  ├─ 403f205d7567445df746c3456f6edd34eba016
│  │  │  └─ 7d85799510c205174915cf1c2b441be63d5952
│  │  ├─ e3
│  │  │  └─ 285714acecdeb75fa528aad2eb635ecd45cd71
│  │  ├─ e7
│  │  │  └─ af75e4436fca1a23b56d62fcf39798f96190f6
│  │  ├─ e8
│  │  │  └─ 2196673a5e60b153b365fc4a8d4e7f5b76c4aa
│  │  ├─ f0
│  │  │  ├─ 4b2423ec8152e4a4b6d5b00e888ff2cf34afbc
│  │  │  └─ 787802b781dde7e7cb5cd331d362a27f6545de
│  │  ├─ f2
│  │  │  ├─ 2cf967c6e536cff2e926f676a6f17e06dcdc76
│  │  │  └─ 3e220225338f6e1024daacbd7677f9ced5d4f8
│  │  ├─ f3
│  │  │  └─ 8ab68ca3009966ffd07b41a87493a5b45f4a7c
│  │  ├─ f4
│  │  │  └─ 3ce9f0d336ceef8e278efdec076154c88ddbed
│  │  ├─ f9
│  │  │  └─ 518232d37cd51ff3767bc06be62ef71cec5e99
│  │  ├─ fb
│  │  │  └─ 5dec39d2807946680ee1e7a404d0e0a51cc11c
│  │  ├─ fc
│  │  │  └─ 7020bccc3c0fa63de59c70b255e9495155abf4
│  │  ├─ ff
│  │  │  └─ 39d663e5d85d66cf72551e51e6cddcc18318e8
│  │  ├─ info
│  │  └─ pack
│  │     ├─ pack-5dec45e367a5970e665eda045750bfbf8de772b6.idx
│  │     ├─ pack-5dec45e367a5970e665eda045750bfbf8de772b6.pack
│  │     └─ pack-5dec45e367a5970e665eda045750bfbf8de772b6.rev
│  ├─ packed-refs
│  └─ refs
│     ├─ heads
│     │  └─ main
│     ├─ remotes
│     │  └─ origin
│     │     ├─ HEAD
│     │     └─ main
│     └─ tags
├─ .gitignore
├─ app
│  ├─ (chat)
│  │  ├─ chat
│  │  │  └─ [id]
│  │  │     └─ page.tsx
│  │  ├─ error.tsx
│  │  ├─ layout.tsx
│  │  ├─ page.tsx
│  │  └─ waiting-room
│  │     └─ page.tsx
│  ├─ 149e9513-01fa-4fb0-aad4-566afd725d1b
│  │  └─ 2d206a39-8ed7-437e-a3be-862e0f06eea3
│  │     └─ [[...restpath]]
│  │        └─ route.ts
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
│  ├─ flights
│  │  ├─ boarding-pass.tsx
│  │  ├─ destinations.tsx
│  │  ├─ flight-status.tsx
│  │  ├─ list-flights.tsx
│  │  ├─ purchase-ticket.tsx
│  │  └─ select-seats.tsx
│  ├─ footer.tsx
│  ├─ header.tsx
│  ├─ hotels
│  │  └─ list-hotels.tsx
│  ├─ login-button.tsx
│  ├─ login-form.tsx
│  ├─ markdown.tsx
│  ├─ media
│  │  └─ video.tsx
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
│  │  ├─ actions.tsx
│  │  ├─ ratelimit.ts
│  │  └─ responses.tsx
│  ├─ hooks
│  │  ├─ use-copy-to-clipboard.tsx
│  │  ├─ use-enter-submit.tsx
│  │  ├─ use-local-storage.ts
│  │  ├─ use-scroll-anchor.tsx
│  │  ├─ use-sidebar.tsx
│  │  └─ use-streamable-text.ts
│  ├─ kasada
│  │  ├─ kasada-client.tsx
│  │  └─ kasada-server.ts
│  ├─ types.ts
│  └─ utils.ts
├─ LICENSE
├─ middleware.ts
├─ next-env.d.ts
├─ next.config.js
├─ package-lock.json
├─ package.json
├─ pnpm-lock.yaml
├─ postcss.config.js
├─ prettier.config.cjs
├─ public
│  ├─ apple-touch-icon.png
│  ├─ favicon-16x16.png
│  ├─ favicon.ico
│  ├─ images
│  │  ├─ 1.jpg
│  │  ├─ 2.jpg
│  │  ├─ 3.jpg
│  │  └─ gemini.png
│  ├─ next.svg
│  ├─ og.png
│  ├─ thirteen.svg
│  ├─ vercel.svg
│  └─ videos
│     └─ books.mp4
├─ README.md
├─ tailwind.config.ts
└─ tsconfig.json

```
