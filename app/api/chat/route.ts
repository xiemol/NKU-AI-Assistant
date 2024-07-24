import fetch from 'node-fetch';

export async function POST(req: Request) {
  try {
    const { messages } = await req.json();

    const latestMessage = messages[messages?.length - 1]?.content;

    const response = await fetch('http://localhost:8000/invoke', {
      method: 'POST',
      headers: {
        'accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        input: {
          messages: [
            {
              content: '',
              additional_kwargs: {},
              response_metadata: {},
              type: 'system',
              name: 'string',
              id: 'string'
            },
            {
              content: '',
              additional_kwargs: {},
              response_metadata: {},
              type: 'ai',
              name: 'string',
              id: 'string',
              example: false,
              tool_calls: [],
              invalid_tool_calls: [],
              usage_metadata: {
                input_tokens: 0,
                output_tokens: 0,
                total_tokens: 0
              }
            },
            {
              content: latestMessage,
              additional_kwargs: {},
              response_metadata: {},
              type: 'human',
              name: 'string',
              id: 'string',
              example: false
            }
          ]
        },
        config: {},
        kwargs: {}
      })
    });

    const result = await response.json();
    
    // Print the result to the console
    console.log(result);

    return new Response(result.output.content, {
      headers: { 'Content-Type': 'text/plain' },
    });
  } catch (e) {
    console.error(e);
    throw e;
  }
}
