from langchain_community.chat_models import ChatZhipuAI, ChatSparkLLM
from langchain_core.messages import AIMessage
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
import os

def openai():
    chat_model = ChatOpenAI(
        base_url=os.getenv('BASE_URL'),
        api_key=os.getenv('API_KEY'),
        # model="gpt-3.5-turbo",
        model="gpt-3.5-turbo-0125",
        temperature=0,
        streaming=True,
    )
    return chat_model

def zhipu():
    os.environ["ZHIPUAI_API_KEY"] = os.getenv('ZHIPUAI_API_KEY')
    chat_model = ChatZhipuAI(
        model="glm-4",
        temperature=100,
    )
    return chat_model

def spark():
    chat_model = ChatSparkLLM(
        spark_app_id="e4b7c93d",
        spark_api_key="f0eb8b0dc66e61ccbaa856e81288a7ac",
        spark_api_secret="NzQyOWVkMWZiZDU4MjA4ZTc2MTY0YmZh",
        spark_api_url="wss://spark-api.xf-yun.com/v3.1/chat",
        spark_llm_domain="generalv2",
    )
    return chat_model

def Llama3():
    model=ChatGroq(temperature=0,
    model_name="Llama3-8b-8192",
    api_key="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")
    return model