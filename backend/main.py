import json
from pprint import pprint

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from starlette.responses import StreamingResponse

from transform import chToEn
from graph import graph
from  models import openai

app = FastAPI()

trans1=chToEn()
trans2=openai()

class ChatMessage(BaseModel):
    type: str
    content: str

class ChatRequest(BaseModel):
    chat_history: List[ChatMessage]
    input: str

class ChatResponse(BaseModel):
    answer: str

graph=graph()
config={"configurable":{"thread_id":"1"}}

@app.post("/chat_stream")
async def chat_stream(request: ChatRequest):
    print(request)
    input_text = request.input
    chathistory = request.chat_history
    # 调用trans1生成问题
    questions = trans1.invoke(input={"text": input_text})['text']
    print(questions)
    inputs = {"question": questions}

    # 处理graph的流式输出
    for output in graph.stream(inputs, config):
        for key, value in output.items():
            pprint(f"Node '{key}':")
        pprint("\n---\n")

    # 获取最终生成的答案
    answer = value["generation"]
    prompt="你是一位语言翻译专家，擅长将英文翻译成中文。请将以下文本从英文翻译成中文\n"
    answer=prompt+answer
    ret = trans2.stream(answer)

    def predict():
        text = ""
        for _token in ret:
            s_answer = _token.content
            if answer:
                js_data = {"code": "200", "msg": "ok", "data": s_answer}
                yield f"data: {json.dumps(js_data, ensure_ascii=False)}\n\n"
                text += s_answer
    generate = predict()
    return StreamingResponse(generate, media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app=app, host="localhost", port=8000)
