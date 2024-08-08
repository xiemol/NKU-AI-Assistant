import os
import json
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.document_loaders import YoutubeLoader # 导入YoutubeLoader，用于加载YouTube视频数据
from langchain.text_splitter import RecursiveCharacterTextSplitter # 导入文本分割器，用于处理文档
from langchain.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import MessagesPlaceholder
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import create_history_aware_retriever
from webscrap.webscrap_single import get_chat_model

# 初始化嵌入模型和聊天模型
EMBEDDING_DEVICE = "cpu"
embeddings = HuggingFaceEmbeddings(model_name="./models/m3e-base-huggingface",
                                   model_kwargs={'device': EMBEDDING_DEVICE}
                                   )

# 获取 chat_model


chat_model = get_chat_model()


# 创建向量数据库函数
def create_vector_db_from_youtube_url(video_url: str) -> FAISS:
    # 加载YouTube视频字幕
    loader = YoutubeLoader.from_youtube_url(video_url)
    print(loader)
    transcript = loader.load()

    # 将字幕分割成较小的片段
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents(transcript)
    if(docs==[]):
        return "No documents found"

    # 从文档片段创建FAISS数据库
    db = FAISS.from_documents(docs, embeddings)
    return db



retrieval_prompt = ChatPromptTemplate.from_messages([
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
    ("user",
    "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation")
    ])

prompt = ChatPromptTemplate.from_messages([
    ("system", "上述你获取到的信息来自于网页视频的解析内容，你需要根据上述网页视频的解析内容回答下面的问题。"
               "基于上面的提示和下面的 context 回答用户问题:\n\n{context}"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
])
# 创建文档链和检索链
document_chain = create_stuff_documents_chain(chat_model, prompt)

# 查询响应函数
def get_response_from_query(db):
    # # 对给定查询执行数据库的相似性搜索
    # docs = db.similarity_search(query, k=k)
    #
    # # 连接前几个文档的内容：使用FAISS数据库对用户查询进行相似性搜索，返回最相似的k个文档，并且将其连成一个字符串
    # docs_page_content = " ".join([d.page_content for d in docs])
    # 定义语言模型的提示模板

    # 创建一个带有历史感知的检索链
    retriever_chain = create_history_aware_retriever(chat_model, db.as_retriever(), retrieval_prompt)
    retrieval_chain = create_retrieval_chain(retriever_chain, document_chain)

    return retrieval_chain
