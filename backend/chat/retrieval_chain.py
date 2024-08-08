from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.chat_models import ChatZhipuAI, ChatSparkLLM
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_huggingface import HuggingFaceEmbeddings

import os
def zhipu():
    os.environ["ZHIPUAI_API_KEY"] = "19ffa5597bd867ae38b9f2a356551e69.EjQJJKQAhVrGomtU"
    chat_model = ChatZhipuAI(model="glm-4")
    return chat_model

def retrieval_chain():
    chat_model = zhipu()

    EMBEDDING_DEVICE = 'cpu'
    embeddings = HuggingFaceEmbeddings(model_name='models\m3e-base-huggingface', model_kwargs={'device': EMBEDDING_DEVICE})
    vector = FAISS.load_local('files_faiss_index', embeddings=embeddings, allow_dangerous_deserialization=True)
    # 建立索引，将词向量存入向量数据库
    retriever = vector.as_retriever()

    # 继续对话，记住检索到的文档等信息
    prompt = ChatPromptTemplate.from_messages([
        ('system',
         """Your name is 南开大学院校消息通 .Answer the user's questions based on the below context:\n\n{context}"""),
        MessagesPlaceholder(variable_name='chat_history'),
        ('user', '{input}')
    ])

    documents_chain = create_stuff_documents_chain(chat_model, prompt)
    retrieval_chain = create_retrieval_chain(retriever, documents_chain)

    return retrieval_chain

chain = retrieval_chain()
result = chain.invoke({"input": "南开大学有哪些学院？","chat_history":[]})
print(result)
print(type(result))
