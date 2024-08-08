from langchain.chains.llm import LLMChain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_huggingface import HuggingFaceEmbeddings
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options
from bs4 import BeautifulSoup
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import InMemoryVectorStore
from langchain_core.documents import Document
import time

def fetch_dynamic_webpage_content(url, depth=1):
    # 配置EdgeOptions
    edge_options = Options()
    edge_options.add_argument("--headless")  # 运行时不打开浏览器
    edge_options.add_argument("--disable-gpu")

    # 设置EdgeDriver路径
    service = EdgeService(executable_path='../edgedriver/msedgedriver.exe')  # 确保路径格式正确

    # 启动EdgeDriver
    driver = webdriver.Edge(service=service, options=edge_options)
    driver.get(url)

    # 等待页面加载完成，可以根据具体页面调整等待时间或方式
    driver.implicitly_wait(10)

    # 获取页面内容
    page_source = driver.page_source
    driver.quit()

    # 使用BeautifulSoup解析内容
    soup = BeautifulSoup(page_source, 'html.parser')
    text = soup.get_text()

    # 获取页面内的所有链接
    links = [a.get('href') for a in soup.find_all('a', href=True)]

    if depth > 0:
        for link in links:
            if link.startswith('http'):
                time.sleep(1)  # 添加延时，避免过快请求被封禁
                try:
                    text += fetch_dynamic_webpage_content(link, depth-1)
                except Exception as e:
                    print(f"无法访问链接 {link}: {e}")

    return text

# 获取 chat_model
def get_chat_model():
    chat_model = ChatOpenAI(
        base_url="https://free.gpt.ge/v1/",
        api_key="sk-lo2dRdQWyh8rJLsJCd6bD73d4a07495fA6A8448e61B04f65",
        model="gpt-3.5-turbo",
    )
    return chat_model

chat_model = get_chat_model()


def setup_langchain(text_data, chat_model):
    EMBEDDING_DEVICE = "cpu"
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2",
                                       model_kwargs={'device': EMBEDDING_DEVICE})
    from langchain_community.vectorstores import FAISS
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    text_splitter = RecursiveCharacterTextSplitter()
    docx=[Document(page_content=text_data, metadata={"source": "url"})]
    documents = text_splitter.split_documents(documents=docx)
    vector = FAISS.from_documents(documents=documents, embedding=embeddings)
    retriever = vector.as_retriever()
    from langchain.chains import create_history_aware_retriever
    from langchain_core.prompts import MessagesPlaceholder,ChatPromptTemplate
    #生成ChatModel会话提示词
    prompt = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name="chat_history"),
        ("user","{input}"),
        ("user","根据以上对话历史，生成一个检索查询，以便查找对话相关信息")
    ])
    #生成含有历史信息的检索链
    retriever_chain = create_history_aware_retriever(chat_model,retriever,prompt)
    #继续对话，记住检索到的文档等信息
    prompt=ChatPromptTemplate.from_messages([
        ("system", "上述你获取到的信息来自于网页的解析内容，你需要根据上述网页的解析内容回答下面的问题。"
               "基于上面的提示和下面的 context 回答用户问题:\n\n{context}"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user","{input}"),
    ])
    #生成回答的文档链，主要是用prompt告诉chat_model怎么生成回答
    from langchain.chains.combine_documents import create_stuff_documents_chain
    document_chain = create_stuff_documents_chain(chat_model,prompt)
    #检索链＋文档链形成的整合链
    from langchain.chains.retrieval import create_retrieval_chain
    retrieval_chain = create_retrieval_chain(retriever_chain,document_chain)
    return retrieval_chain

# def main():
#     url = input("请输入网页链接: ")
#     depth = int(input("请输入爬取深度: "))
#     print("获取信息时间较长，请耐心等待......")
#     webpage_content = fetch_dynamic_webpage_content(url, depth)
#
#     # 设置LangChain
#     chain = setup_langchain(webpage_content,chat_model)
#     chat_history=[]
#     # 提问环节
#     while True:
#         question = input("你有什么问题？（输入'end'退出）: ")
#         if question.lower() == 'end':
#             break
#         answer = chain.invoke(
#             {
#                 "chat_history": chat_history,
#                 "input" : question
#             }
#         )
#         print("回答:", answer["answer"])
# if __name__ == "__main__":
#     main()
