from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import MessagesPlaceholder, ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from webscrap.webscrap_single import get_chat_model
from langchain_core.documents import Document


# 读取文件
from docx import Document as document
import fitz  # PyMuPDF

def extract_content(input_file):
    # 获取文件扩展名
    file_extension = input_file.split('.')[-1].lower()
    content=" "
    if file_extension == "docx":
        doc = document(input_file)
        content = "\n".join(para.text for para in doc.paragraphs)
    elif file_extension == "pdf":
        doc = fitz.open(input_file)
        content = ""
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            content += page.get_text()
    elif file_extension == "txt":
        with open(input_file, "r", encoding="utf-8") as file:
            content = file.read()
    return content

# 获取 chat_model
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
        ("system", "上述你获取到的信息来自于我上传文件的解析内容，你需要根据上述文件的解析内容回答下面的问题。"
               "基于上面的提示和下面的 context 回答用户问题:\n\n{context}"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
    ])
document_chain = create_stuff_documents_chain(chat_model, prompt2)

vector=None
def create_llm(path):
    global vector
    document_text = extract_content(path)
    if document_text==" ":
        return "no content"
    docs = [Document(page_content=document_text, meta_data={"source": path})]
    documents = text_splitter.split_documents(documents=docs)
    if vector is None:
        vector = FAISS.from_documents(documents=documents, embedding=embeddings)
    else:
        vector.add_documents(documents=documents, embedding=embeddings)
    retriever = vector.as_retriever()

    retriever_chain = create_history_aware_retriever(chat_model,retriever,prompt)
    retrieval_chain = create_retrieval_chain(retriever_chain,document_chain)
    return retrieval_chain