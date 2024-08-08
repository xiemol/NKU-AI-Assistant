from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import MessagesPlaceholder, ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain

# 加载网页
def fetch_dynamic_webpage_content(url):
    loader = WebBaseLoader(
        web_paths=[url]
    )
# 将网页的数据的加载到Document
    docs=loader.load()
    return docs

# 获取 chat_model
def get_chat_model():
    chat_model = ChatOpenAI(
        base_url="https://free.gpt.ge/v1/",
        api_key="sk-lo2dRdQWyh8rJLsJCd6bD73d4a07495fA6A8448e61B04f65",
        model="gpt-3.5-turbo",
    )
    return chat_model

chat_model = get_chat_model()
EMBEDDING_DEVICE = "cpu"
embeddings = HuggingFaceEmbeddings(model_name="./models/m3e-base-huggingface",
                                       model_kwargs={'device': EMBEDDING_DEVICE}
                                       )
text_splitter = RecursiveCharacterTextSplitter()
# 生成ChatModel会话提示词
prompt = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        ("user", "根据以上对话历史，生成一个检索查询，以便查找对话相关信息")
    ])
prompt2 = ChatPromptTemplate.from_messages([
        ("system", "上述你获取到的信息来自于网页的解析内容，你需要根据上述网页的解析内容回答下面的问题。"
               "基于上面的提示和下面的 context 回答用户问题:\n\n{context}"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
    ])
document_chain = create_stuff_documents_chain(chat_model, prompt2)

vector=None
def setup_langchain(text_data):
    global vector

    documents = text_splitter.split_documents(documents=text_data)
    if vector is None:
        vector = FAISS.from_documents(documents=documents, embedding=embeddings)
    else:
        vector.add_documents(documents=documents, embedding=embeddings)
    retriever = vector.as_retriever()

    retriever_chain = create_history_aware_retriever(chat_model,retriever,prompt)
    retrieval_chain = create_retrieval_chain(retriever_chain,document_chain)
    return retrieval_chain

