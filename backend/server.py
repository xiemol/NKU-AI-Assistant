from pprint import pprint

from pydantic import BaseModel
import re
from fastapi.responses import JSONResponse
import json
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
import os
from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage, AIMessage
from fastapi.responses import FileResponse
from fastapi import FastAPI, UploadFile, File
# 导入网页抓取模块
from webscrap.webscrap_single import fetch_dynamic_webpage_content as fetch_single, setup_langchain as setup_langchain_single
# 导入视频分析模块
# from videoinfo.videoinfo_bilibili import create_vector_db_from_bilibili_url
from videoinfo.videoinfo_youtube import create_vector_db_from_youtube_url, get_response_from_query as youtube_response
#导入新闻获取模块
from NewsGet.news import NankaiNewsScraper, get_url, driver_path
#导入文献翻译模块
from file.transform import trans_pdf,trans_txt,trans_docx
from file.file_analyze import create_llm
#导入聊天模块
from chat.langgraph_RAG import langgraph_RAG
from chat.transform import trans1,trans2
from chat.retrieval_chain import retrieval_chain as chat_chain
from chat.graphRAG import graphRAG

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    url: str

class ChatMessage(BaseModel):
    content: str
    type: str
class ChatRequest(BaseModel):
    chat_history: List[ChatMessage]
    input: str

class GraphRequest(BaseModel):
    input: str


chat_history = []
db= None
retrieval_chain = None
chat_chain = chat_chain()
graphRAG = graphRAG()
langgraph=langgraph_RAG()
config={"configurable":{"thread_id":"1"}}


def stream(request,retrieval_chain):
    chathistory = request.chat_history
    if len(chat_history) != 0:
        chathistory = chathistory[-1:]
    for message in chathistory:
        if message.type == "human":
            chat_history.append(HumanMessage(content=message.content))
        else:
            chat_history.append(AIMessage(content=message.content))
    input_text = request.input
    ret = retrieval_chain.stream({
        "input": input_text,
        "chat_history": chat_history
    })

    def predict():
        text = ""
        for _token in ret:
            answer = _token.get('answer', '')
            if answer:
                js_data = {"code": "200", "msg": "ok", "data": answer}
                yield f"data: {json.dumps(js_data, ensure_ascii=False)}\n\n"
                text += answer
        chat_history.append(AIMessage(content=text))

    generate = predict()
    return StreamingResponse(generate, media_type="text/event-stream")



@app.post("/videoinfo_analyze")
async def analyze_video(request: AnalyzeRequest):
    url = request.url
    global db

    if re.match(r'https://www\.youtube\.com/', url):
        try:
            db = create_vector_db_from_youtube_url(url)
            if(db=="No documents found"):
                return{"message": "您发送的视频没有字幕文件，读取失败"}
        except Exception as e:
            return {"message": f"处理youtube视频时出错，或您发送的并非有效视频网址，请稍后再试：{str(e)}"}

        return {"message": "已完成视频分析，请继续提问。"}

    elif re.match(r'https://www\.bilibili\.com/', url):
        try:
            #db = create_vector_db_from_bilibili_url(url)
            if (db == "No documents found"):
                return {"message": "您发送的视频没有字幕文件，读取失败"}
        except Exception as e:
            return {"message": f"处理bilibiili视频时出错，或您发送的并非有效视频网址，：{str(e)}"}
        return {"message": "已完成视频分析，请继续提问。"}

    else:
        return {"message": "目前仅支持有效的bilibili网址或者youtube网址"}


@app.post("/videoinfo_chat")
async def chat_with_system(request: ChatRequest):
    if(db=="No documents found" or db==None):
        def fun():
            js_data = {"code": "200", "msg": "ok", "data": "请先发送有效视频链接"}
            yield f"data: {json.dumps(js_data, ensure_ascii=False)}\n\n"
        ans = fun()
        return StreamingResponse(ans, media_type="text/event-stream")

    retrieval_chain = youtube_response(db)
    return stream(request,retrieval_chain)


@app.post("/webscrap_analyze")
async def analyze_webpage(request: AnalyzeRequest):
    global retrieval_chain
    retrieval_chain = None
    url = request.url
    try:
        webpage_content = fetch_single(url)
        retrieval_chain = setup_langchain_single(webpage_content)
    except Exception as e:
        return {"message": f"网页分析出错，请重试：{str(e)}"}

    return {"message": "已完成网页分析，请继续提问。"}


@app.post("/webscrap_chat")
async def chat_with_system(request: ChatRequest):
    if (retrieval_chain == None):
        def fun():
            js_data = {"code": "200", "msg": "ok", "data": "请先发送网页链接"}
            yield f"data: {json.dumps(js_data, ensure_ascii=False)}\n\n"
        ans = fun()
        return StreamingResponse(ans, media_type="text/event-stream")

    return stream(request, retrieval_chain)


@app.post("/nk_news_get")
async def get_news(request: AnalyzeRequest):
    t = request.url
    url,type = get_url(t)
    scraper = NankaiNewsScraper(driver_path, url)
    if type in ['yaowen', 'meiti']:
        news = scraper.extract_latest_news2()
    else:
        news = scraper.extract_latest_news()

    return JSONResponse(content=news)


@app.post("/translate")
async def translate_file(file: UploadFile = File(...)):
    file_location = f"static/{file.filename}"
    # 将上传的文件保存到本地
    with open(file_location, "wb") as buffer:
        buffer.write(await file.read())
    # 返回文件的本地路径或URL路径
    file_url = file_location
    out_url = f"static/translated_{file.filename}"
    # 读取文件内容
    if(".txt" in file.filename):
        trans_txt(file_url, out_url)
    elif (".docx" in file.filename):
        trans_docx(file_url, out_url)
    elif(".pdf" in file.filename):
        trans_pdf(file_url, out_url)

    file_url = f"http://localhost:8000/download/translated_{file.filename}"
    return {"download_url": file_url}


@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(os.path.abspath("static"), filename)

    if os.path.exists(file_path):
        return FileResponse(
            path=file_path,
            filename=filename,
            media_type='application/octet-stream',
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    return {"message": "File not found"}, 404


@app.post("/file_analyze")
async def analyze_file(file: UploadFile = File(...)):
    global retrieval_chain
    retrieval_chain = None
    file_location = f"static/{file.filename}"
    # 将上传的文件保存到本地
    with open(file_location, "wb") as buffer:
        buffer.write(await file.read())
    # 返回文件的本地路径或URL路径
    file_url = file_location
    retrieval_chain = create_llm(file_url)
    if retrieval_chain == "no content":
        return {"message": "目前仅支持pdf,docx与txt文件的读取"}
    return {"message": "已完成文件分析，请继续提问。"}


@app.post("/file_chat")
async def chat_with_system(request: ChatRequest):
    if (retrieval_chain == None):
        def fun():
            js_data = {"code": "200", "msg": "ok", "data": "请先发送有效文件"}
            yield f"data: {json.dumps(js_data, ensure_ascii=False)}\n\n"
        ans = fun()
        return StreamingResponse(ans, media_type="text/event-stream")

    return stream(request, retrieval_chain)


@app.post("/chat_graph")
async def chat_graph(request: GraphRequest):
    print(request)
    input_text = request.input
    # 调用trans1生成问题
    questions = trans1.invoke(input={"text": input_text})['text']
    print(questions)
    inputs = {"question": questions}

    # 处理graph的流式输出
    for output in langgraph.stream(inputs, config):
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

@app.post("/chat_stream")
async def chat_stream(request: ChatRequest):
    return stream(request, chat_chain)

@app.post("/chat_GraphRAG")
async def chat_graph_RAG(request: ChatRequest):
    return stream(request, graphRAG)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
